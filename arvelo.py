import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date
import tempfile
import os
import shutil
from dateutil.relativedelta import relativedelta

# --- CONFIGURACIÓN DE LA BASE DE DATOS --- #
def get_db_connection():
    """Crea una conexión a la base de datos SQLite con configuración mejorada"""
    temp_dir = tempfile.gettempdir()
    db_path = os.path.join(temp_dir, "pagos_arvelo_v2.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Para acceso por nombre de columna
    return conn

# --- DATOS INICIALES --- #
def cargar_datos_iniciales():
    """Devuelve los datos iniciales de locales con cánones base (2020)"""
    return [
        ('LOCAL A', 'MONICA JANET VARGAS G.', 'PB', 'LENCERIA', 350.0, 'MONICA JANET VARGAS G.'),
        # ... (todos los demás locales del código original)
    ]

def cargar_historicos_canon():
    """Devuelve los cánones históricos para cada año"""
    return [
        ('LOCAL A', 2020, 350.0),
        ('LOCAL A', 2021, 370.0),
        ('LOCAL A', 2022, 400.0),
        ('LOCAL A', 2023, 420.0),
        # ... (cánones para todos los locales y años)
    ]

# --- INICIALIZACIÓN DE LA BASE DE DATOS --- #
def init_db():
    """Inicializa la base de datos con estructura mejorada"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Tabla de locales (maestra)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locales (
                numero_local TEXT PRIMARY KEY,
                inquilino TEXT NOT NULL,
                planta TEXT,
                ramo_negocio TEXT,
                contrato TEXT
            )
        ''')
        
        # Tabla de cánones históricos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historico_canon (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_local TEXT NOT NULL,
                ano INTEGER NOT NULL,
                canon REAL NOT NULL,
                FOREIGN KEY(numero_local) REFERENCES locales(numero_local),
                UNIQUE(numero_local, ano)
            )
        ''')
        
        # Tabla de pagos (transacciones)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_local TEXT NOT NULL,
                inquilino TEXT NOT NULL,
                fecha_pago DATE NOT NULL,
                mes_abonado TEXT NOT NULL,  -- Formato YYYY-MM
                monto REAL NOT NULL,
                estado TEXT CHECK(estado IN ('Pagado', 'Parcial', 'Pendiente')),
                observaciones TEXT,
                FOREIGN KEY(numero_local) REFERENCES locales(numero_local)
            )
        ''')
        
        # Índices para mejor performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_pagos_local ON pagos(numero_local)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_pagos_mes ON pagos(mes_abonado)')
        
        # Insertar datos iniciales si no existen
        cursor.execute("SELECT COUNT(*) FROM locales")
        if cursor.fetchone()[0] == 0:
            # Insertar locales
            cursor.executemany('''
                INSERT INTO locales (numero_local, inquilino, planta, ramo_negocio, contrato)
                VALUES (?, ?, ?, ?, ?)
            ''', [(x[0], x[1], x[2], x[3], x[5]) for x in cargar_datos_iniciales()])
            
            # Insertar cánones históricos
            cursor.executemany('''
                INSERT INTO historico_canon (numero_local, ano, canon)
                VALUES (?, ?, ?)
            ''', cargar_historicos_canon())
        
        conn.commit()
    except Exception as e:
        st.error(f"Error al inicializar la base de datos: {str(e)}")
    finally:
        conn.close()

# --- FUNCIONES DE CONSULTA --- #
def obtener_locales():
    """Obtiene lista de todos los locales"""
    conn = get_db_connection()
    df = pd.read_sql("SELECT numero_local FROM locales ORDER BY numero_local", conn)
    conn.close()
    return df['numero_local'].tolist()

def obtener_inquilinos():
    """Obtiene lista de inquilinos únicos"""
    conn = get_db_connection()
    df = pd.read_sql("SELECT DISTINCT inquilino FROM locales ORDER BY inquilino", conn)
    conn.close()
    return df['inquilino'].tolist()

def obtener_locales_por_inquilino(inquilino):
    """Obtiene locales asociados a un inquilino"""
    conn = get_db_connection()
    df = pd.read_sql(
        "SELECT numero_local FROM locales WHERE inquilino = ? ORDER BY numero_local",
        conn, params=(inquilino,)
    )
    conn.close()
    return df['numero_local'].tolist()

def obtener_info_local(numero_local):
    """Obtiene información detallada de un local"""
    conn = get_db_connection()
    df = pd.read_sql('''
        SELECT l.*, h.canon 
        FROM locales l
        JOIN (
            SELECT numero_local, MAX(ano) as max_ano 
            FROM historico_canon 
            GROUP BY numero_local
        ) ultimo ON l.numero_local = ultimo.numero_local
        JOIN historico_canon h ON l.numero_local = h.numero_local AND h.ano = ultimo.max_ano
        WHERE l.numero_local = ?
    ''', conn, params=(numero_local,))
    conn.close()
    return df.iloc[0] if not df.empty else None

def obtener_canon_historico(numero_local, ano=None):
    """Obtiene el canon de un local para un año específico"""
    conn = get_db_connection()
    if ano:
        df = pd.read_sql(
            "SELECT canon FROM historico_canon WHERE numero_local = ? AND ano = ?",
            conn, params=(numero_local, ano)
        )
    else:
        df = pd.read_sql('''
            SELECT canon FROM historico_canon 
            WHERE numero_local = ? 
            ORDER BY ano DESC LIMIT 1
        ''', conn, params=(numero_local,))
    conn.close()
    return df.iloc[0]['canon'] if not df.empty else None

# --- FUNCIONES DE REGISTRO --- #
def registrar_pago(local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
    """Registra un nuevo pago con validación de datos"""
    if not validar_formato_mes(mes_abonado):
        raise ValueError("Formato de mes inválido. Use YYYY-MM")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si ya existe un pago para este mes
        cursor.execute('''
            SELECT 1 FROM pagos 
            WHERE numero_local = ? AND mes_abonado = ?
        ''', (local, mes_abonado))
        
        if cursor.fetchone():
            raise ValueError(f"Ya existe un pago registrado para {local} en {mes_abonado}")
        
        # Insertar el nuevo pago
        cursor.execute('''
            INSERT INTO pagos (
                numero_local, inquilino, fecha_pago, mes_abonado, 
                monto, estado, observaciones
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def actualizar_canon_local(numero_local, ano, nuevo_canon):
    """Actualiza el canon de un local para un año específico"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO historico_canon (numero_local, ano, canon)
            VALUES (?, ?, ?)
        ''', (numero_local, ano, nuevo_canon))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# --- FUNCIONES DE CÁLCULO --- #
def calcular_morosidad(inquilino=None, local=None):
    """Calcula meses adeudados y montos pendientes"""
    conn = get_db_connection()
    
    # Construir consulta dinámica
    query = '''
        WITH meses_pagados AS (
            SELECT 
                numero_local,
                mes_abonado
            FROM pagos
            WHERE estado IN ('Pagado', 'Parcial')
            GROUP BY numero_local, mes_abonado
        ),
        meses_adeudados AS (
            SELECT 
                l.numero_local,
                l.inquilino,
                h.ano,
                h.canon,
                printf("%04d-%02d", h.ano, m.mes) AS mes
            FROM locales l
            JOIN historico_canon h ON l.numero_local = h.numero_local
            JOIN (
                WITH RECURSIVE meses(mes) AS (
                    SELECT 1
                    UNION ALL
                    SELECT mes+1 FROM meses WHERE mes < 12
                ) SELECT mes FROM meses
            ) m
            WHERE printf("%04d-%02d", h.ano, m.mes) NOT IN (
                SELECT mes_abonado FROM meses_pagados WHERE numero_local = l.numero_local
            )
            AND printf("%04d-%02d", h.ano, m.mes) < strftime("%Y-%m", date('now'))
        )
        SELECT 
            numero_local,
            inquilino,
            COUNT(*) AS meses_adeudados,
            SUM(canon) AS total_adeudado,
            GROUP_CONCAT(mes, ', ') AS periodos_adeudados
        FROM meses_adeudados
        WHERE 1=1
    '''
    
    params = []
    if inquilino:
        query += " AND inquilino = ?"
        params.append(inquilino)
    if local:
        query += " AND numero_local = ?"
        params.append(local)
    
    query += " GROUP BY numero_local, inquilino ORDER BY total_adeudados DESC"
    
    df = pd.read_sql(query, conn, params=params if params else None)
    conn.close()
    return df

# --- FUNCIONES DE VALIDACIÓN --- #
def validar_formato_mes(mes_str):
    """Valida que el string tenga formato YYYY-MM"""
    try:
        datetime.strptime(mes_str, "%Y-%m")
        return True
    except ValueError:
        return False

# --- INTERFAZ DE USUARIO --- #
def mostrar_formulario_pago():
    """Formulario principal para registrar pagos"""
    st.subheader("📝 Registrar Pago")
    
    with st.form(key='form_pago'):
        col1, col2 = st.columns(2)
        
        with col1:
            inquilino = st.selectbox(
                "Inquilino*",
                options=obtener_inquilinos(),
                key="select_inquilino"
            )
            
            local = st.selectbox(
                "Local*",
                options=obtener_locales_por_inquilino(inquilino) if inquilino else [],
                key="select_local"
            )
            
            if local:
                info = obtener_info_local(local)
                st.markdown(f"""
                    **Planta:** {info['planta']}  
                    **Ramo:** {info['ramo_negocio']}  
                    **Canon Actual:** ${info['canon']:,.2f}  
                    **Contrato:** {info['contrato']}
                """)
        
        with col2:
            fecha_pago = st.date_input(
                "Fecha de Pago*",
                value=date.today(),
                max_value=date.today()
            )
            
            mes_abonado = st.text_input(
                "Mes Abonado* (YYYY-MM)",
                value=date.today().strftime("%Y-%m")
            )
            
            monto = st.number_input(
                "Monto*",
                min_value=0.0,
                value=float(info['canon']) if local else 0.0,
                step=10.0
            )
            
            estado = st.selectbox(
                "Estado*",
                options=["Pagado", "Parcial"]
            )
            
            observaciones = st.text_area("Observaciones")
        
        submitted = st.form_submit_button("💾 Guardar Pago")
        
        if submitted:
            if not all([local, inquilino, mes_abonado]):
                st.error("Campos obligatorios faltantes")
            elif not validar_formato_mes(mes_abonado):
                st.error("Formato de mes inválido. Use YYYY-MM")
            else:
                try:
                    registrar_pago(
                        local, inquilino, fecha_pago, 
                        mes_abonado, monto, estado, observaciones
                    )
                    st.success("✅ Pago registrado exitosamente!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

def mostrar_morosos():
    """Interfaz para consultar morosidad"""
    st.subheader("🚨 Consulta de Morosidad")
    
    filtro = st.radio("Filtrar por:", ["Todos", "Inquilino", "Local"])
    
    if filtro == "Inquilino":
        inquilino = st.selectbox("Seleccione inquilino", obtener_inquilinos())
        df = calcular_morosidad(inquilino=inquilino)
    elif filtro == "Local":
        local = st.selectbox("Seleccione local", obtener_locales())
        df = calcular_morosidad(local=local)
    else:
        df = calcular_morosidad()
    
    if not df.empty:
        st.dataframe(
            df.style.format({
                'total_adeudado': '${:,.2f}'
            }),
            use_container_width=True
        )
        
        total_adeudado = df['total_adeudado'].sum()
        st.metric("Total Adeudado", f"${total_adeudado:,.2f}")
    else:
        st.success("👍 No hay morosidad registrada")

def mostrar_historial():
    """Interfaz para consultar historial de pagos"""
    st.subheader("📜 Historial de Pagos")
    
    col1, col2 = st.columns(2)
    with col1:
        local = st.selectbox(
            "Local (opcional)",
            options=["Todos"] + obtener_locales(),
            index=0
        )
    
    with col2:
        inquilino = st.selectbox(
            "Inquilino (opcional)",
            options=["Todos"] + obtener_inquilinos(),
            index=0
        )
    
    # Construir consulta dinámica
    query = '''
        SELECT 
            p.numero_local,
            p.inquilino,
            p.fecha_pago,
            p.mes_abonado,
            p.monto,
            p.estado,
            p.observaciones
        FROM pagos p
        WHERE 1=1
    '''
    
    params = []
    if local != "Todos":
        query += " AND p.numero_local = ?"
        params.append(local)
    if inquilino != "Todos":
        query += " AND p.inquilino = ?"
        params.append(inquilino)
    
    query += " ORDER BY p.fecha_pago DESC"
    
    conn = get_db_connection()
    df = pd.read_sql(query, conn, params=params if params else None)
    conn.close()
    
    if not df.empty:
        st.dataframe(
            df.style.format({
                'monto': '${:,.2f}'
            }),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No se encontraron registros")

def mostrar_administracion():
    """Interfaz para administrar cánones"""
    st.subheader("⚙️ Administrar Cánones")
    
    tab1, tab2 = st.tabs(["Actualizar Canon", "Histórico por Local"])
    
    with tab1:
        with st.form(key='form_canon'):
            local = st.selectbox("Local", obtener_locales())
            ano = st.number_input("Año", min_value=2020, max_value=date.today().year, value=date.today().year)
            nuevo_canon = st.number_input("Nuevo Canon", min_value=0.0, step=10.0)
            
            if st.form_submit_button("💾 Actualizar Canon"):
                try:
                    actualizar_canon_local(local, ano, nuevo_canon)
                    st.success(f"✅ Canon actualizado: Local {local} - Año {ano} = ${nuevo_canon:,.2f}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab2:
        local_hist = st.selectbox("Seleccione local para ver histórico", obtener_locales())
        conn = get_db_connection()
        df = pd.read_sql('''
            SELECT ano, canon 
            FROM historico_canon 
            WHERE numero_local = ?
            ORDER BY ano
        ''', conn, params=(local_hist,))
        conn.close()
        
        if not df.empty:
            st.dataframe(
                df.style.format({
                    'canon': '${:,.2f}'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # Mostrar gráfico de evolución
            st.line_chart(df.set_index('ano'), y='canon')
        else:
            st.warning("No hay histórico registrado para este local")

# --- APLICACIÓN PRINCIPAL --- #
def main():
    st.set_page_config(
        page_title="Sistema de Pagos Arvelo",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    init_db()  # Inicializar base de datos
    
    st.title("💰 Sistema de Gestión de Pagos - Arvelo")
    st.markdown("---")
    
    menu = st.sidebar.selectbox(
        "Menú Principal",
        ["Registrar Pago", "Consultar Morosidad", "Historial de Pagos", "Administración"]
    )
    
    if menu == "Registrar Pago":
        mostrar_formulario_pago()
    elif menu == "Consultar Morosidad":
        mostrar_morosos()
    elif menu == "Historial de Pagos":
        mostrar_historial()
    elif menu == "Administración":
        mostrar_administracion()
    
    # Backup en el sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Generar Backup de la Base de Datos"):
        try:
            db_path = os.path.join(tempfile.gettempdir(), "pagos_arvelo_v2.db")
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                shutil.copy2(db_path, tmp.name)
                with open(tmp.name, 'rb') as f:
                    st.sidebar.download_button(
                        "⬇️ Descargar Backup",
                        f,
                        file_name="backup_pagos_arvelo.db"
                    )
            st.sidebar.success("Backup generado correctamente")
        except Exception as e:
            st.sidebar.error(f"Error al generar backup: {str(e)}")

if __name__ == "__main__":
    main()
