# cert_chain
Decentralized Academic Certificate Registry

A Python-based blockchain simulation for securely registering, transferring, and verifying academic certificates. Each certificate is stored as a unique digital asset (similar to NFTs) within a local blockchain ledger.

Features

Mint/Register new certificates in PDF or image format

Transfer certificate ownership between users

Verify authenticity and transaction history of certificates

View the complete blockchain ledger

Automatic file path handling for Windows and Linux

Prerequisites

Python 3.8 or higher

Standard Python libraries: hashlib, json, datetime

Usage Overview

Register a certificate by providing its file path and owner details

Transfer ownership securely using the blockchain ledger

Verify certificates and view their transaction history

Ledger is stored locally in ledger.json

Certificate File Path

Ensure correct file name and extension (.jpg, .png, .pdf)

Use forward slashes (/) in paths

Optionally, place the certificate in the same folder as the script

Data Storage

Each transaction is recorded as a block in ledger.json

Blockchain structure includes:

Certificate ID

Owner information

Timestamp

Previous hash for integrity

Troubleshooting

Verify correct file path and extension if "File not found" occurs

Ensure terminal has permission to access directories

Future Enhancements

Graphical interface for easier certificate selection

Integration with IPFS or an actual blockchain network

QR-code verification for on-chain certificates
