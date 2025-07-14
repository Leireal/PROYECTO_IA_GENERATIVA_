import sqlite3
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
POSTGRES_URL = os.getenv("DATABASE_URL")

sqlite_conn = sqlite3.connect("viajes.db")
sqlite_cursor = sqlite_conn.cursor()
sqlite_cursor.execute("SELECT respuesta FROM interacciones")
registros = sqlite_cursor.fetchall()
sqlite_conn.close()

postgres_conn = psycopg2.connect(POSTGRES_URL)
postgres_cursor = postgres_conn.cursor()

# Crear tabla si no existe (por seguridad)
postgres_cursor.execute('''
    CREATE TABLE IF NOT EXISTS interacciones (
        id SERIAL PRIMARY KEY,
        fecha TIMESTAMP,
        estado TEXT,
        respuesta TEXT
    )
''')

# Insertar registros
for respuesta in registros:
    postgres_cursor.execute(
        "INSERT INTO interacciones (respuesta) VALUES (%s)",
        (respuesta)
    )
postgres_conn.commit()
postgres_conn.close()
print(f":marca_de_verificación_blanca: Migrados {len(registros)} registros a PostgreSQL.")






