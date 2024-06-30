from pydantic import BaseModel
from typing import Optional

class InventoryItemCreate(BaseModel):
    product_id: int
    quantity: int

class InventoryItemRead(InventoryItemCreate):
    id: int

class InventoryItemUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
