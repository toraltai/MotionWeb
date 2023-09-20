from fastapi import APIRouter, HTTPException
from typing import List
from .models import *
from . import schemas


restaurant = APIRouter()


@restaurant.post("/", response_model=schemas.RestaurantShow, response_model_exclude_unset=True)
async def create_restaurant(restaurant: CreateRestaurant):
    try:
        restaurant_obj = await Restaurant.create(
                                                title=restaurant.title,
                                                kitchen=restaurant.kitchen
                                                )
        
        return schemas.RestaurantShow(**restaurant_obj.__dict__)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create restaurant: {str(e)}")
    

@restaurant.get('/', response_model=List[GetRestaurant])
async def get_restaurant():
    rest_objs = await GetRestaurant.from_queryset(Restaurant.all())
    return rest_objs