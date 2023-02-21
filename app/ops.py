from bson import ObjectId
from . import database
from . import responses

async def inserter(metadata: dict):
    database.collection.insert_one(metadata)
    return responses.response(True, "inserted successfully" ,metadata)

def deleter(id):
    database.collection.delete_one({'_id':ObjectId(id)})
    return responses.response(True, "deleted", None)
