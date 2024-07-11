from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Float,DateTime,Date
from sqlalchemy.orm import relationship
from enum import Enum
from .database import Base
from datetime import date




class Dept(Base):
    __tablename__='depts'
    id = Column(Integer,primary_key=True)
    dept_type = Column(String,nullable=False)
    first_name=Column(String(15),index=True)
    day = Column(Integer)
    last_name=Column(String(15),index=True)
    price_dept = Column(Float,index=True)
    type_curr = Column(String,nullable=False)
    description = Column(String,index=True)
    from_time = Column(Date, default=date.today())
    to_time = Column(Date)
    paid=Column(Boolean,default=False)
