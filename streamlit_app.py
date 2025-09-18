import streamlit as st
import pandas as pd
import numpy as np

# sección de encabezado de la app
seccionHeader = st.container()
with seccionHeader:
    st.title("App de Desnutrición Cronica Infantil")
    st.text("Esta es una app para analizar la desnutrición cronica infantil en niños menores de 5 años en el Ecuador")
    st.text("Creada por Diego Marcelo Altamirano Plazarte")

# sección de datos del menor de 5 años
seccionDatos = st.container(border=True)
with seccionDatos:
    st.header("Datos del menor de 5 años")
    st.text("En esta sección se ingresan los datos del menor de 5 años")
    nombre = st.text_input("Nombre del menor")
    edad = st.number_input("Edad del menor (en meses)", min_value=0, max_value=60, step=1)
    peso = st.number_input("Peso del menor (en kg)", min_value=0.0, max_value=50.0, step=0.1)
    estatura = st.number_input("Estatura del menor (en cm)", min_value=0.0, max_value=150.0, step=0.1)
    if st.button("Guardar datos"):
        st.success(f"Datos guardados: {nombre}, {edad} meses, {peso} kg, {estatura} cm")    

# sección de análisis de desnutrición
seccionAnalisis = st.container()
with seccionAnalisis:
    st.header("Análisis de Desnutrición")
    st.text("En esta sección se analiza si el menor presenta desnutrición crónica")
    
    if st.button("Analizar desnutrición"):
        if edad > 0 and peso > 0 and estatura > 0:
            # Cálculo del índice de masa corporal (IMC) como ejemplo simple
            imc = peso / ((estatura / 100) ** 2)
            if imc < 14.0:
                st.error(f"El menor {nombre} presenta desnutrición crónica (IMC: {imc:.2f})")
            else:
                st.success(f"El menor {nombre} no presenta desnutrición crónica (IMC: {imc:.2f})")
        else:
            st.warning("Por favor, ingrese todos los datos del menor para realizar el análisis.")
