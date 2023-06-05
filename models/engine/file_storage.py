#!/usr/bin/python3
# class FileStorage that serializes instances to a JSON file
# and deserializes JSON file to instances
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os
import datetime


class FileStorage:
    """  serializes and deserializes instances to a JSON file and viceversa """
    __file_path = "file.json"
    __objects = {}
    class_dict = {}

    def all(self):
        """ returns the dictionary __objects """
        return self.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializing __objects to the JSON file."""
        serialized_objects = {}
        for key, obj in self.__objects.items():
            serialized_objects[key] = obj.to_dict()

        with open(self.__file_path, 'w', encoding="utf-8") as f:
            json.dump(serialized_objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        try:
            if os.path.exists(self.__file_path):
                with open(self.__file_path, "r") as f:
                    data = json.load(f)
                    for key, value in data.items():
                        class_name, obj_id = key.split(".")
                        class_obj = eval(class_name)
                        obj = class_obj(**value)
                        self.__objects[key] = obj
        except FileNotFoundError:
            pass
