import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date
import tempfile
import os
import re
from time import sleep

# 1. CONFIGURACIÓN DE LA BASE DE DATOS
@st.cache_resource(ttl=3600)
def get_db_connection():
    """Conexión persistente a la base de datos SQLite."""
    temp_dir = tempfile.gettempdir()
    db_path = os.path.join(temp_dir, "pagos_arvelo_optimized.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# 2. DATOS INICIALES
def cargar_datos_iniciales():
    """Datos iniciales de locales."""
    return [
        ('LOCAL A', 'MONICA JANET VARGAS G.', 'PB', 'LENCERIA', 350.0, 'MONICA JANET VARGAS G.'),
        ('LOCAL B', 'OSCAR DUQUE ECHEVERRIA', 'PB', 'LENCERIA', 350.0, 'OSCAR DUQUE ECHEVERRI'),
        ('LOCAL 1', 'JOSE MANUEL ANDRADE PEREIRA', 'PB', 'MANUFACTURA', 70.0, 'JOSE M. ANDRADE PEREIRA'),
        ('LOCAL 2', 'JOSE MANUEL ANDRADE PEREIRA', 'PB', 'MANUFACTURA', 70.0, 'JOSE M. ANDRADE PEREIRA'),
        ('LOCAL 3', 'JOSE MANUEL ANDRADE PEREIRA', 'PB', 'MANUFACTURA', 70.0, 'JOSE M. ANDRADE PEREIRA'),
        ('LOCAL 4', 'JOSE R. RODRIGUEZ V.', 'PB', 'DOMESA', 33.33, 'YORMAN JOSE VALERA'),
        ('LOCAL 5', 'JOSE R. RODRIGUEZ V.', 'PB', 'DOMESA', 33.33, 'YORMAN JOSE VALERA'),
        ('LOCAL 5A', 'JOSE R. RODRIGUEZ V.', 'PB', 'DOMESA', 33.33, 'YORMAN JOSE VALERA'),
        ('LOCAL 6', 'Daniel', 'PB', 'Compra/Venta Oro', 50.0, 'DANNYS JOSE GARCIA'),
        ('LOCAL 7', 'YAMILETH JOSEFINA CHACON', 'PB', 'SANTERIA', 70.0, 'YAMILET JOSEFINA CHACON'),
        ('LOCAL 8', 'JOSE ANTONIO SPANO', 'PB', 'ODONTOLOGIA', 50.0, 'JOSE ANTONIO SPANO'),
        ('LOCAL 9', 'JOSE ANTONIO SPANO', 'PB', 'ODONTOLOGIA', 50.0, 'JOSE ANTONIO SPANO'),
        ('LOCAL 10', 'YANIRE NAVARRO VIVES', 'PB', 'ARTESANIA', 150.0, 'YANIRE NAVARRO VIDES'),
        ('LOCAL 11 A', 'IVAN SILVA', 'PB', 'ROPA', 80.0, 'ARENAS DEL NILO C.A'),
        ('LOCAL 11', 'MARTIN SANTOS', 'PB', 'NO SE', 60.0, 'MARTIN SANTOS'),
        ('LOCAL 12', 'MARTIN SANTOS', 'PB', 'NO SE', 60.0, 'MARTIN SANTOS'),
        ('LOCAL 13', 'ESPERANZA RUEDA', 'PB', 'ROPA', 70.0, 'ESPERANZA RUEDA'),
        ('LOCAL 14', 'SUSANA DO LIVRAMENTO', 'PB', 'PERFUMES', 70.0, 'SUSANA DO LIVRAMENTO'),
        ('LOCAL 15', 'JUAN ANTONIO RODRIGUEZ', 'PB', 'OPTICA', 70.0, 'JUAN ANTONIO RODRÍGUEZ'),
        ('LOCAL 16', 'MARYABETH TOVAR Y ALDO M.', 'PB', 'CYBER', 70.0, 'YULIANA SINDY POVES VALLADARES'),
        ('LOCAL 17', 'YANIRE NAVARRO VIVES', 'PB', 'ARTESANIA', 37.5, 'YANIRE NAVARRO VIDES'),
        ('LOCAL 18', 'YANIRE NAVARRO VIVES', 'PB', 'ARTESANIA', 37.5, 'YANIRE NAVARRO VIDES'),
        ('LOCAL 19', 'YANIRE NAVARRO VIVES', 'PB', 'ARTESANIA', 37.5, 'YANIRE NAVARRO VIDES'),
        ('MEZZANINA 1', 'OSCAR DUQUE', 'MEZZANINA 1', '', 100.0, 'OSCAR DUQUE ECHEVERRI'),
        ('LOCAL 27', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 25.0, 'CARLOS Y ELVIS MIÑANO'),
        ('LOCAL 28', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 25.0, 'CARLOS Y ELVIS MIÑANO'),
        ('LOCAL 29', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 25.0, 'CARLOS Y ELVIS MIÑANO'),
        ('LOCAL 30', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 25.0, 'CARLOS Y ELVIS MIÑANO'),
        ('LOCAL 34', 'JACQUELINE QUINTANA', 'MEZZANINA 1', '', 60.0, 'JACQUELINE QUINTANA'),
        ('LOCAL 35', 'JACQUELINE QUINTANA', 'MEZZANINA 1', '', 60.0, 'JACQUELINE QUINTANA'),
        ('MEZZANINA 2', 'CARLOS GOMEZ ZULOAGA', 'MEZZANINA 1', '', 120.0, 'CARLOS MARIO GOMEZ'),
        ('LOCAL 40', 'JHON SERNA GOMEZ', 'MEZZANINA 1', '', 120.0, 'JHON SERNA GOMEZ'),
        ('LOCAL 42', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 16.67, 'GERARDO MIÑANO TRUJILLO'),
        ('LOCAL 43', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 16.67, 'GERARDO MIÑANO TRUJILLO'),
        ('LOCAL 44', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 16.67, 'GERARDO MIÑANO TRUJILLO'),
        ('LOCAL 45', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 16.67, 'GERARDO MIÑANO TRUJILLO'),
        ('LOCAL 46', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 16.67, 'GERARDO MIÑANO TRUJILLO'),
        ('LOCAL 47', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 16.67, 'GERARDO MIÑANO TRUJILLO'),
        ('LOCAL 31', 'ALDO MUÑOZ Y JARRISON HEVER', 'MEZZANINA 1', 'SUSHI', 50.0, 'ALDO MUÑOZ y JARRISON HEVER'),
        ('LOCAL 32', 'ALDO MUÑOZ Y JARRISON HEVER', 'MEZZANINA 1', 'SUSHI', 50.0, 'ALDO MUÑOZ y JARRISON HEVER'),
        ('LOCAL S/N', 'SALVADOR FREITAS NUNES', 'MEZZANINA 1', 'RESTAURANT', 200.0, 'SALVADOR FREITAS NUNES'),
        ('LOCAL 2-4', 'AURA MARINA', 'MEZZANINA 1', 'TELAS', 50.0, 'AURA MARINA MONTILLA'),
        ('LOCAL 2-5', 'AURA MARINA', 'MEZZANINA 1', 'TELAS', 50.0, 'AURA MARINA MONTILLA'),
        ('LOCAL 2-2', 'ESPERANZA RUEDA', 'MEZZANINA 2', '', 23.33, 'FEDERICK JACOB OVALLES'),
        ('LOCAL 2-3', 'ESPERANZA RUEDA', 'MEZZANINA 2', '', 23.33, 'FEDERICK JACOB OVALLES'),
        ('LOCAL 2 -3', 'DESOCUPADO', 'MEZZANINA 2', '', 23.33, 'FEDERICK JACOB OVALLES'),
        ('LOCAL 2 -7', 'DESOCUPADO', 'MEZZANINA 2', '', 23.33, 'Martin Santos'),
        ('LOCAL 2-4', 'JOSE ANTONIO DO FAIAL', 'MEZZANINA 2', 'ACRILICOS', 60.0, 'JOSE ANTONIO FAIAL PESTAÑA'),
        ('LOCAL 2-5', 'JOSE ANTONIO DO FAIAL', 'MEZZANINA 2', 'ACRILICOS', 60.0, 'JOSE ANTONIO FAIAL PESTAÑA'),
        ('LOCAL 34', 'ELY SAUL QUINTERO CUELLAE', 'MEZZANINA 2', '', 16.67, 'ELY SAUL QUINTERO CUELLAR'),
        ('LOCAL 35', 'ELY SAUL QUINTERO CUELLAE', 'MEZZANINA 2', '', 16.67, 'ELY SAUL QUINTERO CUELLAR'),
        ('LOCAL 36', 'ELY SAUL QUINTERO CUELLAE', 'MEZZANINA 2', '', 16.67, 'ELY SAUL QUINTERO CUELLAR'),
        ('LOCAL 37', 'ELY SAUL QUINTERO CUELLAE', 'MEZZANINA 2', '', 16.67, 'ELY SAUL QUINTERO CUELLAR'),
        ('LOCAL 38', 'ELY SAUL QUINTERO CUELLAE', 'MEZZANINA 2', '', 16.67, 'ELY SAUL QUINTERO CUELLAR'),
        ('LOCAL 39', 'ELY SAUL QUINTERO CUELLAE', 'MEZZANINA 2', '', 16.67, 'ELY SAUL QUINTERO CUELLAR')

    ]

# 3. INICIALIZACIÓN DE LA BASE DE DATOS
def init_db():
    """Inicializa la estructura de la base de datos."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Tabla de locales
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locales (
                numero_local TEXT PRIMARY KEY,
                inquilino TEXT NOT NULL,
                planta TEXT,
                ramo_negocio TEXT,
                contrato TEXT
            )
        ''')
        
        # Tabla de pagos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_local TEXT NOT NULL,
                inquilino TEXT NOT NULL,
                fecha_pago DATE NOT NULL,
                mes_abonado TEXT NOT NULL,
                monto REAL NOT NULL,
                estado TEXT CHECK(estado IN ('Pagado', 'Parcial', 'Pendiente')),
                observaciones TEXT,
                FOREIGN KEY(numero_local) REFERENCES locales(numero_local)
            )
        ''')
        
        # Insertar datos iniciales si la tabla está vacía
        if cursor.execute("SELECT COUNT(*) FROM locales").fetchone()[0] == 0:
            with st.spinner('Cargando datos iniciales...'):
                for dato in cargar_datos_iniciales():
                    cursor.execute(
                        '''INSERT OR IGNORE INTO locales 
                        (numero_local, inquilino, planta, ramo_negocio, contrato)
                        VALUES (?, ?, ?, ?, ?)''',
                        (dato[0], dato[1], dato[2], dato[3], dato[5])
                    )
                conn.commit()
    except Exception as e:
        st.error(f"Error al inicializar la base de datos: {str(e)}")
        st.stop()

# 4. FUNCIONES DE CONSULTA OPTIMIZADAS
@st.cache_data(ttl=300)
def obtener_inquilinos():
    """Obtiene todos los inquilinos únicos."""
    conn = get_db_connection()
    df = pd.read_sql("SELECT DISTINCT inquilino FROM locales ORDER BY inquilino", conn)
    return [""] + df['inquilino'].tolist()

@st.cache_data(ttl=300)
def obtener_locales_por_inquilino(inquilino):
    """Obtiene locales de un inquilino específico."""
    if not inquilino or not inquilino.strip():
        return []
        
    conn = get_db_connection()
    df = pd.read_sql(
        "SELECT numero_local FROM locales WHERE inquilino = ? ORDER BY numero_local",
        conn, params=(inquilino,)
    )
    return df['numero_local'].tolist()

@st.cache_data(ttl=300)
def obtener_info_local(numero_local):
    """Obtiene información de un local específico."""
    if not numero_local:
        return None
        
    conn = get_db_connection()
    df = pd.read_sql(
        "SELECT * FROM locales WHERE numero_local = ?",
        conn, params=(numero_local,)
    )
    return df.iloc[0] if not df.empty else None

@st.cache_data(ttl=300)
def obtener_pagos(filtro_mes=None, filtro_inquilino=None):
    """Obtiene pagos con filtros opcionales."""
    conn = get_db_connection()
    query = "SELECT * FROM pagos WHERE 1=1"
    params = []
    
    if filtro_mes:
        query += " AND mes_abonado = ?"
        params.append(filtro_mes)
        
    if filtro_inquilino:
        query += " AND inquilino = ?"
        params.append(filtro_inquilino)
        
    query += " ORDER BY fecha_pago DESC, id DESC"
    return pd.read_sql(query, conn, params=params if params else None)

# 5. FUNCIÓN DE REGISTRO DE PAGOS
def registrar_pago(local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
    """Registra un nuevo pago en la base de datos."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO pagos (
                numero_local, inquilino, fecha_pago, mes_abonado, 
                monto, estado, observaciones
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (local, inquilino, fecha_pago.strftime('%Y-%m-%d'), mes_abonado, monto, estado, observaciones))
        
        conn.commit()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error al registrar el pago: {str(e)}")
        conn.rollback()
        return False

