from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    message: str
    type: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
