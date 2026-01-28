from pymongo import MongoClient
from pymongo.encryption import ClientEncryption
from bson.codec_options import CodecOptions
from bson.binary import STANDARD
import base64
import dotenv
import os
dotenv.load_dotenv()

provider = os.getenv("provider")

kms_provider_credentials = {
    "aws": {
        "accessKeyId": os.getenv("AWS_ACCESS_KEY"),
        "secretAccessKey": os.getenv("AWS_SECRET_KEY")
    }
}

master_key = {
    "region": os.getenv("REGION"),  
    "key": os.getenv("CMK_ARN")     
}

key_vault_namespace = f"{os.getenv("key_vault_db")}.{os.getenv("key_vault_collection")}"

connection_string = os.getenv("MONGO_URI")
if not connection_string:
    raise ValueError("MONGO_URI environment variable not set")

client = MongoClient(connection_string)

client_encryption = ClientEncryption(
    kms_provider_credentials,
    key_vault_namespace,
    client,
    CodecOptions(uuid_representation=STANDARD),
)

data_key_id = client_encryption.create_data_key(provider, master_key)
base64_dek = base64.b64encode(data_key_id).decode()

print("Your Base64 DEK:", base64_dek)
print("Data encryption key created")