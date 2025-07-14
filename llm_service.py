import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno desde el archivo .env

def itinerario(prompt):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Falta la clave GROQ_API_KEY en el entorno")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()  # Por si hay error en la respuesta
    return response.json()["choices"][0]["message"]["content"]


