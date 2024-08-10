from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from sqlalchemy.orm import relationship

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id", nullable=False)
    product_id: int
    quantity: int
    order: Optional["Order"] = Relationship(back_populates="items")

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    total_price: float
    items: List["OrderItem"] = Relationship(back_populates="order")

# Resolve forward references
Order.model_rebuild()
OrderItem.model_rebuild()

# Add cascading behavior using SQLAlchemy's relationship
Order.items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