# 6. FORMULARIO DE PAGOS OPTIMIZADO
def mostrar_formulario_pago():
    """Muestra el formulario para registrar pagos."""
    st.subheader("📝 Registrar Nuevo Pago")
    
    # Inicializar estado de sesión
    if 'current_inquilino' not in st.session_state:
        st.session_state.current_inquilino = ""
    
    with st.form(key='form_pago', clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Selector de inquilino
            inquilinos = obtener_inquilinos()
            selected_inquilino = st.selectbox(
                "Seleccione Inquilino*",
                options=inquilinos,
                index=0,
                key='inquilino_select'
            )
            
            # Actualizar locales cuando cambia el inquilino
            locales_disponibles = [""]
            if selected_inquilino:
                if selected_inquilino != st.session_state.current_inquilino:
                    obtener_locales_por_inquilino.clear()
                    st.session_state.current_inquilino = selected_inquilino
                
                locales = obtener_locales_por_inquilino(selected_inquilino)
                locales_disponibles += locales
            
            # Selector de local
            selected_local = st.selectbox(
                "Seleccione Local*",
                options=locales_disponibles,
                index=0,
                key='local_select'
            )
            
            # Mostrar información del local
            if selected_local:
                info_local = obtener_info_local(selected_local)
                if info_local:
                    st.info(f"""
                        **Planta:** {info_local['planta']}  
                        **Ramo:** {info_local['ramo_negocio']}  
                        **Contrato:** {info_local['contrato']}
                    """)
        
        with col2:
            fecha_pago = st.date_input("Fecha de Pago*", value=date.today())
            mes_abonado = st.text_input("Mes Abonado* (YYYY-MM)", placeholder="Ej: 2023-01")
            monto = st.number_input("Monto* (USD)", min_value=0.0, value=0.0, step=1.0, format="%.2f")
            estado = st.selectbox("Estado*", options=["Pagado", "Parcial", "Pendiente"])
            observaciones = st.text_area("Observaciones (opcional)")
        
        submitted = st.form_submit_button("💾 Guardar Pago")
        
        if submitted:
            # Validaciones
            if not selected_inquilino:
                st.error("Seleccione un inquilino")
            elif not selected_local:
                st.error("Seleccione un local")
            elif not mes_abonado or not re.match(r"^\d{4}-\d{2}$", mes_abonado):
                st.error("El mes abonado debe tener formato YYYY-MM")
            elif monto <= 0:
                st.error("El monto debe ser mayor que cero")
            else:
                with st.spinner('Guardando pago...'):
                    if registrar_pago(
                        selected_local, selected_inquilino,
                        fecha_pago, mes_abonado, monto, estado, observaciones
                    ):
                        st.success("✅ Pago registrado exitosamente!")
                        sleep(1)
                        st.experimental_rerun()

# 7. HISTORIAL DE PAGOS MEJORADO
def mostrar_historial_pagos():
    """Muestra el historial de pagos con filtros."""
    st.subheader("📜 Historial de Pagos")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        filtro_mes = st.text_input("Filtrar por mes (YYYY-MM)", "")
    with col2:
        filtro_inquilino = st.selectbox("Filtrar por inquilino", [""] + obtener_inquilinos()[1:])
    
    # Obtener datos
    pagos_df = obtener_pagos(
        filtro_mes if filtro_mes and re.match(r"^\d{4}-\d{2}$", filtro_mes) else None,
        filtro_inquilino if filtro_inquilino else None
    )
    
    if pagos_df.empty:
        st.info("No hay pagos registrados con los filtros seleccionados.")
    else:
        st.dataframe(pagos_df, use_container_width=True, hide_index=True)
        
        # Exportar a Excel
        if st.button("📤 Exportar a Excel"):
            with st.spinner('Generando archivo...'):
                excel_file = pagos_df.to_excel("historial_pagos.xlsx", index=False)
                with open("historial_pagos.xlsx", "rb") as f:
                    st.download_button(
                        label="⬇️ Descargar archivo",
                        data=f,
                        file_name=f"historial_pagos_{date.today()}.xlsx",
                        mime="application/vnd.ms-excel"
                    )

# 8. REPORTE DE MOROSIDAD
def mostrar_reporte_morosidad():
    """Muestra un reporte de morosidad."""
    st.subheader("⚠️ Reporte de Morosidad")
    
    conn = get_db_connection()
    try:
        meses_df = pd.read_sql(
            "SELECT DISTINCT mes_abonado FROM pagos ORDER BY mes_abonado DESC",
            conn
        )
        
        if meses_df.empty:
            st.info("No hay datos suficientes para generar reportes.")
            return
            
        mes_seleccionado = st.selectbox("Seleccione mes para reporte", meses_df['mes_abonado'])
        
        if st.button("Generar Reporte"):
            with st.spinner('Analizando datos...'):
                morosos_df = pd.read_sql('''
                    SELECT l.numero_local, l.inquilino, l.planta, l.ramo_negocio
                    FROM locales l
                    WHERE NOT EXISTS (
                        SELECT 1 FROM pagos p 
                        WHERE p.numero_local = l.numero_local 
                        AND p.mes_abonado = ?
                        AND p.estado = 'Pagado'
                    )
                    ORDER BY l.inquilino
                ''', conn, params=(mes_seleccionado,))
                
                if morosos_df.empty:
                    st.success(f"¡Todos los locales pagaron en {mes_seleccionado}!")
                else:
                    st.dataframe(morosos_df, use_container_width=True)
    except Exception as e:
        st.error(f"Error al generar reporte: {str(e)}")

# 9. INTERFAZ PRINCIPAL
def main():
    """Configuración principal de la aplicación."""
    st.set_page_config(
        page_title="Sistema de Pagos Arvelo",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inicializar base de datos
    init_db()
    
    # UI Principal
    st.title("💰 Sistema de Gestión de Pagos - Arvelo")
    st.markdown("---")
    
    # Menú de navegación
    with st.sidebar:
        st.header("Menú Principal")
        menu = st.radio(
            "Seleccione una opción",
            ["Registrar Pago", "Historial de Pagos", "Reporte de Morosidad"],
            index=0
        )
        st.markdown("---")
        st.info(f"Versión: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Mostrar sección correspondiente
    if menu == "Registrar Pago":
        mostrar_formulario_pago()
    elif menu == "Historial de Pagos":
        mostrar_historial_pagos()
    elif menu == "Reporte de Morosidad":
        mostrar_reporte_morosidad()

if __name__ == "__main__":
    main()
