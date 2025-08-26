#!/usr/bin/env python3
"""
cert_chain.py
Decentralized Academic Certificate Registry (CLI)
Run: python cert_chain.py
"""
import json
import os
import sys
from dataclasses import dataclass, asdict
from hashlib import sha256
from time import time, ctime
from typing import List, Dict, Optional
from pathlib import Path

CHAIN_FILE = "cert_chain.json"

@dataclass
class Block:
    index: int
    timestamp: float
    prev_hash: str
    data: Dict      # MINT or TRANSFER payload
    current_hash: str

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        if os.path.exists(CHAIN_FILE):
            try:
                self._load()
            except Exception as e:
                print("Failed to load existing chain:", e)
                print("Creating new chain.")
                self._create_genesis()
        else:
            self._create_genesis()

    def _create_genesis(self):
        genesis_data = {"type": "GENESIS", "note": "Decentralized Certificate Registry"}
        h = sha256(repr(genesis_data).encode()).hexdigest()
        self.chain = [Block(0, time(), "0"*64, genesis_data, h)]
        self._save()

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def compute_hash(self, data: Dict, prev_hash: str) -> str:
        payload = f"{repr(data)}|{prev_hash}|{len(self.chain)}|{time()}"
        return sha256(payload.encode()).hexdigest()

    def add_block(self, data: Dict) -> Block:
        prev_hash = self.last_block.current_hash
        current_hash = self.compute_hash(data, prev_hash)
        block = Block(len(self.chain), time(), prev_hash, data, current_hash)
        self.chain.append(block)
        self._save()
        return block

    def has_cert_hash(self, cert_hash: str) -> bool:
        return any(b.data.get("cert_hash") == cert_hash for b in self.chain)

    def history(self, cert_hash: str) -> List[Dict]:
        return [asdict(b) for b in self.chain if b.data.get("cert_hash") == cert_hash]

    def serialize(self) -> List[Dict]:
        return [asdict(b) for b in self.chain]

    def _save(self):
        with open(CHAIN_FILE, "w", encoding="utf-8") as f:
            json.dump(self.serialize(), f, indent=2, ensure_ascii=False)

    def _load(self):
        with open(CHAIN_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        self.chain = [Block(**b) for b in raw]

# Utilities
def file_sha256(path: str) -> str:
    h = sha256()
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def prompt(msg: str, required=True) -> str:
    v = input(msg).strip()
    if required and not v:
        return prompt(msg, required)
    return v

def pretty_block(b: Dict) -> str:
    t = ctime(b["timestamp"])
    typ = b["data"].get("type")
    if typ == "MINT":
        d = b["data"]
        return f"#{b['index']} {typ} | student: {d.get('student_name')} | course: {d.get('course')} | year: {d.get('year')} | cert_hash: {d.get('cert_hash')[:12]}... | time: {t}"
    elif typ == "TRANSFER":
        d = b["data"]
        return f"#{b['index']} {typ} | cert_hash: {d.get('cert_hash')[:12]}... | from: {d.get('from')} → to: {d.get('to')} | time: {t}"
    else:
        return f"#{b['index']} {typ} | time: {t}"

def main_menu():
    print("""
Decentralized Academic Certificate Registry
==========================================
1) Mint/register certificate
2) Transfer certificate (change owner/holder)
3) Verify certificate (history)
4) View full ledger
5) Exit
""")
    return prompt("Choose an option (1-5): ")

def mint_flow(chain: Blockchain):
    print("\n--- Mint/Register Certificate ---")
    student = prompt("Student name: ")
    course = prompt("Course name: ")
    year = prompt("Year (e.g., 2025): ")
    file_path = prompt("Path to certificate file (PDF/image): ")
    try:
        fhash = file_sha256(file_path)
    except Exception as e:
        print("Error:", e)
        return
    # Combine file hash + metadata to make a deterministic cert fingerprint
    combined = sha256((fhash + "|" + student + "|" + course + "|" + year).encode()).hexdigest()
    if chain.has_cert_hash(combined):
        print("❌ Certificate already registered with hash:", combined)
        return
    data = {
        "type": "MINT",
        "cert_hash": combined,
        "file_hash": fhash,
        "student_name": student,
        "course": course,
        "year": year,
        "owner": student  # initial owner = student (can be any identifier)
    }
    block = chain.add_block(data)
    print("✅ Minted certificate. Block index:", block.index)
    print("Certificate fingerprint (cert_hash):", combined)

def transfer_flow(chain: Blockchain):
    print("\n--- Transfer Certificate ---")
    cert_hash = prompt("Certificate fingerprint (cert_hash): ")
    # confirm it exists
    hist = chain.history(cert_hash)
    if not hist:
        print("❌ No record found for that certificate.")
        return
    current_owner = None
    for h in hist:
        if h["data"].get("type") == "MINT":
            current_owner = h["data"].get("owner", current_owner)
        elif h["data"].get("type") == "TRANSFER":
            current_owner = h["data"].get("to", current_owner)
    print("Current owner:", current_owner)
    new_owner = prompt("New owner/holder identifier (email or org): ")
    data = {
        "type": "TRANSFER",
        "cert_hash": cert_hash,
        "from": current_owner,
        "to": new_owner
    }
    block = chain.add_block(data)
    print("✅ Transfer recorded. Block index:", block.index)

def verify_flow(chain: Blockchain):
    print("\n--- Verify Certificate ---")
    cert_hash = prompt("Certificate fingerprint (cert_hash): ")
    hist = chain.history(cert_hash)
    if not hist:
        print("❌ No record found for that certificate.")
        return
    print("✅ Certificate found. History:")
    for b in hist:
        print(pretty_block(b))
    # latest owner
    current_owner = None
    for h in hist:
        if h["data"].get("type") == "MINT":
            current_owner = h["data"].get("owner", current_owner)
        elif h["data"].get("type") == "TRANSFER":
            current_owner = h["data"].get("to", current_owner)
    print("Current owner/holder:", current_owner)

def view_ledger(chain: Blockchain):
    print("\n--- Full Ledger ---")
    for b in chain.serialize():
        print(pretty_block(b))

def run():
    chain = Blockchain()
    while True:
        try:
            choice = main_menu()
            if choice == "1":
                mint_flow(chain)
            elif choice == "2":
                transfer_flow(chain)
            elif choice == "3":
                verify_flow(chain)
            elif choice == "4":
                view_ledger(chain)
            elif choice == "5":
                print("Bye.")
                sys.exit(0)
            else:
                print("Invalid choice.")
        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.")
            sys.exit(0)

if __name__ == "__main__":
    run()