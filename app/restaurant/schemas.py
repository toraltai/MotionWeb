from pydantic import BaseModel
from .models import *


class Menu(BaseModel):
    title: str


class RestaurantShow(BaseModel):
    id: int
    title: str
    kitchen: Kitchen


class RestaurantCreate(RestaurantShow):
    pass