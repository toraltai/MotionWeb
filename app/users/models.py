from fastapi.security import OAuth2PasswordBearer
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from tortoise import fields
from enum import Enum

from passlib.hash import bcrypt


class Role(str, Enum):
    owner = 'owner'
    user = 'user'
    admin = 'admin'


class User(Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(25)
    last_name = fields.CharField(25)
    email = fields.CharField(40, unique=True)
    role = fields.CharEnumField(Role)
    phone_number = fields.CharField(16, unique=True)
    password_hash = fields.CharField(128)


    @classmethod
    async def get_user(cls, first_name, last_name):
        user = await cls.filter(first_name=first_name, last_name=last_name)
        return user
    
    def verify_pass(self, passowrd):
        return bcrypt.verify(passowrd, self.password_hash)


User_Pydantic = pydantic_model_creator(User, name="Users", exclude=['password_hash'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def auth_user(email: str, password:str):
    user = await User.get(email=email)
    if not user:
        return False
    if not user.verify_pass(password):
        return False
    return user
