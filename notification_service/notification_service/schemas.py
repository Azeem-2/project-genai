from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificationCreate(BaseModel):
    user_id: int
    message: str
    type: str

class NotificationRead(NotificationCreate):
    id: int
    created_at: datetime
