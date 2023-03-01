#!/usr/bin/python3
""" holds class Message"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class Message(BaseModel, Base):
    """Representation of a message"""

    __tablename__ = 'message'
    content = Column(String(2048), nullable=False)
    user_id = Column(String(128), ForeignKey('users.id'), nullable=False)
    conversation_id = Column(String(128), ForeignKey('conversation.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        super().__setattr__(name, value)
