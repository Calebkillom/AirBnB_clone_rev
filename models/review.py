#!/usr/bin/python3
from models.base_model import BaseModel
# Review class that inherits from BaseClass Model

class Review(BaseModel):
    """ inherits from the BaseClass Model """
    place_id = ""
    user_id = ""
    text = ""
