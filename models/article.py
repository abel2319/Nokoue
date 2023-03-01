#!/usr/bin/python3
""" holds class Article"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class Article(BaseModel, Base):
    """Representation of an article"""

    __tablename__ = 'article'
    title = Column(String(128), nullable=False)
    images = Column(String(128), nullable=False)
    content = Column(String(128), nullable=False)
    comment = relationship("Comment", backref="user")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        super().__setattr__(name, value)
