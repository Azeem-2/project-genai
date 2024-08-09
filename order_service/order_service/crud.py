from order_service.models import Order, OrderItem
from sqlmodel import Session, select
from typing import List, Optional
from order_service.schemas import OrderCreate, OrderItemCreate, OrderUpdate, OrderItemUpdate, OrderVerify

def create_order(db: Session, order: OrderCreate) -> Order:
    db_order = Order(user_id=order.user_id, total_price=order.total_price)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    for item in order.items:
        db_item = OrderItem(**item.model_dump(), order_id=db_order.id)
        db.add(db_item)
    
    db.commit()  # Commit after adding items
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
    return db.exec(select(Order).offset(skip).limit(limit)).all()

def get_order_by_id(db: Session, order_id: int) -> Order:
    return db.get(Order, order_id)

def update_order(db: Session, order_id: int, order: OrderUpdate):
    db_order = db.get(Order, order_id)
    if not db_order:
        return None

    if order.user_id is not None:
        db_order.user_id = order.user_id
    if order.total_price is not None:
        db_order.total_price = order.total_price

    for item_update in order.items:
        db_item = db.get(OrderItem, item_update.id)
        if db_item:
            if item_update.product_id is not None:
                db_item.product_id = item_update.product_id
            if item_update.quantity is not None:
                db_item.quantity = item_update.quantity

    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int) -> Order:
    db_order = db.get(Order, order_id)
    if db_order is None:
        return None
    db.delete(db_order)
    db.commit()
    return db_order

def get_order_items(db: Session, order_id: int) -> List[OrderItem]:
    return db.exec(select(OrderItem).where(OrderItem.order_id == order_id)).all()

def get_order_item_by_id(db: Session, order_id: int, item_id: int) -> OrderItem:
    return db.get(OrderItem, item_id)

def update_order_item(db: Session, order_id: int, item_id: int, item: OrderItemUpdate) -> OrderItem:
    db_item = db.get(OrderItem, item_id)
    if db_item is None:
        return None
    if item.product_id is not None:
        db_item.product_id = item.product_id
    if item.quantity is not None:
        db_item.quantity = item.quantity
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_order_item(db: Session, order_id: int, item_id: int) -> OrderItem:
    db_item = db.get(OrderItem, item_id)
    if db_item is None:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

# Function to verify an order based on user ID and total price
def verify_order(db: Session, order: OrderVerify) -> Optional[Order]:
    return db.exec(select(Order).where(Order.user_id == order.user_id, Order.total_price == order.total_price)).first()

# Function to delete an order based on user ID
def delete_order_by_user_id(db: Session, user_id: int) -> Optional[Order]:
    db_order = db.exec(select(Order).where(Order.user_id == user_id)).first()
    if db_order is None:
        return None
    db.delete(db_order)
    db.commit()
    return db_order

# Function to delete an order based on user ID and total price
def delete_order_by_user_id_and_total_price(db: Session, user_id: int, total_price: float) -> Optional[Order]:
    db_order = db.exec(select(Order).where(Order.user_id == user_id, Order.total_price == total_price)).first()
    if db_order is None:
        return None
    db.delete(db_order)
    db.commit()
    return db_order

# Function to get an order based on user ID and total price
def get_order_by_user_id_and_total_price(db: Session, user_id: int, total_price: float) -> Optional[Order]:
    return db.exec(select(Order).where(Order.user_id == user_id, Order.total_price == total_price)).first()
