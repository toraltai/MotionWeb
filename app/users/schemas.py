from pydantic import BaseModel
from .models import *

class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password_hash: str
    role: Role = "user"