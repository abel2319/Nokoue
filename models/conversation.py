u#!/usr/bin/python3
""" holds class Conversation"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class Conversation(BaseModel, Base):
    """Representation of a conversation"""

    __tablename__ = 'comment'
    content = Column(String(1024), nullable=False)
    user_id = Column(String(128), ForeignKey('users.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
