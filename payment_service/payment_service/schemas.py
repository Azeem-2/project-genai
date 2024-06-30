from sqlmodel import Field, SQLModel
from typing import List, Optional

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
