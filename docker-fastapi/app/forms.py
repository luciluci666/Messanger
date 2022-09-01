from typing import Optional
from pydantic import BaseModel

class UserLoginForm(BaseModel):
    login: str
    password: str

class UserCreateForm(BaseModel):
    email: str
    login: str
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class CreateContact(BaseModel):
    token: str
    friend_login: str
 
class CreateMessage(BaseModel):
    token: str
    contact_id: int
    message: str





 