
#!/usr/bin/env python
# coding: utf-8
# In[ ]:


from re import I
import streamlit as st
from streamlit import sidebar
import streamlit as st
from opciones import Inicio, InicioSesion, Registro, CrearEvento, BuscarDescripcion, Eventos


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

menu = st.sidebar.selectbox('Selecciona una opción:', ['Inicio', 'Inicio de Sesión', 'Registro', 'Crear evento', 'Buscar descripcion', 'Eventos'])


if menu == 'Inicio':
    Inicio.mostrar_inicio()
elif menu == 'Inicio de Sesión':
    InicioSesion.mostrar_inicio_sesion(BASE_URL)
elif menu == 'Registro':
    privilegio = InicioSesion.obtener_privilegio(BASE_URL)
    if privilegio == 1:
        Registro.mostrar_registro_usuario(BASE_URL)
    else:
        st.error("No tienes suficientes privilegios para acceder a esta opción.")
elif menu == 'Crear evento':
    CrearEvento.mostrar_creacion_evento(BASE_URL)
elif menu == 'Buscar descripcion':
    privilegio = InicioSesion.obtener_privilegio(BASE_URL)
    if privilegio == 1:
        BuscarDescripcion.mostrar_busqueda_descripcion(BASE_URL)
    else:
        st.error("No tienes suficientes privilegios para acceder a esta opción.")
elif menu == 'Eventos':
    privilegio = InicioSesion.obtener_privilegio(BASE_URL)
    if privilegio == 1:
        Eventos.mostrar_eventos_registrados(BASE_URL)
    else:
        st.error("No tienes suficientes privilegios para acceder a esta opción.")