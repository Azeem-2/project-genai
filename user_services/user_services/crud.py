from sqlmodel import Session, select
from user_services.models import User, UserData
from user_services.auth import get_password_hash, verify_password
from user_services.schemas import UserCreate, UserDataCreate
from typing import Optional, List

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def create_user(session: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def create_user_data(session: Session, data: UserDataCreate, user: User) -> UserData:
    user_data = UserData(data=data.data, owner_id=user.id)
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(session, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_user_data(session: Session, user: User) -> List[UserData]:
    statement = select(UserData).where(UserData.owner_id == user.id)
    return session.exec(statement).all()
