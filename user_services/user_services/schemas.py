from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    email: str

class UserDataCreate(BaseModel):
    data: str

class UserDataRead(BaseModel):
    id: int
    data: str
    owner_id: int

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    access_token: str
    token_type: str