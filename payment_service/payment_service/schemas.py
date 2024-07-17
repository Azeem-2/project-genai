from sqlmodel import SQLModel
from typing import Optional

class PaymentBase(SQLModel):
    order_id: int
    amount: float
    status: str

class PaymentCreate(PaymentBase):
    pass

class PaymentList(PaymentBase):
    id: int

class PaymentDetail(PaymentBase):
    id: int

class PaymentResponse(PaymentBase):
    id: int
    client_secret: Optional[str] = None  # Ensure this field is included
