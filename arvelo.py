import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Configuración inicial de la base de datos
def init_db():
    conn = sqlite3.connect('pagos_inquilinos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pagos (
            ID_Pago INTEGER PRIMARY KEY AUTOINCREMENT,
            NUMERO_LOCAL TEXT,
            INQUILINO TEXT,
            FECHA_PAGO DATE,
            MES_ABONADO TEXT,
            MONTO REAL,
            ESTADO TEXT,
            OBSERVACIONES TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Función para agregar pagos
def agregar_pago(numero_local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
    conn = sqlite3.connect('pagos_inquilinos.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pagos (NUMERO_LOCAL, INQUILINO, FECHA_PAGO, MES_ABONADO, MONTO, ESTADO, OBSERVACIONES)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (numero_local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones))
    conn.commit()
    conn.close()

# Función para visualizar morosos
def obtener_morosos():
    conn = sqlite3.connect('pagos_inquilinos.db')
    query = '''
        SELECT NUMERO_LOCAL, INQUILINO, MES_ABONADO, MONTO, ESTADO
        FROM pagos
        WHERE ESTADO = "Pendiente" OR FECHA_PAGO IS NULL
    '''
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Interfaz de Streamlit
def main():
    st.title("📊 Dashboard de Pagos de Cánones Comerciales")
    st.markdown("---")

    # Inicializar DB
    init_db()

    # Menú lateral
    menu = st.sidebar.selectbox("Menú", ["Registrar Pago", "Morosidad", "Reportes"])

    if menu == "Registrar Pago":
        st.subheader("Registrar Nuevo Pago")
        with st.form("pago_form"):
            numero_local = st.text_input("Número de Local")
            inquilino = st.text_input("Inquilino")
            fecha_pago = st.date_input("Fecha de Pago")
            mes_abonado = st.text_input("Mes Abonado (YYYY-MM)", placeholder="2023-10")
            monto = st.number_input("Monto", min_value=0.0)
            estado = st.selectbox("Estado", ["Pagado", "Pendiente", "Parcial"])
            observaciones = st.text_area("Observaciones")
            submit = st.form_submit_button("Guardar")

            if submit:
                agregar_pago(numero_local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones)
                st.success("¡Pago registrado exitosamente!")

    elif menu == "Morosidad":
        st.subheader("Inquilinos Morosos")
        df_morosos = obtener_morosos()
        if not df_morosos.empty:
            st.dataframe(df_morosos)
            st.download_button("Descargar Reporte", df_morosos.to_csv(index=False), "morosos.csv")
        else:
            st.info("No hay morosos registrados.")

    elif menu == "Reportes":
        st.subheader("Reportes Históricos")
        # Aquí puedes agregar gráficos con matplotlib/plotly para visualizar tendencias.

if __name__ == "__main__":
    main()
