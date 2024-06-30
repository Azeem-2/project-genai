from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    product_id: int
    quantity: int
    order: 'Order' = Relationship(back_populates="items")

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    items: List[OrderItem] = Relationship(back_populates="order")
    total_price: float

# Resolve forward references
Order.model_rebuild()
OrderItem.model_rebuild()
