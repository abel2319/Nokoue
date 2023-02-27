#!/usr/bin/python3
"""Base for all classes"""
import uuid
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


class BaseModel:
    """Class BaseModel
    """

     id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization
        Args:
            args (list):
            kwargs (dict):
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
        else:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ('created_at', 'updated_at'):
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)

    def __str__(self):
        """string representation the base
        """
        return ("[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__))

    def save(self):
        """updates the public instance attribute updated_at
        with the current datetime
        """
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        '''function that returns a dictionary containing all keys/values
        of __dict__ of the instance
        '''
        ins_dict = self.__dict__.copy()
        ins_dict['__class__'] = type(self).__name__
        ins_dict['created_at'] = self.__dict__['created_at'].isoformat()
        ins_dict['updated_at'] = self.__dict__['updated_at'].isoformat()
        return (ins_dict)

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
