import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- INICIALIZACIÓN DE LA BASE DE DATOS CON DATOS PREDEFINIDOS --- #
def init_db():
    conn = sqlite3.connect('pagos.db')
    cursor = conn.cursor()
    
    # Crear tabla de pagos si no existe
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
            estado TEXT NOT NULL,
            observaciones TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Verificar si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM pagos")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Datos iniciales basados en el Excel que proporcionaste
        datos_iniciales = [
            ('LOCAL A', 'MONICA JANET VARGAS G.', 'PB', 'LENCERIA', 350.0, 'MONICA JANET VARGAS G.', None, None, 'Pendiente', ''),
            ('LOCAL B', 'OSCAR DUQUE ECHEVERRIA', 'PB', 'LENCERIA', 350.0, 'OSCAR DUQUE ECHEVERRI', None, None, 'Pendiente', ''),
            ('LOCAL 1', 'JOSE MANUEL ANDRADE PEREIRA', 'PB', 'MANUFACTURA', 70.0, 'JOSE M. ANDRADE PEREIRA', None, None, 'Pendiente', ''),
            ('LOCAL 2', 'JOSE MANUEL ANDRADE PEREIRA', 'PB', 'MANUFACTURA', 70.0, 'JOSE M. ANDRADE PEREIRA', None, None, 'Pendiente', ''),
            ('LOCAL 3', 'JOSE MANUEL ANDRADE PEREIRA', 'PB', 'MANUFACTURA', 70.0, 'JOSE M. ANDRADE PEREIRA', None, None, 'Pendiente', ''),
            ('LOCAL 4', 'JOSE R. RODRIGUEZ V.', 'PB', 'DOMESA', 33.33, 'YORMAN JOSE VALERA', None, None, 'Pendiente', ''),
            ('LOCAL 5', 'JOSE R. RODRIGUEZ V.', 'PB', 'DOMESA', 33.33, 'YORMAN JOSE VALERA', None, None, 'Pendiente', ''),
            ('LOCAL 5A', 'JOSE R. RODRIGUEZ V.', 'PB', 'DOMESA', 33.33, 'YORMAN JOSE VALERA', None, None, 'Pendiente', ''),
            ('LOCAL 6', 'Daniel', 'PB', 'Compra/Venta Oro', 50.0, 'DANNYS JOSE GARCIA', None, None, 'Pendiente', ''),
            ('LOCAL 7', 'YAMILETH JOSEFINA CHACON', 'PB', 'SANTERIA', 70.0, 'YAMILET JOSEFINA CHACON', None, None, 'Pendiente', ''),
            ('LOCAL 8', 'JOSE ANTONIO SPANO', 'PB', 'ODONTOLOGIA', 50.0, 'JOSE ANTONIO SPANO', None, None, 'Pendiente', ''),
            ('LOCAL 9', 'JOSE ANTONIO SPANO', 'PB', 'ODONTOLOGIA', 50.0, 'JOSE ANTONIO SPANO', None, None, 'Pendiente', ''),
            ('LOCAL 10', 'YANIRE NAVARRO VIVES', 'PB', 'ARTESANIA', 150.0, 'YANIRE NAVARRO VIDES', None, None, 'Pendiente', ''),
            ('LOCAL 11 A', 'IVAN SILVA', 'PB', 'ROPA', 80.0, 'ARENAS DEL NILO C.A', None, None, 'Pendiente', ''),
            ('LOCAL 11', 'MARTIN SANTOS', 'PB', 'NO SE', 60.0, 'MARTIN SANTOS', None, None, 'Pendiente', ''),
            ('LOCAL 12', 'MARTIN SANTOS', 'PB', 'NO SE', 60.0, 'MARTIN SANTOS', None, None, 'Pendiente', ''),
            ('LOCAL 13', 'ESPERANZA RUEDA', 'PB', 'ROPA', 70.0, 'ESPERANZA RUEDA', None, None, 'Pendiente', ''),
            ('LOCAL 14', 'SUSANA DO LIVRAMENTO', 'PB', 'PERFUMES', 70.0, 'SUSANA DO LIVRAMENTO', None, None, 'Pendiente', ''),
            ('LOCAL 15', 'JUAN ANTONIO RODRIGUEZ', 'PB', 'OPTICA', 70.0, 'JUAN ANTONIO RODRÍGUEZ', None, None, 'Pendiente', ''),
            ('LOCAL 16', 'MARYABETH TOVAR Y ALDO M.', 'PB', 'CYBER', 70.0, 'YULIANA SINDY POVES VALLADARES', None, None, 'Pendiente', ''),
            ('LOCAL 17', 'YANIRE NAVARRO VIVES', 'PB', 'ARTESANIA', 37.5, 'YANIRE NAVARRO VIDES', None, None, 'Pendiente', ''),
            ('LOCAL 18', 'YANIRE NAVARRO VIVES', 'PB', 'ARTESANIA', 37.5, 'YANIRE NAVARRO VIDES', None, None, 'Pendiente', ''),
            ('LOCAL 19', 'YANIRE NAVARRO VIVES', 'PB', 'ARTESANIA', 37.5, 'YANIRE NAVARRO VIDES', None, None, 'Pendiente', ''),
            ('MEZZANINA 1', 'OSCAR DUQUE', 'MEZZANINA 1', '', 100.0, 'OSCAR DUQUE ECHEVERRI', None, None, 'Pendiente', ''),
            ('LOCAL 27', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 25.0, 'CARLOS Y ELVIS MIÑANO', None, None, 'Pendiente', ''),
            ('LOCAL 28', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 25.0, 'CARLOS Y ELVIS MIÑANO', None, None, 'Pendiente', ''),
            ('LOCAL 29', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 25.0, 'CARLOS Y ELVIS MIÑANO', None, None, 'Pendiente', ''),
            ('LOCAL 30', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 25.0, 'CARLOS Y ELVIS MIÑANO', None, None, 'Pendiente', ''),
            ('LOCAL 34', 'JACQUELINE QUINTANA', 'MEZZANINA 1', '', 60.0, 'JACQUELINE QUINTANA', None, None, 'Pendiente', ''),
            ('LOCAL 35', 'JACQUELINE QUINTANA', 'MEZZANINA 1', '', 60.0, 'JACQUELINE QUINTANA', None, None, 'Pendiente', ''),
            ('MEZZANINA 2', 'CARLOS GOMEZ ZULOAGA', 'MEZZANINA 1', '', 120.0, 'CARLOS MARIO GOMEZ', None, None, 'Pendiente', ''),
            ('LOCAL 40', 'JHON SERNA GOMEZ', 'MEZZANINA 1', '', 120.0, 'JHON SERNA GOMEZ', None, None, 'Pendiente', ''),
            ('LOCAL 42', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 16.67, 'GERARDO MIÑANO TRUJILLO', None, None, 'Pendiente', ''),
            ('LOCAL 43', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 16.67, 'GERARDO MIÑANO TRUJILLO', None, None, 'Pendiente', ''),
            ('LOCAL 44', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 16.67, 'GERARDO MIÑANO TRUJILLO', None, None, 'Pendiente', ''),
            ('LOCAL 45', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 16.67, 'GERARDO MIÑANO TRUJILLO', None, None, 'Pendiente', ''),
            ('LOCAL 46', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 16.67, 'GERARDO MIÑANO TRUJILLO', None, None, 'Pendiente', ''),
            ('LOCAL 47', 'CARLOS Y ELIS MIÑANO', 'MEZZANINA 1', '', 16.67, 'GERARDO MIÑANO TRUJILLO', None, None, 'Pendiente', ''),
            ('LOCAL 31', 'ALDO MUÑOZ Y JARRISON HEVER', 'MEZZANINA 1', 'SUSHI', 50.0, 'ALDO MUÑOZ y JARRISON HEVER', None, None, 'Pendiente', ''),
            ('LOCAL 32', 'ALDO MUÑOZ Y JARRISON HEVER', 'MEZZANINA 1', 'SUSHI', 50.0, 'ALDO MUÑOZ y JARRISON HEVER', None, None, 'Pendiente', ''),
            ('LOCAL S/N', 'SALVADOR FREITAS NUNES', 'MEZZANINA 1', 'RESTAURANT', 200.0, 'SALVADOR FREITAS NUNES', None, None, 'Pendiente', ''),
            ('LOCAL 2-4', 'AURA MARINA', 'MEZZANINA 1', 'TELAS', 50.0, 'AURA MARINA MONTILLA', None, None, 'Pendiente', ''),
            ('LOCAL 2-5', 'AURA MARINA', 'MEZZANINA 1', 'TELAS', 50.0, 'AURA MARINA MONTILLA', None, None, 'Pendiente', ''),
            ('LOCAL 2-2', 'ESPERANZA RUEDA', 'MEZZANINA 2', '', 23.33, 'FEDERICK JACOB OVALLES', None, None, 'Pendiente', ''),
            ('LOCAL 2-3', 'ESPERANZA RUEDA', 'MEZZANINA 2', '', 23.33, 'FEDERICK JACOB OVALLES', None, None, 'Pendiente', ''),
            ('LOCAL 2 -3', 'DESOCUPADO', 'MEZZANINA 2', '', 23.33, 'FEDERICK JACOB OVALLES', None, None, 'Pendiente', ''),
            ('LOCAL 2 -7', 'DESOCUPADO', 'MEZZANINA 2', '', 23.33, 'Martin Santos', None, None, 'Pendiente', ''),
            ('LOCAL 2-4', 'JOSE ANTONIO DO FAIAL', 'MEZZANINA 2', 'ACRILICOS', 60.0, 'JOSE ANTONIO FAIAL PESTAÑA', None, None, 'Pendiente', ''),
            ('LOCAL 2-5', 'JOSE ANTONIO DO FAIAL', 'MEZZANINA 2', 'ACRILICOS', 60.0, 'JOSE ANTONIO FAIAL PESTAÑA', None, None, 'Pendiente', ''),
            ('LOCAL 34', 'ELY SAUL QUINTERO CUELLAE', 'MEZZANINA 2', '', 16.67, 'ELY SAUL QUINTERO CUELLAR', None, None, 'Pendiente', ''),
            ('LOCAL 35', 'ELY SAUL QUINTERO CUELLAE', 'MEZZANINA 2', '', 16.67, 'ELY SAUL QUINTERO CUELLAR', None, None, 'Pendiente', ''),
            ('LOCAL 36', 'ELY SAUL QUINTERO CUELLAE', 'MEZZANINA 2', '', 16.67, 'ELY SAUL QUINTERO CUELLAR', None, None, 'Pendiente', ''),
            ('LOCAL 37', 'ELY SAUL QUINTERO CUELLAE', 'MEZZANINA 2', '', 16.67, 'ELY SAUL QUINTERO CUELLAR', None, None, 'Pendiente', ''),
            ('LOCAL 38', 'ELY SAUL QUINTERO CUELLAE', 'MEZZANINA 2', '', 16.67, 'ELY SAUL QUINTERO CUELLAR', None, None, 'Pendiente', ''),
            ('LOCAL 39', 'ELY SAUL QUINTERO CUELLAE', 'MEZZANINA 2', '', 16.67, 'ELY SAUL QUINTERO CUELLAR', None, None, 'Pendiente', '')
        ]
        
        # Insertar datos iniciales
        cursor.executemany('''
            INSERT INTO pagos (numero_local, inquilino, planta, ramo_negocio, canon, contrato, fecha_pago, mes_abonado, estado, observaciones)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', datos_iniciales)
        conn.commit()
    
    conn.close()

# --- FUNCIONES PARA OBTENER DATOS --- #
def obtener_locales():
    """Obtiene la lista de locales únicos."""
    conn = sqlite3.connect('pagos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT numero_local FROM pagos ORDER BY numero_local")
    locales = [row[0] for row in cursor.fetchall()]
    conn.close()
    return locales

def obtener_inquilinos():
    """Obtiene la lista de inquilinos únicos."""
    conn = sqlite3.connect('pagos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT inquilino FROM pagos ORDER BY inquilino")
    inquilinos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return inquilinos

def obtener_info_local(numero_local):
    """Obtiene información específica de un local."""
    conn = sqlite3.connect('pagos.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT planta, ramo_negocio, canon, contrato 
        FROM pagos 
        WHERE numero_local = ? 
        LIMIT 1
    ''', (numero_local,))
    info = cursor.fetchone()
    conn.close()
    return info if info else (None, None, None, None)

