import pymongo
import os
import dotenv

dotenv.load_dotenv()

query_str = "?retryWrites=true&w=majority"


def get_mongo_client():
    myclient = pymongo.MongoClient(os.getenv("MONGO_PROTOCOL") + os.getenv("MONGO_USER") + ":" + os.getenv("MONGO_PWD") + os.getenv("MONGO_URI") + os.getenv("MONGO_DB") + query_str)
    return myclient