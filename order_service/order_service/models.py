from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from sqlalchemy.orm import relationship

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id", nullable=False)
    product_id: int
    quantity: int
    order: "Order" = Relationship(back_populates="items")

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    total_price: float
    # Use SQLAlchemy's relationship to enable cascading
    items: List[OrderItem] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

# Resolve forward references
Order.model_rebuild()
OrderItem.model_rebuild()