# --- FUNCIONES PARA REGISTRAR PAGOS --- #
def registrar_pago(numero_local, inquilino, fecha_pago, mes_abonado, monto, estado, observaciones):
    """Registra un nuevo pago en la base de datos."""
    conn = sqlite3.connect('pagos.db')
    cursor = conn.cursor()
    
    # Actualizar el registro existente o insertar uno nuevo
    cursor.execute('''
        UPDATE pagos 
        SET fecha_pago = ?, mes_abonado = ?, estado = ?, observaciones = ?
        WHERE numero_local = ? AND inquilino = ? AND estado = 'Pendiente'
    ''', (fecha_pago, mes_abonado, estado, observaciones, numero_local, inquilino))
    
    if cursor.rowcount == 0:
        # Si no había registro pendiente, insertamos uno nuevo
        planta, ramo_negocio, canon, contrato = obtener_info_local(numero_local)
        cursor.execute('''
            INSERT INTO pagos (
                numero_local, inquilino, planta, ramo_negocio, canon, contrato, 
                fecha_pago, mes_abonado, estado, observaciones
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (numero_local, inquilino, planta, ramo_negocio, canon, contrato, 
              fecha_pago, mes_abonado, estado, observaciones))
    
    conn.commit()
    conn.close()

# --- INTERFAZ DE STREAMLIT --- #
def main():
    st.set_page_config(page_title="Dashboard de Pagos", layout="wide")
    st.title("📊 Dashboard de Pagos de Cánones Comerciales")
    st.markdown("---")
    
    # Inicializar la base de datos
    init_db()
    
    # Obtener listas para los selectbox
    locales = obtener_locales()
    inquilinos = obtener_inquilinos()
    
    # Menú lateral
    menu = st.sidebar.selectbox(
        "Menú Principal",
        ["Registrar Pago", "Consultar Morosidad", "Historial de Pagos"]
    )
    
    if menu == "Registrar Pago":
        st.subheader("Registrar Nuevo Pago")
        
        with st.form("form_pago", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                # Selector de local
                local_seleccionado = st.selectbox(
                    "Número de Local*",
                    options=locales,
                    index=0
                )
                
                # Obtener información del local seleccionado
                planta, ramo_negocio, canon, contrato = obtener_info_local(local_seleccionado)
                
                # Mostrar información del local
                st.text(f"Planta: {planta}")
                st.text(f"Ramo del negocio: {ramo_negocio}")
                st.text(f"Canon: ${canon}")
                st.text(f"Contrato: {contrato}")
                
            with col2:
                # Selector de inquilino (filtrado por local)
                inquilinos_local = [inquilino for inquilino in inquilinos 
                                   if any(local_seleccionado in loc for loc in locales)]
                inquilino_seleccionado = st.selectbox(
                    "Inquilino*",
                    options=inquilinos_local,
                    index=0
                )
                
                fecha_pago = st.date_input("Fecha de Pago*", datetime.now())
                mes_abonado = st.text_input("Mes Abonado* (YYYY-MM)", placeholder="2025-06")
                monto = st.number_input("Monto*", min_value=0.0, value=float(canon) if canon else 0.0)
                estado = st.selectbox("Estado*", ["Pagado", "Parcial"])
                observaciones = st.text_area("Observaciones")
            
            submit = st.form_submit_button("Registrar Pago")
            
            if submit:
                if not all([local_seleccionado, inquilino_seleccionado, mes_abonado, monto]):
                    st.error("Por favor complete los campos obligatorios (*)")
                else:
                    registrar_pago(
                        local_seleccionado, inquilino_seleccionado, fecha_pago,
                        mes_abonado, monto, estado, observaciones
                    )
                    st.success("¡Pago registrado exitosamente!")
    
    elif menu == "Consultar Morosidad":
        st.subheader("Inquilinos Morosos")
        
        conn = sqlite3.connect('pagos.db')
        query = '''
            SELECT numero_local, inquilino, canon, MAX(mes_abonado) as ultimo_mes
            FROM pagos
            WHERE estado = 'Pendiente' OR fecha_pago IS NULL
            GROUP BY numero_local, inquilino, canon
            ORDER BY numero_local
        '''
        df_morosos = pd.read_sql(query, conn)
        conn.close()
        
        if not df_morosos.empty:
            st.dataframe(df_morosos, use_container_width=True)
            
            # Calcular deuda total
            deuda_total = df_morosos['canon'].sum()
            st.metric("Deuda Total Pendiente", f"${deuda_total:,.2f}")
            
            # Opción para descargar
            st.download_button(
                "Descargar Reporte de Morosidad",
                df_morosos.to_csv(index=False),
                "reporte_morosidad.csv",
                "text/csv"
            )
        else:
            st.success("¡No hay morosidad registrada!")
    
    elif menu == "Historial de Pagos":
        st.subheader("Historial de Pagos")
        
        conn = sqlite3.connect('pagos.db')
        query = '''
            SELECT numero_local, inquilino, fecha_pago, mes_abonado, monto, estado
            FROM pagos
            WHERE estado = 'Pagado' OR estado = 'Parcial'
            ORDER BY fecha_pago DESC
        '''
        df_historial = pd.read_sql(query, conn)
        conn.close()
        
        if not df_historial.empty:
            st.dataframe(df_historial, use_container_width=True)
            
            # Opción para descargar
            st.download_button(
                "Descargar Historial Completo",
                df_historial.to_csv(index=False),
                "historial_pagos.csv",
                "text/csv"
            )
        else:
            st.info("No hay pagos registrados aún.")

if __name__ == "__main__":
    main()
