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

# 1. CONFIGURACIÓN MEJORADA DE LA BASE DE DATOS
@st.cache_resource
def get_db_connection():
    """Crea una conexión persistente a SQLite con mejor configuración."""
    temp_dir = tempfile.gettempdir()
    db_path = os.path.join(temp_dir, "pagos_arvelo_final_corregido.db")
    
    # Configuración mejorada para concurrencia
    conn = sqlite3.connect(db_path, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL")  # Mejor rendimiento multihilo
    conn.execute("PRAGMA foreign_keys=ON")   # Habilitar claves foráneas
    conn.row_factory = sqlite3.Row
    
    # Crear tabla de auditoría si no existe
    conn.execute('''
        CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tabla_afectada TEXT NOT NULL,
            operacion TEXT NOT NULL,
            fecha_hora DATETIME NOT NULL,
            usuario TEXT,
            detalles TEXT
        )
    ''')
    
    return conn

# 2. FUNCIÓN DE BACKUP AUTOMÁTICO
def hacer_backup():
    """Realiza backup de la base de datos y retorna la ruta del archivo."""
    conn = get_db_connection()
    conn.commit()  # Asegurar que todos los cambios estén escritos
    
    backup_dir = os.path.join(os.path.expanduser("~"), "backups_pagos_arvelo")
    os.makedirs(backup_dir, exist_ok=True)
    
    db_path = os.path.join(tempfile.gettempdir(), "pagos_arvelo_final_corregido.db")
    backup_path = os.path.join(backup_dir, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
    
    try:
        shutil.copy2(db_path, backup_path)
        registrar_auditoria("backup", "CREATE", f"Backup creado en {backup_path}")
        return backup_path
    except Exception as e:
        st.error(f"Error al crear backup: {str(e)}")
        return None

# 3. SISTEMA DE AUDITORÍA
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

# 4. VALIDACIÓN MEJORADA DE DATOS
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
    inquilinos = obtener_inquilinos()[1:]  # Excluir el primer item vacío
    sugerencias = difflib.get_close_matches(query, inquilinos, n=3, cutoff=0.6)
    return sugerencias if sugerencias else []

# 5. FUNCIONES DE CONSULTA OPTIMIZADAS
@st.cache_data(ttl=3600)
def obtener_inquilinos():
    """Retorna todos los inquilinos únicos con caché."""
    conn = get_db_connection()
    try:
        df = pd.read_sql("SELECT DISTINCT inquilino FROM locales ORDER BY inquilino", conn)
        return [""] + df['inquilino'].tolist()
    except Exception as e:
        st.error(f"Error al obtener inquilinos: {str(e)}")
        return [""]

# 6. REPORTE DE MOROSIDAD COMPLETO
def generar_reporte_morosidad():
    """Genera reporte de morosidad con análisis detallado."""
    conn = get_db_connection()
    
    # Obtener meses esperados (últimos 12 meses)
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
    
    # Calcular porcentaje de morosidad
    if not reporte.empty:
        reporte['porcentaje_morosidad'] = (reporte['meses_morosidad'] / reporte['meses_esperados']) * 100
        reporte['estado'] = pd.cut(
            reporte['porcentaje_morosidad'],
            bins=[-1, 0, 30, 70, 101],
            labels=['Al día', 'Morosidad leve', 'Morosidad media', 'Morosidad grave']
        )
    
    return reporte

# 7. VISUALIZACIONES MEJORADAS
def mostrar_metricas(df):
    """Muestra métricas resumidas con gráficos."""
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
    
    # Gráfico de morosidad por planta
    fig = px.bar(
        df.groupby('planta')['meses_morosidad'].sum().reset_index(),
        x='planta',
        y='meses_morosidad',
        title='Meses en morosidad por planta'
    )
    st.plotly_chart(fig, use_container_width=True)

# 8. FORMULARIO MEJORADO
def mostrar_formulario_pago():
    """Muestra el formulario mejorado para registrar pagos."""
    st.subheader("📝 Registrar Nuevo Pago")
    
    with st.form(key='form_pago', clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Búsqueda inteligente de inquilinos
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
            
            # Selector de local con búsqueda
            locales_disponibles = [""] + (obtener_locales_por_inquilino(selected_inquilino) if selected_inquilino else [])
            selected_local = st.selectbox(
                "Seleccione Local*",
                options=locales_disponibles,
                index=0
            )
            
        with col2:
            fecha_pago = st.date_input("Fecha de Pago*", value=date.today())
            
            mes_abonado = st.text_input(
                "Mes Abonado* (YYYY-MM)",
                placeholder="Ej: 2023-01",
                help="Formato requerido: YYYY-MM (ej. 2023-01 para Enero 2023)"
            )
            
            monto = st.number_input(
                "Monto* (USD)",
                min_value=0.0,
                value=0.0,
                step=1.0,
                format="%.2f"
            )
            
            estado = st.selectbox(
                "Estado*",
                options=["Pagado", "Parcial", "Pendiente"]
            )
            
            observaciones = st.text_area("Observaciones (opcional)")
        
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

# 9. FUNCIÓN PRINCIPAL ACTUALIZADA
def main():
    """Configuración principal mejorada de la aplicación."""
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
            ["Registrar Pago", "Historial de Pagos", "Reporte de Morosidad", "Backup"],
            index=0
        )
        
        st.markdown("---")
        st.info(f"Versión: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Backup manual desde el sidebar
        if st.button("🛡️ Crear Backup Ahora"):
            backup_path = hacer_backup()
            if backup_path:
                st.success(f"Backup creado en: {backup_path}")
    
    # Mostrar la sección correspondiente
    if menu == "Registrar Pago":
        mostrar_formulario_pago()
    elif menu == "Historial de Pagos":
        mostrar_historial_pagos()
    elif menu == "Reporte de Morosidad":
        st.subheader("⚠️ Reporte Detallado de Morosidad")
        reporte = generar_reporte_morosidad()
        
        if not reporte.empty:
            mostrar_metricas(reporte)
            
            # Filtros para el reporte
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
            
            # Aplicar filtros
            reporte_filtrado = reporte[
                (reporte['estado'].isin(filtro_estado)) & 
                (reporte['planta'].isin(filtro_planta))
            ]
            
            st.dataframe(reporte_filtrado, use_container_width=True)
            
            # Exportar a Excel
            if st.button("📤 Exportar Reporte a Excel"):
                with st.spinner('Generando archivo...'):
                    excel_file = reporte_filtrado.to_excel("reporte_morosidad.xlsx", index=False)
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
