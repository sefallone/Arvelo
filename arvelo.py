# 1. IMPORTACIONES
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date
import os
import re
from time import sleep

# 2. CONEXIÓN A LA BASE DE DATOS (mejorado con manejo de contexto)
@st.cache_resource
def get_db_connection():
    """Establece y retorna una conexión a la base de datos SQLite."""
    try:
        db_path = "pagos_arvelo.db"
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        # Habilitar foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.Error as e:
        st.error(f"¡Error crítico! No se pudo conectar/crear la base de datos. Detalles: {e}")
        st.stop()

# 3. FUNCIONES DE VALIDACIÓN (nuevas)
def validar_mes_abonado(mes):
    """Valida que el formato sea YYYY-MM y que sea un mes válido"""
    if not re.match(r"^\d{4}-(0[1-9]|1[0-2])$", mes):
        return False
    try:
        datetime.strptime(mes, "%Y-%m")
        return True
    except ValueError:
        return False

def validar_monto(monto):
    """Valida que el monto sea positivo y tenga formato correcto"""
    try:
        return float(monto) > 0
    except (ValueError, TypeError):
        return False

# 4. DATOS INICIALES (sin cambios)
def cargar_datos_iniciales():
    """Retorna los datos iniciales para poblar la base de datos"""
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

