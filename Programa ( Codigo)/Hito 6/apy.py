#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, jsonify, request
from openai_operations import configure_api_key, obtener_tipo_tallerista, obtener_insumos
from google_search_operations import buscar_tallerista, buscar_insumos
from tabulate import tabulate
import os
from datetime import datetime
from flask import send_file 

app = Flask(__name__)

# Configurar API key de OpenAI
@app.route('/configure_openai_key', methods=['POST'])
def configure_openai_key():
    api_key = request.json.get('api_key')
    configure_api_key(api_key)
    return jsonify({'message': 'OpenAI API Key configured successfully'})

# Almacenar la información de tipo de tallerista e insumos
tipo_tallerista_cache = {}
insumos_cache = {}
resultados_google_tallerista_cache = {}
resultados_google_insumos_cache = {}

# Endpoint para obtener tipo de tallerista
@app.route('/tipo_tallerista', methods=['POST'])
def get_tipo_tallerista():
    descripcion = request.json.get('descripcion')
    tipo_tallerista_cache[descripcion] = obtener_tipo_tallerista(descripcion)
    return jsonify({'tipo_tallerista': tipo_tallerista_cache[descripcion]})

# Endpoint para obtener recomendación de insumos
@app.route('/insumos', methods=['POST'])
def get_insumos():
    descripcion = request.json.get('descripcion')
    insumos_cache[descripcion] = obtener_insumos(descripcion)
    return jsonify({'insumos': insumos_cache[descripcion]})


# Endpoint para buscar tallerista en Google.
@app.route('/buscar_tallerista', methods=['POST'])
def search_tallerista():
    descripcion = request.json.get('descripcion')
    if descripcion not in tipo_tallerista_cache:
        return jsonify({'error': 'Primero debe obtener el tipo de tallerista para la descripción dada'})

    resultados = buscar_tallerista(tipo_tallerista_cache[descripcion])
    resultados_google_tallerista_cache[descripcion] = [{'title': resultado['title'], 'link': resultado['link']} for resultado in resultados]
    return jsonify({'tabla_tallerista': resultados_google_tallerista_cache[descripcion]})


# Endpoint para buscar insumos en Google.
@app.route('/buscar_insumos', methods=['POST'])
def search_insumos():
    descripcion = request.json.get('descripcion')
    if descripcion not in insumos_cache:
        return jsonify({'error': 'Primero debe obtener los insumos para la descripción dada'})

    insumos_lista = insumos_cache[descripcion].split(", ")
    resultados_insumos = {}
    for insumo in insumos_lista:
        resultados_insumos[insumo] = buscar_insumos(insumo)
        
    resultados_google_insumos_cache[descripcion] = resultados_insumos
    return jsonify({'tabla_insumos': resultados_insumos})

@app.route('/guardar_resultados', methods=['POST'])
def guardar_resultados():
    descripcion = request.json.get('descripcion')

    # Obtener los resultados desde las cachés usando la descripción
    resultados_tallerista = tipo_tallerista_cache.get(descripcion)
    resultados_insumos = insumos_cache.get(descripcion)
    resultados_google_tallerista = resultados_google_tallerista_cache.get(descripcion)
    resultados_google_insumos = resultados_google_insumos_cache.get(descripcion)

    # Obtener la fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Crear el contenido del archivo .txt con los resultados
    contenido = f"Resultados para '{descripcion}' - {fecha_actual}\n\n"
    contenido +=f"Tipo de tallerista recomendado: {resultados_tallerista}\n"
    contenido +=f"Insumos recomendados: {resultados_insumos}\n\n"
    contenido += "Resultados de búsqueda en Google por Tipo de Tallerista:\n"
    contenido += f"\nResultados para {resultados_tallerista} en Chile:\n"
    for resultado in resultados_google_tallerista:
        contenido += f"{resultado['title']} - {resultado['link']}\n"
    contenido += "\nResultados de búsqueda en Google por Insumos:\n"
    for insumo, resultados in resultados_google_insumos.items():
            contenido +=(f"\nResultados para {insumo} en Chile:\n")
            for resultado in resultados:
                contenido += f"{resultado['title']} - {resultado['link']}\n"
    # Nombre del archivo
    nombre_archivo = f"Registros/{fecha_actual}.txt"

    # Guardar el archivo
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(contenido)


    # Enviar el archivo como respuesta
    return send_file(nombre_archivo, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)



