#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, jsonify, request
from openai_operations import configure_api_key, obtener_tipo_tallerista, obtener_insumos
from google_search_operations import configure_google_credentials, buscar_tallerista, buscar_insumos

app = Flask(__name__)

# Configurar API key de OpenAI
@app.route('/configure_openai_key', methods=['POST'])
def configure_openai_key():
    api_key = request.json.get('api_key')
    configure_api_key(api_key)
    return jsonify({'message': 'OpenAI API Key configured successfully'})

# Endpoint para obtener tipo de tallerista
@app.route('/tipo_tallerista', methods=['POST'])
def get_tipo_tallerista():
    descripcion = request.json.get('descripcion')
    tipo_tallerista = obtener_tipo_tallerista(descripcion)
    return jsonify({'tipo_tallerista': tipo_tallerista})

# Endpoint para obtener insumos
@app.route('/insumos', methods=['POST'])
def get_insumos():
    descripcion = request.json.get('descripcion')
    insumos = obtener_insumos(descripcion)
    return jsonify({'insumos': insumos})

# Endpoint para buscar tallerista en Google
@app.route('/buscar_tallerista', methods=['POST'])
def search_tallerista():
    query = request.json.get('query')
    resultados = buscar_tallerista(query)
    return jsonify({'resultados': resultados})

# Endpoint para buscar insumos en Google
@app.route('/buscar_insumos', methods=['POST'])
def search_insumos():
    query = request.json.get('query')
    resultados = buscar_insumos(query)
    return jsonify({'resultados': resultados})

if __name__ == '__main__':
    app.run(debug=True)

