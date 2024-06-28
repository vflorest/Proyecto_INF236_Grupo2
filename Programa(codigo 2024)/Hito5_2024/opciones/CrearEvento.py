import streamlit as st
import requests
import base64

def leer_y_codificar_archivo(file):
    if file:
        file_bytes = file.read()
        return base64.b64encode(file_bytes).decode('utf-8')
    return None

def preparar_payload(titulo_evento, descripcion_evento, vacantes, sesiones, modalidad, contenido_base64, imagen_evento_base64, imagen_tallerista_base64, experiencia_tallerista, instagram, tiktok):
    return {
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

def manejar_respuesta_servidor(response):
    if response.status_code == 200:
        st.success("Evento creado correctamente.")
    else:
        st.error("Error al crear el evento. Inténtalo de nuevo.")

def mostrar_creacion_evento(base_url):
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
        contenido_base64 = leer_y_codificar_archivo(contenido_file)
        imagen_evento_base64 = leer_y_codificar_archivo(imagen_evento_file)
        imagen_tallerista_base64 = leer_y_codificar_archivo(imagen_tallerista_file)

        payload = preparar_payload(titulo_evento, descripcion_evento, vacantes, sesiones, modalidad, contenido_base64, imagen_evento_base64, imagen_tallerista_base64, experiencia_tallerista, instagram, tiktok)

        response = requests.post(f"{base_url}/crear_evento", json=payload)
        manejar_respuesta_servidor(response)
