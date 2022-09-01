from datetime import datetime
from enum import Enum

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from app.config import DATABASE_URL

Base = declarative_base()

class MessageStatus(Enum):
    PLANED = 'planed'
    ACTIVE = 'active'
    CLOSED = 'closed'


def connect_db():
    engine = create_engine(DATABASE_URL, connect_args={})
    session = Session(bind=engine.connect())
    return session

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    login = Column(String)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(String, default=datetime.utcnow())

class AuthToken(Base):
    __tablename__ = 'auth_token'

    id = Column(Integer, primary_key=True)
    token = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(String, default=datetime.utcnow())

class Contact(Base):
    __tablename__ = 'contact'

    id = Column(Integer, primary_key=True)
    first_id = Column(Integer, ForeignKey('users.id'))
    second_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(String, default=datetime.utcnow())

class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contact.id'))
    send_id = Column(Integer, ForeignKey('users.id'))
    msg = Column(Text)
    status = Column(String, default=MessageStatus.PLANED.value)
    created_at = Column(String, default=datetime.now)

