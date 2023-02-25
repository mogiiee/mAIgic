import copy
from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from . import models, responses, ops, database
from app.auth.jwt_bearer import JWTBearer
from app.auth import jwt_handler
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [""]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

@app.get("/")
async def greet():
    return {"hello": "world"}


@app.post("/signup/creator", tags=["creator"])
async def creator_signup(signup_details: models.CreatorSignUp):
    # Checking if email already exists
    email_count = database.user_collection.count_documents(
        {"email": signup_details.email}
    )
    if email_count > 0:
        return responses.response(False, "duplicated user, email already in use", None)
    # Insert new user
    encoded_password = ops.hash_password(str(signup_details.password))
    signup_details.password = encoded_password
    json_signup_details = jsonable_encoder(signup_details)
    await ops.inserter(json_signup_details)
    return responses.response(True, "inserted", str(json_signup_details))


@app.post("/login/creator", tags=["creator"])
async def login(email: str, password: str):
    # Verify credentials
    if await ops.verify_credentials(email, password):
        return jwt_handler.signJWT(email)
    else:
        raise HTTPException(401, "unauthorised login or email is wrong")


@app.post("/creator/add_job", dependencies=[Depends(JWTBearer())], tags=["creator"])
async def add_job(job_deets: models.JobSchema):
    json_job_deets = jsonable_encoder(job_deets)
    email = job_deets.confirm_email
    full_profile = await ops.find_user_email(email)
    creator_user_attributes = full_profile["creator_attributes"]
    original_attributes = copy.deepcopy(full_profile["creator_attributes"])
    creator_user_attributes.append(json_job_deets)

    ops.creator_attributes_updater(original_attributes,creator_user_attributes)

    ops.job_inserter(json_job_deets)
    return responses.response(True, "job posted!", str(full_profile) and json_job_deets)


@app.post("/signup/user", tags=["user"])
async def user_signup(signup_details: models.UserSignUp):
    email_count = database.user_collection.count_documents(
        {"email": signup_details.email}
    )
    if email_count > 0:
        return responses.response(False, "duplicated user, email already in use", None)
    # Insert new user
    encoded_password = ops.hash_password(str(signup_details.password))
    signup_details.password = encoded_password
    json_signup_details = jsonable_encoder(signup_details)
    await ops.job_inserter(json_signup_details)
    return responses.response(True, "inserted", str(json_signup_details))


@app.post("/login/user", tags=["user"])
async def login(email: str, password: str):
    # Verify credentials
    if await ops.verify_credentials(email, password):
        return jwt_handler.signJWT(email)
    else:
        raise HTTPException(401, "unauthorised login or email is wrong")

@app.post("/user/add_job", dependencies=[Depends(JWTBearer())], tags=["user"])
async def add_job(registeration_deets: models.RegisterForJob):
    json_registeration_deets = jsonable_encoder(registeration_deets)
    user_email = registeration_deets.comfirm_email
    user_full_profile = await ops.find_user_email(user_email)
    creator_email = registeration_deets.course_owner_email
    if ops.creator_or_user(creator_email):
        user_attributes = user_full_profile["user_attributes"]
        original_attributes = copy.deepcopy(user_attributes)
        user_attributes.append(json_registeration_deets)
        ops.user_attributes_updater(original_attributes,user_attributes)


        full_creator_profile = await ops.find_user_email(creator_email)
        registered_users = full_creator_profile["registered_users"]
        original_attributes = copy.deepcopy(full_creator_profile["registered_users"])
        registered_users.append(user_full_profile)

        


        return responses.response(True, "course added!", str(full_profile) and json_registeration_deets)


    else: 
        return responses.response(False, "creator email is wrong", str(creator_email) )










@app.delete("/collection/", tags=["do not touch"])
async def delete_collection():
    # Delete all documents in the user_collection
    database.user_collection.delete_one({})

    return {"success": True}

@app.get('/get_user')
async def find_user_email(email):
    user = database.user_collection.find_one({"email": email})
    print(user)
    if not user:
        return responses.response(False, "does not exist", email)
    return str(user)

