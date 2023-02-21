from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from . import models, responses, ops

app = FastAPI()




@app.get("/")
async def greet():
    return {"hello":"world"}


@app.post('/inserter')
async def inserter(signup_details: models.UserSignUp) :
    json_signup_details = jsonable_encoder(signup_details)
    print(json_signup_details)
    await ops.inserter(json_signup_details)
    return responses.response(True, "inserted", str(json_signup_details))

