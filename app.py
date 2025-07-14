from flask import Flask, request, jsonify
import os
import sqlite3

from llm_service import itinerario

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/", methods=['GET'])
def main():
    return "API del asistente de viajes"


#-----------------------Solo para comprobar---------------------
@app.route("/test_get", methods=['GET'])
def test_get():
    pais = request.args.get('pais')
    dias = request.args.get('dias')
    return jsonify({"mensaje": f"País: {pais}, días: {dias}"})

# --------------------------------------------------------------

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
            "Genera 3 apartados: Un ITINERARIO día por día con actividades, alojamiento, transporte y consejos; CONSEJOS; PRESUPUESTO TOTAL DESGLOSADO POR TEMA"
            "Si elpresupuesto es demasiado bajo dimelo en la primera frase"
            "Al final pon: Si necesitas ayuda contacta con www.viajate.com"
        )

        respuesta = itinerario(prompt)

        # Guardar en la base de datos
        con = sqlite3.connect("data/viajes.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO interacciones (prompt, respuesta) VALUES (?, ?)", (prompt, respuesta))
        con.commit()
        con.close()

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

        con = sqlite3.connect("data/viajes.db")
        cursor = con.cursor()
        query = "INSERT INTO interacciones (prompt, respuesta) VALUES (?, ?)"

        for entry in data['interacciones']:
            cursor.execute(query, (entry['prompt'], entry['respuesta']))

        con.commit()
        con.close()

        return jsonify({"message": "Datos ingresados correctamente"}), 200

    except Exception as e:
        return jsonify({"Error": f"Ocurrió un error: {e}"}), 500


# 3. Ver interacciones guardadas
@app.route("/interacciones", methods=['GET'])
def ver_interacciones():
    try:
        con = sqlite3.connect("data/viajes.db")
        cursor = con.cursor()
        result = cursor.execute("SELECT * FROM interacciones").fetchall()
        con.close()

        datos = [{"id": r[0], "prompt": r[1], "respuesta": r[2]} for r in result]
        return jsonify(datos), 200

    except Exception as e:
        return jsonify({"Error": f"Ocurrió un error: {e}"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)


