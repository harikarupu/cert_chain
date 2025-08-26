# cert_chain
# Decentralized Academic Certificate Registry

A Python-based blockchain-inspired application that securely registers, transfers, and verifies academic certificates. Each transaction (minting or transfer) appends a block to the ledger, ensuring a tamper-resistant, transparent history.

---

## Features

- Register (mint) certificates with owner details  
- Transfer certificate ownership between users  
- View the complete certificate transaction history  
- Enforce data integrity using SHA-256 hashing

---

## Requirements

- Python 3.8 or higher  
- No external dependencies; uses only standard Python libraries (`hashlib`, `json`, `dataclasses`)

---

## How It Works

1. **Mint/Register a Certificate** – Upload or reference a certificate file (PDF/image) along with student/course/year metadata. A unique fingerprint (`cert_hash`) is created and stored in the blockchain.  
2. **Transfer Ownership** – Append a transfer event to the ledger, updating who currently holds the certificate.  
3. **Verify History** – Retrieve full mint and transfer history for any given certificate.  
4. **View Ledger** – Inspect the entire blockchain-style record of all certificate events.

---

## Example Use Case

- **Mint** – Register *John Doe’s* course completion certificate → generates a unique `cert_hash`.  
- **Transfer** – Transfer certificate verification control from John Doe to *University Admin*.  
- **Verify** – Check the history and current owner using the `cert_hash`.

---

## Purpose

This tool serves as an educational demonstration of how blockchain concepts—like hashing, immutability, and append-only ledgers—can be applied beyond cryptocurrency. It’s ideal for learning, prototyping, and internal submissions.

---

## Future Enhancements

- Enhanced file-handling logic (auto-quote stripping, path normalization)  
- GUI with file picker (Tkinter or web interface)  
- Transition to real blockchain (Ethereum, IPFS, NFTs, QR-code validation)

