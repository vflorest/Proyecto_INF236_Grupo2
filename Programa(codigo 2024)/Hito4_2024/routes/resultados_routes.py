from flask import Blueprint, request, jsonify

resultados_bp = Blueprint('resultados', __name__)

@resultados_bp.route('/guardar_resultados', methods=['POST'])
def guardar_resultados():
    try:
        from api import conn
        clave_busqueda = request.json.get('clave_busqueda')
        descripcion = request.json.get('descripcion')
        tipo_tallerista = request.json.get('tipo_tallerista')
        insumos = request.json.get('insumos')
        resultados_google_tallerista = request.json.get('resultados_google_tallerista')
        resultados_google_insumos = request.json.get('resultados_google_insumos')

        cursor = conn.cursor()
        cursor.execute("INSERT INTO resultados_busqueda (clave_busqueda, descripcion, tipo_tallerista, insumos) VALUES (%s, %s, %s, %s)", (clave_busqueda, descripcion, tipo_tallerista, insumos))
        conn.commit()
        cursor.execute("SELECT lastval()")
        resultado = cursor.fetchone()
        if resultado:
            id_busqueda = resultado[0]
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
    
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500
