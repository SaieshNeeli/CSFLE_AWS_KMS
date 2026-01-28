# MongoDB CSFLE with AWS KMS (Python)

This repository demonstrates MongoDB Client-Side Field Level Encryption (CSFLE) using AWS Key Management Service (KMS).

It explains how to securely encrypt sensitive fields on the client side before data is stored in MongoDB, ensuring that the database never sees plaintext data.

---

## Overview

This project shows how to:

- Configure AWS KMS
- Create a Data Encryption Key (DEK)
- Store encryption metadata in the MongoDB key vault
- Automatically encrypt and decrypt sensitive fields on the client

No plaintext sensitive data is stored in MongoDB.  
All encryption and decryption operations happen entirely on the client.

---

## Why Use CSFLE with AWS KMS

Client-Side Field Level Encryption is designed to protect highly sensitive data such as personal, financial, and medical information.

Using AWS KMS provides the following advantages:

- Encryption keys are never exposed to the database
- Centralized and managed key lifecycle
- Audit logs using AWS CloudTrail
- Built-in key rotation support
- Compliance readiness for standards such as PCI, HIPAA, and SOC

---

## Project Structure


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


---

## Prerequisites

Before running this project, ensure the following requirements are met:

- Python version 3.9 or higher
- MongoDB version 6.0 or higher (Atlas or self-hosted)
- AWS account with access to KMS
- One AWS Customer Managed Key

---

## Step 1 AWS KMS Configuration

Log in to the AWS Console.

Navigate to the Key Management Service section.

Create a new Customer Managed Key using symmetric encryption.

Copy and securely store the Key ARN.

Official MongoDB documentation for AWS KMS setup:  
https://www.mongodb.com/docs/manual/core/queryable-encryption/fundamentals/kms-providers/#std-label-qe-fundamentals-kms-providers-aws

---

## Step 2 Environment Variable Setup

Create a `.env` file using the `.env.example` file provided in the repository.

Populate the file with the following information:

- MongoDB connection string
- AWS access key
- AWS secret key
- AWS region
- AWS KMS Key ARN
- Key vault database and collection names

Do not commit the `.env` file to version control.

---

## Step 3 Create the MongoDB Key Vault

MongoDB uses a dedicated key vault collection to store encryption metadata.

Run the following command:

python key_vault_db.py


This creates the key vault database and collection used by CSFLE.

---

## Step 4 Create the Data Encryption Key

The Data Encryption Key is encrypted using the AWS KMS Customer Managed Key.

Run:

python dke_from_aws_kms.py


The generated `dek_id` is required for encrypting fields.  
Store this value securely as an environment variable.

---

## Step 5 Automatic Encryption and Decryption

Run the application using:

python automatic_csfle.py


This script automatically encrypts sensitive fields before inserting data into MongoDB and transparently decrypts them when data is read.

No manual cryptographic logic is required.

---

## Example Use Case

This implementation is suitable for protecting sensitive fields such as:

- Patient names
- Aadhaar or PAN numbers
- Phone numbers
- Medical or financial details

MongoDB stores only encrypted data and never has access to plaintext values.

---

## Security Best Practices

- Never commit AWS credentials to version control
- Use IAM roles instead of static AWS keys in production environments
- Rotate AWS KMS keys periodically
- Apply least-privilege IAM policies for KMS access


