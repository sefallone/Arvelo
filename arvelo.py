# 1. IMPORTACIONES
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date
import tempfile
import os
import re
from time import sleep
import shutil
import difflib
import plotly.express as px

# 2. CONFIGURACIÓN DE BASE DE DATOS
@st.cache_resource
def get_db_connection():
    """Crea una conexión persistente a SQLite con mejor configuración."""
    temp_dir = tempfile.gettempdir()
    db_path = os.path.join(temp_dir, "pagos_arvelo_final_corregido.db")
    
    conn = sqlite3.connect(db_path, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    
    return conn

# 3. FUNCIÓN DE BACKUP
def hacer_backup():
    """Realiza backup de la base de datos."""
    conn = get_db_connection()
    conn.commit()
    
    backup_dir = os.path.join(os.path.expanduser("~"), "backups_pagos_arvelo")
    os.makedirs(backup_dir, exist_ok=True)
    
    db_path = os.path.join(tempfile.gettempdir(), "pagos_arvelo_final_corregido.db")
    backup_path = os.path.join(backup_dir, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
    
    try:
        shutil.copy2(db_path, backup_path)
        return backup_path
    except Exception as e:
        st.error(f"Error al crear backup: {str(e)}")
        return None

# 4. SISTEMA DE AUDITORÍA
def registrar_auditoria(tabla, operacion, detalles=""):
    """Registra una entrada en el log de auditoría."""
    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO auditoria (tabla_afectada, operacion, fecha_hora, detalles)
            VALUES (?, ?, ?, ?)
        ''', (tabla, operacion, datetime.now(), detalles))
        conn.commit()
    except Exception as e:
        st.error(f"Error al registrar auditoría: {str(e)}")

# 5. DATOS INICIALES
def cargar_datos_iniciales():
    """Retorna datos iniciales con todos los locales."""
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

# 6. INICIALIZACIÓN DE BASE DE DATOS
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
                contrato TEXT,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
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
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(numero_local) REFERENCES locales(numero_local)
            )
        ''')
        
        # Tabla de auditoría
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auditoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tabla_afectada TEXT NOT NULL,
                operacion TEXT NOT NULL,
                fecha_hora DATETIME NOT NULL,
                usuario TEXT,
                detalles TEXT
            )
        ''')
        
        # Insertar datos iniciales
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
                
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_locales_timestamp
            AFTER UPDATE ON locales
            FOR EACH ROW
            BEGIN
                UPDATE locales SET fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE numero_local = OLD.numero_local;
            END;
        ''')
        
        conn.commit()
        
    except Exception as e:
        st.error(f"Error al inicializar la base de datos: {str(e)}")
        conn.rollback()
        st.stop()

# 7. VALIDACIÓN DE DATOS
def validar_mes(mes_str):
    """Valida que el formato del mes sea YYYY-MM."""
    try:
        datetime.strptime(mes_str, "%Y-%m")
        return True
    except ValueError:
        st.error("Formato de mes inválido. Use YYYY-MM (ej. 2023-01)")
        return False

def sugerir_inquilinos(query):
    """Sugiere inquilinos similares usando difflib."""
    inquilinos = obtener_inquilinos()[1:]
    sugerencias = difflib.get_close_matches(query, inquilinos, n=3, cutoff=0.6)
    return sugerencias if sugerencias else []

# 8. FUNCIONES DE CONSULTA
@st.cache_data(ttl=3600)
def obtener_inquilinos():
    """Retorna todos los inquilinos únicos con caché."""
    conn = get_db_connection()
    df = pd.read_sql("SELECT DISTINCT inquilino FROM locales ORDER BY inquilino", conn)
    return [""] + df['inquilino'].tolist()

def obtener_locales_por_inquilino(inquilino):
    """Retorna locales del inquilino especificado."""
    if not inquilino:
        return []
        
    conn = get_db_connection()
    df = pd.read_sql(
        "SELECT numero_local FROM locales WHERE inquilino = ? ORDER BY numero_local",
        conn, params=(inquilino,)
    )
    return df['numero_local'].tolist()

def obtener_info_local(numero_local):
    """Obtiene información detallada de un local."""
    if not numero_local:
        return None
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT planta, ramo_negocio, contrato FROM locales WHERE numero_local = ?",
        (numero_local,)
    )
    return dict(cursor.fetchone())

def obtener_pagos(filtro_mes=None, filtro_inquilino=None):
    """Obtiene pagos con opciones de filtrado."""
    conn = get_db_connection()
    query = "SELECT * FROM pagos"
    params = []
    
    conditions = []
    if filtro_mes:
        conditions.append("mes_abonado = ?")
        params.append(filtro_mes)
    if filtro_inquilino:
        conditions.append("inquilino = ?")
        params.append(filtro_inquilino)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY fecha_pago DESC"
    
    return pd.read_sql(query, conn, params=params if params else None)

