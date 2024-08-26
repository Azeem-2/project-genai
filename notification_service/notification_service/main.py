from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from notification_service import schemas, crud, notifications
from notification_service.db import create_db_and_tables, get_session
from typing import List
from contextlib import asynccontextmanager
import asyncio
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from notification_service.kafka import notification_pb2
from notification_service.kafka.producer import NOTIFICATION_TOPIC, KafkaProducer, get_kafka_producer

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_db_and_tables()
        yield
    finally:
        pass

app: FastAPI = FastAPI(lifespan=lifespan)

@app.post("/notification/", response_model=schemas.NotificationRead)
async def create_notification(notification: schemas.NotificationCreate, session: Session = Depends(get_session), kafka_producer: KafkaProducer = Depends(get_kafka_producer)):
    db_notification = crud.create_notification(notification, session)
    notification_message = notification_pb2.NotificationCreate(
        user_id=db_notification.user_id,
        message=db_notification.message,
        type=db_notification.type
    )
    await kafka_producer.send(NOTIFICATION_TOPIC, notification_message)
    
    try:
        if db_notification.type == "email":
            notifications.send_email_notification(
                to_email="hassankhan13351@gmail.com",  # Replace with the actual user's email
                subject="Notification Subject",
                message=db_notification.message
            )
        elif db_notification.type == "sms":
            notifications.send_sms_notification(
                to_phone="+14158147533",  # Replace with the actual user's phone number
                message=db_notification.message
            )
        return db_notification
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")
        raise HTTPException(status_code=500, detail="Failed to send notification")


@app.get("/notification/", response_model=List[schemas.NotificationRead])
def get_notifications(session: Session = Depends(get_session)):
    return crud.get_notifications(session)

@app.get("/notification/{notification_id}", response_model=schemas.NotificationRead)
def get_notification(notification_id: int, session: Session = Depends(get_session)):
    notification = crud.get_notification_by_id(notification_id, session)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@app.delete("/notification/{notification_id}")
def delete_notification(notification_id: int, session: Session = Depends(get_session)):
    crud.delete_notification(notification_id, session)
    return {"message": "Notification deleted successfully"}

@app.put("/notification/{notification_id}", response_model=schemas.NotificationRead)
def update_notification(notification_id: int, notification: schemas.NotificationCreate, session: Session = Depends(get_session)):
    return crud.update_notification(notification_id, notification, session)
