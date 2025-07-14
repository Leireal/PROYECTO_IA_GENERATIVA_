import sqlite3
import os

# Ruta donde se guardará la base de datos
DB_PATH = "data/viajes.db"

# Asegurarse de que el directorio exista
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def crear_base_de_datos():
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    # Crear la tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            respuesta TEXT NOT NULL
        );
    """)

    con.commit()
    con.close()
    print(f"Base de datos creada en {DB_PATH} con la tabla 'interacciones'.")

if __name__ == "__main__":
    crear_base_de_datos()
