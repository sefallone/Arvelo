import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date
import tempfile
import os
import re
from time import sleep

# 1. CONFIGURACIÓN DE LA BASE DE DATOS
@st.cache_resource
def get_db_connection():
    """Crea y retorna una conexión persistente a la base de datos SQLite."""
    temp_dir = tempfile.gettempdir()
    db_path = os.path.join(temp_dir, "pagos_arvelo_final_corregido.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# 2. DATOS INICIALES VERIFICADOS
def cargar_datos_iniciales():
    """Retorna datos iniciales con todos los locales correctamente asociados."""
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

# 3. INICIALIZACIÓN DE LA BASE DE DATOS CON VERIFICACIÓN
def init_db():
    """Inicializa la estructura de la base de datos con verificación de datos."""
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
                    try:
                        cursor.execute(
                            '''INSERT OR IGNORE INTO locales 
                            (numero_local, inquilino, planta, ramo_negocio, contrato)
                            VALUES (?, ?, ?, ?, ?)''',
                            (dato[0], dato[1], dato[2], dato[3], dato[5])
                        )
                    except Exception as e:
                        st.error(f"Error al insertar local {dato[0]}: {str(e)}")
                conn.commit()
                
                # Verificación de datos insertados
                st.success("Datos iniciales cargados. Verificando...")
                locales_count = cursor.execute("SELECT COUNT(*) FROM locales").fetchone()[0]
                st.write(f"Total de locales cargados: {locales_count}")
                
                # Mostrar muestra de datos para verificación
                sample = pd.read_sql("SELECT * FROM locales LIMIT 5", conn)
                st.write("Muestra de datos:", sample)
        
    except Exception as e:
        st.error(f"Error crítico al inicializar la base de datos: {str(e)}")
        st.stop()

# 4. FUNCIONES DE CONSULTA CON VERIFICACIÓN
def obtener_inquilinos():
    """Retorna todos los inquilinos únicos con verificación."""
    conn = get_db_connection()
    try:
        df = pd.read_sql(
            "SELECT DISTINCT inquilino FROM locales ORDER BY inquilino", 
            conn
        )
        # Verificación de datos obtenidos
        if df.empty:
            st.warning("No se encontraron inquilinos en la base de datos")
            return [""]
        
        return [""] + df['inquilino'].tolist()
    except Exception as e:
        st.error(f"Error al obtener inquilinos: {str(e)}")
        return [""]

def obtener_locales_por_inquilino(inquilino):
    """Retorna locales del inquilino especificado con verificación."""
    if not inquilino or not inquilino.strip():
        return []
        
    conn = get_db_connection()
    try:
        # Consulta exacta primero
        exact_df = pd.read_sql(
            "SELECT numero_local FROM locales WHERE inquilino = ? ORDER BY numero_local",
            conn, params=(inquilino,)
        )
        
        if not exact_df.empty:
            return exact_df['numero_local'].tolist()
        
        # Si no hay resultados, buscar por similitud
        similar_df = pd.read_sql(
            "SELECT numero_local FROM locales WHERE inquilino LIKE ? ORDER BY numero_local",
            conn, params=(f"%{inquilino}%",)
        )
        
        if not similar_df.empty:
            st.warning(f"Usando resultados similares para: {inquilino}")
            return similar_df['numero_local'].tolist()
            
        return []
    except Exception as e:
        st.error(f"Error al obtener locales: {str(e)}")
        return []

# 5. FORMULARIO DE PAGOS CON MECANISMOS DE DEBUG
def mostrar_formulario_pago():
    """Muestra el formulario para registrar pagos con verificación completa."""
    st.subheader("📝 Registrar Nuevo Pago")
    
    # Obtener lista de inquilinos con verificación
    inquilinos = obtener_inquilinos()
    
    # Debug: Mostrar inquilinos disponibles
    st.write(f"DEBUG: Inquilinos disponibles ({len(inquilinos)-1}):", inquilinos[1:])
    
    with st.form(key='form_pago', clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Selector de inquilino
            selected_inquilino = st.selectbox(
                "Seleccione Inquilino*",
                options=inquilinos,
                index=0,
                key='select_inquilino'
            )
            
            # Debug: Mostrar inquilino seleccionado
            st.write(f"DEBUG: Inquilino seleccionado: '{selected_inquilino}'")
            
            # Obtener locales para el inquilino seleccionado
            locales_disponibles = [""]
            if selected_inquilino:
                locales = obtener_locales_por_inquilino(selected_inquilino)
                
                # Debug: Mostrar resultados de la consulta
                st.write(f"DEBUG: Locales encontrados ({len(locales)}):", locales)
                
                if not locales:
                    st.warning("No se encontraron locales para este inquilino")
                    # Mostrar posibles coincidencias en la base de datos
                    conn = get_db_connection()
                    similar = pd.read_sql(
                        "SELECT DISTINCT inquilino FROM locales WHERE inquilino LIKE ? LIMIT 5",
                        conn, params=(f"%{selected_inquilino}%",)
                    )
                    if not similar.empty:
                        st.info("Posibles coincidencias similares:")
                        st.write(similar)
                else:
                    locales_disponibles += locales
            
            # Selector de local
            selected_local = st.selectbox(
                "Seleccione Local*",
                options=locales_disponibles,
                index=0,
                key='select_local'
            )
            
            # Mostrar información del local seleccionado
            if selected_local:
                info_local = obtener_info_local(selected_local)
                if info_local:
                    st.info(f"""
                        **Planta:** {info_local['planta']}  
                        **Ramo:** {info_local['ramo_negocio']}  
                        **Contrato:** {info_local['contrato']}
                    """)
                else:
                    st.warning("No se encontró información detallada para este local")
        
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
            # Validaciones
            if not selected_inquilino:
                st.error("Por favor, seleccione un inquilino")
            elif not selected_local:
                st.error("Por favor, seleccione un local")
            elif not mes_abonado or not re.match(r"^\d{4}-\d{2}$", mes_abonado):
                st.error("El formato del 'Mes Abonado' debe ser YYYY-MM (ej. 2023-01)")
            elif monto <= 0:
                st.error("El monto debe ser mayor que cero")
            else:
                # Confirmación antes de guardar
                with st.expander("📋 Ver resumen del pago", expanded=True):
                    st.write(f"**Inquilino:** {selected_inquilino}")
                    st.write(f"**Local:** {selected_local}")
                    st.write(f"**Fecha Pago:** {fecha_pago.strftime('%Y-%m-%d')}")
                    st.write(f"**Mes Abonado:** {mes_abonado}")
                    st.write(f"**Monto:** ${monto:.2f}")
                    st.write(f"**Estado:** {estado}")
                    if observaciones:
                        st.write(f"**Observaciones:** {observaciones}")
                
                if st.checkbox("✅ Confirmo que los datos son correctos"):
                    with st.spinner('Guardando pago...'):
                        if registrar_pago(
                            selected_local, selected_inquilino,
                            fecha_pago, mes_abonado, monto, estado, observaciones
                        ):
                            st.success("✅ Pago registrado exitosamente!")
                            sleep(2)
                            st.experimental_rerun()

# 6. FUNCIÓN PARA REGISTRAR PAGOS
def registrar_pago(local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
    """Registra un nuevo pago con manejo de errores mejorado."""
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
        st.cache_data.clear()  # Limpiar cachés para actualizar vistas
        return True
    except Exception as e:
        st.error(f"Error al registrar el pago: {str(e)}")
        conn.rollback()
        return False

# 7. HISTORIAL DE PAGOS CON FILTROS
def mostrar_historial_pagos():
    """Muestra el historial de pagos con opciones de filtrado."""
    st.subheader("📜 Historial de Pagos")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        filtro_mes = st.text_input("Filtrar por mes (YYYY-MM)", "")
    with col2:
        filtro_inquilino = st.selectbox("Filtrar por inquilino", [""] + obtener_inquilinos()[1:])
    
    # Obtener datos filtrados
    pagos_df = obtener_pagos(
        filtro_mes if filtro_mes and re.match(r"^\d{4}-\d{2}$", filtro_mes) else None,
        filtro_inquilino if filtro_inquilino else None
    )
    
    if pagos_df.empty:
        st.info("No hay pagos registrados con los filtros seleccionados.")
    else:
        # Mostrar estadísticas
        total = pagos_df['monto'].sum()
        st.metric("Total filtrado", f"${total:,.2f}")
        
        # Mostrar tabla
        st.dataframe(pagos_df, use_container_width=True)
        
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

# 8. FUNCIÓN PRINCIPAL
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
    
    # Mostrar la sección correspondiente
    if menu == "Registrar Pago":
        mostrar_formulario_pago()
    elif menu == "Historial de Pagos":
        mostrar_historial_pagos()
    elif menu == "Reporte de Morosidad":
        st.subheader("⚠️ Reporte de Morosidad")
        st.info("Esta funcionalidad está en desarrollo. ¡Pronto estará disponible!")

if __name__ == "__main__":
    main()
