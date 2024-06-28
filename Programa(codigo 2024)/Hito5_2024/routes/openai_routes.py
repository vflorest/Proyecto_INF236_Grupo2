from flask import Blueprint, request, jsonify
from openai_operations import configure_api_key, obtener_tipo_tallerista, obtener_insumos
import openai

openai_bp = Blueprint('openai', __name__)

# Definir constante
ERROR_INTERNO_SERVIDOR = 'Error interno del servidor'

tipo_tallerista_cache = {}
insumos_cache = {}

@openai_bp.route('/configure_openai_key', methods=['POST'])
def configure_openai_key():
    try:
        api_key = request.json.get('api_key')
        openai.api_key = api_key
        
        # Realiza una solicitud de prueba a la API de OpenAI
        response = openai.Completion.create(engine="davinci", prompt="Hello, world!")
        
        if response['id']:
            return jsonify({'message': 'OpenAI API Key configured successfully'}), 200
        else:
            return jsonify({'error': 'La clave de API de OpenAI no es válida'}), 400
    
    except Exception:
        return jsonify({'error': ERROR_INTERNO_SERVIDOR}), 500

@openai_bp.route('/tipo_tallerista', methods=['POST'])
def get_tipo_tallerista():
    try:
        descripcion = request.json.get('descripcion')
        tipo_tallerista_cache[descripcion] = obtener_tipo_tallerista(descripcion)
        return jsonify({'tipo_tallerista': tipo_tallerista_cache[descripcion]}), 200
    
    except Exception:
        return jsonify({'error': ERROR_INTERNO_SERVIDOR}), 500

@openai_bp.route('/insumos', methods=['POST'])
def get_insumos():
    try:
        descripcion = request.json.get('descripcion')
        insumos_cache[descripcion] = obtener_insumos(descripcion)
        return jsonify({'insumos': insumos_cache[descripcion]}), 200
    
    except Exception:
        return jsonify({'error': ERROR_INTERNO_SERVIDOR}), 500
