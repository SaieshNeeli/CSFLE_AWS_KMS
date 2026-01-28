MongoDB CSFLE with AWS KMS (Python)

This repository demonstrates MongoDB Client-Side Field Level Encryption (CSFLE) using AWS KMS as the Key Management Service.

The project explains how to configure AWS KMS, create a Data Encryption Key (DEK), store encryption metadata in MongoDB, and automatically encrypt and decrypt sensitive fields on the client side.

No plaintext sensitive data is stored in MongoDB.
Encryption and decryption happen entirely on the client.

Why CSFLE with AWS KMS

Client-Side Field Level Encryption protects sensitive data such as personal, financial, and health information.

With AWS KMS:

Encryption keys are never exposed to MongoDB

Keys are centrally managed

Audit logs are available using CloudTrail

Key rotation is supported

Suitable for compliance requirements such as PCI, HIPAA, and SOC

Project Structure
<pre>
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
</pre>

Prerequisites

Python version 3.9 or higher

MongoDB version 6.0 or higher (Atlas or self hosted)

AWS account with KMS access

One AWS Customer Managed Key

Step 1 AWS KMS Setup

Log in to the AWS Console.

Go to the Key Management Service section.

Create a new Customer Managed Key using symmetric encryption.

Copy and save the Key ARN.

Official MongoDB documentation for AWS KMS setup:
https://www.mongodb.com/docs/manual/core/queryable-encryption/fundamentals/kms-providers/#std-label-qe-fundamentals-kms-providers-aws

Step 2 Environment Variables

Create a .env file using the .env.example file provided in the repository.

Fill in values for:

MongoDB connection string

AWS access key

AWS secret key

AWS region

KMS key ARN

Key vault database and collection names

Do not commit the .env file to GitHub.

Step 3 Create Key Vault

MongoDB uses a key vault collection to store encryption metadata.

Run the following command:

python key_vault_db.py


This creates the key vault database and collection.

Step 4 Create Data Encryption Key

The Data Encryption Key is encrypted using the AWS KMS Customer Managed Key.

Run:

python dke_from_aws_kms.py


The generated dek_id is required for encrypting fields.
Store this value securely as an environment variable.

Step 5 Automatic Encryption and Decryption

Run:

python automatic_csfle.py


This script automatically encrypts sensitive fields before inserting data into MongoDB and decrypts them when reading.

No manual cryptographic logic is required.

Example Use Case

This setup is suitable for encrypting sensitive fields such as:

Patient name

Aadhaar or PAN number

Phone number

Medical or financial details

MongoDB stores only encrypted data and never sees plaintext values.
