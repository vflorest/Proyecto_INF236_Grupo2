import streamlit as st
import requests
from opciones.Utils import descargar_pdf, mostrar_imagen
import base64

# Definir constantes
SIN_REVISAR = 'Sin revisar'
APROBADOS = 'Aprobados'
DESAPROBADOS = 'Desaprobados'

def obtener_filtro_api(estado_filtro):
    if estado_filtro == SIN_REVISAR:
        return '1'
    elif estado_filtro == APROBADOS:
        return '2'
    elif estado_filtro == DESAPROBADOS:
        return '3'
    return ''

def obtener_estado_aprobacion(aprobacion):
    if aprobacion == 1:
        return SIN_REVISAR
    elif aprobacion == 2:
        return APROBADOS
    elif aprobacion == 3:
        return DESAPROBADOS
    return 'Desconocido'

def mostrar_info_evento(evento):
    st.write(f"**{evento['titulo_evento']}**")
    st.write(f"Descripción: {evento['descripcion_evento'][:100]}...")
    st.write(f"Vacantes: {evento['vacantes']}")
    st.write(f"Sesiones: {evento['sesiones']}")
    st.write(f"Modalidad: {'Presencial' if evento['modalidad'] == 1 else 'Virtual'}")
    st.write(f"Contenido: {'Sí' if evento['contenido'] else 'No'}")

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

def manejar_aprobacion(base_url, evento_id, aprobar):
    endpoint = 'aprobar_evento' if aprobar else 'desaprobar_evento'
    response = requests.post(f'{base_url}/{endpoint}/{evento_id}')
    if response.status_code == 200:
        st.success(f'Evento {"aprobado" if aprobar else "desaprobado"} correctamente.')
    else:
        st.error(f'Error al {"aprobar" if aprobar else "desaprobar"} el evento.')

def mostrar_eventos_registrados(base_url):
    st.header('Eventos Registrados')
    
    estado_filtro = st.selectbox('Filtrar por estado de aprobación:', ['Todos', SIN_REVISAR, APROBADOS, DESAPROBADOS])
    filtro_api = obtener_filtro_api(estado_filtro)
    
    response = requests.get(f'{base_url}/eventos?aprobacion={filtro_api}')
    if response.status_code == 200:
        eventos = response.json()
        for evento in eventos:
            mostrar_info_evento(evento)
            estado_aprobacion = obtener_estado_aprobacion(evento['aprobacion'])
            st.write(f"Aprobación: {estado_aprobacion}")

            if estado_filtro == SIN_REVISAR:
                if st.button(f"Aprobar {evento['titulo_evento']}"):
                    manejar_aprobacion(base_url, evento["id"], True)
                if st.button(f"Desaprobar {evento['titulo_evento']}"):
                    manejar_aprobacion(base_url, evento["id"], False)
            st.write('---')
    else:
        st.error('Error al obtener los eventos.')
