from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from tortoise import fields
from enum import Enum


class Kitchen(str, Enum):
    italian = "Italian"
    mexican = "Mexican"
    chinese = "Chinese"
    indian = "Indian"


# class Menu(Model):
#     id = fields.IntField(pk=True)
#     title = fields.CharField(50, unique=True)


class Restaurant(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(50, unique=True)
    kitchen = fields.CharEnumField(Kitchen)


###Pydantic
GetRestaurant = pydantic_model_creator(Restaurant, name="Restaurnts")
CreateRestaurant = pydantic_model_creator(Restaurant, name="RestaurntsIn", exclude_readonly=True)


# {
#     "title":"Barashek",
#     "menu":[{"category:"[{
#                           "первое":[],
#                           "второе":[],
#                           "напитки":[]
#                           }]
#             }]
# }