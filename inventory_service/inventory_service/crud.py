from sqlmodel import Session, select
from inventory_service.models import InventoryItem
from inventory_service.schemas import InventoryItemCreate, InventoryItemUpdate

def create_inventory_item(session: Session, item: InventoryItemCreate):
    db_item = InventoryItem(**item.dict())
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def get_inventory_item(session: Session, item_id: int):
    return session.get(InventoryItem, item_id)

def get_inventory_items(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(InventoryItem).offset(skip).limit(limit)).all()

def update_inventory_item(session: Session, item_id: int, item: InventoryItemUpdate):
    db_item = session.get(InventoryItem, item_id)
    if not db_item:
        return None
    item_data = item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def delete_inventory_item(session: Session, item_id: int):
    db_item = session.get(InventoryItem, item_id)
    if not db_item:
        return None
    session.delete(db_item)
    session.commit()
    return db_item
