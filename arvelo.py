# 1. IMPORTACIONES
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date
import os
import re
from time import sleep

# 2. CONEXIÓN A LA BASE DE DATOS
@st.cache_resource
def get_db_connection():
    """Establece y retorna una conexión a la base de datos SQLite.
    Esta conexión es manejada por st.cache_resource y NO debe ser cerrada manualmente
    por las funciones que la obtienen, sino solo por Streamlit al finalizar la app.
    """
    try:
        db_path = "pagos_arvelo.db"
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"ERROR CRÍTICO (get_db_connection): No se pudo conectar/crear la base de datos en {db_path}. Error: {e}")
        st.error(f"¡Error crítico! No se pudo iniciar la base de datos. Por favor, contacta a soporte. Detalles: {e}")
        st.stop()

# 3. DATOS INICIALES (sin cambios)
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

# 4. INICIALIZACIÓN DE LA BASE DE DATOS
def init_db():
    """Inicializa la estructura de la base de datos (tablas y datos iniciales si no existen).
    Obtiene la conexión cacheada, realiza las operaciones y NO cierra la conexión.
    """
    try:
        conn = get_db_connection() # Obtiene la conexión cacheada
        cursor = conn.cursor()
        
        # Crear tabla de locales
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locales (
                numero_local TEXT PRIMARY KEY,
                inquilino TEXT NOT NULL,
                planta TEXT,
                ramo_negocio TEXT,
                monto_alquiler REAL,
                contrato TEXT
            )
        ''')
        
        # Crear tabla de pagos
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
        
        # Verificar si la tabla de locales está vacía
        cursor.execute("SELECT COUNT(*) FROM locales")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insertar datos iniciales
            for dato in cargar_datos_iniciales():
                cursor.execute(
                    '''INSERT INTO locales 
                    (numero_local, inquilino, planta, ramo_negocio, monto_alquiler, contrato)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                    (dato[0], dato[1], dato[2], dato[3], dato[4], dato[5])
                )
            conn.commit() # Confirma los cambios de inserción
            
    except sqlite3.Error as e:
        print(f"ERROR CRÍTICO (init_db): Error al inicializar las tablas de la base de datos. Error: {e}")
        # Si la conexión ya existe y hubo un error de DB, intentar un rollback.
        # No se llama a conn.close() aquí, la conexión es cacheada.
        if 'conn' in locals() and conn:
            conn.rollback()
        st.error(f"¡Error crítico! Falló la inicialización de las tablas de la base de datos. Detalles: {e}")
        st.stop()
    except Exception as e:
        print(f"ERROR INESPERADO (init_db): {e}")
        # Idem para otros errores
        if 'conn' in locals() and conn:
            conn.rollback()
        st.error(f"¡Error inesperado! durante la inicialización de la base de datos. Detalles: {e}")
        st.stop()
    # ¡IMPORTANTE!: No hay bloque 'finally' con conn.close(). La conexión es gestionada por @st.cache_resource.

# 5. FUNCIONES DE CONSULTA (obtienen la conexión cacheada y NO la cierran)
# @st.cache_data(ttl=3600) # Reconsiderar el caché para datos que cambian
def obtener_inquilinos():
    """Retorna una lista de todos los inquilinos"""
    try:
        conn = get_db_connection()
        df = pd.read_sql("SELECT DISTINCT inquilino FROM locales ORDER BY inquilino", conn)
        return [""] + df['inquilino'].tolist()
    except Exception as e:
        st.error(f"Error al obtener inquilinos: {e}")
        return [""]
    # No hay finally con conn.close() aquí

def obtener_locales_por_inquilino(inquilino):
    """Retorna los locales asociados a un inquilino específico"""
    if not inquilino:
        return []
    try:
        conn = get_db_connection()
        df = pd.read_sql(
            "SELECT numero_local FROM locales WHERE inquilino = ? ORDER BY numero_local",
            conn, params=(inquilino,)
        )
        return df['numero_local'].tolist()
    except Exception as e:
        st.error(f"Error al obtener locales: {e}")
        return []
    # No hay finally con conn.close() aquí

def obtener_monto_alquiler_local(numero_local):
    """Retorna el monto de alquiler base de un local específico."""
    if not numero_local:
        return 0.0
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT monto_alquiler FROM locales WHERE numero_local = ?", (numero_local,))
        result = cursor.fetchone()
        return result['monto_alquiler'] if result and result['monto_alquiler'] is not None else 0.0
    except Exception as e:
        st.error(f"Error al obtener el monto de alquiler del local: {e}")
        return 0.0
    # No hay finally con conn.close() aquí

