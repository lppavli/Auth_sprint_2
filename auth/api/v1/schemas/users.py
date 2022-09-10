from datetime import datetime
from pydantic import BaseModel, UUID4


class UserBase(BaseModel):
    login: str
    password: str
    email: str


class UserCreate(UserBase):
    pass


class UserLogin(UserBase):
    pass


class UserModel(UserBase):
    id: UUID4
    is_superuser: bool


class History(BaseModel):
    user_agent: str
    ip_address: str
    auth_datetime: datetime


class PasswordChange(BaseModel):
    old_password: str
    new_password: str
