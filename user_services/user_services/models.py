from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    
    user_data: List["UserData"] = Relationship(back_populates="owner")

class UserData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: str
    owner_id: int = Field(foreign_key="user.id")
    
    owner: User = Relationship(back_populates="user_data")
