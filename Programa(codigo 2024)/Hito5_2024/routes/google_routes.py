from flask import Blueprint, request, jsonify
from google_search_operations import buscar_tallerista, buscar_insumos
from routes.openai_routes import tipo_tallerista_cache, insumos_cache

google_bp = Blueprint('google', __name__)

resultados_google_tallerista_cache = {}
resultados_google_insumos_cache = {}

@google_bp.route('/buscar_tallerista', methods=['POST'])
def search_tallerista():
    try:
        descripcion = request.json.get('descripcion')
        if descripcion not in tipo_tallerista_cache:
            return jsonify({'error': 'Primero debe obtener el tipo de tallerista para la descripción dada'}), 400

        resultados = buscar_tallerista(tipo_tallerista_cache[descripcion])
        resultados_google_tallerista_cache[descripcion] = [{'title': resultado['title'], 'link': resultado['link']} for resultado in resultados]
        return jsonify({'tabla_tallerista': resultados_google_tallerista_cache[descripcion]}), 200

    except Exception:
        return jsonify({'error': 'Error interno del servidor'}), 500

@google_bp.route('/buscar_insumos', methods=['POST'])
def search_insumos():
    try:
        descripcion = request.json.get('descripcion')
        if descripcion not in insumos_cache:
            return jsonify({'error': 'Primero debe obtener los insumos para la descripción dada'}), 400

        insumos_lista = insumos_cache[descripcion].split(", ")
        resultados_insumos = {}
        for insumo in insumos_lista:
            resultados_insumos[insumo] = buscar_insumos(insumo)
            
        resultados_google_insumos_cache[descripcion] = resultados_insumos
        return jsonify({'tabla_insumos': resultados_insumos}), 200

    except Exception:
        return jsonify({'error': 'Error interno del servidor'}), 500
