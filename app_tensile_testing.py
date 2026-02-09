import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import scipy
from fpdf import FPDF

# Function to handle decimal separators
def convert_decimal(value):
    if isinstance(value, str):
        value = value.replace(',', '.')  # Replace comma with point
    return float(value)

# Young's Modulus Calculation
def calculate_youngs_modulus(stress, strain):
    try:
        # slope of the linear portion of the stress-strain curve
        E, _ = np.polyfit(strain, stress, 1)
        return E
    except Exception as e:
        st.error(f"Error calculating Young's modulus: {e}")

# Rp0.2 Offset Method Implementation
def calculate_rp02_offset(stress, strain):
    try:
        # Find the intersection for the Rp0.2
        return np.interp(0.002, strain, stress)
    except Exception as e:
        st.error(f"Error calculating Rp0.2: {e}")

# Identify Tensile Strength
def identify_tensile_strength(stress):
    try:
        return np.max(stress)
    except Exception as e:
        st.error(f"Error identifying tensile strength: {e}")

# Calculate Elongation at Break
def calculate_elongation_at_break(original_length, final_length):
    try:
        return (final_length - original_length) / original_length * 100
    except Exception as e:
        st.error(f"Error calculating elongation: {e}")

# Generate interactive Plotly visualizations
def plot_interactive(stress, strain):
    fig = px.line(x=strain, y=stress, labels={'x':'Strain','y':'Stress'}, title='Stress-Strain Curve')
    st.plotly_chart(fig)

# Matplotlib Stress-Strain Curves
def plot_stress_strain_curve(stress, strain):
    plt.plot(strain, stress, label='Stress-Strain Curve')
    plt.xlabel('Strain')
    plt.ylabel('Stress')
    plt.axhline(y=identify_tensile_strength(stress), color='r', linestyle='--', label='Tensile Strength')
    plt.title('Stress-Strain Curve with Critical Points')
    plt.legend()
    st.pyplot()  

# PDF Export of Results
def export_pdf(results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(40, 10, 'Test Results')
    pdf.ln(10)
    for key, value in results.items():
        pdf.cell(0, 10, f'{key}: {value}', ln=True)
    pdf.output('test_results.pdf')

# Main Streamlit Function
def main():
    st.title('Tensile Testing Application')
    st.sidebar.header('Specimen Dimensions')
    original_length = st.sidebar.number_input('Original Length (mm)', min_value=0.0, format='%.2f')
    final_length = st.sidebar.number_input('Final Length (mm)', min_value=0.0, format='%.2f')
    # Input data
    stress_input = st.text_area('Enter Stress Values (comma or point separated, new line for each):')
    strain_input = st.text_area('Enter Strain Values (comma or point separated, new line for each):')
    
    if st.button('Calculate'):  
        try:
            stress_values = [convert_decimal(x) for x in stress_input.split()]  # Adjusted handling
            strain_values = [convert_decimal(x) for x in strain_input.split()]
            # Calculations
            youngs_modulus = calculate_youngs_modulus(stress_values, strain_values)
            rp02 = calculate_rp02_offset(stress_values, strain_values)
            tensile_strength = identify_tensile_strength(stress_values)
            elongation = calculate_elongation_at_break(original_length, final_length)  
            results = {
                'Youngs Modulus (E)': youngs_modulus,
                'Rp0.2': rp02,
                'Tensile Strength': tensile_strength,
                'Elongation at Break (%)': elongation
            }
            st.write(results)
            export_pdf(results)
            plot_interactive(stress_values, strain_values)
            plot_stress_strain_curve(stress_values, strain_values)
        except ValueError:
            st.error("Please enter valid numerical values for stress and strain.")

if __name__ == '__main__':
    main()