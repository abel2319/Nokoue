#!/usr/bin/python3
""" holds class Article"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment
from hashlib import md5


class Article(BaseModel, Base):
    """Representation of an article"""

    __tablename__ = 'articles'
    title = Column(String(128), nullable=False)
    images = image_attachment('PostPhoto', uselist=True)
    content = Column(String(128), nullable=False)
    comment = relationship("Comment", backref="user")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        super().__setattr__(name, value)


class PostPhoto(Base, Image):
    """Photo contained by post."""
    post_id = Column(String(60), ForeignKey(Article.id), primary_key=True)
    post = relationship(Article)
    order_index = Column(Integer, primary_key=True) # least is first
    __tablename__ = 'post_photo'