# MongoDB CSFLE with AWS KMS (Python)

This repository demonstrates MongoDB Client-Side Field Level Encryption (CSFLE) using AWS Key Management Service (KMS).

The project supports both local Windows development and Linux-based deployment using Docker, while ensuring that sensitive data is always encrypted on the client side before being stored in MongoDB.

---

## Overview

This project shows how to:

- Configure AWS KMS for CSFLE
- Create a Data Encryption Key (DEK)
- Store encryption metadata in the MongoDB key vault
- Automatically encrypt and decrypt sensitive fields on the client
- Run CSFLE on Windows using a crypt shared library
- Run CSFLE on Linux using Docker without requiring Windows DLL files

No plaintext sensitive data is stored in MongoDB.  
All encryption and decryption operations happen entirely on the client.

---

## Why Use CSFLE with AWS KMS

Client-Side Field Level Encryption is designed to protect highly sensitive data such as personal, financial, and medical information.

Using AWS KMS provides the following advantages:

- Encryption keys are never exposed to MongoDB
- Centralized key management
- Audit logs using AWS CloudTrail
- Automatic key rotation support
- Compliance readiness for PCI, HIPAA, and SOC standards

---

## Project Structure



<pre>
.
│   README.md
│
├───CSFLE_AWS_KMS
│       .env.example
│       automatic_csfle.py
│       dke_from_aws_kms.py
│       docker-compose.yml
│       dockerfile
│       key_vault_db.py
│       requirements.txt
│
└───ctipt_file
        mongo_crypt_v1.dll
</pre>


---


---

## Prerequisites

- Python version 3.9 or higher
- MongoDB version 6.0 or higher (Atlas or self-hosted)
- AWS account with KMS access
- One AWS Customer Managed Key
- Docker (for Linux or production deployment)

---

## AWS KMS Configuration

Log in to the AWS Console.

Navigate to the Key Management Service.

Create a new Customer Managed Key using symmetric encryption.

Copy and securely store the Key ARN.

Official MongoDB documentation:
https://www.mongodb.com/docs/manual/core/queryable-encryption/fundamentals/kms-providers/#std-label-qe-fundamentals-kms-providers-aws

---

## Environment Variable Setup

Create a `.env` file using the `.env.example` file provided.

Set values for:

- MongoDB connection string
- AWS access key
- AWS secret key
- AWS region
- AWS KMS Key ARN
- Key vault database and collection
- Deployment environment

Example:

ENVIRONMENT=local

or for deployment:

ENVIRONMENT=deployment

Do not commit the `.env` file to version control.

---

## How CSFLE Works Across Environments

This project automatically switches encryption behavior based on the environment.

### Local Development (Windows)

- Uses `mongo_crypt_v1.dll`
- Requires the crypt shared library path
- Intended for local testing and development

The DLL file is located at:
ctipt_file/mongo_crypt_v1.dll

### Deployment (Linux / Docker)

- Uses MongoDB crypt shared library installed inside the container
- Does not require any Windows DLL files
- Fully portable and production ready

---

## Environment-Based Encryption Logic

The encryption configuration changes automatically based on the `ENVIRONMENT` variable.

When running in deployment mode:
- Uses system-installed crypt shared library
- Skips DLL-specific configuration

When running locally:
- Explicitly loads the Windows DLL file

This ensures cross-platform compatibility without code changes.

---

## Create the MongoDB Key Vault

MongoDB stores encryption metadata in a key vault collection.

Run:

python key_vault_db.py

This initializes the key vault database and collection.

---

## Create the Data Encryption Key

The Data Encryption Key is encrypted using the AWS KMS Customer Managed Key.

Run:

python dke_from_aws_kms.py

The generated `dek_id` is required for encrypting fields.  
Store it securely as an environment variable.

---

## Automatic Encryption and Decryption

Run locally:

python automatic_csfle.py

This script automatically encrypts sensitive fields before inserting data into MongoDB and transparently decrypts them when data is read.

No manual cryptographic logic is required.

---

## Running with Docker (Linux / Production)

Build the Docker image:

docker build -t csfle-aws .

Run the container:

docker run --env-file .env csfle-aws

The Docker image installs the MongoDB crypt shared library internally, enabling CSFLE without Windows dependencies.

---

## Example Use Case

This implementation is suitable for encrypting sensitive fields such as:

- Patient names
- Aadhaar or PAN numbers
- Phone numbers
- Medical or financial data

MongoDB stores only encrypted data and never has access to plaintext values.

---

## Security Best Practices

- Never commit AWS credentials to GitHub
- Use IAM roles instead of static access keys in production
- Rotate AWS KMS keys periodically
- Apply least-privilege IAM policies
- Store DEK identifiers securely

---

## Notes

- This implementation uses Automatic CSFLE
- Designed for both development and production
- Docker-based deployment eliminates platform-specific crypt dependencies

---

##Output 


<img width="801" height="310" alt="Screenshot 2026-01-28 101739" src="https://github.com/user-attachments/assets/11a1d211-4842-4d75-b807-d855ef472b00" />


##In MongoDB


<img width="650" height="104" alt="Screenshot 2026-01-28 101249" src="https://github.com/user-attachments/assets/eebb8b24-2e8b-4c2e-9b28-0fafa54d23e2" />
