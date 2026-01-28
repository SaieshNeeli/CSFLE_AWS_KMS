MongoDB CSFLE with AWS KMS (Python)

This repository demonstrates MongoDB Client-Side Field Level Encryption (CSFLE) using AWS KMS as the Key Management Service.

It shows how to:

Configure AWS KMS

Create a Data Encryption Key (DEK)

Store encryption metadata in MongoDB Key Vault

Automatically encrypt and decrypt sensitive fields on the client side

✅ No plaintext sensitive data is stored in MongoDB
✅ Encryption & decryption happen entirely on the client

🧠 Why CSFLE with AWS KMS?

Protects PII / sensitive data (health, financial, identity)

Encryption keys are never exposed to the database

AWS KMS provides:

Centralized key management

Audit logs (CloudTrail)

Key rotation

Compliance readiness (PCI, HIPAA, SOC)

📁 Project Structure

aws_csfle/
│
├── automatic_csfle.py        # Automatic encryption & decryption
├── dke_from_aws_kms.py       # Create Data Encryption Key (DEK)
├── key_vault_db.py           # Key vault database & collection setup
├── requirements.txt
├── .env.example              # Environment variable template
│
└── CSFLE_AWS_KMS/
    └── README.md


Prerequisites

Python 3.9+

MongoDB 6.0+ (Atlas or self-hosted)

AWS Account with KMS access

An AWS Customer Managed Key (CMK)

 Step 1: AWS KMS Setup

Go to AWS Console → KMS

Create a Customer Managed Key (Symmetric)

Note down the Key ARN

AWS documentation (official):
 https://www.mongodb.com/docs/manual/core/queryable-encryption/fundamentals/kms-providers/#std-label-qe-fundamentals-kms-providers-aws

Step 2: Environment Variables

Create a .env file using the .env.example that i have uploded in the project repo

Step 3: Create Key Vault

MongoDB stores encryption metadata in a key vault collection.

python key_vault_db.py
This initializes:
__keyVault.__keyVaultCollection

Step 4: Create Data Encryption Key (DEK)

The DEK is encrypted using the AWS KMS CMK.

python dke_from_aws_kms.py

The generated dek_id is used for field encryption
Store it securely (env variable)

Step 5: Automatic Encryption & Decryption

Run:

python automatic_csfle.py

This script:

Encrypts sensitive fields automatically before insert

Transparently decrypts data during read

Requires no manual crypto logic

Example Use Case

Sensitive fields like:

Patient name

Aadhaar / PAN

Phone number

Medical details

are encrypted before reaching MongoDB.

MongoDB only sees ciphertext, not plaintext.