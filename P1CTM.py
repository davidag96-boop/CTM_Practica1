import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Configuración de la página
st.set_page_config(page_title="Analizador de Tracción - EEAE UVigo", layout="wide")

st.title("🚀 Analizador de Ensayos de Tracción Aeroespacial")
st.write("### Escuela de Ingeniería Aeroespacial | Universidade de Vigo")

# --- SIDEBAR: DATOS DE LA PROBETA ---
with st.sidebar:
    st.header("Configuración de la Probeta")
    st.write("Introduce los datos de la ficha CTM:")
    
    geometria = st.selectbox("Tipo de Probeta", ["Cilíndrica", "Plana"])
    if geometria == "Cilíndrica":
        d0 = st.number_input("Diámetro inicial d₀ (mm)", value=10.0, format="%.2f")
        s0 = np.pi * (d0**2) / 4
    else:
        ancho = st.number_input("Ancho b₀ (mm)", value=10.0)
        espesor = st.number_input("Espesor a₀ (mm)", value=2.0)
        s0 = ancho * espesor
        
    l0 = st.number_input("Longitud inicial L₀ (mm)", value=50.0, format="%.2f")
    lu = st.number_input("Longitud final tras rotura Lᵤ (mm)", value=55.0, format="%.2f")
    su = st.number_input("Sección final tras rotura Sᵤ (mm²)", value=s0*0.8, format="%.2f")

    st.divider()
    st.info(f"**Sección Inicial calculada S₀:** {s0:.2f} mm²")

# --- CARGA Y LIMPIEZA ROBUSTA DE DATOS ---
st.write("### 1. Carga de Datos")
uploaded_file = st.file_uploader("Sube tu archivo CSV (PLA_1H3, 7075_ejemplo, etc.)", type=["csv"])

if uploaded_file:
    try:
        # Leemos el archivo saltando la primera fila de metadatos
        # Usamos decimal=',' porque los archivos de Vigo usan coma para decimales
        df = pd.read_csv(uploaded_file, header=1, decimal=',', skipinitialspace=True)
        
        # LIMPIEZA: Los nombres de columnas a veces vienen con comillas extra
        # Forzamos los nombres por posición para evitar KeyErrors
        # Posición 0: Tiempo, 1: Fuerza, 2: Desplazamiento
        df.columns = ['Tiempo', 'Fuerza', 'Desplazamiento']
        
        # ELIMINAR FILA DE UNIDADES: La fila que dice "seg", "N", "mm"
        # Intentamos convertir la primera fila de datos a número; si falla, la borramos
        if pd.to_numeric(df.iloc[0, 1], errors='coerce') is np.nan:
            df = df.iloc[1:].reset_index(drop=True)
        
        # Convertir todo a numérico (por si quedaron strings)
        df = df.apply(pd.to_numeric, errors='coerce').dropna()
        
        st.success("✅ Archivo procesado correctamente.")
        
        # --- CÁLCULOS SEGÚN FICHA CTM ---
        # Tensión (sigma) = F / S0
        df['Tension_MPa'] = df['Fuerza'] / s0
        # Deformación (epsilon) = Delta_L / L0
        df['Deformacion_unit'] = df['Desplazamiento'] / l0
        
        # 1. Resistencia a la tracción (Rm)
        rm = df['Tension_MPa'].max()
        idx_max = df['Tension_MPa'].idxmax()
        
        # 2. Módulo de Young (E)
        # Regresión lineal en el primer 10% de la curva (zona elástica)
        rango_e = df.iloc[:int(len(df)*0.1)]
        slope, intercept, r_value, p_value, std_err = stats.linregress(rango_e['Deformacion_unit'], rango_e['Tension_MPa'])
        e_young = slope # MPa
        
        # 3. Alargamiento a rotura (A%) y Estricción (Z%)
        a_porc = ((lu - l0) / l0) * 100
        z_porc = ((s0 - su) / s0) * 100

        # --- VISUALIZACIÓN ---
        st.subheader("2. Gráfica de Ensayo")
        
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df['Deformacion_unit'], df['Tension_MPa'], label='Curva de Tracción', color='#004b87', lw=2)
        
        # Marcar Rm
        ax.scatter(df['Deformacion_unit'].iloc[idx_max], rm, color='red', label=f'Rm = {rm:.1f} MPa')
        
        ax.set_xlabel("Deformación Unitaria ε (mm/mm)")
        ax.set_ylabel("Tensión σ (MPa)")
        ax.set_title("Diagrama Tensión-Deformación")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)

        # --- RESULTADOS FINALES ---
        st.subheader("3. Resultados del Informe")
        col_res1, col_res2, col_res3 = st.columns(3)
        
        col_res1.metric("Resistencia Rm", f"{rm:.1f} MPa")
        col_res2.metric("Módulo Young E", f"{e_young/1000:.1f} GPa")
        col_res3.metric("Alargamiento A", f"{a_porc:.1f} %")
        
        st.write(f"**Estricción (Z):** {z_porc:.1f} %")
        
        # Mostrar tabla de datos limpia
        with st.expander("Ver tabla de datos procesados"):
            st.dataframe(df.head(20))

    except Exception as e:
        st.error(f"❌ Error al leer el archivo: {e}")
        st.info("Asegúrate de que el CSV tiene el formato exportado por la máquina (Tiempo, Fuerza, Desplazamiento).")
