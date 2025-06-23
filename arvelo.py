import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Cargar datos iniciales del Excel
@st.cache_data
def cargar_datos_iniciales():
    # Reemplaza esta línea con la carga de tu archivo Excel real
    # df_inquilinos = pd.read_excel("Python Control Arvelo.xlsx")
    
    # Datos de ejemplo basados en el Excel que me compartiste
    data = {
        "NUMERO LOCAL": ["LOCAL A", "LOCAL B", "LOCAL 1", "LOCAL 2", "LOCAL 3", "LOCAL 4", "LOCAL 5"],
        "INQUILINO": ["MONICA JANET VARGAS G.", "OSCAR DUQUE ECHEVERRIA", 
                     "JOSE MANUEL ANDRADE PEREIRA", "JOSE MANUEL ANDRADE PEREIRA",
                     "JOSE MANUEL ANDRADE PEREIRA", "JOSE R. RODRIGUEZ V.", "JOSE R. RODRIGUEZ V."],
        "PLANTA": ["PB", "PB", "PB", "PB", "PB", "PB", "PB"],
        "RAMO DEL NEGOCIO": ["LENCERIA", "LENCERIA", "MANUFACTURA", "MANUFACTURA", 
                            "MANUFACTURA", "DOMESA", "DOMESA"],
        "CANON": [350, 350, 70, 70, 70, 33.33, 33.33],
        "CONTRATO": ["MONICA JANET VARGAS G.", "OSCAR DUQUE ECHEVERRI", 
                    "JOSE M. ANDRADE PEREIRA", "JOSE M. ANDRADE PEREIRA",
                    "JOSE M. ANDRADE PEREIRA", "YORMAN JOSE VALERA", "YORMAN JOSE VALERA"]
    }
    return pd.DataFrame(data)

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
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pagos (
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

# Obtener opciones para los selectbox
def obtener_opciones(df):
    locales = sorted(df["NUMERO LOCAL"].unique().tolist())
    inquilinos = sorted(df["INQUILINO"].unique().tolist())
    return locales, inquilinos

# Interfaz de Streamlit
def main():
    st.set_page_config(page_title="Dashboard de Pagos", layout="wide")
    
    # Cargar datos iniciales
    df_inquilinos = cargar_datos_iniciales()
    locales, inquilinos = obtener_opciones(df_inquilinos)
    
    # Inicializar la base de datos
    init_db()
    
    st.title("📊 Dashboard de Pagos de Cánones Comerciales")
    st.markdown("---")
    
    # Menú lateral
    menu = st.sidebar.selectbox(
        "Menú Principal",
        ["Registrar Pago", "Consultar Pagos"]
    )
    
    if menu == "Registrar Pago":
        st.subheader("Registrar Nuevo Pago")
        
        with st.form("pago_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                # Menú desplegable para número de local
                numero_local = st.selectbox(
                    "Número de Local*",
                    options=locales,
                    index=0
                )
                
                # Menú desplegable para inquilino
                inquilino = st.selectbox(
                    "Inquilino*",
                    options=inquilinos,
                    index=0
                )
                
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
    
    elif menu == "Consultar Pagos":
        st.subheader("Consultar Pagos Registrados")
        
        # Filtros de búsqueda
        with st.expander("Filtros de Búsqueda"):
            col1, col2 = st.columns(2)
            
            with col1:
                filtro_local = st.selectbox(
                    "Filtrar por Local",
                    options=["Todos"] + locales
                )
            
            with col2:
                filtro_inquilino = st.selectbox(
                    "Filtrar por Inquilino",
                    options=["Todos"] + inquilinos
                )
        
        # Consultar pagos según filtros
        try:
            conn = get_connection()
            query = "SELECT * FROM pagos WHERE 1=1"
            params = []
            
            if filtro_local != "Todos":
                query += " AND numero_local = %s"
                params.append(filtro_local)
                
            if filtro_inquilino != "Todos":
                query += " AND inquilino = %s"
                params.append(filtro_inquilino)
                
            query += " ORDER BY fecha_pago DESC NULLS LAST"
            
            df_pagos = pd.read_sql(query, conn, params=params if params else None)
            
            if not df_pagos.empty:
                st.dataframe(df_pagos, use_container_width=True)
                
                # Mostrar resumen
                total_pagos = len(df_pagos)
                total_monto = df_pagos['monto'].sum()
                
                st.metric("Total de Pagos", total_pagos)
                st.metric("Monto Total", f"${total_monto:,.2f}")
                
                # Opción para descargar
                st.download_button(
                    "Descargar Reporte",
                    df_pagos.to_csv(index=False),
                    "reporte_pagos.csv",
                    "text/csv"
                )
            else:
                st.info("No se encontraron pagos con los filtros seleccionados")
                
        except Exception as e:
            st.error(f"Error al consultar pagos: {e}")
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    main()
