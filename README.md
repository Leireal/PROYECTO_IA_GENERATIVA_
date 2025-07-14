# 🧳  Proyecto Final - Aplicación de IA Generativa: **Planificador de Viajes**

---

## 🧠 1. Descripción

Este proyecto final del módulo de **Data Engineering** consiste en el desarrollo de una aplicación web de **IA Generativa** especializada en viajes. A través de una API construida con **Flask**, la app permite a los usuarios generar un **itinerario personalizado** en base a parámetros como destino, duración, estilo de viaje, número de personas y presupuesto.

La lógica de generación está basada en un **LLM** conectado vía una función (`itinerario`) y se almacena el historial de interacciones en una base de datos PostgreSQL desplegada en **RENDER** ☁️.

---

## 🎯 2. Objetivos

1. ⚙️ Construir una API REST con **Flask**.
2. 💬 Integrar un modelo de lenguaje (LLM) usando GROQ.
3. 🧠 Generar itinerarios de viaje detallados y personalizados.
4. 🗃️ Almacenar las consultas/respuestas en una base de datos PostgreSQL en RENDER.
5. 🐳 Dockerizar la aplicación para su despliegue multiplataforma.
6. ☁️ Publicar en **DockerHub** y **GitHub**.

---

## ✨ 3. Funcionalidades

* 🧍 Entrada de datos del usuario: país, días, personas, estilo y presupuesto.
* 🤖 Generación automática de:

  * 🗓️ Itinerario día a día.
  * 🧳 Consejos útiles de viaje.
  * 💸 Presupuesto total desglosado.
* 🚫 Detección de presupuesto insuficiente.
* 🧾 Registro automático en base de datos.
* 🔍 Consulta del historial de interacciones.

---

## 🛠️ 4. Estructura de la API (`Flask`)

### 🏠 4.1 `GET /`

Mensaje de bienvenida a la API.

### 🔄 4.2 `GET /test_get`

Test rápido de conexión. Recibe `pais` y `dias` como parámetros.

### 📥 4.3 `POST /insertar_param`

Genera un itinerario a partir de los datos del usuario y guarda la interacción en la base de datos.

### 📝 4.4 `POST /ingest`

Permite ingresar manualmente múltiples interacciones en la base de datos.

### 📂 4.5 `GET /interacciones`

Muestra todas las interacciones registradas en la base de datos.

---

## 💡 5. Prompt Generativo

```python
prompt = (
    f"Quiero visitar {data['pais']} durante {data['dias']} días, estilo de viaje {data['tipo']}, "
    f"con {data['personas']} personas, y presupuesto de {data['presupuesto']} euros por persona (sin vuelos). "
    "Genera 3 apartados: Un ITINERARIO día por día con actividades, alojamiento, transporte y consejos; "
    "CONSEJOS; PRESUPUESTO TOTAL DESGLOSADO POR TEMA. "
    "Si el presupuesto es demasiado bajo dímelo en la primera frase. "
    "Al final pon: Si necesitas ayuda contacta con www.viajate.com"
)
```

---

## 🧩 6. Dependencias Principales

* `Flask` 🌐 - Framework web ligero.
* `psycopg2` 🐘 - Conector PostgreSQL.
* `dotenv` 🔐 - Manejo de variables de entorno.
* `Langchain`, `OpenAI` o `transformers` - Para integración LLM (en `llm_service.py`).
* `Docker` 🐳 - Contenedorización.

---

## 🔐 7. Variables de Entorno

Crea un archivo `.env` con las siguientes claves:

```env
DB_HOST=tu-host-de-aws
DB_PORT=5432
DB_NAME=nombre_de_base
DB_USER=usuario
DB_PASSWORD=contraseña
PORT=5000
```

---

## 🐳 8. Dockerización

### 8.1 `Dockerfile`

### 8.2 Comandos para correr


## ▶️ 9. Cómo Usar la API (modo local)

1. 📥 Clona el repositorio:

   ```bash
   git clone https://github.com/usuario/nombre-del-repo.git
   cd nombre-del-repo
   ```

2. 📦 Instala dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. 🔐 Crea `.env` con tus credenciales.

4. ▶️ Ejecuta la app:

   ```bash
   python app.py
   ```

5. 🌐 Abre en tu navegador:

   ```
   http://localhost:5000
   ```

---

## 💾 10. Estructura de la Base de Datos

Tabla `interacciones`:

| id  | prompt | respuesta |
| --- | ------ | --------- |
| int | text   | text      |


```sql
CREATE TABLE interacciones (
    id SERIAL PRIMARY KEY,
    prompt TEXT,
    respuesta TEXT
);
```

---

## 📦 11. Entregables

* 📁 Código en GitHub.
* 🐳 Imagen Docker en DockerHub: docker pull leireal/mi_api_proyecto:latest
* 📘 Documentación técnica completa.
* 📊 Base de datos con historial de interacciones.

