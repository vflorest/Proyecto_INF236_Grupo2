from flask import Blueprint, request, jsonify
from api import conn, set_privilegio_actual, get_privilegio_actual

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro_usuario', methods=['POST'])
def registro_usuario():
    privilegio_actual = get_privilegio_actual()  # Obtener el privilegio actual
    try:
        datos_usuario = request.json
        nombre = datos_usuario.get('nombre')
        contrasena = datos_usuario.get('contraseña')
        privilegio = datos_usuario.get('privilegio')

        if not nombre or not contrasena or not privilegio:
            raise ValueError("Faltan datos de usuario")

        if privilegio_actual != 1:
            raise PermissionError("No tienes privilegios suficientes para registrar usuarios.")

        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE nombre = %s", (nombre,))
        existe_usuario = cursor.fetchone()

        if existe_usuario:
            return jsonify({'error': 'El usuario ya está registrado'}), 400

        cursor.execute("INSERT INTO usuarios (nombre, contraseña, privilegio) VALUES (%s, %s, %s)", (nombre, contrasena, privilegio))
        conn.commit()
        cursor.close()

        return jsonify({'message': 'Usuario registrado correctamente'}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except PermissionError as pe:
        return jsonify({'error': str(pe)}), 403

    except Exception:
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/inicio_sesion', methods=['POST'])
def inicio_sesion():
    try:
        datos_usuario = request.json
        nombre = datos_usuario.get('nombre')
        contrasena = datos_usuario.get('contraseña')

        if not nombre or not contrasena:
            raise ValueError("Faltan datos de inicio de sesión")

        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, privilegio FROM usuarios WHERE nombre = %s AND contraseña = %s", (nombre, contrasena))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({'error': 'Credenciales incorrectas'}), 401

        usuario_id, nombre_usuario, privilegio = usuario
        # Actualizar privilegio_actual con el privilegio del usuario
        set_privilegio_actual(privilegio)
        return jsonify({'message': 'Inicio de sesión exitoso', 'usuario_id': usuario_id, 'nombre': nombre_usuario, 'privilegio': privilegio}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except Exception:
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route("/obtener_privilegio", methods=["GET"])
def obtener_privilegio():
    privilegio_actual = get_privilegio_actual()
    if privilegio_actual is not None:
        return jsonify({"privilegio": privilegio_actual}), 200
    else:
        return jsonify({"mensaje": "Privilegio no establecido"}), 404
