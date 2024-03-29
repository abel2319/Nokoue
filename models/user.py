#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy_imageattach.entity import Image, image_attachment
from hashlib import md5


participant = Table('participant', Base.metadata,
                          Column('user_id', String(60),
                                 ForeignKey('user.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                          Column('conversation_id', String(60),
                                 ForeignKey('conversation.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))

class User(BaseModel, Base):
    """Representation of a user """

    __tablename__ = 'users'
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    phone_number = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    city = Column(String(128), nullable=False)
    company_code = Column(String(128), nullable=True)
    company_name = Column(String(128), nullable=True)
    picture = image_attachment('UserPicture')
    article = relationship("Articles", backref="user", cascade="all, delete, delete-orphan")
    comment = relationship("Comments", backref="user", cascade="all, delete, delete-orphan")
    message = relationship("Messages", backref="user")
    participant = relationship("Partipant", secondary=participant, viewonly=False)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)

class UserPicture(Base, Image):
    """User picture model."""
    user_id = Column(String(60), ForeignKey('User.id'), primary_key=True)
    user = relationship('User')
    __tablename__ = 'user_picture'
