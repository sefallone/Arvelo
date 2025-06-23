import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import tempfile
import os

# --- CONFIGURACIÓN DE LA BASE DE DATOS --- #
def get_db_connection():
    """Crea una conexión a la base de datos SQLite"""
    temp_dir = tempfile.gettempdir()
    db_path = os.path.join(temp_dir, "pagos_arvelo.db")
    return sqlite3.connect(db_path, check_same_thread=False)

# --- DATOS INICIALES (Del Excel proporcionado) --- #
def cargar_datos_iniciales():
    """Devuelve los datos iniciales basados en el archivo Excel"""
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

# --- INICIALIZACIÓN DE LA BASE DE DATOS --- #
def init_db():
    """Inicializa la base de datos con estructura y datos iniciales"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_local TEXT NOT NULL,
                inquilino TEXT NOT NULL,
                planta TEXT,
                ramo_negocio TEXT,
                canon REAL NOT NULL,
                contrato TEXT,
                fecha_pago DATE,
                mes_abonado TEXT,
                estado TEXT DEFAULT 'Pendiente',
                observaciones TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute("SELECT COUNT(*) FROM pagos")
        if cursor.fetchone()[0] == 0:
            cursor.executemany('''
                INSERT INTO pagos (
                    numero_local, inquilino, planta, ramo_negocio, canon, contrato
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', cargar_datos_iniciales())
        
        conn.commit()
    except Exception as e:
        st.error(f"Error al inicializar la base de datos: {str(e)}")
    finally:
        conn.close()

# --- FUNCIONES DE CONSULTA --- #
def obtener_inquilinos():
    """Obtiene lista de inquilinos únicos"""
    conn = get_db_connection()
    df = pd.read_sql("SELECT DISTINCT inquilino FROM pagos ORDER BY inquilino", conn)
    conn.close()
    return df['inquilino'].tolist()

def obtener_locales_por_inquilino(inquilino):
    """Obtiene locales asociados a un inquilino específico"""
    conn = get_db_connection()
    df = pd.read_sql(
        "SELECT DISTINCT numero_local FROM pagos WHERE inquilino = ? ORDER BY numero_local",
        conn, params=(inquilino,)
    )
    conn.close()
    return df['numero_local'].tolist()

def obtener_info_local(numero_local):
    """Obtiene información detallada de un local"""
    conn = get_db_connection()
    df = pd.read_sql(
        "SELECT planta, ramo_negocio, canon, contrato FROM pagos WHERE numero_local = ? LIMIT 1",
        conn, params=(numero_local,)
    )
    conn.close()
    return df.iloc[0] if not df.empty else None

def registrar_pago(local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
    """Registra un nuevo pago en la base de datos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        info_local = obtener_info_local(local)
        
        cursor.execute('''
            INSERT INTO pagos (
                numero_local, inquilino, planta, ramo_negocio, canon, contrato,
                fecha_pago, mes_abonado, monto, estado, observaciones
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            local, inquilino,
            info_local['planta'], info_local['ramo_negocio'],
            info_local['canon'], info_local['contrato'],
            fecha_pago, mes_abonado, monto, estado, observaciones
        ))
        
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error al registrar pago: {str(e)}")
        return False
    finally:
        conn.close()

# --- INTERFAZ DE USUARIO --- #
def mostrar_formulario_pago():
    """Muestra el formulario de registro de pagos con filtrado dinámico"""
    st.subheader("📝 Registrar Nuevo Pago")
    
    # Obtener lista de inquilinos
    inquilinos = obtener_inquilinos()
    
    # Formulario principal CON LA ESTRUCTURA CORRECTA
    with st.form(key='pago_form'):
        # Selector de inquilino
        inquilino_seleccionado = st.selectbox(
            "Seleccione Inquilino*",
            options=inquilinos,
            key="select_inquilino"
        )
        
        # Obtener locales asociados al inquilino seleccionado
        locales = obtener_locales_por_inquilino(inquilino_seleccionado) if inquilino_seleccionado else []
        
        if not locales:
            st.warning("Este inquilino no tiene locales asignados")
            st.stop()  # Detiene la ejecución si no hay locales
        
        # Selector de local
        local_seleccionado = st.selectbox(
            "Seleccione Local*",
            options=locales,
            key="select_local"
        )
        
        # Mostrar información del local seleccionado
        info_local = obtener_info_local(local_seleccionado)
        if info_local is not None:
            st.text(f"Planta: {info_local['planta']}")
            st.text(f"Ramo del negocio: {info_local['ramo_negocio']}")
            st.text(f"Canon: ${info_local['canon']:.2f}")
            st.text(f"Contrato: {info_local['contrato']}")
        
        # Campos del formulario
        fecha_pago = st.date_input("Fecha de Pago*", datetime.now())
        mes_abonado = st.text_input("Mes Abonado* (YYYY-MM)", placeholder="2025-06")
        monto = st.number_input("Monto Pagado*", min_value=0.0, value=float(info_local['canon']) if info_local else 0.0)
        estado = st.selectbox("Estado*", ["Pagado", "Parcial"])
        observaciones = st.text_area("Observaciones")
        
        # BOTÓN DE SUBMIT CORRECTO (parte esencial del formulario)
        submitted = st.form_submit_button("💾 Guardar Pago")
        
        # Lógica al enviar el formulario
        if submitted:
            if not mes_abonado:
                st.error("Debe especificar el mes abonado")
            else:
                if registrar_pago(
                    local_seleccionado, 
                    inquilino_seleccionado,
                    fecha_pago,
                    mes_abonado,
                    monto,
                    estado,
                    observaciones
                ):
                    st.success("✅ Pago registrado exitosamente!")
                    st.balloons()# --- APLICACIÓN PRINCIPAL --- #
def main():
    st.set_page_config(
        page_title="Dashboard de Pagos Arvelo",
        page_icon="💰",
        layout="wide"
    )
    
    init_db()  # Inicializar base de datos
    
    st.title("💰 Dashboard de Pagos - Arvelo")
    st.markdown("---")
    
    menu = st.sidebar.selectbox(
        "Menú Principal",
        ["Registrar Pago", "Consultar Morosidad", "Historial de Pagos"]
    )
    
    if menu == "Registrar Pago":
        mostrar_formulario_pago()
    elif menu == "Consultar Morosidad":
        mostrar_morosos()
    elif menu == "Historial de Pagos":
        mostrar_historial()

if __name__ == "__main__":
    main()
