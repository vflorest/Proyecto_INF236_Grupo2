import streamlit as st
import requests
from opciones.Utils import descargar_pdf, mostrar_imagen
import base64

def mostrar_eventos_registrados(BASE_URL):
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
