#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, jsonify, request
from openai_operations import configure_api_key, obtener_tipo_tallerista, obtener_insumos
from google_search_operations import buscar_tallerista, buscar_insumos
from tabulate import tabulate

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
    table = [{'title': resultado['title'], 'link': resultado['link']} for resultado in resultados]
    return jsonify({'tabla_tallerista': table})

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
        
    return jsonify({'tabla_insumos': resultados_insumos})




if __name__ == '__main__':
    app.run(debug=True)



