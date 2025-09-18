
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import json
import os

# Set page configuration
st.set_page_config(page_title="Diagnóstico de Desnutrición Crónica Infantil", layout="wide")

# API Key de OpenAI desde secretos de Streamlit
api_key = os.getenv("OPENAI_API_KEY")

def classify_dci(age_months, height_cm):
    """
    Clasifica el riesgo de desnutrición crónica infantil (DCI)
    basado en un modelo simplificado de talla para la edad.
    
    NOTA: Para un uso real, se necesitarían las tablas de la OMS y un cálculo preciso del Z-score.
    Este es un modelo de reglas simplificado para el proyecto.
    """
    
    # Datos de referencia simplificados (basados en promedios de la OMS para niños)
    # Talla promedio para la edad
    if age_months <= 24:
        expected_height = 49.9 + (age_months * 2.5)  # Aprox. 2.5 cm/mes
    else:
        expected_height = 90 + ((age_months - 24) * 0.7) # Aprox. 0.7 cm/mes después de 2 años

    # Umbral simplificado: 90% de la talla esperada. Un umbral más preciso sería un Z-score < -2.
    if height_cm < (expected_height * 0.9):
        return "Riesgo de Desnutrición Crónica"
    else:
        return "Normal"

def get_recommendations_from_openai(age_months, weight_kg, height_cm, dci_status):
    """
    Envía los datos a la API de OpenAI para generar recomendaciones personalizadas.
    """
    if not api_key:
        st.error("Error: La clave de la API de OpenAI no está configurada. Por favor, configura la variable de entorno 'OPENAI_API_KEY'.")
        return None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt = (
        f"Un niño de {age_months} meses de edad, que pesa {weight_kg} kg y mide {height_cm} cm, "
        f"ha sido clasificado con un estado de salud de '{dci_status}'. "
        f"Basado en esta información y en los estándares nutricionales para niños de esta edad, "
        "por favor, genera una guía práctica y personalizada de alimentación que incluya recomendaciones de alimentos, "
        "frecuencias y porciones, adaptadas al contexto de una comunidad rural en Ecuador, con énfasis en alimentos locales."
    )

    data = {
        "model": "gpt-4o",  # Usamos el modelo más reciente y capaz
        "messages": [
            {"role": "system", "content": "Eres un experto en nutrición infantil que provee recomendaciones prácticas."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()  # Lanza una excepción para errores HTTP
        recommendation_text = response.json()["choices"][0]["message"]["content"]
        return recommendation_text
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con la API de OpenAI: {e}")
        return None
    except KeyError:
        st.error("Error al procesar la respuesta de la API. El formato no es el esperado.")
        return None

# --- Interfaz de la aplicación Streamlit ---

st.title("Proyecto Final: Diagnóstico de Desnutrición Crónica Infantil")
st.markdown("---")

st.header("1. Ingreso de Parámetros")

with st.form("input_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age_months = st.number_input("Edad del niño (meses)", min_value=1, max_value=60, step=1, value=24)
    with col2:
        weight_kg = st.number_input("Peso (kg)", min_value=1.0, max_value=50.0, step=0.1, value=10.0)
    with col3:
        height_cm = st.number_input("Estatura (cm)", min_value=30.0, max_value=150.0, step=0.1, value=85.0)

    submitted = st.form_submit_button("Analizar")

st.markdown("---")

if submitted:
    st.header("2. Resultados del Análisis")
    
    # 1. Clasificación
    dci_status = classify_dci(age_months, height_cm)
    st.write(f"### Estado de Salud Detectado: **{dci_status}**")
    
    # 2. Gráfico comparativo
    st.subheader("Gráfico Comparativo: Estatura vs. Estándares de Referencia")
    
    # Datos para el gráfico (curvas de referencia de la OMS para el Z-score 0, -2 y +2)
    # Nota: Estos son datos de ejemplo, para un proyecto real se usarían los datos oficiales.
    months = np.arange(1, 61)
    height_normal = 49.9 + (months * 2.5)  # Simplified normal growth curve
    height_dci_threshold = height_normal * 0.9 # Simplified DCI threshold
    
    data = {
        'Edad (meses)': months,
        'Estatura Normal (cm)': height_normal,
        'Umbral DCI (cm)': height_dci_threshold
    }
    df = pd.DataFrame(data)
    
    fig = px.line(df, x='Edad (meses)', y=['Estatura Normal (cm)', 'Umbral DCI (cm)'],
                  labels={'value': 'Estatura (cm)', 'variable': 'Curva de Crecimiento'},
                  title='Estatura del Niño en Comparación con los Estándares de la OMS')
    
    # Agregar el punto del niño
    fig.add_scatter(x=[age_months], y=[height_cm], mode='markers', name='Estatura del Niño',
                    marker=dict(color='red', size=15))
    
    st.plotly_chart(fig, use_container_width=True)

    # 3. Recomendaciones de OpenAI
    st.subheader("Recomendaciones de Alimentación Personalizada")
    with st.spinner("Generando recomendaciones..."):
        recommendations = get_recommendations_from_openai(age_months, weight_kg, height_cm, dci_status)
        if recommendations:
            st.markdown(recommendations)
    
    