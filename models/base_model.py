#!/usr/bin/python3
# class BaseModel that defines all common attributes/methods for other classes
import uuid
from datetime import datetime
import models


class BaseModel:
    """ defines all common attributes/methods for other classes """
    def __init__(self, *args, **kwargs):
        """Initializes the BaseModel instance"""
        if kwargs:
            kwargs.pop('__class__', None)
            for key, value in kwargs.items():
                setattr(self, key, value)
                if key == 'created_at' or key == 'updated_at':
                    if isinstance(value, str):
                        setattr(self, key, datetime
                                .strptime(value, '%Y-%m-%dT%H:%M:%S.%f'))

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        return "[{}]({}){}".format(
            type(self).__name__, self.id, self.__dict__)

    def save(self):
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        data_dict = self.__dict__.copy()
        data_dict['__class__'] = self.__class__.__name__

        data_dict["created_at"] = data_dict["created_at"].isoformat()
        data_dict["updated_at"] = data_dict["updated_at"].isoformat()
        return data_dict
