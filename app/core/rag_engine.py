from app.services.vector_store import get_collection
from app.services.llm_service import get_llm
from app.services.embeddings import get_embeddings_cohere
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime

from app.core.prompts import RAG_PROMPT_TEMPLATE, TRANSLATION_PROMPT_TEMPLATE

async def generate_answer(question: str, user_name: str) -> dict:
    """
    Generates response using RAG
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
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    formatted_prompt = prompt.format_prompt(
        context=context, 
        question=question
    ).to_messages()
    
    # 3. Generate answer
    llm = get_llm()
    response = llm.invoke(formatted_prompt)
    initial_answer = response.content.strip()

    # 4. Translate answer
    translation_prompt = ChatPromptTemplate.from_template(TRANSLATION_PROMPT_TEMPLATE)
    formatted_translation_prompt = translation_prompt.format_prompt(
        question=question,
        text=initial_answer
    ).to_messages()
    
    translation_response = llm.invoke(formatted_translation_prompt)
    answer = translation_response.content.strip()
    
    # 4. Return response
    return {
        "user_name": user_name,
        "question": question,
        "answer": answer,
        "chunk_used": chunk_id,
        "timestamp": datetime.now().isoformat()
    }
