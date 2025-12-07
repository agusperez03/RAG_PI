from app.services.vector_store import get_collection
from app.services.llm_service import get_llm
from app.services.embeddings import get_embeddings_cohere
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime

PROMPT_TEMPLATE = """Eres un asistente experto que responde preguntas basándote ÚNICAMENTE en el contexto proporcionado.

REQUISITOS OBLIGATORIOS:
1. Responde en EXACTAMENTE UNA ORACIÓN (no más, no menos)
2. Responde en el MISMO IDIOMA que la ultima pregunta realizada (español, inglés o portugués)
3. SIEMPRE escribe en TERCERA PERSONA (nunca uses "yo", "tú", "nosotros")
4. Incluye 1-3 emojis relevantes que resuman el contenido
5. Sé preciso y conciso

CONTEXTO:
{context}

INSTRUCCIONES ADICIONALES:
- Si la pregunta actual está en español, responde en español
- Si la pregunta actual está en inglés, responde en inglés
- Si la pregunta actual está en portugués, responde en portugués
- Usa SOLO información del contexto proporcionado
- Nunca uses primera o segunda persona
- La respuesta debe ser una oración completa y gramaticalmente correcta

EJEMPLO DE PREGUNTAS Y RESPUESTAS:

Pregunta: Quien es Zara?
Respuesta: Zara es un intrépido explorador que emprende una misión crucial para evitar la guerra intergaláctica en Zenthoria. 🌌🛡️🤝

Pregunta: What did Emma decide to do?
Respuesta: Emma decided to share her gift with the town, leaving an indelible mark on the heart of each inhabitant. ❤️🎁✨

PREGUNTA ACTUAL DEL USUARIO:
{question}

RESPUESTA (una sola oración con emojis):"""

async def generate_answer(question: str, user_name: str) -> dict:
    """
    Genera respuesta usando RAG
    """
    # 1. Search relevant chunk
    collection = get_collection()
    embeddings_service = get_embeddings_cohere()
    
    query_embedding = embeddings_service.embed_query(question)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )
    
    if results['documents'] and results['documents'][0]:
        context = results['documents'][0][0]
        chunk_id = results['ids'][0][0]
    else:
        context = ""
        chunk_id = "none"
        
    # 2. Construct prompt
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    formatted_prompt = prompt.format_prompt(context=context, question=question).to_messages()
    
    # 3. Generate answer
    llm = get_llm()
    response = llm.invoke(formatted_prompt)
    answer = response.content.strip()
    
    # 4. Return response
    return {
        "user_name": user_name,
        "question": question,
        "answer": answer,
        "chunk_used": chunk_id,
        "timestamp": datetime.now().isoformat()
    }
