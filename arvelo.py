import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import tempfile
import os

# --- CONFIGURACIÓN DE LA BASE DE DATOS --- #
def get_db_connection():
    """Crea una conexión a la base de datos SQLite con permisos de escritura"""
    temp_dir = tempfile.gettempdir()
    db_path = os.path.join(temp_dir, "pagos_arvelo.db")
    return sqlite3.connect(db_path, check_same_thread=False)

# --- DATOS INICIALES (Del Excel que proporcionaste) --- #
def cargar_datos_iniciales():
    """Devuelve los datos iniciales basados en tu archivo Excel"""
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
    """Inicializa la base de datos con la estructura y datos iniciales"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Crear tabla si no existe
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
        
        # Verificar si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM pagos")
        if cursor.fetchone()[0] == 0:
            # Insertar datos iniciales
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
def obtener_locales():
    """Obtiene la lista de locales únicos"""
    conn = get_db_connection()
    locales = pd.read_sql("SELECT DISTINCT numero_local FROM pagos ORDER BY numero_local", conn)['numero_local'].tolist()
    conn.close()
    return locales

def obtener_inquilinos_por_local(local):
    """Obtiene inquilinos para un local específico"""
    conn = get_db_connection()
    inquilinos = pd.read_sql(
        "SELECT DISTINCT inquilino FROM pagos WHERE numero_local = ? ORDER BY inquilino",
        conn, params=(local,)
    )['inquilino'].tolist()
    conn.close()
    return inquilinos

def obtener_info_local(local):
    """Obtiene información detallada de un local"""
    conn = get_db_connection()
    info = pd.read_sql(
        "SELECT planta, ramo_negocio, canon, contrato FROM pagos WHERE numero_local = ? LIMIT 1",
        conn, params=(local,)
    ).iloc[0]
    conn.close()
    return info

def registrar_pago(local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
    """Registra un nuevo pago en la base de datos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Actualizar registro existente o insertar nuevo
        cursor.execute('''
            INSERT INTO pagos (
                numero_local, inquilino, planta, ramo_negocio, canon, contrato,
                fecha_pago, mes_abonado, estado, observaciones
            )
            SELECT 
                ?, ?, planta, ramo_negocio, canon, contrato,
                ?, ?, ?, ?
            FROM pagos
            WHERE numero_local = ? AND inquilino = ?
            LIMIT 1
        ''', (local, inquilino, fecha_pago, mes_abonado, estado, observaciones, local, inquilino))
        
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error al registrar pago: {str(e)}")
        return False
    finally:
        conn.close()

def obtener_morosos():
    """Obtiene la lista de inquilinos morosos"""
    conn = get_db_connection()
    morosos = pd.read_sql('''
        SELECT 
            numero_local, 
            inquilino, 
            canon,
            COUNT(*) as meses_pendientes,
            SUM(canon) as deuda_total
        FROM pagos
        WHERE estado = 'Pendiente'
        GROUP BY numero_local, inquilino, canon
        ORDER BY deuda_total DESC
    ''', conn)
    conn.close()
    return morosos

def obtener_historial_pagos():
    """Obtiene el historial completo de pagos"""
    conn = get_db_connection()
    historial = pd.read_sql('''
        SELECT 
            numero_local,
            inquilino,
            fecha_pago,
            mes_abonado,
            monto,
            estado,
            observaciones
        FROM pagos
        WHERE estado IN ('Pagado', 'Parcial')
        ORDER BY fecha_pago DESC
    ''', conn)
    conn.close()
    return historial

# --- INTERFAZ DE USUARIO --- #
def mostrar_formulario_pago():
    """Muestra el formulario para registrar pagos"""
    st.subheader("📝 Registrar Nuevo Pago")
    
    locales = obtener_locales()
    
    with st.form("form_pago", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            local = st.selectbox("Número de Local*", locales)
            inquilinos = obtener_inquilinos_por_local(local)
            inquilino = st.selectbox("Inquilino*", inquilinos)
            fecha_pago = st.date_input("Fecha de Pago*", datetime.now())
        
        with col2:
            info_local = obtener_info_local(local)
            st.text(f"Planta: {info_local['planta']}")
            st.text(f"Ramo: {info_local['ramo_negocio']}")
            st.text(f"Canon: ${info_local['canon']:.2f}")
            
            mes_abonado = st.text_input("Mes Abonado* (YYYY-MM)", placeholder="2025-06")
            monto = st.number_input("Monto Pagado*", min_value=0.0, value=float(info_local['canon']))
            estado = st.selectbox("Estado*", ["Pagado", "Parcial"])
        
        observaciones = st.text_area("Observaciones")
        
        if st.form_submit_button("💾 Guardar Pago"):
            if not mes_abonado:
                st.error("Debe especificar el mes abonado")
            else:
                if registrar_pago(local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
                    st.success("Pago registrado exitosamente!")
                    st.balloons()

def mostrar_morosos():
    """Muestra el reporte de morosidad"""
    st.subheader("⚠️ Inquilinos Morosos")
    
    morosos = obtener_morosos()
    
    if not morosos.empty:
        st.dataframe(morosos, use_container_width=True)
        
        deuda_total = morosos['deuda_total'].sum()
        st.metric("Deuda Total Pendiente", f"${deuda_total:,.2f}")
        
        st.download_button(
            "📥 Descargar Reporte",
            morosos.to_csv(index=False),
            "reporte_morosidad.csv",
            "text/csv"
        )
    else:
        st.success("🎉 No hay morosidad registrada!")

def mostrar_historial():
    """Muestra el historial de pagos"""
    st.subheader("📜 Historial de Pagos")
    
    historial = obtener_historial_pagos()
    
    if not historial.empty:
        st.dataframe(historial, use_container_width=True)
        
        st.download_button(
            "📥 Descargar Historial",
            historial.to_csv(index=False),
            "historial_pagos.csv",
            "text/csv"
        )
    else:
        st.info("No hay pagos registrados aún")

# --- APLICACIÓN PRINCIPAL --- #
def main():
    st.set_page_config(
        page_title="Dashboard de Pagos Arvelo",
        page_icon="💰",
        layout="wide"
    )
    
    # Inicializar base de datos
    init_db()
    
    st.title("💰 Dashboard de Pagos - Arvelo")
    st.markdown("---")
    
    # Menú lateral
    menu = st.sidebar.selectbox(
        "Menú Principal",
        ["Registrar Pago", "Morosidad", "Historial de Pagos"]
    )
    
    if menu == "Registrar Pago":
        mostrar_formulario_pago()
    elif menu == "Morosidad":
        mostrar_morosos()
    elif menu == "Historial de Pagos":
        mostrar_historial()

if __name__ == "__main__":
    main()
