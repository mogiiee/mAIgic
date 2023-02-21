from pydantic import BaseModel


class UserSignUp(BaseModel) :
    name: str
    email: str
    password:str
    age: int
