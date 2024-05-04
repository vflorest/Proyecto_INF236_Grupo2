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
from config import dbname, user, password, host
import base64

app = Flask(__name__)

import psycopg2
from flask import jsonify, request

conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host
)
privilegio_actual = None  # Variable global para almacenar el privilegio del usuario actual

@app.route('/registro_usuario', methods=['POST'])
def registro_usuario():
    global privilegio_actual
    datos_usuario = request.json
    nombre = datos_usuario.get('nombre')
    contraseña = datos_usuario.get('contraseña')
    privilegio = datos_usuario.get('privilegio')
    print(f"El privilegio actual es: {privilegio_actual}")
    # Verifica que el usuario actual tenga privilegio 1 para permitir el registro
    if privilegio_actual != 1:
        return jsonify({'error': 'No tienes privilegios suficientes para registrar usuarios.'}), 403

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE nombre = %s", (nombre,))
    existe_usuario = cursor.fetchone()

    if existe_usuario:
        return jsonify({'error': 'El usuario ya está registrado'}), 400

    cursor.execute("INSERT INTO usuarios (nombre, contraseña, privilegio) VALUES (%s, %s, %s)", (nombre, contraseña, privilegio))
    conn.commit()
    cursor.close()

    return jsonify({'message': 'Usuario registrado correctamente'}), 200

@app.route('/inicio_sesion', methods=['POST'])
def inicio_sesion():
    datos_usuario = request.json
    nombre = datos_usuario.get('nombre')
    contraseña = datos_usuario.get('contraseña')

    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, privilegio FROM usuarios WHERE nombre = %s AND contraseña = %s", (nombre, contraseña))
    usuario = cursor.fetchone()

    if not usuario:
        return jsonify({'error': 'Credenciales incorrectas'}), 401

    # Obtener los datos del usuario y su privilegio
    usuario_id, nombre_usuario, privilegio = usuario

    # Almacenar el privilegio del usuario actual en la variable global
    global privilegio_actual
    privilegio_actual = privilegio

    # Devolver más información del usuario, incluido su privilegio
    return jsonify({'message': 'Inicio de sesión exitoso', 'usuario_id': usuario_id, 'nombre': nombre_usuario, 'privilegio': privilegio}), 200