# 5. INICIALIZACIÓN DE LA BASE DE DATOS (mejorado)
def init_db():
    """Inicializa la estructura de la base de datos con mejor manejo de errores"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Crear tabla de locales con constraints mejorados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locales (
                numero_local TEXT PRIMARY KEY,
                inquilino TEXT NOT NULL,
                planta TEXT,
                ramo_negocio TEXT,
                monto_alquiler REAL CHECK(monto_alquiler >= 0),
                contrato TEXT
            )
        ''')
        
        # Crear tabla de pagos con constraints mejorados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_local TEXT NOT NULL,
                inquilino TEXT NOT NULL,
                fecha_pago DATE NOT NULL,
                mes_abonado TEXT NOT NULL CHECK(mes_abonado LIKE '____-__'),
                monto REAL NOT NULL CHECK(monto > 0),
                estado TEXT NOT NULL CHECK(estado IN ('Pagado', 'Parcial', 'Pendiente')),
                observaciones TEXT,
                FOREIGN KEY(numero_local) REFERENCES locales(numero_local) ON DELETE CASCADE
            )
        ''')
        
        # Crear índice para mejorar búsquedas
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_pagos_inquilino ON pagos(inquilino)
        ''')
        
        cursor.execute("SELECT COUNT(*) FROM locales")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                '''INSERT INTO locales 
                (numero_local, inquilino, planta, ramo_negocio, monto_alquiler, contrato)
                VALUES (?, ?, ?, ?, ?, ?)''',
                cargar_datos_iniciales()
            )
            conn.commit()
            
    except sqlite3.Error as e:
        st.error(f"¡Error crítico! Falló la inicialización de la base de datos. Detalles: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
        st.stop()
    except Exception as e:
        st.error(f"¡Error inesperado! durante la inicialización. Detalles: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
        st.stop()

# 6. FUNCIONES DE CONSULTA (mejoradas)
@st.cache_data(ttl=600)
def obtener_inquilinos():
    """Retorna una lista de todos los inquilinos con caché de 10 minutos"""
    try:
        conn = get_db_connection()
        df = pd.read_sql("SELECT DISTINCT inquilino FROM locales ORDER BY inquilino", conn)
        return [""] + df['inquilino'].tolist()
    except Exception as e:
        st.error(f"Error al obtener inquilinos: {e}")
        return [""]

@st.cache_data(ttl=600)
def obtener_locales_por_inquilino(inquilino):
    """Retorna los locales asociados a un inquilino con caché"""
    if not inquilino:
        return []
    try:
        conn = get_db_connection()
        df = pd.read_sql(
            "SELECT numero_local, monto_alquiler FROM locales WHERE inquilino = ? ORDER BY numero_local",
            conn, params=(inquilino,)
        )
        return df.to_dict('records')
    except Exception as e:
        st.error(f"Error al obtener locales: {e}")
        return []

def obtener_monto_alquiler_local(numero_local):
    """Retorna el monto de alquiler base de un local específico."""
    if not numero_local:
        return 0.0
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT monto_alquiler FROM locales WHERE numero_local = ?", (numero_local,))
        result = cursor.fetchone()
        return result['monto_alquiler'] if result else 0.0
    except Exception as e:
        st.error(f"Error al obtener el monto de alquiler: {e}")
        return 0.0

# 7. FUNCIONES PARA REGISTRAR PAGOS (mejoradas)
def registrar_pago(local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
    """Registra un nuevo pago con validaciones mejoradas"""
    try:
        # Validaciones mejoradas
        if not all([local, inquilino, mes_abonado, fecha_pago]):
            raise ValueError("Todos los campos obligatorios deben estar completos")
            
        if not validar_mes_abonado(mes_abonado):
            raise ValueError("Formato de mes inválido. Use YYYY-MM (ej. 2023-01)")
            
        if not validar_monto(monto):
            raise ValueError("El monto debe ser un número positivo")
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar que el local existe
        cursor.execute("SELECT 1 FROM locales WHERE numero_local = ?", (local,))
        if not cursor.fetchone():
            raise ValueError(f"El local {local} no existe en la base de datos")
            
        # Insertar el pago
        cursor.execute(
            '''INSERT INTO pagos 
            (numero_local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones)
        )
        conn.commit()
        return True
        
    except ValueError as ve:
        st.error(str(ve))
        return False
    except sqlite3.Error as se:
        st.error(f"Error de base de datos: {se}")
        if 'conn' in locals() and conn:
            conn.rollback()
        return False
    except Exception as e:
        st.error(f"Error inesperado: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
        return False

# 8. INTERFAZ DE USUARIO - FORMULARIO (mejorado)
def mostrar_formulario_pago():
    """Muestra el formulario mejorado para registrar nuevos pagos"""
    st.subheader("📝 Registrar Nuevo Pago")
    
    with st.form(key='form_pago', clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Selectbox con búsqueda mejorada
            inquilinos = obtener_inquilinos()
            selected_inquilino = st.selectbox(
                "Seleccione Inquilino*",
                options=inquilinos,
                index=0,
                key="inquilino_selector",
                help="Seleccione o escriba para buscar un inquilino"
            )
            
            # Mostrar locales con información adicional
            locales_info = obtener_locales_por_inquilino(selected_inquilino)
            locales_opciones = {f"{loc['numero_local']} (${loc['monto_alquiler']})": loc['numero_local'] for loc in locales_info}
            
            selected_local = st.selectbox(
                "Seleccione Local*",
                options=[""] + list(locales_opciones.keys()),
                index=0,
                key="local_selector",
                help="Seleccione un local para ver el monto sugerido"
            )
            
            # Obtener el número de local real (sin el monto en el texto)
            local_real = locales_opciones.get(selected_local, "")
            
        with col2:
            fecha_pago = st.date_input("Fecha de Pago*", value=date.today())
            mes_abonado = st.text_input("Mes Abonado* (YYYY-MM)", placeholder="2023-01", 
                                       help="Formato: AAAA-MM (ej. 2023-05)")
            
            # Mostrar monto sugerido y permitir edición
            monto_sugerido = obtener_monto_alquiler_local(local_real)
            monto = st.number_input(
                "Monto* (USD)", 
                min_value=0.0, 
                value=float(monto_sugerido) if monto_sugerido else 0.0, 
                step=1.0,
                format="%.2f"
            )
            
            estado = st.selectbox("Estado*", ["Pagado", "Parcial", "Pendiente"])
            observaciones = st.text_area("Observaciones", placeholder="Detalles adicionales del pago")
        
        # Botón de submit con confirmación
        if st.form_submit_button("💾 Guardar Pago"):
            if not all([selected_inquilino, local_real, mes_abonado, monto > 0]):
                st.error("❌ Por favor complete todos los campos obligatorios (*)")
            elif not validar_mes_abonado(mes_abonado):
                st.error("❌ Formato de mes inválido. Use YYYY-MM (ej. 2023-01)")
            else:
                with st.spinner("Registrando pago..."):
                    if registrar_pago(
                        local_real, selected_inquilino,
                        fecha_pago, mes_abonado, monto, estado, observaciones
                    ):
                        st.success("✅ Pago registrado exitosamente!")
                        st.cache_data.clear()
                        sleep(1.5)
                        st.experimental_rerun()

# 9. INTERFAZ DE USUARIO - HISTORIAL (mejorado con filtros)
def mostrar_historial_pagos():
    """Muestra el historial de pagos con filtros avanzados"""
    st.subheader("📋 Historial de Pagos")
    
    # Filtros avanzados
    with st.expander("🔍 Filtros Avanzados", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtro_inquilino = st.selectbox(
                "Por Inquilino",
                options=["Todos"] + obtener_inquilinos()[1:]
            )
            
        with col2:
            filtro_mes = st.text_input(
                "Por Mes (YYYY-MM)",
                placeholder="2023-01",
                help="Dejar vacío para todos los meses"
            )
            
        with col3:
            filtro_estado = st.selectbox(
                "Por Estado",
                options=["Todos", "Pagado", "Parcial", "Pendiente"]
            )
    
    # Construir consulta SQL dinámica
    query = """
        SELECT 
            p.id,
            p.numero_local,
            p.inquilino,
            p.fecha_pago,
            p.mes_abonado,
            p.monto,
            p.estado,
            p.observaciones,
            l.planta,
            l.ramo_negocio
        FROM pagos p
        LEFT JOIN locales l ON p.numero_local = l.numero_local
        WHERE 1=1
    """
    params = []
    
    if filtro_inquilino != "Todos":
        query += " AND p.inquilino = ?"
        params.append(filtro_inquilino)
        
    if filtro_mes and validar_mes_abonado(filtro_mes):
        query += " AND p.mes_abonado = ?"
        params.append(filtro_mes)
        
    if filtro_estado != "Todos":
        query += " AND p.estado = ?"
        params.append(filtro_estado)
        
    query += " ORDER BY p.fecha_pago DESC"
    
    try:
        conn = get_db_connection()
        df = pd.read_sql(query, conn, params=params if params else None)
        
        if df.empty:
            st.info("No hay pagos registrados que coincidan con los filtros.")
        else:
            # Formatear columnas
            df['fecha_pago'] = pd.to_datetime(df['fecha_pago']).dt.date
            df['monto'] = df['monto'].apply(lambda x: f"${x:,.2f}")
            
            # Mostrar dataframe con estilo
            st.dataframe(
                df,
                use_container_width=True,
                column_config={
                    "monto": st.column_config.NumberColumn(format="$%.2f")
                },
                hide_index=True
            )
            
            # Resumen estadístico
            st.subheader("📊 Resumen")
            total_pagos = pd.to_numeric(df['monto'].str.replace('$', '').str.replace(',', '')).sum()
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Pagos", len(df))
                
            with col2:
                st.metric("Total Recaudado", f"${total_pagos:,.2f}")
                
            with col3:
                st.metric("Promedio por Pago", f"${total_pagos/len(df):,.2f}" if len(df) > 0 else "$0.00")
                
    except Exception as e:
        st.error(f"Error al cargar el historial: {e}")

# 10. FUNCIÓN PRINCIPAL (mejorada)
def main():
    """Función principal con layout mejorado"""
    # Configuración de página mejorada
    st.set_page_config(
        page_title="Sistema de Pagos Arvelo",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inicialización de la base de datos
    init_db()
    
    # Sidebar con más opciones
    with st.sidebar:
        st.title("💰 Gestión de Pagos")
        menu_option = st.radio(
            "Menú Principal",
            ["Registrar Pago", "Historial de Pagos"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("**Información:**")
        st.markdown("- ℹ️ Complete todos los campos obligatorios (*)")
        st.markdown("- 📅 Use formato YYYY-MM para los meses")
        
        if st.button("🔄 Limpiar caché"):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("¡Caché limpiado!")
            st.experimental_rerun()
    
    # Contenido principal
    st.title("Sistema de Gestión de Pagos Comerciales")
    
    if menu_option == "Registrar Pago":
        mostrar_formulario_pago()
    elif menu_option == "Historial de Pagos":
        mostrar_historial_pagos()

if __name__ == "__main__":
    main()
