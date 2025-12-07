from langchain_cohere import CohereEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings

def get_embeddings():
    """Returns the Google Generative AI Embeddings model"""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=settings.GOOGLE_API_KEY
    )
    return embeddings

def get_embeddings_cohere():
    """Returns the Cohere Embeddings model"""
    embeddings = CohereEmbeddings(
        model="embed-multilingual-v3.0",
        cohere_api_key=settings.COHERE_API_KEY
    )
    return embeddings