from pydantic import BaseModel
from datetime import datetime

class UserRead(BaseModel):
    id: int
    username: str
    created_at: datetime
