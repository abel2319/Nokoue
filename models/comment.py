#!/usr/bin/python3
""" holds class Comment"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class Comment(BaseModel, Base):
    """Representation of a comment"""

    __tablename__ = 'comment'
    content = Column(String(1024), nullable=False)
    user_id = Column(String(128), ForeignKey('users.id'), nullable=False)
    article_id = Column(String(128), ForeignKey('article.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        super().__setattr__(name, value)
