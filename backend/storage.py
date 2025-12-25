import json
import os

FILE_PATH = "backend/transactions.json"

def load_transactions():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_transactions(transactions):
    with open(FILE_PATH, "w") as f:
        json.dump(transactions, f, indent=4)

def add_transaction(tx):
    transactions = load_transactions()
    transactions.append(tx)
    save_transactions(transactions)

def update_transaction(tx_id, new_status):
    transactions = load_transactions()
    for tx in transactions:
        if tx["tx_id"] == tx_id:
            tx["status"] = new_status
    save_transactions(transactions)

def transaction_exists(tx_id):
    transactions = load_transactions()
    return any(tx["tx_id"] == tx_id for tx in transactions)
