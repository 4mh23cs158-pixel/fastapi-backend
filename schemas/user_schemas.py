from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    phonenumber:str


class UserLogin(BaseModel):
    email: EmailStr
    password: str