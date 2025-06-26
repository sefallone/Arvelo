import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os

# Configuración inicial
st.set_page_config(page_title="Sistema de Pagos de Inquilinos", page_icon="🏢", layout="wide")

# Conexión a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect('pagos_inquilinos.db')
    conn.row_factory = sqlite3.Row
    return conn

# Inicializar la base de datos
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabla de inquilinos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inquilinos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        local TEXT NOT NULL,
        inquilino TEXT NOT NULL,
        ramo_negocio TEXT,
        canon_actual REAL,
        contrato TEXT,
        UNIQUE(local, inquilino)
    )
    ''')
    
    # Tabla de pagos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pagos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        inquilino_id INTEGER,
        mes TEXT NOT NULL,
        monto REAL NOT NULL,
        fecha_pago TEXT,
        estado TEXT CHECK(estado IN ('Pagado', 'Pendiente', 'Parcial')),
        FOREIGN KEY (inquilino_id) REFERENCES inquilinos (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Funciones CRUD para inquilinos
def agregar_inquilino(local, inquilino, ramo, canon, contrato):
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO inquilinos (local, inquilino, ramo_negocio, canon_actual, contrato) VALUES (?, ?, ?, ?, ?)',
            (local, inquilino, ramo, canon, contrato)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error("Este local-inquilino ya existe en la base de datos")
        return False
    finally:
        conn.close()

def actualizar_inquilino(id_inquilino, local, inquilino, ramo, canon, contrato):
    conn = get_db_connection()
    conn.execute(
        'UPDATE inquilinos SET local=?, inquilino=?, ramo_negocio=?, canon_actual=?, contrato=? WHERE id=?',
        (local, inquilino, ramo, canon, contrato, id_inquilino)
    )
    conn.commit()
    conn.close()

def eliminar_inquilino(id_inquilino):
    conn = get_db_connection()
    conn.execute('DELETE FROM inquilinos WHERE id=?', (id_inquilino,))
    conn.commit()
    conn.close()

def obtener_inquilinos():
    conn = get_db_connection()
    inquilinos = conn.execute('SELECT * FROM inquilinos ORDER BY inquilino').fetchall()
    conn.close()
    return inquilinos

def buscar_inquilinos(termino):
    conn = get_db_connection()
    resultados = conn.execute(
        'SELECT * FROM inquilinos WHERE local LIKE ? OR inquilino LIKE ?',
        (f'%{termino}%', f'%{termino}%')
    ).fetchall()
    conn.close()
    return resultados

# Funciones CRUD para pagos
def agregar_pago(inquilino_id, mes, monto, estado):
    conn = get_db_connection()
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute(
        'INSERT INTO pagos (inquilino_id, mes, monto, fecha_pago, estado) VALUES (?, ?, ?, ?, ?)',
        (inquilino_id, mes, monto, fecha, estado)
    )
    conn.commit()
    conn.close()

def obtener_pagos(inquilino_id):
    conn = get_db_connection()
    pagos = conn.execute(
        'SELECT * FROM pagos WHERE inquilino_id=? ORDER BY mes DESC',
        (inquilino_id,)
    ).fetchall()
    conn.close()
    return pagos

def actualizar_pago(pago_id, mes, monto, estado):
    conn = get_db_connection()
    conn.execute(
        'UPDATE pagos SET mes=?, monto=?, estado=? WHERE id=?',
        (mes, monto, estado, pago_id)
    )
    conn.commit()
    conn.close()

def eliminar_pago(pago_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM pagos WHERE id=?', (pago_id,))
    conn.commit()
    conn.close()

# Interfaz de usuario
def mostrar_formulario_inquilino():
    with st.expander("➕ Agregar Nuevo Inquilino", expanded=False):
        with st.form(key='form_inquilino', clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                local = st.text_input("Local*")
                inquilino = st.text_input("Inquilino*")
            with col2:
                ramo = st.text_input("Ramo del Negocio")
                canon = st.number_input("Canon Actual*", min_value=0.0, step=1.0)
            contrato = st.text_input("Contrato")
            
            if st.form_submit_button("Guardar Inquilino"):
                if local and inquilino and canon:
                    if agregar_inquilino(local, inquilino, ramo, canon, contrato):
                        st.success("Inquilino agregado exitosamente!")
                        st.experimental_rerun()
                else:
                    st.error("Los campos marcados con * son obligatorios")

def mostrar_busqueda_inquilinos():
    st.subheader("🔍 Buscar Inquilinos")
    termino = st.text_input("Buscar por local o nombre de inquilino")
    
    if termino:
        resultados = buscar_inquilinos(termino)
    else:
        resultados = obtener_inquilinos()
    
    if resultados:
        df = pd.DataFrame(resultados)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Selección para edición
        inquilinos_lista = [f"{row['local']} - {row['inquilino']}" for row in resultados]
        seleccionado = st.selectbox("Seleccionar inquilino para editar/eliminar", [""] + inquilinos_lista)
        
        if seleccionado:
            id_inquilino = resultados[inquilinos_lista.index(seleccionado)]['id']
            mostrar_edicion_inquilino(id_inquilino)
    else:
        st.info("No se encontraron inquilinos")

def mostrar_edicion_inquilino(id_inquilino):
    conn = get_db_connection()
    inquilino = conn.execute('SELECT * FROM inquilinos WHERE id=?', (id_inquilino,)).fetchone()
    conn.close()
    
    with st.expander(f"✏️ Editar Inquilino: {inquilino['inquilino']}", expanded=True):
        with st.form(key='form_editar_inquilino'):
            col1, col2 = st.columns(2)
            with col1:
                local = st.text_input("Local*", value=inquilino['local'])
                inquilino_nombre = st.text_input("Inquilino*", value=inquilino['inquilino'])
            with col2:
                ramo = st.text_input("Ramo del Negocio", value=inquilino['ramo_negocio'])
                canon = st.number_input("Canon Actual*", min_value=0.0, step=1.0, value=float(inquilino['canon_actual']))
            contrato = st.text_input("Contrato", value=inquilino['contrato'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.form_submit_button("💾 Actualizar Datos"):
                    actualizar_inquilino(id_inquilino, local, inquilino_nombre, ramo, canon, contrato)
                    st.success("Datos actualizados!")
                    st.experimental_rerun()
            with col2:
                if st.button("🗑️ Eliminar Inquilino"):
                    eliminar_inquilino(id_inquilino)
                    st.success("Inquilino eliminado!")
                    st.experimental_rerun()
            with col3:
                if st.button("📝 Registrar Pago"):
                    st.session_state['pago_inquilino_id'] = id_inquilino
                    st.session_state['mostrar_form_pago'] = True
                    st.experimental_rerun()

def mostrar_formulario_pago():
    if 'pago_inquilino_id' in st.session_state and st.session_state['mostrar_form_pago']:
        with st.expander("💰 Registrar Nuevo Pago", expanded=True):
            with st.form(key='form_pago'):
                mes = st.text_input("Mes (YYYY-MM)*", placeholder="2023-01")
                monto = st.number_input("Monto*", min_value=0.0, step=1.0)
                estado = st.selectbox("Estado*", ["Pagado", "Pendiente", "Parcial"])
                
                if st.form_submit_button("Guardar Pago"):
                    if mes and monto:
                        agregar_pago(st.session_state['pago_inquilino_id'], mes, monto, estado)
                        st.success("Pago registrado!")
                        st.session_state['mostrar_form_pago'] = False
                        st.experimental_rerun()
                    else:
                        st.error("Los campos marcados con * son obligatorios")
                
                if st.button("Cancelar"):
                    st.session_state['mostrar_form_pago'] = False
                    st.experimental_rerun()

def mostrar_historial_pagos():
    if 'pago_inquilino_id' in st.session_state:
        pagos = obtener_pagos(st.session_state['pago_inquilino_id'])
        
        if pagos:
            st.subheader("📜 Historial de Pagos")
            df = pd.DataFrame(pagos)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Opciones para cada pago
            pago_seleccionado = st.selectbox(
                "Seleccionar pago para editar/eliminar",
                [""] + [f"{pago['mes']} - ${pago['monto']} ({pago['estado']})" for pago in pagos]
            )
            
            if pago_seleccionado:
                pago_id = pagos[[f"{pago['mes']} - ${pago['monto']} ({pago['estado']})" for pago in pagos].index(pago_seleccionado)]['id']
                
                with st.expander("Editar/Eliminar Pago", expanded=True):
                    pago = [p for p in pagos if p['id'] == pago_id][0]
                    with st.form(key='form_editar_pago'):
                        mes = st.text_input("Mes", value=pago['mes'])
                        monto = st.number_input("Monto", value=float(pago['monto']))
                        estado = st.selectbox("Estado", ["Pagado", "Pendiente", "Parcial"], index=["Pagado", "Pendiente", "Parcial"].index(pago['estado']))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("Actualizar Pago"):
                                actualizar_pago(pago_id, mes, monto, estado)
                                st.success("Pago actualizado!")
                                st.experimental_rerun()
                        with col2:
                            if st.button("Eliminar Pago"):
                                eliminar_pago(pago_id)
                                st.success("Pago eliminado!")
                                st.experimental_rerun()
        else:
            st.info("No hay pagos registrados para este inquilino")

# Aplicación principal
def main():
    st.title("🏢 Sistema de Gestión de Pagos de Inquilinos")
    
    # Inicializar base de datos
    init_db()
    
    # Menú principal
    opcion = st.sidebar.radio(
        "Menú Principal",
        ["Gestión de Inquilinos", "Registro de Pagos"]
    )
    
    if opcion == "Gestión de Inquilinos":
        mostrar_formulario_inquilino()
        mostrar_busqueda_inquilinos()
    elif opcion == "Registro de Pagos":
        if 'pago_inquilino_id' in st.session_state:
            conn = get_db_connection()
            inquilino = conn.execute('SELECT * FROM inquilinos WHERE id=?', (st.session_state['pago_inquilino_id'],)).fetchone()
            conn.close()
            
            st.subheader(f"Pagos de: {inquilino['local']} - {inquilino['inquilino']}")
            mostrar_formulario_pago()
            mostrar_historial_pagos()
        else:
            st.info("Seleccione un inquilino desde la opción 'Gestión de Inquilinos' para registrar pagos")

if __name__ == "__main__":
    main()
