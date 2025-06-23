import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- FUNCIONES DE BASE DE DATOS (SQLite) --- #
def init_db():
    """Inicializa la base de datos SQLite."""
    conn = sqlite3.connect("pagos.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_local TEXT NOT NULL,
            inquilino TEXT NOT NULL,
            fecha_pago DATE,
            mes_abonado TEXT NOT NULL,
            monto REAL NOT NULL,
            estado TEXT NOT NULL,
            observaciones TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def agregar_pago(numero_local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
    """Registra un nuevo pago en la base de datos."""
    conn = sqlite3.connect("pagos.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pagos (numero_local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (numero_local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones))
    conn.commit()
    conn.close()

def obtener_morosos():
    """Obtiene la lista de inquilinos morosos."""
    conn = sqlite3.connect("pagos.db")
    df = pd.read_sql("""
        SELECT numero_local, inquilino, mes_abonado, monto, estado
        FROM pagos
        WHERE estado = 'Pendiente' OR fecha_pago IS NULL
        ORDER BY mes_abonado
    """, conn)
    conn.close()
    return df

def obtener_historial():
    """Obtiene el historial completo de pagos."""
    conn = sqlite3.connect("pagos.db")
    df = pd.read_sql("SELECT * FROM pagos ORDER BY fecha_pago DESC", conn)
    conn.close()
    return df

# --- CARGAR DATOS DEL EXCEL (INQUILINOS Y LOCALES) --- #
@st.cache_data
def cargar_inquilinos():
    """Carga el listado de inquilinos y locales desde el Excel."""
    try:
        df = pd.read_excel("Python Control Arvelo.xlsx", sheet_name="Hoja1")
        # Elimina duplicados y ordena
        locales = sorted(df["NUMERO LOCAL"].dropna().unique().tolist())
        inquilinos = sorted(df["INQUILINO"].dropna().unique().tolist())
        return locales, inquilinos
    except Exception as e:
        st.error(f"No se pudo cargar el archivo Excel: {e}")
        return [], []

# --- INTERFAZ DE STREAMLIT --- #
def main():
    st.set_page_config(page_title="Dashboard de Pagos", layout="wide")
    st.title("📊 **Dashboard de Pagos de Cánones Comerciales**")
    st.markdown("---")

    # Inicializar DB y cargar datos del Excel
    init_db()
    locales, inquilinos = cargar_inquilinos()

    # --- MENÚ LATERAL --- #
    menu = st.sidebar.selectbox(
        "Menú Principal",
        ["Registrar Pago", "Morosidad", "Historial de Pagos"]
    )

    # --- FORMULARIO DE PAGO --- #
    if menu == "Registrar Pago":
        st.subheader("📝 **Registrar Nuevo Pago**")
        
        with st.form("form_pago", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                # Menú desplegable para NÚMERO DE LOCAL
                numero_local = st.selectbox(
                    "🔹 **Número de Local**",
                    options=locales,
                    index=0
                )
                
                # Menú desplegable para INQUILINO
                inquilino = st.selectbox(
                    "👤 **Inquilino**",
                    options=inquilinos,
                    index=0
                )
                
                fecha_pago = st.date_input("📅 **Fecha de Pago**", datetime.now())
            
            with col2:
                mes_abonado = st.text_input("🗓️ **Mes Abonado (YYYY-MM)**", placeholder="2025-06")
                monto = st.number_input("💰 **Monto**", min_value=0.0, step=0.01)
                estado = st.selectbox("📌 **Estado**", ["Pagado", "Pendiente", "Parcial"])
            
            observaciones = st.text_area("📝 **Observaciones**")
            
            if st.form_submit_button("💾 **Guardar Pago**"):
                if not mes_abonado:
                    st.error("⚠️ **Debes especificar el mes abonado (YYYY-MM).**")
                else:
                    agregar_pago(numero_local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones)
                    st.success("✅ **Pago registrado correctamente.**")

    # --- PESTAÑA DE MOROSIDAD --- #
    elif menu == "Morosidad":
        st.subheader("⚠️ **Inquilinos Morosos**")
        df_morosos = obtener_morosos()
        
        if not df_morosos.empty:
            st.dataframe(df_morosos, use_container_width=True)
            
            # Resumen de deuda
            total_morosos = len(df_morosos)
            total_deuda = df_morosos["monto"].sum()
            
            st.metric("🔴 **Total de Morosos**", total_morosos)
            st.metric("💸 **Deuda Pendiente**", f"${total_deuda:,.2f}")
            
            # Botón para descargar
            st.download_button(
                "📥 **Descargar Reporte de Morosidad**",
                df_morosos.to_csv(index=False),
                "morosos.csv",
                "text/csv"
            )
        else:
            st.success("🎉 **¡No hay morosidad registrada!**")

    # --- PESTAÑA DE HISTORIAL --- #
    elif menu == "Historial de Pagos":
        st.subheader("📜 **Historial de Pagos**")
        df_historial = obtener_historial()
        
        if not df_historial.empty:
            st.dataframe(df_historial, use_container_width=True)
            
            # Botón para descargar
            st.download_button(
                "📥 **Descargar Historial Completo**",
                df_historial.to_csv(index=False),
                "historial_pagos.csv",
                "text/csv"
            )
        else:
            st.info("ℹ️ **No hay pagos registrados aún.**")

if __name__ == "__main__":
    main()
