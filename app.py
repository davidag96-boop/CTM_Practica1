import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from fpdf import FPDF
import numpy as np

# Function to calculate material properties

def calculate_material_properties(data):
    # Calculate Young's modulus, Rp0.2, tensile strength, elongation
    # Placeholder calculations
    youngs_modulus = np.mean(data['stress']) / np.mean(data['strain'])
    Rp0_2 = 0.2 * youngs_modulus
    tensile_strength = np.max(data['stress'])
    elongation = (data['length'].iloc[-1] - data['length'].iloc[0]) / data['length'].iloc[0] * 100
    return youngs_modulus, Rp0_2, tensile_strength, elongation

# Function to generate PDF report

def generate_pdf_report(properties):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(40, 10, 'Material Properties Report')
    pdf.set_font("Arial", size=12)
    for prop, value in properties.items():
        pdf.cell(0, 10, f'{prop}: {value}', ln=True)
    buf = BytesIO()
    pdf.output(buf)
    return buf.getvalue()

# Streamlit app

def main():
    st.title('Material Properties Calculator')
    data = None

    # File upload
    uploaded_file = st.file_uploader('Upload your Excel file', type=['xlsx'])
    if uploaded_file:
        data = pd.read_excel(uploaded_file)
        st.write(data)
    else:
        # Manual input
        st.warning('Please upload a file or enter data manually.')

    if data is not None:
        # Calculate properties
        properties = calculate_material_properties(data)
        st.write('Calculations complete. Metrics:')
        st.write(f'Young\'s Modulus: {properties[0]}')
        st.write(f'Rp0.2: {properties[1]}')
        st.write(f'Tensile Strength: {properties[2]}')
        st.write(f'Elongation: {properties[3]}')

        # Interactive Plotly visualization
        fig = px.line(data, x='strain', y='stress', title='Stress-Strain Curve')
        st.plotly_chart(fig)

        # PDF report generation
        if st.button('Generate PDF Report'):
            pdf_bytes = generate_pdf_report({
                'Young\'s Modulus': properties[0],
                'Rp0.2': properties[1],
                'Tensile Strength': properties[2],
                'Elongation': properties[3]
            })
            st.download_button('Download PDF Report', pdf_bytes, 'report.pdf', 'application/pdf')

if __name__ == '__main__':
    main()