from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from tortoise import fields
from passlib.hash import bcrypt


class User(Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(25)
    last_name = fields.CharField(25)
    email = fields.CharField(40, unique=True)
    phone_number = fields.CharField(16, unique=True)
    password_hash = fields.CharField(128)

    @classmethod
    async def get_user(cls, first_name, second_name):
        return cls.get(first_name=first_name, second_name=second_name,)
    
    def verify_pass(self, passowrd):
        return bcrypt.verify(passowrd, self.password_hash)


User_Pydantic = pydantic_model_creator(User, name="Users")
UserIn_Pydantic = pydantic_model_creator(User, name="UsersIn", exclude_readonly=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def auth_user(email: str, password:str):
    user = await User.get(email=email)
    if not user:
        return False
    if not user.verify_pass(password):
        return False
    return user