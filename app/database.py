import os
import pymongo


realcluster = os.environ.get("CLUSTER")
db_name = os.environ.get("DB")
db_collection = os.environ.get("COLLECTION")

cluster = pymongo.MongoClient(realcluster)
db = cluster[db_name]
collection = db[db_collection]