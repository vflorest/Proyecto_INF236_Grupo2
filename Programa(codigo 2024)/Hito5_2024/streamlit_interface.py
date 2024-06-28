#!/usr/bin/env python
# coding: utf-8

from re import I
import streamlit as st
from streamlit import sidebar
import streamlit as st
from opciones import Inicio, InicioSesion, Registro, CrearEvento, BuscarDescripcion, Eventos

# URL base de la API Flask
base_url = 'http://localhost:5000'  # Cambia esto por la URL donde se ejecute la API Flask

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

menu = st.sidebar.selectbox('Selecciona una opción:', ['Inicio', 'Inicio de Sesión', 'Registro', 'Crear evento', 'Buscar descripcion', 'Eventos'])

# Definir constante
PRIVILEGIO_ERROR = "No tienes suficientes privilegios para acceder a esta opción."

if menu == 'Inicio':
    Inicio.mostrar_inicio()
elif menu == 'Inicio de Sesión':
    InicioSesion.mostrar_inicio_sesion(base_url)
elif menu == 'Registro':
    privilegio = InicioSesion.obtener_privilegio(base_url)
    if privilegio == 1:
        Registro.mostrar_registro_usuario(base_url)
    else:
        st.error(PRIVILEGIO_ERROR)
elif menu == 'Crear evento':
    CrearEvento.mostrar_creacion_evento(base_url)
elif menu == 'Buscar descripcion':
    privilegio = InicioSesion.obtener_privilegio(base_url)
    if privilegio == 1:
        BuscarDescripcion.mostrar_busqueda_descripcion(base_url)
    else:
        st.error(PRIVILEGIO_ERROR)
elif menu == 'Eventos':
    privilegio = InicioSesion.obtener_privilegio(base_url)
    if privilegio == 1:
        Eventos.mostrar_eventos_registrados(base_url)
    else:
        st.error(PRIVILEGIO_ERROR)
