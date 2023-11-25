#!/usr/bin/env python
# coding: utf-8
# In[ ]:


from re import I
import streamlit as st
from streamlit import sidebar
import requests
from PIL import Image
import pandas as pd
from tabulate import tabulate

# URL base de la API Flask
BASE_URL = 'http://localhost:5000'  # Cambia esto por la URL donde se ejecute la API Flask

# Definir estilos CSS para la interfaz
estilos = """
    <style>
    body {
        color: #ffffff; /* Texto blanco */
        background-color: #6a0572; /* Fondo morado */
    }
    .st-bw {
        color: #000000; /* Texto negro */
    }
    .stButton > button {
        background-color: #f4b41a; /* Botón amarillo */
    }
    </style>
"""

# Aplicar estilos
st.markdown(estilos, unsafe_allow_html=True)

    
with st.container():
    st.subheader("Hola! Bienvenid@ a OiGenie")

# Configurar título y descripción de la aplicación Streamlit
st.title('OiGenie')
text_placeholder = st.empty()
text_placeholder.write('Primero debes configurar tu API Key.')

def show_popup():
    st.session_state.clicked = True

    # Crear un contenedor de columna para el popup
    with sidebar:
        st.header("Configuración de API Key")
        api_input = "Ingrese aquí su API Key"

        # Cuadro de texto para la búsqueda
        api_key = st.text_input(api_input,
            value="",
            placeholder=api_input,
            label_visibility='collapsed')
        
        #save_api_button = sidebar.button("Guardar API Key")

        if  st.button("Guardar API Key"):
            text_placeholder.empty()
            response_api_key = requests.post(f'{BASE_URL}/configure_openai_key', json={'api_key': api_key})
            if response_api_key.status_code == 200:
                st.success("API Key Guardada!")
            else:
                st.error("Error al configurar la API Key.")
                


#API Key
if "clicked" not in st.session_state:
    st.session_state["clicked"] = False

with st.container():
    # Botón para abrir el popup
    if st.session_state.clicked or st.button("API Key"):
        show_popup()

        
# Sección para obtener la descripción y realizar acciones
st.header('Descripción sobre el taller que desea realizar')
descripcion = st.text_input('Ingresa la descripción:')     

    
# Botón para realizar todas las acciones con una sola búsqueda
if st.button('Realizar Búsqueda'):
    response = requests.post(f'{BASE_URL}/tipo_tallerista', json={'descripcion': descripcion})
    if response.status_code == 200:
        tipo_tallerista = response.json()['tipo_tallerista']
        st.success(f'Tipo de tallerista recomendado: {tipo_tallerista}')

        insumos_response = requests.post(f'{BASE_URL}/insumos', json={'descripcion': descripcion})
        if insumos_response.status_code == 200:
            insumos = insumos_response.json()['insumos']
            st.success(f'Insumos recomendados: {insumos}')

        # Búsqueda de talleristas en Google
        response_google_tallerista = requests.post(f'{BASE_URL}/buscar_tallerista', json={'descripcion': descripcion})
        if response_google_tallerista.status_code == 200:
            resultados_google_tallerista = response_google_tallerista.json().get('tabla_tallerista')
            st.subheader('Resultados de búsqueda en Google por Tipo de Tallerista')
            for resultado in resultados_google_tallerista:
                st.write([resultado['title'], resultado['link']])

        # Búsqueda de insumos en Google
        response_google_insumos = requests.post(f'{BASE_URL}/buscar_insumos', json={'descripcion': descripcion})
        if response_google_insumos.status_code == 200:
            resultados_google_insumos = response_google_insumos.json().get('tabla_insumos')
            st.subheader('Resultados de búsqueda en Google por Isumos Recomendados')
            for insumo, resultados in resultados_google_insumos.items():
                st.write(f"\nResultados para {insumo} en Chile:")
                for resultado in resultados:
                    st.write([resultado['title'][:50], resultado['link']])
                st.markdown("---")



# Botón para guardar resultados
if st.button('Guardar Resultados'):
    data = {
        'descripcion': descripcion,
    }
    response_guardar = requests.post(f'{BASE_URL}/guardar_resultados', json=data)
    if response_guardar.status_code == 200:
        st.success('Resultados guardados correctamente en el archivo.')
    else:
        st.error('Error al guardar los resultados.')