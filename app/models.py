from pydantic import BaseModel, EmailStr


class UserSignUp(BaseModel) :
    _id:0
    name: str
    email: EmailStr
    password:str
    age: int
