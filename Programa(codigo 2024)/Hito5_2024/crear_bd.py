import psycopg2
from psycopg2 import sql
import config  # Asegúrate de tener el archivo config.py en el mismo directorio

# Obtén los parámetros de conexión desde el archivo config.py
dbname = config.dbname
user = config.user
password = config.password
host = config.host
port = config.port

# Conectarse a PostgreSQL sin seleccionar una base de datos específica
conn = psycopg2.connect(user=user, password=password, host=host, port=port)
conn.autocommit = True  # Establecer autocommit en True para realizar operaciones de base de datos

# Crear la base de datos si no existe
cursor = conn.cursor()
cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
cursor.close()
conn.close()

# Conectarse a la base de datos creada
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cursor = conn.cursor()

# Crear la tabla eventos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos (
        id SERIAL PRIMARY KEY,
        titulo_evento VARCHAR(255) NOT NULL,
        descripcion_evento TEXT,
        vacantes INTEGER,
        sesiones INTEGER CHECK (sesiones >= 1 AND sesiones <= 3),
        modalidad INTEGER,
        contenido BYTEA,
        imagen_evento BYTEA,
        imagen_tallerista BYTEA,
        experiencia_tallerista TEXT,
        instagram VARCHAR(255),
        tiktok VARCHAR(255),
        aprobacion INTEGER DEFAULT 1 CHECK (aprobacion >= 1 AND aprobacion <= 3)
    )
""")

# Crear la tabla usuarios
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) UNIQUE NOT NULL,
        contraseña VARCHAR(255) NOT NULL,
        privilegio INT DEFAULT 1
    )
""")

# Agregar el primer usuario
cursor.execute("""
    INSERT INTO usuarios (nombre, contraseña, privilegio)
    VALUES (%s, %s, %s)
""", ('ADMIN', '1234', 1))

# Crear la tabla resultados_busqueda
cursor.execute("""
    CREATE TABLE IF NOT EXISTS resultados_busqueda (
        id SERIAL PRIMARY KEY,
        clave_busqueda VARCHAR(50) NOT NULL,
        descripcion VARCHAR(255) NOT NULL,
        tipo_tallerista VARCHAR(255),
        insumos VARCHAR(255),
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Crear la tabla resultados_google
cursor.execute("""
    CREATE TABLE IF NOT EXISTS resultados_google (
        id SERIAL PRIMARY KEY,
        clave_busqueda VARCHAR(50) NOT NULL,
        tipo_tallerista VARCHAR(255),
        insumo VARCHAR(255),
        title VARCHAR(255),
        link VARCHAR(255),
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")


# Confirmar los cambios en la base de datos
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()

print("Base de datos creada, tablas creadas y primer usuario agregado con éxito.")
