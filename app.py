import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Configuración de la página de Streamlit ---
st.set_page_config(
    page_title="Detección de Desnutrición Crónica Infantil",
    page_icon="👶",
    layout="wide",
)

# --- Título y Justificación del Problema ---
st.title("👶 Detección de Desnutrición Crónica Infantil")
st.markdown(
    """
    Este proyecto utiliza la Inteligencia Artificial para la **detección y prevención de la desnutrición crónica infantil** en niños y niñas menores de 5 años. 
    Se enfoca en la parroquia rural de San Antonio de Aláquez, Latacunga, una zona con alta vulnerabilidad socioeconómica.

    **Objetivo:** Clasificar el estado nutricional de un niño basado en su edad, peso y estatura,
    proporcionando un diagnóstico visual y recomendaciones personalizadas.
    """
)

st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRk1m3Yp3W1T0_3G_W9XmQ7XnQ9lJ4_rY_wzQ&s", caption="Una alimentación balanceada es crucial en la primera infancia.", use_column_width=True)

# --- Simulador de modelo de clasificación y recomendaciones ---
def clasificar_nino(edad_meses, estatura_cm):
    """
    Simula una clasificación de desnutrición crónica basada en reglas de la OMS.
    (Simplificado para fines del proyecto)
    """
    # Reglas simplificadas: la talla debe estar dentro de un rango normal para la edad.
    # Estos valores son puramente ilustrativos y no corresponden a percentiles reales de la OMS.
    tallas_referencia = {
        # 'edad_meses': [talla_min_referencia, talla_max_referencia]
        12: [70, 78], 
        24: [80, 88],
        36: [88, 96],
        48: [95, 103],
        60: [100, 110]
    }

    if edad_meses not in tallas_referencia:
        return "Fuera del rango de edad analizado (1-5 años).", None

    talla_min, talla_max = tallas_referencia[edad_meses]
    
    if estatura_cm < talla_min:
        return "El niño o niña presenta **desnutrición crónica**. Su estatura está significativamente por debajo de lo normal para su edad. 😥", "bajo"
    elif estatura_cm > talla_max:
        return "El niño o niña presenta un crecimiento superior al promedio para su edad. Se recomienda seguimiento médico. 😊", "alto"
    else:
        return "El niño o niña presenta un crecimiento normal para su edad. Sigue así. 🎉", "normal"

def generar_recomendaciones(edad_meses, peso_kg, estatura_cm, resultado_clasificacion):
    """
    Simula la respuesta de la API de GPT-4.1 con recomendaciones personalizadas.
    """
    if "desnutrición crónica" in resultado_clasificacion:
        return f"""
        **Guía de Alimentación Personalizada:**
        - **Énfasis en micronutrientes:** Incluir alimentos ricos en hierro y zinc (lentejas, carne, espinacas).
        - **Aumentar la densidad calórica:** Añadir aceites saludables a las comidas para aumentar las calorías sin aumentar el volumen.
        - **Proteínas de calidad:** Incorporar huevos, lácteos y legumbres en cada comida principal.
        - **Frecuencia:** Ofrecer 5 a 6 comidas pequeñas y nutritivas a lo largo del día.
        """
    elif "crecimiento normal" in resultado_clasificacion:
        return f"""
        **Guía de Alimentación para Crecimiento Saludable:**
        - **Dieta balanceada:** Continuar con una dieta que incluya frutas, verduras, granos enteros y proteínas magras.
        - **Hábitos saludables:** Fomentar el consumo de agua y limitar los alimentos procesados y azúcares.
        - **Variedad:** Introducir nuevos alimentos de forma gradual para asegurar una ingesta variada de nutrientes.
        """
    else:
        return """
        **Recomendaciones Generales:**
        - Consultar a un pediatra para una evaluación completa.
        - Asegurar una dieta balanceada y variada.
        """

# --- Layout de columnas para la interfaz ---
col1, col2 = st.columns(2)

