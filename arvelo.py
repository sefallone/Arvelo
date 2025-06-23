import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la conexión a PostgreSQL
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "pagos_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        port=os.getenv("DB_PORT", "5432")
    )

# Inicializar la base de datos
def init_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si la tabla ya existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'pagos'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            cursor.execute("""
                CREATE TABLE pagos (
                    id_pago SERIAL PRIMARY KEY,
                    numero_local TEXT NOT NULL,
                    inquilino TEXT NOT NULL,
                    fecha_pago DATE,
                    mes_abonado TEXT NOT NULL,
                    monto DECIMAL(10, 2) NOT NULL,
                    estado TEXT NOT NULL,
                    observaciones TEXT,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            st.sidebar.success("Tabla 'pagos' creada exitosamente!")
        
        # Crear índice para búsquedas más rápidas
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_inquilino ON pagos (inquilino);
        """)
        conn.commit()
        
    except Exception as e:
        st.sidebar.error(f"Error al inicializar la base de datos: {e}")
    finally:
        if conn:
            conn.close()

# Función para agregar pagos
def agregar_pago(numero_local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pagos (numero_local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (numero_local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error al registrar pago: {e}")
        return False
    finally:
        if conn:
            conn.close()

# Función para obtener morosos
def obtener_morosos():
    try:
        conn = get_connection()
        query = """
            SELECT numero_local, inquilino, mes_abonado, monto, estado
            FROM pagos
            WHERE estado = 'Pendiente' OR fecha_pago IS NULL
            ORDER BY mes_abonado DESC
        """
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error al obtener morosos: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

# Función para obtener historial de pagos
def obtener_historial_pagos(limit=100):
    try:
        conn = get_connection()
        query = f"""
            SELECT numero_local, inquilino, fecha_pago, mes_abonado, monto, estado
            FROM pagos
            ORDER BY fecha_pago DESC NULLS LAST, mes_abonado DESC
            LIMIT {limit}
        """
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error al obtener historial: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

# Función para obtener resumen por inquilino
def obtener_resumen_inquilinos():
    try:
        conn = get_connection()
        query = """
            SELECT 
                inquilino,
                COUNT(*) AS total_pagos,
                SUM(CASE WHEN estado = 'Pagado' THEN 1 ELSE 0 END) AS pagados,
                SUM(CASE WHEN estado = 'Pendiente' THEN 1 ELSE 0 END) AS pendientes,
                SUM(CASE WHEN estado = 'Pagado' THEN monto ELSE 0 END) AS monto_pagado,
                SUM(CASE WHEN estado = 'Pendiente' THEN monto ELSE 0 END) AS monto_pendiente
            FROM pagos
            GROUP BY inquilino
            ORDER BY monto_pendiente DESC
        """
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error al obtener resumen: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

# Interfaz de Streamlit
def main():
    st.set_page_config(page_title="Dashboard de Pagos", layout="wide")
    
    # Inicializar la base de datos
    init_db()
    
    st.title("📊 Dashboard de Pagos de Cánones Comerciales")
    st.markdown("---")
    
    # Menú lateral
    menu = st.sidebar.selectbox(
        "Menú Principal",
        ["Registrar Pago", "Morosidad", "Historial de Pagos", "Resumen por Inquilino"]
    )
    
    if menu == "Registrar Pago":
        st.subheader("Registrar Nuevo Pago")
        with st.form("pago_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                numero_local = st.text_input("Número de Local*", placeholder="LOCAL A")
                inquilino = st.text_input("Inquilino*", placeholder="Nombre del inquilino")
                fecha_pago = st.date_input("Fecha de Pago")
            
            with col2:
                mes_abonado = st.text_input("Mes Abonado* (YYYY-MM)", placeholder="2023-10")
                monto = st.number_input("Monto*", min_value=0.0, step=0.01)
                estado = st.selectbox("Estado*", ["Pagado", "Pendiente", "Parcial"])
            
            observaciones = st.text_area("Observaciones")
            
            submit = st.form_submit_button("Registrar Pago")
            
            if submit:
                if not all([numero_local, inquilino, mes_abonado, monto]):
                    st.error("Por favor complete los campos obligatorios (*)")
                else:
                    if agregar_pago(numero_local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
                        st.success("¡Pago registrado exitosamente!")
    
    elif menu == "Morosidad":
        st.subheader("Inquilinos Morosos")
        df_morosos = obtener_morosos()
        
        if not df_morosos.empty:
            st.dataframe(df_morosos, use_container_width=True)
            
            # Mostrar resumen de morosidad
            total_morosos = len(df_morosos)
            total_deuda = df_morosos['monto'].sum()
            
            col1, col2 = st.columns(2)
            col1.metric("Total Morosos", total_morosos)
            col2.metric("Deuda Total", f"${total_deuda:,.2f}")
            
            st.download_button(
                "Descargar Reporte de Morosidad",
                df_morosos.to_csv(index=False),
                "reporte_morosidad.csv",
                "text/csv"
            )
        else:
            st.success("¡No hay morosos registrados!")
    
    elif menu == "Historial de Pagos":
        st.subheader("Historial de Pagos Recientes")
        limit = st.slider("Número de registros a mostrar", 10, 500, 100)
        df_historial = obtener_historial_pagos(limit)
        
        if not df_historial.empty:
            st.dataframe(df_historial, use_container_width=True)
            
            st.download_button(
                "Descargar Historial Completo",
                df_historial.to_csv(index=False),
                "historial_pagos.csv",
                "text/csv"
            )
        else:
            st.info("No hay registros de pagos aún.")
    
    elif menu == "Resumen por Inquilino":
        st.subheader("Resumen de Pagos por Inquilino")
        df_resumen = obtener_resumen_inquilinos()
        
        if not df_resumen.empty:
            # Mostrar métricas generales
            total_inquilinos = len(df_resumen)
            total_pendientes = df_resumen['pendientes'].sum()
            total_deuda = df_resumen['monto_pendiente'].sum()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Inquilinos", total_inquilinos)
            col2.metric("Pagos Pendientes", total_pendientes)
            col3.metric("Deuda Total", f"${total_deuda:,.2f}")
            
            # Mostrar tabla con resumen
            st.dataframe(df_resumen, use_container_width=True)
            
            st.download_button(
                "Descargar Resumen",
                df_resumen.to_csv(index=False),
                "resumen_inquilinos.csv",
                "text/csv"
            )
        else:
            st.info("No hay datos para mostrar.")

if __name__ == "__main__":
    main()
