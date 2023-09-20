from fastapi import APIRouter
from .users.urls import user_router
from .restaurant.urls import restaurant


api_router = APIRouter()


api_router.include_router(user_router, prefix='/acc', tags=['users'])
api_router.include_router(restaurant, prefix='/cat', tags=['restaurant'])