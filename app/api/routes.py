from fastapi import APIRouter, HTTPException, Request
from app.api.models import QuestionRequest, QuestionResponse
from app.core.rag_engine import generate_answer
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Endpoint principal para hacer preguntas al documento.
    """
    try:
        logger.info(f"Received question from {request.user_name}: {request.question}")
        
        result = await generate_answer(
            question=request.question, 
            user_name=request.user_name
        )
        
        return QuestionResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
