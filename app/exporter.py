import os
from dotenv import load_dotenv
load_dotenv()

realcluster = os.environ.get("CLUSTER")
db_name = os.environ.get("DB")
db_collection = os.environ.get("COLLECTION")

