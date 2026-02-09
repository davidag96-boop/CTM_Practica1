import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Function to handle decimal separators
def convert_to_float(value):
    if isinstance(value, str):
        value = value.replace(',', '.')
    return float(value)

# Function to calculate Young's modulus, yield strength, tensile strength, and elongation
def calculate_material_properties(data):
    # Placeholder calculations based on the data
    young_modulus = np.mean(data['stress']) / np.mean(data['strain'])  # Dummy calculation
    yield_strength = young_modulus * 0.002  # Dummy yield strength
    tensile_strength = max(data['stress'])  # Maximum stress
    elongation = (data['final_length'] - data['original_length']) / data['original_length'] * 100
    return young_modulus, yield_strength, tensile_strength, elongation

# Streamlit Layout
st.title("Tensile Testing Application")

# Input Methods
input_method = st.selectbox("Choose input method:", ["Manual Input", "Excel Upload", "Demo Mode"])

if input_method == "Manual Input":
    original_length = st.number_input("Original Length (mm):")
    final_length = st.number_input("Final Length (mm):")
    stress = st.text_area("Stress (MPa) - comma-separated:").split(',')
    strain = st.text_area("Strain - comma-separated:").split(',')
    stress = [convert_to_float(s) for s in stress]
    strain = [convert_to_float(s) for s in strain]
    data = pd.DataFrame({'stress': stress, 'strain': strain, 'final_length': [final_length], 'original_length': [original_length]})

elif input_method == "Excel Upload":
    uploaded_file = st.file_uploader("Upload Excel file", type=['xls', 'xlsx'])
    if uploaded_file:
        data = pd.read_excel(uploaded_file)
        # Assuming Excel has appropriate columns named 'stress', 'strain', 'original_length', and 'final_length'

elif input_method == "Demo Mode":
    data = pd.DataFrame({
        'stress': np.random.normal(loc=250, scale=50, size=100),
        'strain': np.linspace(0, 0.1, num=100),
        'final_length': [100],
        'original_length': [100]
    })

# Data Processing
if 'data' in locals():
    young_modulus, yield_strength, tensile_strength, elongation = calculate_material_properties(data)
    st.write(f"Young's Modulus: {young_modulus}")
    st.write(f"Yield Strength: {yield_strength}")
    st.write(f"Tensile Strength: {tensile_strength}")
    st.write(f"Elongation at Break: {elongation}%")

    # Interactive Plotly Visualization
    fig = px.line(data, x='strain', y='stress', title="Stress-Strain Curve")
    st.plotly_chart(fig)

    # PDF Export
    if st.button("Export to PDF"):
        # Placeholder for PDF export logic
        st.write("Export functionality to be implemented.")

# Styling
st.markdown("<style>div.stButton > button {background-color: #4CAF50; color: white;}</style>", unsafe_allow_html=True)