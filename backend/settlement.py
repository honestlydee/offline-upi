from storage import load_transactions, update_transaction
import time

MAX_OFFLINE_AMOUNT = 500
EXPIRY_SECONDS = 24 * 60 * 60  # 24 hours

def settle_transaction(tx_id):
    transactions = load_transactions()

    for tx in transactions:
        if tx["tx_id"] == tx_id:
            if tx["status"] != "PENDING":
                return False, "Transaction already settled or invalid"

            if tx["amount"] > MAX_OFFLINE_AMOUNT:
                return False, "Amount exceeds offline limit"

            if time.time() - tx["timestamp"] > EXPIRY_SECONDS:
                return False, "Transaction expired"

            update_transaction(tx_id, "SETTLED")
            return True, "Transaction settled successfully"

    return False, "Transaction not found"
