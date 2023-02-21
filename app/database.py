from . import exporter
import pymongo


cluster = pymongo.MongoClient(exporter.realcluster)

db = cluster[exporter.db_name]

collection = db[exporter.db_collection]