@app.route('/crear_evento', methods=['POST'])
def crear_evento():
    datos_evento = request.json
    titulo_evento = datos_evento.get('titulo_evento')
    descripcion_evento = datos_evento.get('descripcion_evento')
    vacantes = datos_evento.get('vacantes')
    sesiones = datos_evento.get('sesiones')
    modalidad = datos_evento.get('modalidad')
    contenido = datos_evento.get('contenido')
    imagen_evento = datos_evento.get('imagen_evento')
    imagen_tallerista = datos_evento.get('imagen_tallerista')
    experiencia_tallerista = datos_evento.get('experiencia_tallerista')
    instagram = datos_evento.get('instagram')
    tiktok = datos_evento.get('tiktok')

    cursor = conn.cursor()
    cursor.execute("INSERT INTO eventos (titulo_evento, descripcion_evento, vacantes, sesiones, modalidad, contenido, imagen_evento, imagen_tallerista, experiencia_tallerista, instagram, tiktok) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (titulo_evento, descripcion_evento, vacantes, sesiones, modalidad, contenido, imagen_evento, imagen_tallerista, experiencia_tallerista, instagram, tiktok))
    conn.commit()
    cursor.close()

    return jsonify({'message': 'Evento creado correctamente'}), 200




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
    clave_busqueda = request.json.get('clave_busqueda')
    descripcion = request.json.get('descripcion')
    tipo_tallerista = request.json.get('tipo_tallerista')
    insumos = request.json.get('insumos')
    resultados_google_tallerista = request.json.get('resultados_google_tallerista')
    resultados_google_insumos = request.json.get('resultados_google_insumos')

    cursor = conn.cursor()

    # Insertar la clave de búsqueda en la tabla de resultados de búsqueda
    cursor.execute("INSERT INTO resultados_busqueda (clave_busqueda, descripcion, tipo_tallerista, insumos) VALUES (%s, %s, %s, %s)", (clave_busqueda, descripcion, tipo_tallerista, insumos))
    conn.commit()

    # Obtener el ID de la última inserción (clave primaria autogenerada)
    cursor.execute("SELECT lastval()")
    resultado = cursor.fetchone()
    if resultado:
        id_busqueda = resultado[0]

        # Insertar resultados de búsqueda en Google asociados con la clave de búsqueda
        for resultado in resultados_google_tallerista:
            cursor.execute("INSERT INTO resultados_google (clave_busqueda, id_busqueda, tipo_tallerista, title, link) VALUES (%s, %s, %s, %s, %s)", (clave_busqueda, id_busqueda, tipo_tallerista, resultado['title'], resultado['link']))
        for insumo, resultados in resultados_google_insumos.items():
            for resultado in resultados:
                cursor.execute("INSERT INTO resultados_google (clave_busqueda, id_busqueda, insumo, title, link) VALUES (%s, %s, %s, %s, %s)", (clave_busqueda, id_busqueda, insumo, resultado['title'], resultado['link']))

        conn.commit()
        cursor.close()
        return jsonify({'message': 'Resultados guardados correctamente en la base de datos.'}), 200
    else:
        conn.rollback()
        cursor.close()
        return jsonify({'error': 'Error al guardar los resultados.'}), 500


@app.route('/eventos', methods=['GET'])
def obtener_eventos():
    estado_aprobacion = request.args.get('aprobacion')

    cursor = conn.cursor()
    if estado_aprobacion == '2':  # Aprobados
        cursor.execute("SELECT * FROM eventos WHERE aprobacion = 2")
    elif estado_aprobacion == '3':  # Desaprobados
        cursor.execute("SELECT * FROM eventos WHERE aprobacion = 3")
    elif estado_aprobacion == '1':  # Sin revisar
        cursor.execute("SELECT * FROM eventos WHERE aprobacion = 1")
    else:
        cursor.execute("SELECT * FROM eventos")

    eventos = cursor.fetchall()
    cursor.close()

    eventos_json = []
    for evento in eventos:
        evento_dict = {
            'id': evento[0],
            'titulo_evento': evento[1],
            'descripcion_evento': evento[2],
            'vacantes': evento[3],
            'sesiones': evento[4],
            'modalidad': evento[5],
            'contenido': None,  # Inicializar como None por defecto
            'imagen_evento': None,  # También puedes inicializar las imágenes como None
            'imagen_tallerista': None,
            'experiencia_tallerista': evento[9],
            'instagram': evento[10],
            'tiktok': evento[11],
            'aprobacion': evento[12]
        }
        
        # Verificar y codificar en base64 solo si el contenido no es None
        if evento[6] is not None:
            evento_dict['contenido'] = base64.b64encode(evento[6]).decode()
        
        # Similarmente, verifica y codifica las imágenes si no son None
        if evento[7] is not None:
            evento_dict['imagen_evento'] = base64.b64encode(evento[7]).decode()
        
        if evento[8] is not None:
            evento_dict['imagen_tallerista'] = base64.b64encode(evento[8]).decode()
        
        eventos_json.append(evento_dict)

    return jsonify(eventos_json), 200




@app.route('/aprobar_evento/<int:evento_id>', methods=['POST'])
def aprobar_evento(evento_id):
    cursor = conn.cursor()
    cursor.execute("UPDATE eventos SET aprobacion = 2 WHERE id = %s", (evento_id,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Evento aprobado correctamente.'}), 200

@app.route('/desaprobar_evento/<int:evento_id>', methods=['POST'])
def desaprobar_evento(evento_id):
    cursor = conn.cursor()
    cursor.execute("UPDATE eventos SET aprobacion = 3 WHERE id = %s", (evento_id,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Evento desaprobado correctamente.'}), 200


if __name__ == '__main__':
    app.run(debug=True)



