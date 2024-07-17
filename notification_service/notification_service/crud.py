from sqlmodel import Session, select,delete
from notification_service.models import Notification
from notification_service.schemas import NotificationCreate, NotificationRead
from typing import List

def create_notification(notification: NotificationCreate, session: Session):
    db_notification = Notification(**notification.model_dump())
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification

def get_notifications(session: Session) -> List[Notification]:
    notifications = session.exec(select(Notification)).all()
    return notifications

def get_notification_by_id(notification_id: int, session: Session) -> Notification:
    notification = session.exec(select(Notification).where(Notification.id == notification_id)).first()
    return notification

def delete_notification(notification_id: int, session: Session):
    session.exec(delete(Notification).where(Notification.id == notification_id))
    session.commit()

def update_notification(notification_id: int, notification: NotificationCreate, session: Session):
    db_notification = get_notification_by_id(notification_id, session)
    for key, value in notification.dict().items():
        setattr(db_notification, key, value)
    session.commit()
    session.refresh(db_notification)
    return db_notification


