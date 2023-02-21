from bson import ObjectId
import database
from responses import response as r

async def inserter(metadata):
    database.collection.insert_one(metadata)
    return r(True,"inserted successfully",metadata)

def deleter(id):
    database.collection.delete_one({'_id':ObjectId(id)})
    return r(True, "deleted", None)

def get_all_data():
    response =database.collection.find({})
    return list(response)