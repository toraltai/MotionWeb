import jwt

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from .models import *

JWT_SECRET='secret'

user_router = APIRouter()


@user_router.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_user(form_data.username, form_data.password)

    if not user:
        return {'error': 'invalid'}
    
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    return {'access_token':token, 'token_type':'bearer'}


@user_router.post('/', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(first_name=user.first_name, 
                    last_name=user.last_name,
                    email=user.email,
                    phone_number=user.phone_number,
                    password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)


@user_router.get('/all', response_model=List[User_Pydantic])
async def user_list():
    user_obj = await User_Pydantic.from_queryset(User.all())
    return user_obj