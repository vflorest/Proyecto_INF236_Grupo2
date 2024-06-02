import streamlit as st
import requests

def mostrar_busqueda_descripcion(BASE_URL):
    st.header("Buscar Descripción")
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
