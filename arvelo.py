# 1. IMPORTACIONES
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date
import tempfile
import os
import shutil

# 2. CONFIGURACIÓN BASE DE DATOS
def get_db_connection():
    """Crea conexión a SQLite con manejo multi-hilo"""
    temp_dir = tempfile.gettempdir()
    db_path = os.path.join(temp_dir, "pagos_arvelo_v3.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# 3. DATOS INICIALES
def cargar_datos_iniciales():
    """Datos de ejemplo para inicializar la DB"""
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

# 4. INICIALIZACIÓN DB
def init_db():
    """Crea estructura inicial de la base de datos"""
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
                estado TEXT,
                observaciones TEXT,
                FOREIGN KEY(numero_local) REFERENCES locales(numero_local)
            )
        ''')
        
        if cursor.execute("SELECT COUNT(*) FROM locales").fetchone()[0] == 0:
            cursor.executemany(
                '''INSERT INTO locales 
                (numero_local, inquilino, planta, ramo_negocio, contrato)
                VALUES (?, ?, ?, ?, ?)''',
                [(x[0], x[1], x[2], x[3], x[5]) for x in cargar_datos_iniciales()]
            )
            
        conn.commit()
    except Exception as e:
        st.error(f"Error inicializando DB: {str(e)}")
    finally:
        conn.close()

# 5. FUNCIONES DE CONSULTA (CORREGIDAS)
def obtener_inquilinos():
    """Obtiene TODOS los inquilinos sin filtros"""
    conn = get_db_connection()
    try:
        df = pd.read_sql(
            "SELECT DISTINCT inquilino FROM locales ORDER BY inquilino", 
            conn
        )
        return [''] + df['inquilino'].tolist()  # Agrega opción vacía
    finally:
        conn.close()

def obtener_locales(inquilino=None):
    """Obtiene locales, con opción de filtrar por inquilino"""
    conn = get_db_connection()
    try:
        if inquilino:
            df = pd.read_sql(
                "SELECT numero_local FROM locales WHERE inquilino = ? ORDER BY numero_local",
                conn, params=(inquilino,)
            )
        else:
            df = pd.read_sql(
                "SELECT numero_local FROM locales ORDER BY numero_local",
                conn
            )
        return [''] + df['numero_local'].tolist()  # Agrega opción vacía
    finally:
        conn.close()

def obtener_info_local(numero_local):
    """Obtiene información completa de un local"""
    conn = get_db_connection()
    try:
        df = pd.read_sql(
            "SELECT * FROM locales WHERE numero_local = ?",
            conn, params=(numero_local,)
        )
        return df.iloc[0] if not df.empty else None
    finally:
        conn.close()

# 6. INTERFAZ DE USUARIO (CORREGIDA)
def mostrar_formulario_pago():
    """Formulario corregido para mostrar todas las opciones"""
    st.subheader("📝 Registrar Nuevo Pago")
    
    with st.form(key='form_pago'):
        col1, col2 = st.columns(2)
        
        with col1:
            # Selector de inquilino con TODAS las opciones
            inquilino_seleccionado = st.selectbox(
                "Inquilino*",
                options=obtener_inquilinos(),
                index=0  # Selecciona la opción vacía por defecto
            )
            
            # Selector de local que responde al inquilino seleccionado
            if inquilino_seleccionado:
                locales_opciones = obtener_locales(inquilino_seleccionado)
            else:
                locales_opciones = obtener_locales()
                
            local_seleccionado = st.selectbox(
                "Local*",
                options=locales_opciones,
                index=0
            )
            
            # Mostrar info del local si hay uno seleccionado
            if local_seleccionado:
                info = obtener_info_local(local_seleccionado)
                st.markdown(f"""
                    **Planta:** {info['planta']}  
                    **Ramo:** {info['ramo_negocio']}  
                    **Contrato:** {info['contrato']}
                """)
        
        with col2:
            fecha_pago = st.date_input("Fecha de Pago*", value=date.today())
            mes_abonado = st.text_input("Mes Abonado* (YYYY-MM)", placeholder="2023-01")
            monto = st.number_input("Monto*", min_value=0.0, value=350.0)
            estado = st.selectbox("Estado*", ["Pagado", "Parcial"])
            observaciones = st.text_area("Observaciones")
        
        submitted = st.form_submit_button("💾 Guardar Pago")
    
    if submitted:
        if not all([local_seleccionado, inquilino_seleccionado, mes_abonado]):
            st.error("Complete todos los campos obligatorios (*)")
        else:
            if registrar_pago(
                local_seleccionado, inquilino_seleccionado, 
                fecha_pago, mes_abonado, monto, estado, observaciones
            ):
                st.success("✅ Pago registrado!")
                st.balloons()

def mostrar_historial():
    """Historial con filtros mejorados"""
    st.subheader("📜 Historial de Pagos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Filtro por inquilino (todas las opciones)
        inquilino_filtro = st.selectbox(
            "Filtrar por inquilino",
            options=['Todos'] + obtener_inquilinos()[1:],  # Excluye la opción vacía
            index=0
        )
    
    with col2:
        # Filtro por local (todas las opciones)
        local_filtro = st.selectbox(
            "Filtrar por local",
            options=['Todos'] + obtener_locales()[1:],  # Excluye la opción vacía
            index=0
        )
    
    # Construir consulta SQL dinámica
    query = "SELECT * FROM pagos"
    params = []
    
    condiciones = []
    if inquilino_filtro != 'Todos':
        condiciones.append("inquilino = ?")
        params.append(inquilino_filtro)
    if local_filtro != 'Todos':
        condiciones.append("numero_local = ?")
        params.append(local_filtro)
    
    if condiciones:
        query += " WHERE " + " AND ".join(condiciones)
    
    query += " ORDER BY fecha_pago DESC"
    
    conn = get_db_connection()
    try:
        df = pd.read_sql(query, conn, params=params if params else None)
        
        if not df.empty:
            st.dataframe(
                df.style.format({'monto': '${:,.2f}'}),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("No se encontraron registros con esos filtros")
    finally:
        conn.close()

# 7. FUNCIÓN PRINCIPAL
def main():
    st.set_page_config(
        page_title="Sistema Pagos Arvelo",
        page_icon="💰",
        layout="wide"
    )
    
    init_db()
    
    st.title("💰 Sistema de Pagos - Arvelo")
    st.markdown("---")
    
    menu = st.sidebar.selectbox(
        "Menú",
        ["Registrar Pago", "Historial", "Morosidad"]
    )
    
    if menu == "Registrar Pago":
        mostrar_formulario_pago()
    elif menu == "Historial":
        mostrar_historial()
    elif menu == "Morosidad":
        st.subheader("⚠️ Reporte de Morosidad")
        st.write("Funcionalidad en desarrollo")

if __name__ == "__main__":
    main()