with col1:
    st.header("1. Ingresa los Datos del Niño/a")
    edad = st.number_input("Edad (en meses):", min_value=1, max_value=60, step=1)
    peso = st.number_input("Peso (en kg):", min_value=1.0, step=0.1)
    estatura = st.number_input("Estatura (en cm):", min_value=20.0, step=0.1)
    
    if st.button("Analizar"):
        st.session_state.show_results = True
        st.session_state.resultado = clasificar_nino(edad, estatura)
        st.session_state.recomendaciones = generar_recomendaciones(peso, edad, estatura, st.session_state.resultado[0])
        st.session_state.datos_nino = {'edad': edad, 'peso': peso, 'estatura': estatura, 'estado': st.session_state.resultado[1]}

# --- Sección de Resultados (aparece al hacer clic en 'Analizar') ---
if 'show_results' in st.session_state and st.session_state.show_results:
    with col2:
        st.header("2. Resultados y Recomendaciones")
        
        # Muestra el resultado de la clasificación
        st.markdown(f"**Resultado del Análisis:** {st.session_state.resultado[0]}")
        
        # Muestra las recomendaciones generadas
        st.subheader("Guía Práctica de Alimentación")
        st.markdown(st.session_state.recomendaciones)
        
        # --- Gráfico comparativo ---
        st.subheader("Gráfico Comparativo de Crecimiento")
        
        # Datos simplificados de referencia de la OMS (talla para la edad)
        # Nota: estos son valores ilustrativos, no datos reales
        edad_ref = np.arange(12, 61, 12)
        talla_min_ref = np.array([70, 80, 88, 95, 100])
        talla_max_ref = np.array([78, 88, 96, 103, 110])
        talla_media_ref = (talla_min_ref + talla_max_ref) / 2
        
        # Configuración del gráfico
        fig, ax = plt.subplots()
        ax.plot(edad_ref, talla_media_ref, 'g--', label='Talla Media OMS')
        ax.fill_between(edad_ref, talla_min_ref, talla_max_ref, color='green', alpha=0.2, label='Rango Normal OMS')
        ax.plot(st.session_state.datos_nino['edad'], st.session_state.datos_nino['estatura'], 'ro', markersize=10, label='Talla del Niño/a')
        
        ax.set_xlabel("Edad (meses)")
        ax.set_ylabel("Estatura (cm)")
        ax.set_title("Comparación con Estándares de la OMS")
        ax.legend()
        ax.grid(True)
        
        st.pyplot(fig)

st.markdown("---")

# --- Sección de Chatbot ---
st.header("3. Chatbot sobre Desnutrición")
st.markdown("Haz tus preguntas sobre la desnutrición crónica infantil. (Simulado)")

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes del historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Aceptar la entrada del usuario
if prompt := st.chat_input("¿Qué quieres saber sobre la desnutrición?"):
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Simular la respuesta de la IA (aquí iría la llamada a la API de OpenAI)
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            # Lógica simulada de respuesta del chatbot
            if "desnutrición crónica" in prompt.lower():
                response = "La desnutrición crónica es el retraso en la talla para la edad, resultado de una privación nutricional prolongada. Afecta el desarrollo físico y cognitivo de los niños, con consecuencias irreversibles si no se atiende a tiempo. La medición principal es la talla para la edad, comparada con los estándares de la OMS."
            elif "alimentación" in prompt.lower() or "dieta" in prompt.lower():
                response = "Una alimentación adecuada para prevenir la desnutrición incluye alimentos ricos en proteínas (huevos, legumbres, carnes), hierro, zinc (espinacas, lentejas) y vitaminas, además de una buena hidratación. La lactancia materna exclusiva es clave hasta los 6 meses."
            elif "qué hacer" in prompt.lower() or "recomiendas" in prompt.lower():
                response = "Si sospechas que un niño tiene desnutrición, es vital consultar a un pediatra o nutricionista. Una intervención temprana con una dieta balanceada y suplementos puede revertir los efectos a corto plazo."
            else:
                response = "Lo siento, no tengo una respuesta específica para eso. Mi conocimiento se centra en la desnutrición crónica infantil y su prevención. Intenta preguntar sobre la importancia de la nutrición en la primera infancia o sobre las causas de la desnutrición."
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})