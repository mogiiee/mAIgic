from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from schemas import *
import responses
import ops
app = FastAPI()




@app.get("/")
async def greet():
    return {"hello":"world"}


@app.post('/inserter')
async def inserter(signup_details: UserSignUp) -> dict:
    json_signup_details = jsonable_encoder(signup_details)
    when_done =  ops.inserter(json_signup_details)
    return responses.response(True, "inserted", when_done)




