import bcrypt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from . import models, responses, ops, database
from app.auth.jwt_bearer import JWTBearer
from app.auth import  jwt_handler




app = FastAPI()




@app.get("/")
async def greet():
    return {"hello":"world"}


@app.post("/signup/creator",tags= ['creator'])
async def creator_signup(signup_details:  models.CreatorSignUp):
    # Checking if email already exists
    email_count =  database.user_collection.count_documents({"email": signup_details.email})
    if email_count > 0:
        return responses.response(False, "duplicated user, email already in use", None)
    # Insert new user
    encoded_password = ops.hash_password(str(signup_details.password))
    signup_details.password = encoded_password
    json_signup_details = jsonable_encoder(signup_details)
    await ops.inserter(json_signup_details)
    return responses.response(True, "inserted", str(json_signup_details))


@app.post("/login/creator",tags=["creator"])
async def login(email: str, password: str):
    # Verify credentials
    if await ops.verify_credentials(email, password):
        return jwt_handler.signJWT(email)
    else:
        raise HTTPException(401, "unauthorised login or email is wrong")



@app.post("/creator/{email}", dependencies=[Depends(JWTBearer())], tags=['creator'])
async def add_job(job_deets: models.JobSchema):
    json_job_deets = jsonable_encoder(job_deets)
    full_profile = ops.find_user_email(job_deets.confirm_email)
    
    # ops.job_inserter(json_job_deets)
    return responses.response(True, "inserter", full_profile)



@app.post('/signup/user', tags= ['user'])
async def user_login(signup_details: models.UserSignUp) :
    email_count =  database.user_collection.count_documents({"email": signup_details.email})
    if email_count > 0:
        return responses.response(False, "duplicated user, email already in use", None)
    # Insert new user
    encoded_password = ops.hash_password(str(signup_details.password))
    signup_details.password = encoded_password
    json_signup_details = jsonable_encoder(signup_details)
    await ops.inserter(json_signup_details)
    return responses.response(True, "inserted", str(json_signup_details))


@app.post("/login/user",tags=["user"])
async def login(email: EmailStr, password: str):
    # Verify credentials
    if await ops.verify_credentials(email, password):
        return responses.response(True, "Logged in", "Hello"+ email)
    else:
        raise HTTPException(401, "unauthorised login")



@app.delete("/collection/", tags=["do not touch"])
async def delete_collection():
    # Delete all documents in the user_collection
    database.user_collection.delete_many({})

    return {"success": True}