# 9. REGISTRO DE PAGOS
def registrar_pago(local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
    """Registra un nuevo pago."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO pagos (
                numero_local, inquilino, fecha_pago, mes_abonado, 
                monto, estado, observaciones
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones))
        
        conn.commit()
        registrar_auditoria("pagos", "INSERT", f"Pago registrado para local {local}")
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error al registrar el pago: {str(e)}")
        conn.rollback()
        return False

# 10. FORMULARIO DE PAGOS
def mostrar_formulario_pago():
    """Muestra el formulario para registrar pagos."""
    st.subheader("📝 Registrar Nuevo Pago")
    
    with st.form(key='form_pago', clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            input_inquilino = st.text_input("Buscar Inquilino*", "")
            if input_inquilino:
                sugerencias = sugerir_inquilinos(input_inquilino)
                if sugerencias:
                    st.info("Sugerencias: " + ", ".join(sugerencias))
            
            selected_inquilino = st.selectbox(
                "Seleccione Inquilino*",
                options=obtener_inquilinos(),
                index=0
            )
            
            locales_disponibles = [""] + (obtener_locales_por_inquilino(selected_inquilino) if selected_inquilino else [])
            selected_local = st.selectbox(
                "Seleccione Local*",
                options=locales_disponibles,
                index=0
            )
            
        with col2:
            fecha_pago = st.date_input("Fecha de Pago*", value=date.today())
            mes_abonado = st.text_input("Mes Abonado* (YYYY-MM)", placeholder="2023-01")
            monto = st.number_input("Monto* (USD)", min_value=0.0, value=0.0, step=1.0)
            estado = st.selectbox("Estado*", ["Pagado", "Parcial", "Pendiente"])
            observaciones = st.text_area("Observaciones")
        
        submitted = st.form_submit_button("💾 Guardar Pago")
        
        if submitted:
            if not all([selected_inquilino, selected_local, mes_abonado, monto > 0]):
                st.error("Complete todos los campos obligatorios (*)")
            elif not validar_mes(mes_abonado):
                return
            else:
                if registrar_pago(
                    selected_local, selected_inquilino,
                    fecha_pago, mes_abonado, monto, estado, observaciones
                ):
                    st.success("✅ Pago registrado exitosamente!")
                    sleep(2)
                    st.experimental_rerun()

# 11. HISTORIAL DE PAGOS
def mostrar_historial_pagos():
    """Muestra el historial de pagos."""
    st.subheader("📜 Historial de Pagos")
    
    col1, col2 = st.columns(2)
    with col1:
        filtro_mes = st.text_input("Filtrar por mes (YYYY-MM)", "")
    with col2:
        filtro_inquilino = st.selectbox("Filtrar por inquilino", [""] + obtener_inquilinos()[1:])
    
    pagos_df = obtener_pagos(
        filtro_mes if filtro_mes and re.match(r"^\d{4}-\d{2}$", filtro_mes) else None,
        filtro_inquilino if filtro_inquilino else None
    )
    
    if pagos_df.empty:
        st.info("No hay pagos registrados con los filtros seleccionados.")
    else:
        total = pagos_df['monto'].sum()
        st.metric("Total filtrado", f"${total:,.2f}")
        st.dataframe(pagos_df, use_container_width=True)
        
        if st.button("📤 Exportar a Excel"):
            with st.spinner('Generando archivo...'):
                pagos_df.to_excel("historial_pagos.xlsx", index=False)
                with open("historial_pagos.xlsx", "rb") as f:
                    st.download_button(
                        label="⬇️ Descargar archivo",
                        data=f,
                        file_name=f"historial_pagos_{date.today()}.xlsx",
                        mime="application/vnd.ms-excel"
                    )

# 12. REPORTE DE MOROSIDAD
def generar_reporte_morosidad():
    """Genera reporte de morosidad."""
    conn = get_db_connection()
    
    meses_esperados = pd.date_range(end=date.today(), periods=12, freq='MS').strftime('%Y-%m').tolist()
    
    query = f"""
    WITH meses_esperados AS (
        SELECT '{("','").join(meses_esperados)}' as mes
    ),
    pagos_por_local AS (
        SELECT 
            l.numero_local,
            l.inquilino,
            l.planta,
            l.ramo_negocio,
            p.mes_abonado,
            COUNT(p.mes_abonado) as pagos_count
        FROM locales l
        LEFT JOIN pagos p ON l.numero_local = p.numero_local 
            AND p.mes_abonado IN (SELECT * FROM meses_esperados)
        GROUP BY l.numero_local, p.mes_abonado
    )
    SELECT
        numero_local,
        inquilino,
        planta,
        ramo_negocio,
        COUNT(mes_abonado) as meses_pagados,
        {len(meses_esperados)} as meses_esperados,
        ({len(meses_esperados)} - COUNT(mes_abonado)) as meses_morosidad,
        GROUP_CONCAT(mes_abonado, ', ') as meses_pagados_lista
    FROM pagos_por_local
    GROUP BY numero_local
    ORDER BY meses_morosidad DESC
    """
    
    reporte = pd.read_sql(query, conn)
    
    if not reporte.empty:
        reporte['porcentaje_morosidad'] = (reporte['meses_morosidad'] / reporte['meses_esperados']) * 100
        reporte['estado'] = pd.cut(
            reporte['porcentaje_morosidad'],
            bins=[-1, 0, 30, 70, 101],
            labels=['Al día', 'Morosidad leve', 'Morosidad media', 'Morosidad grave']
        )
    
    return reporte

def mostrar_metricas(df):
    """Muestra métricas resumidas."""
    if df.empty:
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_morosidad = df['meses_morosidad'].sum()
        st.metric("Total meses en morosidad", total_morosidad)
    
    with col2:
        locales_morosos = len(df[df['meses_morosidad'] > 0])
        st.metric("Locales morosos", locales_morosos)
    
    with col3:
        porcentaje_promedio = df['porcentaje_morosidad'].mean()
        st.metric("Morosidad promedio", f"{porcentaje_promedio:.1f}%")
    
    fig = px.bar(
        df.groupby('planta')['meses_morosidad'].sum().reset_index(),
        x='planta',
        y='meses_morosidad',
        title='Meses en morosidad por planta'
    )
    st.plotly_chart(fig, use_container_width=True)

# 13. FUNCIÓN PRINCIPAL
def main():
    """Configuración principal de la aplicación."""
    st.set_page_config(
        page_title="Sistema de Pagos Arvelo",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    init_db()
    
    st.title("💰 Sistema de Gestión de Pagos - Arvelo")
    st.markdown("---")
    
    with st.sidebar:
        st.header("Menú Principal")
        menu = st.radio(
            "Seleccione una opción",
            ["Registrar Pago", "Historial de Pagos", "Reporte de Morosidad", "Backup"],
            index=0
        )
        
        st.markdown("---")
        st.info(f"Versión: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        if st.button("🛡️ Crear Backup Ahora"):
            backup_path = hacer_backup()
            if backup_path:
                st.success(f"Backup creado en: {backup_path}")
    
    if menu == "Registrar Pago":
        mostrar_formulario_pago()
    elif menu == "Historial de Pagos":
        mostrar_historial_pagos()
    elif menu == "Reporte de Morosidad":
        st.subheader("⚠️ Reporte Detallado de Morosidad")
        reporte = generar_reporte_morosidad()
        
        if not reporte.empty:
            mostrar_metricas(reporte)
            
            st.subheader("Filtros")
            col1, col2 = st.columns(2)
            with col1:
                filtro_estado = st.multiselect(
                    "Filtrar por estado",
                    options=reporte['estado'].unique(),
                    default=reporte['estado'].unique()
                )
            with col2:
                filtro_planta = st.multiselect(
                    "Filtrar por planta",
                    options=reporte['planta'].unique(),
                    default=reporte['planta'].unique()
                )
            
            reporte_filtrado = reporte[
                (reporte['estado'].isin(filtro_estado)) & 
                (reporte['planta'].isin(filtro_planta))
            ]
            
            st.dataframe(reporte_filtrado, use_container_width=True)
            
            if st.button("📤 Exportar Reporte a Excel"):
                with st.spinner('Generando archivo...'):
                    reporte_filtrado.to_excel("reporte_morosidad.xlsx", index=False)
                    with open("reporte_morosidad.xlsx", "rb") as f:
                        st.download_button(
                            label="⬇️ Descargar reporte",
                            data=f,
                            file_name=f"reporte_morosidad_{date.today()}.xlsx",
                            mime="application/vnd.ms-excel"
                        )
        else:
            st.info("No hay datos suficientes para generar el reporte de morosidad.")
    
    elif menu == "Backup":
        st.subheader("🛡️ Gestión de Backups")
        backup_path = hacer_backup()
        if backup_path:
            st.success(f"Último backup creado en: {backup_path}")
        
        st.info("Los backups automáticos se crean diariamente y al realizar operaciones críticas.")

if __name__ == "__main__":
    main()
