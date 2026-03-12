#Pydantic models for validating FastAPI Request/Response Data
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, Dict, Any

class NutritionRead(BaseModel):
    id: int
    user_id: int
    date: date

    name: str
    description: Optional[str]

    calories: Optional[int]
    protein: Optional[int]
    carbs: Optional[int]
    fat: Optional[int]

    notes: Optional[str]
    metadata: Optional[Dict[str, Any]]

    created_at: datetime
