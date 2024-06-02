from flask import Flask
import psycopg2
from config import dbname, user, password, host
from flask import Blueprint, request, jsonify
app = Flask(__name__)

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host
)

# Inicializar privilegio_actual como None
privilegio_actual = None

# Función para establecer el privilegio actual
def set_privilegio_actual(privilegio):
    global privilegio_actual
    privilegio_actual = privilegio


def get_privilegio_actual():
    global privilegio_actual
    return privilegio_actual



def create_app():
    # Importar y registrar Blueprints
    from routes.auth_routes import auth_bp
    from routes.evento_routes import event_bp
    from routes.openai_routes import openai_bp
    from routes.google_routes import google_bp
    from routes.resultados_routes import resultados_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(openai_bp)
    app.register_blueprint(google_bp)
    app.register_blueprint(resultados_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
