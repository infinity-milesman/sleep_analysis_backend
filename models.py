import uuid
import random

from sqlalchemy import Column, Date, DateTime, Float, Integer, String, text, Boolean, REAL, NUMERIC
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.ext.declarative import declarative_base
import hashlib

from main import db

def generate_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    __tablename__ = 'user_tbl'

    id = Column(Integer, primary_key=True)
    uuid = Column(String, name='uuid',default=generate_uuid())
    first_name = Column(String(50), name='user_firstname')
    last_name = Column(String(50), name='user_lastname')
    email = Column(String(100), name='user_email')
    mobile = Column(String(12), name='user_mobile')
    dob = Column(String(20), name='user_dob')
    gender = Column(String(2), name='user_gender')
    pic_url = Column(String(200000), name='user_profile_pic_url')
    create_dttm = Column(DateTime(True), server_default=text("now()"), name='user_create_dttm')
    password = Column(String(64), name='password')





