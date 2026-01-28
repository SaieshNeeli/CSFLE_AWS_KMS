import os
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv
load_dotenv()
connection_string = os.getenv("MONGODB_URI")
key_vault_db = os.getenv("key_vault_db")
key_vault_coll = os.getenv("key_vault_collection")
client = MongoClient(connection_string)

client[key_vault_db][key_vault_coll].create_index(
    [("keyAltNames", ASCENDING)],
    unique=True,
    partialFilterExpression={"keyAltNames": {"$exists": True}}
)
print("key vault created")