# RAG System with LangChain, Cohere & ChromaDB

## Descripción
Sistema RAG que permite hacer preguntas sobre un documento y obtener respuestas contextuales usando Cohere.

## Requisitos Previos
- Python 3.11+
- Cohere API Key
- Git

## Instalación Local

### 1. Clonar repositorio
git clone <repo-url>
cd rag_project

### 2. Crear entorno virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

### 3. Instalar dependencias
pip install -r requirements.txt

### 4. Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar COHERE_API_KEY

### 5. Inicializar ChromaDB
python -m app.utils.document_processor

### 6. Correr API
uvicorn app.main:app --reload

## Instalación con Docker

docker build -t rag-api .
docker run -p 8000:8000 --env-file .env rag-api

## Uso

### Endpoint: POST /ask

**Request:**
{
  "user_name": "John Doe",
  "question": "Quien es Zara?"
}

**Response:**
{
  "user_name": "John Doe",
  "question": "Quien es Zara?",
  "answer": "Zara es una exploradora intrépida que descubre un antiguo artefacto capaz de traer paz a la galaxia Zenthoria 🚀✨🌌",
  "chunk_used": "chunk_1",
  "timestamp": "2024-01-15T10:30:00"
}

## Testing con Postman
Importar `postman_collection.json` incluido en el repositorio.
