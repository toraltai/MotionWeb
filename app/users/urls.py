import jwt

from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from .models import *
from .schemas import *

JWT_SECRET='secret'

user_router = APIRouter()


@user_router.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_user(form_data.username, form_data.password)

    if not user:
        return {'error': 'invalid'}
    
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    response = Response()

    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'token': token, 'token_type':'bearer'
    }
    
    return response.data


@user_router.post('/', response_model=User_Pydantic, response_model_exclude_unset=True)
async def create_user(user: CreateUser):
    role = user.role if user.role else "user"
    user_obj = User(first_name=user.first_name, 
                    last_name=user.last_name,
                    email=user.email,
                    role=role,
                    phone_number=user.phone_number,
                    password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)



@user_router.get('/all', response_model=List[User_Pydantic])
async def user_list():
    user_obj = await User_Pydantic.from_queryset(User.all())
    return user_obj