import streamlit as st
import base64
from PIL import Image
import io

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
