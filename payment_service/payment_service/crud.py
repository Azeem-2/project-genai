from payment_service.models import Payment
from sqlmodel import Session, select
from typing import List
from payment_service.schemas import PaymentCreate


def create_payment(db: Session, payment: PaymentCreate) -> Payment:
    db_payment = Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payments(db: Session, skip: int = 0, limit: int = 100) -> List[Payment]:
    return db.exec(select(Payment).offset(skip).limit(limit)).all()

def get_payment_by_id(db: Session, payment_id: int) -> Payment:
    return db.get(Payment, payment_id)

def update_payment(db: Session, payment_id: int, payment: PaymentCreate) -> Payment:
    db_payment = db.get(Payment, payment_id)
    if db_payment is None:
        return None
    for key, value in payment.dict(exclude_unset=True).items():
        setattr(db_payment, key, value)
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def delete_payment(db: Session, payment_id: int) -> Payment:
    db_payment = db.get(Payment, payment_id)
    if db_payment is None:
        return None
    db.delete(db_payment)
    db.commit()
    return db_payment
