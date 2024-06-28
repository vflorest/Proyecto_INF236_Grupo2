import streamlit as st
import requests
from opciones.Utils import descargar_pdf, mostrar_imagen
import base64

def mostrar_inicio_sesion(base_url, nombre_login=None, contrasena_login=None):
    if nombre_login is None:
        nombre_login = st.text_input('Nombre de Usuario', key='nombre_usuario')
    if contrasena_login is None:
        contrasena_login = st.text_input('Contraseña', type='password', key='contrasena_usuario')
    
    if st.button('Iniciar Sesión'):
        privilegio = iniciar_sesion(base_url, nombre_login, contrasena_login)
        if privilegio is not None:
            st.success('Inicio de sesión exitoso.')
            return privilegio
        else:
            st.error('Credenciales incorrectas.')

def iniciar_sesion(base_url, nombre, contrasena):
    try:
        payload = {'nombre': nombre, 'contraseña': contrasena}
        response = requests.post(f'{base_url}/inicio_sesion', json=payload)
        if response.status_code == 200:
            return response.json().get("privilegio")
        else:
            return None
    except Exception as e:
        st.error(f"Error al iniciar sesión: {e}")
        return None

def obtener_privilegio(base_url):
    try:
        response = requests.get(f"{base_url}/obtener_privilegio")
        if response.status_code == 200:
            privilegio = response.json().get("privilegio")
            print("Privilegio obtenido:", privilegio)  # Mensaje de depuración
            return privilegio
        else:
            print("Error en la solicitud HTTP:", response.status_code)  # Mensaje de depuración
            return None
    except Exception as e:
        st.error(f"Error al obtener el privilegio: {e}")
        return None
