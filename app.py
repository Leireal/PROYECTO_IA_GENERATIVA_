from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv


from llm_service import itinerario  # Asegúrate de que este archivo exista y esté bien definido

# Cargar variables de entorno
load_dotenv()
load_dotenv(override=True)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", 5432)  # por si falta, default a 5432
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

print("DEBUG ENV:")
print(" DB_HOST:", DB_HOST)
print(" DB_PORT:", DB_PORT)
print(" DB_NAME:", DB_NAME)
print(" DB_USER:", DB_USER)

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/", methods=['GET'])
def main():
    return "API del asistente de viajes"


# ----------------------- Test básico ---------------------
@app.route("/test_get", methods=['GET'])
def test_get():
    pais = request.args.get('pais')
    dias = request.args.get('dias')
    return jsonify({"mensaje": f"País: {pais}, días: {dias}"})


# 1. Generación del itinerario + guardar en base de datos
@app.route("/insertar_param", methods=['POST'])
def insertar_param():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"Error": "No se han proporcionado datos"}), 400

        prompt = (
            f"Quiero visitar {data['pais']} durante {data['dias']} días, estilo de viaje {data['tipo']}, "
            f"con {data['personas']} personas, y presupuesto de {data['presupuesto']} euros por persona (sin vuelos). "
            "Genera 3 apartados: Un ITINERARIO día por día con actividades, alojamiento, transporte y consejos; "
            "CONSEJOS; PRESUPUESTO TOTAL DESGLOSADO POR TEMA. "
            "Si el presupuesto es demasiado bajo dímelo en la primera frase. "
            "Al final pon: Si necesitas ayuda contacta con www.viajate.com"
        )

        respuesta = itinerario(prompt)

        conn = psycopg2.connect(
            host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO interacciones (prompt, respuesta) VALUES (%s, %s)", (prompt, respuesta))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"itinerario": respuesta}), 200

    except Exception as e:
        return jsonify({"Error": f"Ocurrió un error: {e}"}), 500


# 2. Insertar manualmente nuevas interacciones
@app.route("/ingest", methods=['POST'])
def ingest():
    try:
        data = request.get_json()
        if not data or 'interacciones' not in data:
            return jsonify({"Error": "No se han proporcionado interacciones"}), 400

        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        
        cursor = conn.cursor()
        query = "INSERT INTO interacciones (prompt, respuesta) VALUES (%s, %s)"

        for entry in data['interacciones']:
            cursor.execute(query, (entry['prompt'], entry['respuesta']))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Datos ingresados correctamente"}), 200

    except Exception as e:
        return jsonify({"Error": f"Ocurrió un error: {e}"}), 500


# 3. Ver interacciones guardadas
@app.route("/interacciones", methods=['GET'])
def ver_interacciones():
    try:
        conn = psycopg2.connect(
            host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, prompt, respuesta FROM interacciones")
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        datos = [{"id": r[0], "prompt": r[1], "respuesta": r[2]} for r in result]
        return jsonify(datos), 200

    except Exception as e:
        return jsonify({"Error": f"Ocurrió un error: {e}"}), 500


if __name__ == "__main__":
    # Render usa el puerto de entorno, importante si corres localmente con Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


