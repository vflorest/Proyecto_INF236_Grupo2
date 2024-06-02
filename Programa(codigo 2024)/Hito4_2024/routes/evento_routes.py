from flask import Blueprint, request, jsonify
import base64

event_bp = Blueprint('event', __name__)

@event_bp.route('/crear_evento', methods=['POST'])
def crear_evento():
    from api import conn

    try:
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
        
        # Verificar si algún campo requerido está vacío
        if not all([titulo_evento, descripcion_evento]):
            raise ValueError("Faltan datos obligatorios del evento")

        cursor = conn.cursor()
        cursor.execute("INSERT INTO eventos (titulo_evento, descripcion_evento, vacantes, sesiones, modalidad, contenido, imagen_evento, imagen_tallerista, experiencia_tallerista, instagram, tiktok) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (titulo_evento, descripcion_evento, vacantes, sesiones, modalidad, contenido, imagen_evento, imagen_tallerista, experiencia_tallerista, instagram, tiktok))
        conn.commit()
        cursor.close()

        return jsonify({'message':'Evento creado correctamente.'}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@event_bp.route('/eventos', methods=['GET'])
def obtener_eventos():
    from api import conn

    try:
        estado_aprobacion = request.args.get('aprobacion')
        cursor = conn.cursor()
        if estado_aprobacion == '2':
            cursor.execute("SELECT * FROM eventos WHERE aprobacion = 2")
        elif estado_aprobacion == '3':
            cursor.execute("SELECT * FROM eventos WHERE aprobacion = 3")
        elif estado_aprobacion == '1':
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
                'contenido': None,
                'imagen_evento': None,
                'imagen_tallerista': None,
                'experiencia_tallerista': evento[9],
                'instagram': evento[10],
                'tiktok': evento[11],
                'aprobacion': evento[12]
            }
            if evento[6] is not None:
                evento_dict['contenido'] = base64.b64encode(evento[6]).decode()
            if evento[7] is not None:
                evento_dict['imagen_evento'] = base64.b64encode(evento[7]).decode()
            if evento[8] is not None:
                evento_dict['imagen_tallerista'] = base64.b64encode(evento[8]).decode()
            
            eventos_json.append(evento_dict)

        return jsonify(eventos_json), 200

    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@event_bp.route('/aprobar_evento/<int:evento_id>', methods=['POST'])
def aprobar_evento(evento_id):
    from api import conn

    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE eventos SET aprobacion = 2 WHERE id = %s", (evento_id,))
        conn.commit()
        cursor.close()
        return jsonify({'message': 'Evento aprobado correctamente.'}), 200

    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@event_bp.route('/desaprobar_evento/<int:evento_id>', methods=['POST'])
def desaprobar_evento(evento_id):
    from api import conn

    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE eventos SET aprobacion = 3 WHERE id = %s", (evento_id,))
        conn.commit()
        cursor.close()
        return jsonify({'message': 'Evento desaprobado correctamente.'}), 200

    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500
