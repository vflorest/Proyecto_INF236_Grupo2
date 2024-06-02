import streamlit as st
import requests

def mostrar_registro_usuario(BASE_URL):
    st.header('Registro de Usuario')
    nombre_registro = st.text_input('Nombre de usuario')
    contraseña_registro = st.text_input('Contraseña', type='password')
    privilegio = st.selectbox('Privilegio', [1, 2])
    
    if st.button('Registrarse'):
        payload = {'Nombre': nombre_registro, 'Contraseña': contraseña_registro, 'privilegio': privilegio}
        response = requests.post(f'{BASE_URL}/registro_usuario', json=payload)
        if response.status_code == 200:
            st.success('Usuario registrado correctamente.')
        elif response.status_code == 400:
            st.error('El usuario ya está registrado.')
        elif response.status_code == 403:
            st.error('No tienes privilegios suficientes para registrar usuarios.')
        else:
            st.error('Error al registrar usuario.')
