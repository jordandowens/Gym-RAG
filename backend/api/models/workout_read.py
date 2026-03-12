#Pydantic models for validating FastAPI Request/Response Data
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, Dict, Any

class WorkoutRead(BaseModel):
    id: int
    user_id: int
    date: date
    workout_text: str
    energy_level: Optional[int]
    notes: Optional[str]
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
