#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import requests

# URL base de la API Flask
BASE_URL = 'http://localhost:5000'  # Cambia esto por la URL donde se ejecute la API Flask

# Configurar título y descripción de la aplicación Streamlit
st.title('Búsqueda de Talleristas e Insumos')
st.write('Esta aplicación interactúa con la API para realizar búsquedas y mostrar los resultados.')

# Sección para obtener la API Key de OpenAI
st.header('Configurar API Key de OpenAI')
api_key = st.text_input('Introduce tu API Key de OpenAI:')
if st.button('Configurar API Key'):
    response = requests.post(f'{BASE_URL}/configure_openai_key', json={'api_key': api_key})
    if response.status_code == 200:
        st.success('API Key de OpenAI configurada correctamente.')
    else:
        st.error('Error al configurar la API Key de OpenAI.')

# Sección para obtener el tipo de tallerista
st.header('Obtener Tipo de Tallerista')
descripcion_tallerista = st.text_input('Ingresa la descripción para obtener el tipo de tallerista:')
if st.button('Obtener Tipo de Tallerista'):
    response = requests.post(f'{BASE_URL}/tipo_tallerista', json={'descripcion': descripcion_tallerista})
    if response.status_code == 200:
        tipo_tallerista = response.json()['tipo_tallerista']
        st.success(f'Tipo de tallerista recomendado: {tipo_tallerista}')
    else:
        st.error('Error al obtener el tipo de tallerista.')

# Sección para obtener insumos recomendados
st.header('Obtener Insumos Recomendados')
descripcion_insumos = st.text_input('Ingresa la descripción para obtener insumos recomendados:')
if st.button('Obtener Insumos Recomendados'):
    response = requests.post(f'{BASE_URL}/insumos', json={'descripcion': descripcion_insumos})
    if response.status_code == 200:
        insumos_recomendados = response.json()['insumos']
        st.success(f'Insumos recomendados: {insumos_recomendados}')
    else:
        st.error('Error al obtener insumos recomendados.')

