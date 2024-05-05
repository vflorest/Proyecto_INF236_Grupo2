
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
import base64
from io import BytesIO
from docx import Document
from fpdf import FPDF
from PIL import Image
import io
from datetime import date, time, datetime


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
def descargar_pdf(pdf_base64, nombre_archivo):
    try:
        pdf_bytes = base64.b64decode(pdf_base64)
        st.download_button(label=f"Descargar {nombre_archivo}.pdf", data=pdf_bytes, file_name=f"{nombre_archivo}.pdf", mime='application/pdf')
    except Exception as e:
        st.error(f"Error al descargar el PDF: {e}")

def mostrar_imagen(imagen_base64):
    try:
        image_bytes = base64.b64decode(imagen_base64)
        pil_image = Image.open(io.BytesIO(image_bytes))

        # Mostrar la imagen
        st.image(pil_image, use_column_width=True)
    except Exception as e:
        st.error(f"Error al cargar la imagen: {e}")
            
# Aplicar estilos
st.markdown(estilos, unsafe_allow_html=True)

    
with st.container():
    st.subheader("Hola! Bienvenid@ a OiGenie")

# Crear menú de navegación lateral
menu = st.sidebar.selectbox('Selecciona una opción:', ['Inicio', 'Inicio de Sesión','Registro','Crear evento','Buscar descripcion','Eventos'])

if menu == 'Inicio':
    st.header('Bienvenido a OiGenie')
    st.write('Aquí puedes realizar diversas acciones.')
    

elif menu == 'Inicio de Sesión':
    st.header('Inicio de Sesión')
    nombre_login = st.text_input('Nombre de Usuario')
    contraseña_login = st.text_input('Contraseña', type='password')
    
    if st.button('Iniciar Sesión'):
        payload = {'nombre': nombre_login, 'contraseña': contraseña_login}
        response = requests.post(f'{BASE_URL}/inicio_sesion', json=payload)
        if response.status_code == 200:
            st.success('Inicio de sesión exitoso.')
            data = response.json()
            privilegio = data.get('privilegio')
        elif response.status_code == 401:
            st.error('Credenciales incorrectas.')
        else:
            st.error('Error al iniciar sesión.')
            
elif menu == 'Registro':
    st.header('Registro de Usuario')
    nombre_registro = st.text_input('Nombre de usuario')
    contraseña_registro = st.text_input('contraseña', type='password')
    privilegio = st.selectbox('Privilegio', [1, 2])
    
    if st.button('Registrarse'):
        payload = {'nombre': nombre_registro, 'contraseña': contraseña_registro, 'privilegio': privilegio}
        response = requests.post(f'{BASE_URL}/registro_usuario', json=payload)
        if response.status_code == 200:
            st.success('Usuario registrado correctamente.')
        elif response.status_code == 400:
            st.error('El usuario ya está registrado.')
        elif response.status_code == 403:
            st.error('No tienes privilegios suficientes para registrar usuarios.')
        else:
            st.error('Error al registrar usuario.')
            
    
    
elif menu == 'Crear evento':
    # Crear formulario para registrar un nuevo evento
    st.header("Crear Nuevo Evento")
    titulo_evento = st.text_input("Título del Evento")
    descripcion_evento = st.text_area("Descripción del Evento (máx. 500 caracteres)", max_chars=500)
    vacantes = st.number_input("Vacantes", min_value=1)
    sesiones = st.number_input("Sesiones (entre 1 y 3)", min_value=1, max_value=3)
    modalidad = st.selectbox("Modalidad", ["Presencial", "Virtual"])
    contenido_file = st.file_uploader("Contenido (PDF o Word)")
    imagen_evento_file = st.file_uploader("Imagen del Evento (JPG)")
    imagen_tallerista_file = st.file_uploader("Imagen del Tallerista (JPG)")
    experiencia_tallerista = st.text_area("Experiencia del Tallerista (máx. 500 caracteres)", max_chars=500)
    instagram = st.text_input("Instagram del Tallerista")
    tiktok = st.text_input("TikTok del Tallerista")

    
    if st.button("Crear Evento"):
    # Convertir archivos a base64 para enviar al servidor
        contenido_bytes = contenido_file.read() if contenido_file else None
        contenido_base64 = base64.b64encode(contenido_bytes).decode('utf-8') if contenido_bytes else None

        imagen_evento_bytes = imagen_evento_file.read() if imagen_evento_file else None
        imagen_evento_base64 = base64.b64encode(imagen_evento_bytes).decode('utf-8') if imagen_evento_bytes else None

        imagen_tallerista_bytes = imagen_tallerista_file.read() if imagen_tallerista_file else None
        imagen_tallerista_base64 = base64.b64encode(imagen_tallerista_bytes).decode('utf-8') if imagen_tallerista_bytes else None

        payload = {
            "titulo_evento": titulo_evento,
            "descripcion_evento": descripcion_evento,
            "vacantes": vacantes,
            "sesiones": sesiones,
            "modalidad": 1 if modalidad == "Presencial" else 2,  # Por ejemplo, 1 para Presencial, 2 para Virtual
            "contenido": contenido_base64,
            "imagen_evento": imagen_evento_base64,
            "imagen_tallerista": imagen_tallerista_base64,
            "experiencia_tallerista": experiencia_tallerista,
            "instagram": instagram,
            "tiktok": tiktok
        }

        response = requests.post(f"{BASE_URL}/crear_evento", json=payload)

        if response.status_code == 200:
            st.success("Evento creado correctamente.")
        else:
            st.error("Error al crear el evento. Inténtalo de nuevo.")
            
            
            
   
