import json
import os

# Absolute path to the directory this file is in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# transactions.json will always live next to storage.py
FILE_PATH = os.path.join(BASE_DIR, "transactions.json")


def load_transactions():
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


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
        if tx.get("tx_id") == tx_id:
            tx["status"] = new_status

    save_transactions(transactions)


def transaction_exists(tx_id):
    transactions = load_transactions()
    return any(tx.get("tx_id") == tx_id for tx in transactions)
