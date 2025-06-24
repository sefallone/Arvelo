# 1. IMPORTACIONES REQUERIDAS
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date
import tempfile
import os
import shutil

# 2. CONFIGURACIÓN DE LA BASE DE DATOS
def get_db_connection():
    """
    Establece y retorna una conexión a la base de datos SQLite
    con configuración para acceso multi-hilo
    """
    temp_dir = tempfile.gettempdir()
    db_path = os.path.join(temp_dir, "pagos_arvelo_v2.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Permite acceso a columnas por nombre
    return conn

# 3. DATOS INICIALES DEL SISTEMA
def cargar_datos_iniciales():
    """
    Retorna los datos iniciales de locales con su información básica
    Formato: (local, inquilino, planta, ramo, canon, contrato)
    """
    return [
        ('LOCAL A', 'MONICA VARGAS', 'PB', 'LENCERIA', 350.0, 'CONTRATO A'),
        ('LOCAL B', 'OSCAR DUQUE', 'PB', 'LENCERIA', 350.0, 'CONTRATO B'),
        # ... (agregar todos los demás locales)
    ]

# 4. INICIALIZACIÓN DE LA BASE DE DATOS
def init_db():
    """
    Crea las tablas necesarias en la base de datos
    e inserta los datos iniciales si no existen
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Crear tabla de locales si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locales (
                numero_local TEXT PRIMARY KEY,
                inquilino TEXT NOT NULL,
                planta TEXT,
                ramo_negocio TEXT,
                contrato TEXT
            )
        ''')
        
        # Crear tabla de pagos con relaciones
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
        
        # Verificar si hay datos existentes
        if cursor.execute("SELECT COUNT(*) FROM locales").fetchone()[0] == 0:
            # Insertar datos iniciales
            datos = cargar_datos_iniciales()
            cursor.executemany(
                '''INSERT INTO locales 
                (numero_local, inquilino, planta, ramo_negocio, contrato)
                VALUES (?, ?, ?, ?, ?)''',
                [(x[0], x[1], x[2], x[3], x[5]) for x in datos]
            )
            
        conn.commit()
    except Exception as e:
        st.error(f"Error inicializando base de datos: {str(e)}")
    finally:
        conn.close()

# 5. FUNCIONES DE CONSULTA A LA BASE DE DATOS
def obtener_locales():
    """Retorna lista ordenada de todos los locales registrados"""
    conn = get_db_connection()
    try:
        df = pd.read_sql("SELECT numero_local FROM locales ORDER BY numero_local", conn)
        return df['numero_local'].tolist()
    finally:
        conn.close()

def obtener_inquilinos():
    """Retorna lista alfabética de inquilinos únicos"""
    conn = get_db_connection()
    try:
        df = pd.read_sql("SELECT DISTINCT inquilino FROM locales ORDER BY inquilino", conn)
        return df['inquilino'].tolist()
    finally:
        conn.close()

def obtener_locales_por_inquilino(inquilino):
    """
    Retorna los locales asociados a un inquilino específico
    ordenados por número de local
    """
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
    """
    Retorna información completa de un local específico
    como un objeto Row con los campos:
    numero_local, inquilino, planta, ramo_negocio, contrato
    """
    conn = get_db_connection()
    try:
        df = pd.read_sql(
            "SELECT * FROM locales WHERE numero_local = ?",
            conn, params=(numero_local,)
        )
        return df.iloc[0] if not df.empty else None
    finally:
        conn.close()

# 6. FUNCIONES DE REGISTRO Y ACTUALIZACIÓN
def registrar_pago(local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
    """
    Registra un nuevo pago en la base de datos con validación básica
    Retorna True si fue exitoso, False si falló
    """
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

# 7. INTERFACES DE USUARIO
def mostrar_formulario_pago():
    """Muestra el formulario interactivo para registro de pagos"""
    st.subheader("📝 Registrar Nuevo Pago")
    
    with st.form(key='form_pago'):
        # Sección 1: Selección de inquilino y local
        col1, col2 = st.columns(2)
        
        with col1:
            inquilino = st.selectbox(
                "Inquilino*",
                options=obtener_inquilinos(),
                key="select_inquilino"
            )
            
            local = st.selectbox(
                "Local*",
                options=obtener_locales_por_inquilino(inquilino) if inquilino else [],
                key="select_local"
            )
            
            if local:
                info = obtener_info_local(local)
                st.markdown(f"""
                    **Planta:** {info['planta']}  
                    **Ramo:** {info['ramo_negocio']}  
                    **Contrato:** {info['contrato']}
                """)
        
        # Sección 2: Datos del pago
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
        
        # Botón de envío dentro del formulario
        submitted = st.form_submit_button("💾 Guardar Pago")
    
    # Procesamiento después del envío (fuera del form)
    if submitted:
        if not all([local, inquilino, mes_abonado]):
            st.error("Por favor complete todos los campos obligatorios (*)")
        else:
            if registrar_pago(local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
                st.success("✅ Pago registrado exitosamente!")
                st.balloons()

def mostrar_historial():
    """Muestra el historial completo de pagos registrados"""
    st.subheader("📜 Historial de Pagos")
    
    conn = get_db_connection()
    try:
        # Obtener todos los pagos ordenados por fecha descendente
        df = pd.read_sql(
            "SELECT * FROM pagos ORDER BY fecha_pago DESC",
            conn
        )
        
        # Mostrar dataframe con formato mejorado
        if not df.empty:
            st.dataframe(
                df.style.format({
                    'monto': '${:,.2f}'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("No hay pagos registrados aún")
    finally:
        conn.close()

def mostrar_morosos():
    """Muestra reporte de morosidad con cálculos básicos"""
    st.subheader("⚠️ Reporte de Morosidad")
    
    conn = get_db_connection()
    try:
        # Consulta para identificar pagos pendientes
        df = pd.read_sql('''
            SELECT l.numero_local, l.inquilino, 
                   COUNT(p.id) AS pagos_pendientes,
                   SUM(l.canon) AS total_adeudado
            FROM locales l
            LEFT JOIN pagos p ON l.numero_local = p.numero_local 
                            AND p.estado = 'Pendiente'
            GROUP BY l.numero_local, l.inquilino
            HAVING pagos_pendientes > 0
            ORDER BY total_adeudado DESC
        ''', conn)
        
        if not df.empty:
            st.dataframe(
                df.style.format({
                    'total_adeudado': '${:,.2f}'
                }),
                use_container_width=True
            )
            
            # Resumen total
            total_adeudado = df['total_adeudado'].sum()
            st.metric("Total Adeudado", f"${total_adeudado:,.2f}")
        else:
            st.success("👍 No hay morosidad registrada")
    finally:
        conn.close()

# 8. CONFIGURACIÓN PRINCIPAL DE LA APLICACIÓN
def main():
    """Función principal que configura y ejecuta la aplicación"""
    # Configuración de la página
    st.set_page_config(
        page_title="Sistema de Pagos Arvelo",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inicializar base de datos
    init_db()
    
    # Título principal
    st.title("💰 Sistema de Gestión de Pagos - Arvelo")
    st.markdown("---")
    
    # Menú lateral
    menu_opcion = st.sidebar.selectbox(
        "Menú Principal",
        ["Registrar Pago", "Historial de Pagos", "Reporte de Morosidad"]
    )
    
    # Navegación entre secciones
    if menu_opcion == "Registrar Pago":
        mostrar_formulario_pago()
    elif menu_opcion == "Historial de Pagos":
        mostrar_historial()
    elif menu_opcion == "Reporte de Morosidad":
        mostrar_morosos()
    
    # Sección de backup en el sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Generar Backup"):
        try:
            db_path = os.path.join(tempfile.gettempdir(), "pagos_arvelo_v2.db")
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                shutil.copy2(db_path, tmp.name)
                with open(tmp.name, 'rb') as f:
                    st.sidebar.download_button(
                        "⬇️ Descargar Backup",
                        f,
                        file_name="backup_pagos_arvelo.db"
                    )
            st.sidebar.success("Backup generado correctamente")
        except Exception as e:
            st.sidebar.error(f"Error al generar backup: {str(e)}")

# 9. EJECUCIÓN DEL PROGRAMA
if __name__ == "__main__":
    main()