# 6. FUNCIONES PARA REGISTRAR PAGOS (obtienen la conexión cacheada y NO la cierran)
def registrar_pago(local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
    """Registra un nuevo pago en la base de datos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO pagos 
            (numero_local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones)
        )
        conn.commit() # Confirma la transacción
        return True
    except Exception as e:
        st.error(f"Error al registrar pago: {e}")
        # Si hubo un error y la conexión existe, intentar rollback.
        if 'conn' in locals() and conn:
            conn.rollback()
        return False
    # No hay finally con conn.close() aquí

# 7. INTERFAZ DE USUARIO - FORMULARIO (sin cambios en la lógica del formulario)
def mostrar_formulario_pago():
    """Muestra el formulario para registrar nuevos pagos"""
    st.subheader("📝 Registrar Nuevo Pago")
    
    with st.form(key='form_pago', clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            selected_inquilino = st.selectbox(
                "Seleccione Inquilino*",
                options=obtener_inquilinos(),
                index=0,
                key="inquilino_selector"
            )
            
            locales_disponibles = [""] + obtener_locales_por_inquilino(selected_inquilino)
            
            if 'selected_local_value' not in st.session_state:
                st.session_state.selected_local_value = ""

            try:
                current_local_index = locales_disponibles.index(st.session_state.selected_local_value)
            except ValueError:
                current_local_index = 0

            selected_local = st.selectbox(
                "Seleccione Local*",
                options=locales_disponibles,
                index=current_local_index,
                key="local_selector"
            )
            st.session_state.selected_local_value = selected_local

        monto_sugerido = obtener_monto_alquiler_local(selected_local)
            
        with col2:
            fecha_pago = st.date_input("Fecha de Pago*", value=date.today())
            mes_abonado = st.text_input("Mes Abonado* (YYYY-MM)", placeholder="2023-01")
            monto = st.number_input("Monto* (USD)", min_value=0.0, value=monto_sugerido, step=1.0)
            estado = st.selectbox("Estado*", ["Pagado", "Parcial", "Pendiente"])
            observaciones = st.text_area("Observaciones")
        
        if st.form_submit_button("💾 Guardar Pago"):
            if not all([selected_inquilino, selected_local, mes_abonado, monto > 0]):
                st.error("Por favor complete todos los campos obligatorios (*)")
            elif not re.match(r"^\d{4}-\d{2}$", mes_abonado):
                st.error("Formato de mes inválido. Use YYYY-MM (ej. 2023-01)")
            else:
                if registrar_pago(
                    selected_local, selected_inquilino,
                    fecha_pago, mes_abonado, monto, estado, observaciones
                ):
                    st.success("✅ Pago registrado exitosamente!")
                    st.cache_data.clear() # Limpia cachés de datos para refrescar tablas
                    sleep(2)
                    st.experimental_rerun()

# 8. INTERFAZ DE USUARIO - HISTORIAL (obtiene la conexión cacheada y NO la cierra)
def mostrar_historial_pagos():
    """Muestra el historial de pagos registrados"""
    try:
        conn = get_db_connection()
        df = pd.read_sql("SELECT * FROM pagos ORDER BY fecha_pago DESC", conn)
        
        if df.empty:
            st.info("No hay pagos registrados aún.")
        else:
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar el historial: {e}")
    # No hay finally con conn.close() aquí

# 9. FUNCIÓN PRINCIPAL (sin cambios)
def main():
    """Función principal de la aplicación"""
    st.set_page_config(
        page_title="Sistema de Pagos Arvelo",
        page_icon="💰",
        layout="wide"
    )
    
    init_db() # Solo inicializa la estructura de la DB si es necesario
    
    st.title("💰 Sistema de Gestión de Pagos")
    
    menu_option = st.sidebar.radio(
        "Menú Principal",
        ["Registrar Pago", "Historial de Pagos"]
    )
    
    if menu_option == "Registrar Pago":
        mostrar_formulario_pago()
    elif menu_option == "Historial de Pagos":
        mostrar_historial_pagos()

# 10. EJECUCIÓN DEL PROGRAMA (sin cambios)
if __name__ == "__main__":
    main()
