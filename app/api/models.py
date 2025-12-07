from pydantic import BaseModel
from typing import Optional

class QuestionRequest(BaseModel):
    user_name: str
    question: str

class QuestionResponse(BaseModel):
    user_name: str
    question: str
    answer: str
    chunk_used: str
    timestamp: str
