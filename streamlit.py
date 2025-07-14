import streamlit as st
import requests

st.set_page_config(page_title="Planificador de Viajes IA", page_icon="✈️")

st.title("🧳 Planificador de Viajes con IA")

st.markdown("""
Completa el formulario para generar un itinerario personalizado según tus preferencias.
""")

with st.form("formulario_viaje"):
    pais = st.text_input("País a visitar", max_chars=50)
    dias = st.number_input("Número de días", min_value=1, max_value=365, step=1, value=7)
    personas = st.number_input("Número de personas", min_value=1, max_value=20, step=1, value=1)
    tipo = st.selectbox("Tipo de viaje", ["mochilero", "relajado", "lujo"])
    presupuesto = st.number_input("Presupuesto por persona (€)", min_value=50, max_value=10000, step=50, value=1000)

    enviar = st.form_submit_button("Generar Itinerario")

if enviar:
    if not pais.strip():
        st.error("Por favor, ingresa el país a visitar.")
    else:
        # Construir payload para enviar a Flask API
        payload = {
            "pais": pais.strip(),
            "dias": dias,
            "personas": personas,
            "tipo": tipo,
            "presupuesto": presupuesto
        }

        with st.spinner("Generando itinerario..."):
            try:
                # Cambia la URL si tu API está desplegada en otro lugar
                response = requests.post("http://127.0.0.1:5000/insertar_param", json=payload)

                if response.status_code == 200:
                    resultado = response.json()
                    itinerario = resultado.get("itinerario", "")
                    st.success("¡Itinerario generado!")
                    st.markdown(itinerario)
                else:
                    st.error(f"Error {response.status_code}: {response.json().get('Error', 'Error desconocido')}")

            except requests.exceptions.RequestException as e:
                st.error(f"No se pudo conectar con la API: {e}")
