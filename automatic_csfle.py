from pymongo import MongoClient
from pymongo.encryption_options import AutoEncryptionOpts
from bson.binary import  UUID_SUBTYPE, Binary
import base64
import os
import dotenv

def setup_csfle():
    dotenv.load_dotenv()
    
    connection_string = os.getenv("MONGO_URI")
    kms_provider_credentials = {
        "aws": {
            "accessKeyId": os.getenv("AWS_ACCESS_KEY"),
            "secretAccessKey": os.getenv("AWS_SECRET_KEY")
        }
    }
    key_vault_db = os.getenv("key_vault_db")
    key_vault_coll = os.getenv("key_vault_collection")
    key_vault_namespace = f"{key_vault_db}.{key_vault_coll}"
    
    dek_id = os.getenv("dek_id")
    try:
        data_key_id = Binary(base64.b64decode(dek_id), UUID_SUBTYPE)
    except Exception as e:
        raise ValueError(f"Invalid Base64 DEK: {e}")
    
    json_schema = {
        "bsonType": "object",
        "encryptMetadata": {
        "keyId": [data_key_id]
        },
        "properties": {
            "patient_id":{
                "encrypt": {
                "bsonType": "string",
                "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
                }
            },
            "name": {
                "encrypt": {
                "bsonType": "string",
                "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
                }
            }
        }
    }
    
    
    patient_schema = {f"{os.getenv('patient_db')}.{os.getenv('patient_collection')}": json_schema}  
    CRYPT_LIB_PATH_TEST = r"C:\Users\SaiSivaPrakashNeeli\OneDrive - Kodefast\Desktop\git\CSFLE\crypt_file\mongo_crypt_v1.dll"  
    
    # Use different encryption options based on environment
    if os.getenv('ENVIRONMENT', 'local').lower() == 'deployment':
        auto_encryption_opts = AutoEncryptionOpts(
            kms_providers=kms_provider_credentials,
            key_vault_namespace=key_vault_namespace,
            schema_map=patient_schema,
            mongocryptd_bypass_spawn=True
        )
    else:  # local development
        extra_options = {
            "crypt_shared_lib_path": CRYPT_LIB_PATH_TEST
        }
        auto_encryption_opts = AutoEncryptionOpts(
            kms_provider_credentials,
            key_vault_namespace,
            schema_map=patient_schema,
            **extra_options
        )
   
    secure_client = MongoClient(connection_string, auto_encryption_opts=auto_encryption_opts)
 
    return secure_client

secure_client = setup_csfle()
patient_coll = secure_client[os.getenv("patient_db")][os.getenv("patient_collection")]
print("Secure connection to db collection established")
result = patient_coll.insert_one({
    "patient_id": "123456",
    "name": "John Doe"
})
print("\nEncrypted document inserted into the collection\n")

print(result.inserted_id)
print("\nEncrypted document fetched from the collection:\n")
print(patient_coll.find_one(result.inserted_id))

general_client = MongoClient(os.getenv("MONGO_URI"))
patient_coll_unencrypted = general_client[os.getenv("patient_db")][os.getenv("patient_collection")]
print("\nUnencrypted document fetched from the collection:\n")
print(patient_coll_unencrypted.find_one(result.inserted_id))