from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, ForeignKey,Integer, String,DateTime,select,update
from datetime import datetime

from db import Base

class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name  = Column(String(255))
    email = Column(String(255))
    ref_link = Column(String(50),default=None,unique=True)
    coupon = Column(String(50),default=None,unique=True)
    active = Column(Boolean,default=True)
    
class Referral(Base):
    __tablename__ = "referral"

    id = Column(Integer, primary_key=True, index=True)
    ref = Column(Integer,ForeignKey("customer.id"))
    ref_by = Column(Integer,ForeignKey("customer.id"))
    
class Position(Base):
    __tablename__ = "position"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer,ForeignKey("customer.id"))
    position = Column(Integer,default=0)
    admin_priority = Column(Boolean,default=False)
    ref_score  = Column(Integer,default=0)
    created_at = Column(DateTime, default=datetime.now())

class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    name  = Column(String(255))
    email = Column(String(255))
    pwd   = Column(String(400))