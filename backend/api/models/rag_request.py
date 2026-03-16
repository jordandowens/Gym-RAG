#RAG Request Model
from pydantic import BaseModel
class RAGRequest(BaseModel):
    query: str
    user_id: int