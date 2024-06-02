import streamlit as st
import requests
from opciones.Utils import descargar_pdf, mostrar_imagen
import base64

def mostrar_inicio_sesion(BASE_URL, nombre_login='', contraseña_login=''):
    nombre_login = st.text_input('Nombre de Usuario', key='nombre_usuario')
    contraseña_login = st.text_input('Contraseña', type='password', key='contraseña_usuario')
    if st.button('Iniciar Sesión'):
        privilegio = iniciar_sesion(BASE_URL, nombre_login, contraseña_login)
        if privilegio is not None:
            st.success('Inicio de sesión exitoso.')
            return privilegio
        else:
            st.error('Credenciales incorrectas.')
def iniciar_sesion(BASE_URL, nombre, contraseña):
    try:
        payload = {'nombre': nombre, 'contraseña': contraseña}
        response = requests.post(f'{BASE_URL}/inicio_sesion', json=payload)
        if response.status_code == 200:
            return response.json().get("privilegio")
        else:
            return None
    except Exception as e:
        st.error(f"Error al iniciar sesión: {e}")
        return None

def obtener_privilegio(BASE_URL):
    try:
        response = requests.get(f"{BASE_URL}/obtener_privilegio")
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
