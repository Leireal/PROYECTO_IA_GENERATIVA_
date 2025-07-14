import streamlit as st
import requests
import os
from dotenv import load_dotenv
import base64

# Cargar clave de API
load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


#------------

def set_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    css = f"""
    <style>
    [data-testid="stApp"] {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
st.set_page_config(layout="wide")

# Inyectar CSS personalizado
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            color: black !important;
            font-weight: bold !important;
        }
    </style>
""", unsafe_allow_html=True)

# Ruta a la imagen (ajusta si estás en otra carpeta)
img_path = "img/fondo.jpg"

# Verifica si el archivo existe antes de usarlo
if os.path.exists(img_path):
    set_bg_from_local(img_path)
else:
    st.warning(f"No se encontró la imagen en: {img_path}")


#---------------

st.title("🧳 VIAJATE: TE AYUDO A PREPARAR TU RUTA")
st.subheader("No lo pienses mas, genera un itinerario de viaje personalizado")

# Crear dos columnas: formulario estrecho a la izquierda y resultado amplio a la derecha
col1, col2 = st.columns([1, 2])

with col1:
    #st.subheader("✍️ Tus preferencias")
    with st.form("form_viaje"):
        pais = st.text_input("🌍 País de destino", placeholder="Ej: Colombia")
        dias = st.number_input("📆 Número de días", min_value=1, max_value=30, step=1)
        personas = st.number_input("👥 Número de personas", min_value=1, step=1)
        tipo = st.selectbox("🎒 Estilo de viaje", ["mochilero", "relajado", "aventura", "luxury"])
        presupuesto = st.number_input("💰 Presupuesto por persona (€)", min_value=100)
        submit = st.form_submit_button("Generar itinerario")

with col2:
    if submit:
        if not pais:
            st.error("Debes ingresar un país.")
        else:
            url = "http://127.0.0.1:5000/insertar_param"
            headers = {"Content-Type": "application/json"}
            payload = {
                "pais": pais,
                "dias": dias,
                "tipo": tipo,
                "personas": personas,
                "presupuesto": presupuesto
            }

            with st.spinner("✈️ Generando itinerario..."):
                try:
                    response = requests.post(url, json=payload, headers=headers)
                    if response.status_code == 200:
                        data = response.json()

                        st.text_area("✍️ Itinerario generado", value=data['itinerario'], height=500, disabled=True)

                    else:
                        st.error(f"Error: {response.json().get('Error')}")
                except Exception as e:
                    st.error(f"No se pudo conectar al servidor Flask: {e}")


# Botón de imprimir en PDF---------------------
st.markdown("""
    <div style="text-align: right; margin-top: 1rem;">
        <button onclick="window.print()" style="
            background-color: #007BFF;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            font-size: 16px;
            cursor: pointer;
        ">
            📄 Guardar o imprimir como PDF
        </button>
    </div>
""", unsafe_allow_html=True)

#Boton web---------------------

st.markdown("""
    <div style="text-align: right; margin-top: 1rem;">
        <a href="https://www.viajate.com" target="_blank">
            <button style="
                background-color: #28a745;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                font-size: 16px;
                cursor: pointer;
            ">
                🌐 Visitar Viajate.com
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)
