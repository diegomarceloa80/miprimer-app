
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
#import os

# Set page configuration
st.set_page_config(page_title="Diagnóstico de Desnutrición Crónica Infantil", layout="wide")

# API Key de OpenAI desde secretos de Streamlit
#api_key = os.getenv("OPENAI_API_KEY")


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
    if not openai_api_key:
        st.error("Error: La clave de la API de OpenAI no está configurada. Por favor, configura la variable de entorno 'OPENAI_API_KEY'.")
        return None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
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
        "temperature": 0.7 #,  # Controla la creatividad de la respuesta
        #"max_tokens": 500
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

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    #client = OpenAI(api_key=openai_api_key)
 
 
    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []
 
    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    st.header("1. Ingreso de Parámetros")

    with st.form("input_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            #age_months = st.number_input("Edad del niño (meses)", min_value=1, max_value=60, step=1, value=24)
            age_months = st.slider("Edad del niño (meses)", min_value=1, max_value=60, step=1, value=1)
        with col2:
            weight_kg = st.number_input("Peso (kg)", min_value=1.0, max_value=50.0, step=0.1, value=10.0)
        with col3:
            height_cm = st.number_input("Estatura (cm)", min_value=30.0, max_value=150.0, step=0.1, value=58.0)

        submitted = st.form_submit_button("Analizar")

    st.markdown("---")

    if submitted:
        st.header("2. Resultados del Análisis")
        
        # 1. Clasificación
        dci_status = classify_dci(age_months, height_cm)
        # Mostrar el estado de salud coloca un color según el estado
        if dci_status == "Riesgo de Desnutrición Crónica":
            st.error(f"### Estado de Salud Detectado: **{dci_status}**")
        else:
            st.success(f"### Estado de Salud Detectado: **{dci_status}**")
        #
        
    # Datos de ejemplo de la OMS (talla para la edad para niños, de 0 a 60 meses)
    # Nota: En un proyecto real, estos datos se cargarían desde un archivo CSV o una base de datos.
    # Aquí se presentan de forma simplificada para ilustrar el concepto.
    def get_who_data():
        data = {
            'age_months': np.arange(0, 61),
            'mediana_z0': [
                49.9, 54.7, 58.4, 61.4, 63.9, 66.0, 67.8, 69.2, 70.6, 71.9, 73.1, 74.5, 75.7, 76.9, 78.0, 79.1, 80.1, 81.1, 82.0, 82.9, 
                83.8, 84.7, 85.5, 86.4, 87.2, 88.0, 88.8, 89.5, 90.3, 91.0, 91.7, 92.4, 93.0, 93.7, 94.3, 94.9, 95.5, 96.1, 96.7, 97.2, 
                97.8, 98.4, 98.9, 99.5, 100.0, 100.6, 101.1, 101.7, 102.2, 102.8, 103.3, 103.8, 104.3, 104.8, 105.3, 105.8, 106.3, 106.8, 
                107.3, 107.8, 108.3
            ],
            'desviacion_estandar': [
                1.8, 2.1, 2.3, 2.4, 2.5, 2.5, 2.6, 2.6, 2.6, 2.6, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 
                2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 
                2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 2.7, 
                2.7
            ]
        }
        return pd.DataFrame(data)

    def classify_dci(age_months, height_cm, who_df):
        """
        Clasifica el riesgo de DCI usando el Z-score real de la OMS.
        """
        row = who_df[who_df['age_months'] == age_months].iloc[0]
        mediana = row['mediana_z0']
        desviacion_estandar = row['desviacion_estandar']
        
        z_score = (height_cm - mediana) / desviacion_estandar
        
        if z_score < -2:
            return "Riesgo de Desnutrición Crónica"
        else:
            return "Normal"

    # Carga de datos de la OMS
    who_df = get_who_data()


    st.markdown("---")

    if submitted:
        #st.header("2. Resultados del Análisis")
        
    # dci_status = classify_dci(age_months, height_cm, who_df)
        #st.write(f"### Estado de Salud Detectado: **{dci_status}**")
        
        st.subheader("Gráfico Comparativo: Estatura vs. Estándares de Referencia")
        
        # Calcular los rangos de la OMS usando los datos de referencia
        who_df['Z-score +2'] = who_df['mediana_z0'] + (who_df['desviacion_estandar'] * 2)
        who_df['Z-score 0'] = who_df['mediana_z0']
        who_df['Z-score -2'] = who_df['mediana_z0'] - (who_df['desviacion_estandar'] * 2)

        # Crear el gráfico con Plotly
        fig = px.line(
            who_df,
            x='age_months',
            y=['Z-score +2', 'Z-score 0', 'Z-score -2'],
            labels={'age_months': 'Edad (meses)', 'value': 'Estatura (cm)', 'variable': 'Curva de Crecimiento'},
            title='Estatura del Niño en Comparación con los Estándares de la OMS'
        )
        
        # Personalizar las líneas y el legend
        fig.data[0].name = 'Máximo (Z-score +2)'
        fig.data[1].name = 'Normal (Z-score 0)'
        fig.data[2].name = 'Umbral DCI (Z-score -2)'
        fig.data[0].line.color = 'blue'
        fig.data[1].line.color = 'green'
        fig.data[2].line.color = 'orange'
        
        # Agregar el punto del niño
        fig.add_scatter(
            x=[age_months], 
            y=[height_cm], 
            mode='markers', 
            name='Estatura del Niño',
            marker=dict(color='red', size=15)
        )
        
        st.plotly_chart(fig, use_container_width=True)

        # 3. Recomendaciones de OpenAI
        st.subheader("Recomendaciones de Alimentación Personalizada")
        with st.spinner("Generando recomendaciones..."):
            recommendations = get_recommendations_from_openai(age_months, weight_kg, height_cm, dci_status)
            if recommendations:
                st.markdown(recommendations)
        
        