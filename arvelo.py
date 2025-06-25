import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date
import tempfile
import os
import shutil
import re # Importar para validación de formato

# 1. CONFIGURACIÓN DE LA BASE DE DATOS
@st.cache_resource
def get_db_connection():
    """Crea y retorna una conexión a la base de datos SQLite.
    Usa @st.cache_resource para que la conexión se reutilice en las recargas.
    La base de datos se guarda en un directorio temporal, lo que es útil para
    pruebas locales pero podría no ser persistente en algunos despliegues de Streamlit.
    """
    temp_dir = tempfile.gettempdir()
    db_path = os.path.join(temp_dir, "pagos_arvelo_final_v3.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row # Permite acceder a las columnas por nombre
    return conn

# 2. DATOS INICIALES (COMPLETOS Y VERIFICADOS)
def cargar_datos_iniciales():
    """Retorna datos iniciales con todos los locales correctamente asociados."""
    # Formato de cada tupla: (numero_local, inquilino, planta, ramo_negocio, monto_alquiler, nombre_contrato)
    # Nota: el monto_alquiler no se guarda en la tabla 'locales', es solo una referencia inicial.
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
        ('LOCAL 2 -3', 'DESOCUPADO', 'MEZZANINA 2', '', 23.33, 'FEDERICK JACOB OVALLES'), # Posible duplicado o local similar
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
    """Inicializa la estructura de la base de datos (tablas y datos iniciales)."""
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
        
        # Insertar datos iniciales si la tabla de locales está vacía
        if cursor.execute("SELECT COUNT(*) FROM locales").fetchone()[0] == 0:
            st.info("Cargando datos iniciales de locales...")
            datos = cargar_datos_iniciales()
            for dato in datos:
                try:
                    # Solo insertamos los campos relevantes para la tabla 'locales'
                    cursor.execute(
                        '''INSERT OR IGNORE INTO locales 
                        (numero_local, inquilino, planta, ramo_negocio, contrato)
                        VALUES (?, ?, ?, ?, ?)''',
                        (dato[0], dato[1], dato[2], dato[3], dato[5]) # dato[5] es el nombre del contrato
                    )
                except sqlite3.IntegrityError as e:
                    st.warning(f"Error de integridad al insertar local {dato[0]}: {str(e)}")
                except Exception as e:
                    st.error(f"Error inesperado al insertar local {dato[0]}: {str(e)}")
            conn.commit()
            st.success("Datos iniciales de locales cargados exitosamente.")
        else:
            # Added for debugging: Show how many locals are in the DB if it's not empty
            count = cursor.execute("SELECT COUNT(*) FROM locales").fetchone()[0]
            st.info(f"Base de datos de locales ya inicializada con {count} registros.")
        
    except Exception as e:
        st.error(f"Error al inicializar la base de datos: {str(e)}")
    finally:
        # La conexión no se cierra aquí si usamos st.cache_resource, Streamlit la gestiona
        pass

# 4. FUNCIONES DE CONSULTA
def obtener_inquilinos():
    """Retorna todos los inquilinos únicos."""
    conn = get_db_connection()
    df = pd.read_sql(
        "SELECT DISTINCT inquilino FROM locales ORDER BY inquilino", 
        conn
    )
    inquilinos_list = df['inquilino'].tolist()
    # --- NUEVO MENSAJE DE DEPURACIÓN ---
    st.info(f"DEBUG: Inquilinos obtenidos de la DB por obtener_inquilinos(): {inquilinos_list}")
    # --- FIN NUEVO MENSAJE DE DEPURACIÓN ---
    return inquilinos_list

def obtener_locales_por_inquilino(inquilino):
    """Retorna solo los locales del inquilino especificado."""
    if not inquilino:
        return []
        
    conn = get_db_connection()
    df = pd.read_sql(
        "SELECT numero_local FROM locales WHERE inquilino = ? ORDER BY numero_local",
        conn, params=(inquilino,)
    )
    return df['numero_local'].tolist()

def obtener_info_local(numero_local):
    """Retorna información de un local específico."""
    if not numero_local:
        return None
        
    conn = get_db_connection()
    df = pd.read_sql(
        "SELECT * FROM locales WHERE numero_local = ?",
        conn, params=(numero_local,)
    )
    return df.iloc[0] if not df.empty else None

def obtener_pagos():
    """Retorna todos los pagos registrados."""
    conn = get_db_connection()
    df = pd.read_sql(
        "SELECT * FROM pagos ORDER BY fecha_pago DESC, id DESC",
        conn
    )
    return df

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
        return True
    except Exception as e:
        st.error(f"Error al registrar el pago: {str(e)}")
        return False

# 6. FORMULARIO DE PAGOS
def mostrar_formulario_pago():
    """Muestra el formulario para registrar pagos."""
    st.subheader("📝 Registrar Nuevo Pago")
    
    # Obtener lista de inquilinos
    inquilinos = [""] + obtener_inquilinos() # Añadir opción vacía al inicio
    
    # Crear el formulario
    form = st.form(key='form_pago')
    with form:
        col1, col2 = st.columns(2)
        
        with col1:
            # Selector de inquilino
            # Se ha eliminado 'index=0' para permitir que Streamlit mantenga la selección del usuario.
            inquilino_seleccionado = st.selectbox(
                "Seleccione Inquilino*",
                options=inquilinos,
                key="select_inquilino"
            )
            
            # --- INICIO DE DEPURACIÓN EN FORMULARIO ---
            st.info(f"DEBUG: Inquilino seleccionado: '{inquilino_seleccionado}'")
            # --- FIN DE DEPURACIÓN EN FORMULARIO ---

            # Obtener locales del inquilino seleccionado
            locales_del_inquilino = []
            if inquilino_seleccionado:
                locales_del_inquilino = obtener_locales_por_inquilino(inquilino_seleccionado)
            
            # --- INICIO DE DEPURACIÓN EN FORMULARIO ---
            st.info(f"DEBUG: Locales encontrados para '{inquilino_seleccionado}': {locales_del_inquilino}")
            # --- FIN DE DEPURACIÓN EN FORMULARIO ---

            # Selector de local
            # Se ha eliminado 'index=0' para permitir que Streamlit mantenga la selección del usuario.
            local_seleccionado = st.selectbox(
                "Seleccione Local*",
                options=[""] + locales_del_inquilino, # Añadir opción vacía
                key="select_local"
            )
            
            # Mostrar información del local seleccionado
            if local_seleccionado:
                info_local = obtener_info_local(local_seleccionado)
                if info_local:
                    st.markdown(f"""
                        **Planta:** {info_local['planta']}  
                        **Ramo:** {info_local['ramo_negocio']}  
                        **Contrato:** {info_local['contrato']}
                    """)
        
        with col2:
            fecha_pago = st.date_input(
                "Fecha de Pago*",
                value=date.today()
            )
            
            mes_abonado = st.text_input(
                "Mes Abonado* (YYYY-MM)",
                placeholder="Ej: 2023-01",
                help="Formato requerido: YYYY-MM (ej. 2023-01 para Enero 2023)"
            )
            
            monto = st.number_input(
                "Monto*",
                min_value=0.0,
                value=0.0, # Valor inicial a 0.0 para que el usuario lo establezca
                step=1.0,
                format="%.2f"
            )
            
            estado = st.selectbox(
                "Estado*",
                options=["Pagado", "Parcial", "Pendiente"] # Añadir 'Pendiente' si es un estado posible
            )
            
            observaciones = st.text_area("Observaciones (opcional)")
        
        # El botón de submit está CORRECTAMENTE implementado aquí dentro del 'with form:'
        submitted = form.form_submit_button("💾 Guardar Pago")
        
        if submitted:
            # Validaciones antes de registrar
            if not inquilino_seleccionado or inquilino_seleccionado == "":
                st.error("Por favor, seleccione un inquilino.")
            elif not local_seleccionado or local_seleccionado == "":
                st.error("Por favor, seleccione un local.")
            elif not mes_abonado:
                st.error("Por favor, introduzca el mes abonado.")
            elif not re.match(r"^\d{4}-\d{2}$", mes_abonado):
                st.error("El formato del 'Mes Abonado' debe ser YYYY-MM (ej. 2023-01).")
            elif monto <= 0:
                st.error("El monto debe ser mayor que cero.")
            else:
                if registrar_pago(
                    local_seleccionado, inquilino_seleccionado,
                    fecha_pago, mes_abonado, monto, estado, observaciones
                ):
                    st.success("✅ Pago registrado exitosamente!")
                    st.balloons()
                    # Opcional: limpiar el formulario reiniciando la aplicación o los valores de los inputs
                    # st.experimental_rerun() # Esto recarga toda la página de Streamlit
                else:
                    st.error("Hubo un error al guardar el pago. Por favor, revise el log para más detalles.")


# 7. FUNCIÓN PARA MOSTRAR EL HISTORIAL DE PAGOS
def mostrar_historial_pagos():
    """Muestra una tabla con todos los pagos registrados."""
    st.subheader("📜 Historial de Pagos Registrados")
    pagos_df = obtener_pagos()
    
    if pagos_df.empty:
        st.info("No hay pagos registrados aún.")
    else:
        # Opcional: ordenar o filtrar el DataFrame antes de mostrarlo
        st.dataframe(pagos_df, use_container_width=True)

# 8. FUNCIÓN PRINCIPAL
def main():
    """Configuración principal de la aplicación."""
    # Mover st.set_page_config al inicio de la función main
    st.set_page_config(
        page_title="Sistema de Pagos Arvelo",
        page_icon="💰",
        layout="wide"
    )
    
    # --- MENSAJE DE DEPURACIÓN INICIAL (después de set_page_config) ---
    st.info("DEBUG: Aplicación Streamlit iniciada o recargada.")
    # --- FIN MENSAJE DE DEPURACIÓN INICIAL ---

    # Inicializar base de datos
    init_db() # No necesita try/except aquí ya que init_db maneja sus propios errores con st.error
    
    st.title("💰 Sistema de Gestión de Pagos - Arvelo")
    st.markdown("---")
    
    # Menú de navegación
    menu = st.sidebar.selectbox(
        "Menú Principal",
        ["Registrar Pago", "Historial de Pagos", "Reporte de Morosidad"]
    )
    
    if menu == "Registrar Pago":
        mostrar_formulario_pago()
    elif menu == "Historial de Pagos":
        mostrar_historial_pagos()
    elif menu == "Reporte de Morosidad":
        st.subheader("⚠️ Reporte de Morosidad")
        st.info("Esta funcionalidad está en desarrollo. ¡Pronto estará disponible!")

if __name__ == "__main__":
    main()
