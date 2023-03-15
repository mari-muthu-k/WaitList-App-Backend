from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, ForeignKey,Integer, String,DateTime,select,update
from datetime import datetime

from db import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    Name  = Column(String(255))
    email = Column(String(255))
    password = Column(String(1000))
    uid      = Column(String(30),unique=True)
    ip = Column(String(255))
    last_updated = Column(DateTime, default=datetime.now(),onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.now())