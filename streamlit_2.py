import streamlit as st
import requests

st.set_page_config(page_title="VIAJATE", page_icon="🌍")

st.title("🧳 VIAJATE: TE AYUDO A PREPARAR TU RUTA")
st.markdown("No lo pienses mas, genera un itinerario de viaje personalizado basado en tus preferencias")

# Formulario de entrada
with st.form("form_viaje"):
    pais = st.text_input("🌍 País de destino", placeholder="Ej: Indonesia")
    dias = st.number_input("📆 Número de días", min_value=1, max_value=30, step=1)
    personas = st.number_input("👥 Número de personas", min_value=1, step=1)
    tipo = st.selectbox("🎒 Estilo de viaje", ["mochilero", "relajado", "aventura", "luxury"])
    presupuesto = st.number_input("💰 Presupuesto por persona (€)", min_value=100)

    submit = st.form_submit_button("GENERAR ITINERARIO")

if submit:
    # Validación mínima
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

        with st.spinner("Generando itinerario..."):
            try:
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ ESTE ES EL ITINERARIO QUE TE PROPONGO:")
                    st.markdown(f"```{data['itinerario']}```")
                else:
                    st.error(f"Error: {response.json().get('Error')}")
            except Exception as e:
                st.error(f"No se pudo conectar al servidor Flask: {e}")
