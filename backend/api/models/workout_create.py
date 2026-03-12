#Pydantic models for validating FastAPI Request/Response Data
from pydantic import BaseModel
from datetime import date
from typing import Optional, Dict, Any

class WorkoutCreate(BaseModel):
    user_id: int
    date: date
    workout_text: str
    energy_level: Optional[int] = None
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
