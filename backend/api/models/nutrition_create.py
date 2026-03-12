#Pydantic models for validating FastAPI Request/Response Data
from pydantic import BaseModel
from datetime import date
from typing import Optional, Dict, Any

class NutritionCreate(BaseModel):
    user_id: int
    date: date

    name: str
    description: Optional[str] = None

    calories: Optional[int] = None
    protein: Optional[int] = None
    carbs: Optional[int] = None
    fat: Optional[int] = None

    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
