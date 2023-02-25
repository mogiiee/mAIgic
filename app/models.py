from pydantic import BaseModel


class CreatorSignUp(BaseModel):
    _id: 0
    first_name: str
    last_name: str
    email: str
    password: str
    creator = "yes"
    creator_attributes =[] 
    registered_students= []




class UserSignUp(BaseModel):
    _id: 0
    first_name: str
    last_name: str
    email: str
    password: str
    creator = "no"
    user_attributes = []
    registered_courses= []


class LoginSchema(BaseModel):
    email: str
    password: str


class JobSchema(BaseModel):
    confirm_email: str
    position: str
    stipend: float
    title: str
    company: str
    description: str
    qualification: str
    experience: str
    creator= "yes"
    link:str
    tags_of_course: str
    registered_students = []


class RegisterForJob(BaseModel):
    comfirm_email: str
    course_title: str
    course_owner_email :str
    creator =  "no"

