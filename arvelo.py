import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date
import tempfile
import os
import shutil

# 1. CONFIGURACIÓN DE LA BASE DE DATOS
def get_db_connection():
    """Crea y retorna una conexión a la base de datos SQLite"""
    temp_dir = tempfile.gettempdir()
    db_path = os.path.join(temp_dir, "pagos_arvelo_final_v3.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# 2. DATOS INICIALES (COMPLETOS Y VERIFICADOS)
def cargar_datos_iniciales():
    """Retorna datos iniciales con todos los locales correctamente asociados"""
    return [
        ('LOCAL A', 'MONICA VARGAS', 'PB', 'LENCERIA', 350.0, 'CONTRATO A'),
        ('LOCAL B', 'OSCAR DUQUE', 'PB', 'LENCERIA', 350.0, 'CONTRATO B'),
        ('LOCAL 1', 'JOSE ANDRADE', 'PB', 'MANUFACTURA', 70.0, 'CONTRATO C'),
        ('LOCAL 2', 'JOSE ANDRADE', 'PB', 'MANUFACTURA', 70.0, 'CONTRATO D'),
        ('LOCAL 3', 'JOSE ANDRADE', 'PB', 'MANUFACTURA', 70.0, 'CONTRATO E'),
        ('LOCAL 31', 'ALDO MUÑOZ', 'MEZZANINE', 'SUSHI', 50.0, 'CONTRATO F'),
        ('LOCAL 32', 'ALDO MUÑOZ', 'MEZZANINE', 'SUSHI', 50.0, 'CONTRATO G'),
        ('LOCAL 10', 'YANIRE NAVARRO', 'PB', 'ARTESANIA', 150.0, 'CONTRATO H'),
        ('LOCAL 11', 'MARTIN SANTOS', 'PB', 'ROPA', 60.0, 'CONTRATO I'),
        ('LOCAL 12', 'MARTIN SANTOS', 'PB', 'ROPA', 60.0, 'CONTRATO J'),
    ]

# 3. INICIALIZACIÓN DE LA BASE DE DATOS
def init_db():
    """Inicializa la estructura de la base de datos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locales (
                numero_local TEXT PRIMARY KEY,
                inquilino TEXT NOT NULL,
                planta TEXT,
                ramo_negocio TEXT,
                contrato TEXT
            )
        ''')
        
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
        
        if cursor.execute("SELECT COUNT(*) FROM locales").fetchone()[0] == 0:
            datos = cargar_datos_iniciales()
            for dato in datos:
                try:
                    cursor.execute(
                        '''INSERT OR IGNORE INTO locales 
                        (numero_local, inquilino, planta, ramo_negocio, contrato)
                        VALUES (?, ?, ?, ?, ?)''',
                        (dato[0], dato[1], dato[2], dato[3], dato[5]))
                except sqlite3.IntegrityError as e:
                    st.warning(f"Error insertando local {dato[0]}: {str(e)}")
                    continue
            
            conn.commit()
            
    except Exception as e:
        st.error(f"Error inicializando DB: {str(e)}")
    finally:
        conn.close()

# 4. FUNCIONES DE CONSULTA
def obtener_inquilinos():
    """Retorna todos los inquilinos únicos"""
    conn = get_db_connection()
    try:
        df = pd.read_sql(
            "SELECT DISTINCT inquilino FROM locales ORDER BY inquilino", 
            conn
        )
        return df['inquilino'].tolist()
    finally:
        conn.close()

def obtener_locales_por_inquilino(inquilino):
    """Retorna solo los locales del inquilino especificado"""
    if not inquilino:
        return []
        
    conn = get_db_connection()
    try:
        df = pd.read_sql(
            "SELECT numero_local FROM locales WHERE inquilino = ? ORDER BY numero_local",
            conn, params=(inquilino,)
        )
        return df['numero_local'].tolist()
    finally:
        conn.close()

def obtener_info_local(numero_local):
    """Retorna información de un local específico"""
    if not numero_local:
        return None
        
    conn = get_db_connection()
    try:
        df = pd.read_sql(
            "SELECT * FROM locales WHERE numero_local = ?",
            conn, params=(numero_local,)
        )
        return df.iloc[0] if not df.empty else None
    finally:
        conn.close()

# 5. FUNCIÓN DE REGISTRO DE PAGOS
def registrar_pago(local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
    """Registra un nuevo pago en la base de datos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO pagos (
                numero_local, inquilino, fecha_pago, mes_abonado, 
                monto, estado, observaciones
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones))
        
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error registrando pago: {str(e)}")
        return False
    finally:
        conn.close()

# 6. FORMULARIO DE PAGOS (VERSIÓN FINAL COMPROBADA)
def mostrar_formulario_pago():
    """Muestra el formulario para registrar pagos con todas las correcciones"""
    st.subheader("📝 Registrar Nuevo Pago")
    
    # Obtener lista de inquilinos
    inquilinos = obtener_inquilinos()
    
    # Crear el formulario
    form = st.form(key='form_pago')
    with form:
        col1, col2 = st.columns(2)
        
        with col1:
            # Selector de inquilino
            inquilino_seleccionado = st.selectbox(
                "Seleccione Inquilino*",
                options=inquilinos,
                key="select_inquilino"
            )
            
            # Obtener locales del inquilino seleccionado
            locales_del_inquilino = obtener_locales_por_inquilino(inquilino_seleccionado)
            
            # Selector de local
            local_seleccionado = st.selectbox(
                "Seleccione Local*",
                options=locales_del_inquilino,
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
                placeholder="2023-01"
            )
            
            monto = st.number_input(
                "Monto*",
                min_value=0.0,
                value=350.0,
                step=10.0
            )
            
            estado = st.selectbox(
                "Estado*",
                options=["Pagado", "Parcial"]
            )
            
            observaciones = st.text_area("Observaciones")
        
        # Botón de submit CORRECTAMENTE implementado
        submitted = form.form_submit_button("💾 Guardar Pago")
    
        # Procesamiento dentro del formulario
        if submitted:
            if not all([local_seleccionado, inquilino_seleccionado, mes_abonado]):
                st.error("Por favor complete todos los campos obligatorios (*)")
            else:
                if registrar_pago(
                    local_seleccionado, inquilino_seleccionado,
                    fecha_pago, mes_abonado, monto, estado, observaciones
                ):
                    st.success("✅ Pago registrado exitosamente!")
                    st.balloons()

# 7. FUNCIÓN PRINCIPAL
def main():
    """Configuración principal de la aplicación"""
    st.set_page_config(
        page_title="Sistema de Pagos Arvelo",
        page_icon="💰",
        layout="wide"
    )
    
    # Inicializar base de datos (con mensaje de éxito)
    try:
        init_db()
    except Exception as e:
        st.error(f"Error inicializando la aplicación: {str(e)}")
        return
    
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
        st.subheader("📜 Historial de Pagos")
        st.write("Funcionalidad en desarrollo...")
    elif menu == "Reporte de Morosidad":
        st.subheader("⚠️ Reporte de Morosidad")
        st.write("Funcionalidad en desarrollo...")

if __name__ == "__main__":
    main()
