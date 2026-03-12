#Pydantic models for validating FastAPI Request/Response Data
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
