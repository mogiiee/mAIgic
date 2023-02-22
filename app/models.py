from pydantic import BaseModel


class CreatorSignUp(BaseModel) :
    _id:0
    first_name: str
    last_name: str
    email: str
    password:str
    creator =  "yes"



class UserSignUp(BaseModel) :
    _id:0
    first_name: str
    last_name: str
    email: str
    password:str
    creator =  "no"

class LoginSchema(BaseModel):
    email :str
    password:str

class JobSchema(BaseModel):
    position: str
    stipend: float
    company: str
    description: str
    qualification: str
    experience: str
    confirm_email: str