elif menu == 'Buscar descripcion':
    st.header("Configuración de API Key")
    api_input = "Ingrese aquí su API Key"

    # Cuadro de texto para la búsqueda
    api_key = st.text_input(api_input,
        value="",
        placeholder=api_input,
        label_visibility='collapsed')
    
    # Botón para guardar la API Key
    if st.button("Guardar API Key"):
        response_api_key = requests.post(f'{BASE_URL}/configure_openai_key', json={'api_key': api_key})
        if response_api_key.status_code == 200:
            st.success("API Key Guardada!")
        else:
            st.error("Error al configurar la API Key.")
    
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
                st.subheader('Resultados de búsqueda en Google por Insumos Recomendados')
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
            st.success('Resultados guardados correctamente en la base de datos.')
        else:
            st.error('Error al guardar los resultados.')


elif menu == 'Eventos':
    st.header('Eventos Registrados')

    estado_filtro = st.selectbox('Filtrar por estado de aprobación:', ['Todos', 'Sin revisar', 'Aprobados', 'Desaprobados'])

    filtro_api = ''  # Valor de filtro para la API

    if estado_filtro == 'Sin revisar':
        filtro_api = '1'  # Representa eventos sin revisar
    elif estado_filtro == 'Aprobados':
        filtro_api = '2'  # Representa eventos aprobados
    elif estado_filtro == 'Desaprobados':
        filtro_api = '3'  # Representa eventos desaprobados

    response = requests.get(f'{BASE_URL}/eventos?aprobacion={filtro_api}')

    if response.status_code == 200:
        eventos = response.json()
        for evento in eventos:
            st.write(f"**{evento['titulo_evento']}**")
            st.write(f"Descripción: {evento['descripcion_evento'][:100]}...")  # Mostrar solo parte de la descripción
            st.write(f"Vacantes: {evento['vacantes']}")
            st.write(f"Sesiones: {evento['sesiones']}")
            st.write(f"Modalidad: {'Presencial' if evento['modalidad'] == 1 else 'Virtual'}")
            st.write(f"Contenido: {'Sí' if evento['contenido'] else 'No'}")  # Mostrar si hay contenido o no

            # Mostrar contenido y botón de descarga si existe
            if evento['contenido']:
                descargar_pdf(base64.b64decode(evento['contenido']), f"{evento['titulo_evento']}_contenido")
            else:
                st.write("No hay contenido PDF disponible para este evento.")
                    
            if evento['imagen_evento']:
                mostrar_imagen(base64.b64decode(evento['imagen_evento']))
            else:
                st.write("No hay imagen disponible para este evento.")

            if evento['imagen_tallerista']:
                mostrar_imagen(base64.b64decode(evento['imagen_tallerista']))
            else:
                st.write("No hay imagen del tallerista disponible para este evento.")

            st.write(f"Experiencia Tallerista: {evento['experiencia_tallerista']}")
            st.write(f"Instagram: {evento['instagram']}")
            st.write(f"TikTok: {evento['tiktok']}")
            estado_aprobacion = 'Sin revisar' if evento['aprobacion'] == 1 else 'Aprobado' if evento['aprobacion'] == 2 else 'Desaprobado'
            st.write(f"Aprobación: {estado_aprobacion}")

            # Agregar botones para aprobar y desaprobar
            if estado_filtro == 'Sin revisar':
                if st.button(f"Aprobar {evento['titulo_evento']}"):
                    # Enviar acción de aprobación a la API
                    response_aprobacion = requests.post(f'{BASE_URL}/aprobar_evento/{evento["id"]}')
                    if response_aprobacion.status_code == 200:
                        st.success('Evento aprobado correctamente.')
                    else:
                        st.error('Error al aprobar el evento.')

                if st.button(f"Desaprobar {evento['titulo_evento']}"):
                    # Enviar acción de desaprobación a la API
                    response_desaprobacion = requests.post(f'{BASE_URL}/desaprobar_evento/{evento["id"]}')
                    if response_desaprobacion.status_code == 200:
                        st.success('Evento desaprobado correctamente.')
                    else:
                        st.error('Error al desaprobar el evento.')

            st.write('---')
    else:
        st.error('Error al obtener los eventos.')
