from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_cohere import ChatCohere
from app.core.config import settings

def get_llm():
    """Returns the Cohere Chat Model"""
    llm = ChatCohere(
        model="command-r-08-2024",  #128k context lenght, 4k max output tokens
        cohere_api_key=settings.COHERE_API_KEY,
        temperature=0,
        max_tokens=200
    )
    return llm
