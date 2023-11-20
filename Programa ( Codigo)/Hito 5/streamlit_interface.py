#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import requests
import pandas as pd

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

# Configurar título y descripción de la aplicación Streamlit
st.title('Búsqueda de Talleristas e Insumos')
st.write('Esta aplicación interactúa con la API para realizar búsquedas y mostrar los resultados.')

# Sección para configurar la API Key de OpenAI
st.header('Configurar API Key de OpenAI')
api_key = st.text_input('Introduce tu API Key de OpenAI:')

# Botón para configurar la API Key
if st.button('Configurar API Key'):
    response_api_key = requests.post(f'{BASE_URL}/configure_openai_key', json={'api_key': api_key})
    if response_api_key.status_code == 200:
        st.success('API Key de OpenAI configurada correctamente.')
    else:
        st.error('Error al configurar la API Key de OpenAI.')


# Sección para obtener la descripción y realizar acciones
st.header('Descripción para búsqueda')
descripcion = st.text_input('Ingresa la descripción:')

# Variable para almacenar los insumos recomendados
insumos = []

# Botón para realizar el análisis de la descripción y obtener recomendaciones
if st.button('Obtener Recomendación'):
    response = requests.post(f'{BASE_URL}/tipo_tallerista', json={'descripcion': descripcion})
    if response.status_code == 200:
        tipo_tallerista = response.json()['tipo_tallerista']
        st.success(f'Tipo de tallerista recomendado: {tipo_tallerista}')

        insumos_response = requests.post(f'{BASE_URL}/insumos', json={'descripcion': descripcion})
        if insumos_response.status_code == 200:
            insumos = insumos_response.json()['insumos']
            st.success(f'Insumos recomendados: {insumos}')
    else:
        st.error('Error al realizar el análisis.')

# Botón para buscar talleristas en Google
if st.button('Buscar Talleristas con Google'):
    response_google_tallerista = requests.post(f'{BASE_URL}/buscar_tallerista', json={'descripcion': descripcion})
    if response_google_tallerista.status_code == 200:
        resultados_google_tallerista = response_google_tallerista.json().get('tabla_tallerista')
        st.subheader('Resultados de búsqueda en Google por Tipo de Tallerista')
        for resultado in resultados_google_tallerista:
            st.write(f"Descripción: {resultado['title']}")
            st.write(f"Link: {resultado['link']}")
            st.markdown("---")


if st.button('Buscar Insumos en Google'):
    if insumos:
        # Obtener la lista de insumos únicos para el selector
        insumos_lista = insumos.split(", ")

        # Realizar la búsqueda de 10 resultados para cada insumo recomendado
        for insumo in insumos_lista:
            response_google_insumos = requests.post(f'{BASE_URL}/buscar_insumos', json={'descripcion': insumo})
            if response_google_insumos.status_code == 200:
                resultados_google_insumos = response_google_insumos.json().get('tabla_insumos')
                
                # Limitar los resultados a 10
                resultados_insumo = resultados_google_insumos[:10]

                # Mostrar los resultados para este insumo
                st.subheader(f'Resultados para {insumo} en Chile:')
                table_data = []
                for resultado in resultados_insumo:
                    table_data.append({'Descripción': resultado['title'], 'Link': resultado['link']})
                
                # Mostrar la tabla con los resultados para este insumo
                st.write(pd.DataFrame(table_data))
    else:
        st.warning('Primero debes obtener la recomendación de insumos.')
         


