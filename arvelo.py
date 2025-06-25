# 1. IMPORTACIONES
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date
import tempfile # Ya no se usa para la DB, pero se mantiene si hay otros usos
import os
import re
from time import sleep

# 2. CONEXIÓN A LA BASE DE DATOS
@st.cache_resource
def get_db_connection():
    """Establece y retorna una conexión a la base de datos SQLite"""
    conn = None # Initialize conn to None
    try:
        db_path = "pagos_arvelo.db"
        # Ensure the directory exists if you plan to put it in a subdirectory
        # For current working directory, this is usually not needed unless it's a specific mount.
        # os.makedirs(os.path.dirname(db_path), exist_ok=True) # If using a subfolder like 'data/pagos_arvelo.db'

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"ERROR CRÍTICO (get_db_connection): No se pudo conectar/crear la base de datos en {db_path}. Error: {e}")
        st.error(f"Error crítico: No se pudo conectar a la base de datos. Por favor, contacte a soporte. Detalles: {e}")
        st.stop() # Detiene la ejecución de la aplicación de Streamlit
    # No need for finally here, the caller (init_db or others) will handle closing if this returns successfully.


# 3. DATOS INICIALES
def cargar_datos_iniciales():
    """Retorna los datos iniciales para poblar la base de datos
    Formato: (numero_local, inquilino, planta, ramo_negocio, monto_alquiler, contrato)
    """
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
    """Inicializa la estructura de la base de datos"""
    conn = None # Ensure conn is initialized to None
    try:
        conn = get_db_connection() # This function handles its own errors and st.stop()
        if conn is None: # Redundant check if get_db_connection already calls st.stop()
            st.stop() # Should not be reached if get_db_connection works as expected

        cursor = conn.cursor()
        
        # Crear tabla de locales (con la nueva columna 'monto_alquiler')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locales (
                numero_local TEXT PRIMARY KEY,
                inquilino TEXT NOT NULL,
                planta TEXT,
                ramo_negocio TEXT,
                monto_alquiler REAL, -- Nueva columna para el monto del alquiler base
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
            # Insertar datos iniciales (ahora incluyendo monto_alquiler)
            for dato in cargar_datos_iniciales():
                cursor.execute(
                    '''INSERT INTO locales 
                    (numero_local, inquilino, planta, ramo_negocio, monto_alquiler, contrato)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                    (dato[0], dato[1], dato[2], dato[3], dato[4], dato[5])
                )
            conn.commit()
            
    except sqlite3.Error as e:
        print(f"ERROR CRÍTICO (init_db): Error al inicializar la base de datos. Error: {e}")
        if conn:
            conn.rollback() # Attempt rollback if connection exists
        st.error(f"Error crítico: Falló la inicialización de la base de datos. Detalles: {e}")
        st.stop() # Stop the app
    except Exception as e: # Catch any other unexpected errors during DB init
        print(f"ERROR INESPERADO (init_db): {e}")
        if conn:
            conn.rollback()
        st.error(f"Error inesperado durante la inicialización. Detalles: {e}")
        st.stop()
    finally:
        if conn: # Only try to close if conn was successfully assigned
            conn.close()
# 5. FUNCIONES DE CONSULTA
@st.cache_data(ttl=3600)
def obtener_inquilinos():
    """Retorna una lista de todos los inquilinos"""
    conn = None
    try:
        conn = get_db_connection()
        df = pd.read_sql("SELECT DISTINCT inquilino FROM locales ORDER BY inquilino", conn)
        return [""] + df['inquilino'].tolist()
    except Exception as e:
        st.error(f"Error al obtener inquilinos: {e}")
        return [""]
    finally:
        if conn:
            conn.close()

def obtener_locales_por_inquilino(inquilino):
    """Retorna los locales asociados a un inquilino específico"""
    if not inquilino:
        return []
    
    conn = None
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
    finally:
        if conn:
            conn.close()

def obtener_monto_alquiler_local(numero_local):
    """Retorna el monto de alquiler base de un local específico."""
    if not numero_local:
        return 0.0 # Valor por defecto si no hay local seleccionado
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT monto_alquiler FROM locales WHERE numero_local = ?", (numero_local,))
        result = cursor.fetchone()
        return result['monto_alquiler'] if result and result['monto_alquiler'] is not None else 0.0
    except Exception as e:
        st.error(f"Error al obtener el monto de alquiler del local: {e}")
        return 0.0
    finally:
        if conn:
            conn.close()

# 6. FUNCIONES PARA REGISTRAR PAGOS
def registrar_pago(local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
    """Registra un nuevo pago en la base de datos"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO pagos 
            (numero_local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones)
        )
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error al registrar pago: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

# 7. INTERFAZ DE USUARIO - FORMULARIO
def mostrar_formulario_pago():
    """Muestra el formulario para registrar nuevos pagos"""
    st.subheader("📝 Registrar Nuevo Pago")
    
    with st.form(key='form_pago', clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Selector de inquilino
            selected_inquilino = st.selectbox(
                "Seleccione Inquilino*",
                options=obtener_inquilinos(),
                index=0,
                key="inquilino_selector" # Añadir key para mantener el estado
            )
            
            # Selector de local basado en el inquilino
            locales_disponibles = [""] + obtener_locales_por_inquilino(selected_inquilino)
            
            # Intentar mantener el local previamente seleccionado si aún es válido
            # Usamos st.session_state para mantener el valor del selectbox
            if 'selected_local_value' not in st.session_state:
                st.session_state.selected_local_value = ""

            try:
                current_local_index = locales_disponibles.index(st.session_state.selected_local_value)
            except ValueError:
                current_local_index = 0 # Reiniciar si el local anterior ya no es válido para el inquilino

            selected_local = st.selectbox(
                "Seleccione Local*",
                options=locales_disponibles,
                index=current_local_index,
                key="local_selector" # Añadir key para mantener el estado
            )
            # Actualizar el valor del local seleccionado en el estado de la sesión
            st.session_state.selected_local_value = selected_local

        # Obtener el monto de alquiler sugerido para el local seleccionado
        monto_sugerido = obtener_monto_alquiler_local(selected_local)
            
        with col2:
            # Campos del formulario
            fecha_pago = st.date_input("Fecha de Pago*", value=date.today())
            mes_abonado = st.text_input("Mes Abonado* (YYYY-MM)", placeholder="2023-01")
            # Usar el monto sugerido como valor inicial
            monto = st.number_input("Monto* (USD)", min_value=0.0, value=monto_sugerido, step=1.0)
            estado = st.selectbox("Estado*", ["Pagado", "Parcial", "Pendiente"])
            observaciones = st.text_area("Observaciones")
        
        # Botón de envío
        if st.form_submit_button("💾 Guardar Pago"):
            # Validaciones
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
                    # Limpiar caches para que los historiales y selects se actualicen
                    st.cache_data.clear()
                    st.cache_resource.clear()
                    sleep(2)
                    st.experimental_rerun() # Recargar la página para refrescar el formulario y los historiales

# 8. INTERFAZ DE USUARIO - HISTORIAL
def mostrar_historial_pagos():
    """Muestra el historial de pagos registrados"""
    st.subheader("📜 Historial de Pagos")
    
    conn = None
    try:
        conn = get_db_connection()
        df = pd.read_sql("SELECT * FROM pagos ORDER BY fecha_pago DESC", conn)
        
        if df.empty:
            st.info("No hay pagos registrados aún.")
        else:
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar el historial: {e}")
    finally:
        if conn:
            conn.close()

# 9. FUNCIÓN PRINCIPAL
def main():
    """Función principal de la aplicación"""
    # Configuración de la página
    st.set_page_config(
        page_title="Sistema de Pagos Arvelo",
        page_icon="💰",
        layout="wide"
    )
    
    # Inicializar base de datos
    init_db()
    
    # Título principal
    st.title("💰 Sistema de Gestión de Pagos")
    
    # Menú de navegación
    menu_option = st.sidebar.radio(
        "Menú Principal",
        ["Registrar Pago", "Historial de Pagos"]
    )
    
    # Mostrar la sección correspondiente
    if menu_option == "Registrar Pago":
        mostrar_formulario_pago()
    elif menu_option == "Historial de Pagos":
        mostrar_historial_pagos()

# 10. EJECUCIÓN DEL PROGRAMA
if __name__ == "__main__":
    main()
