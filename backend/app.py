from flask import Flask, request, jsonify
from flask_cors import CORS

from crypto import generate_tx_id, hash_id, current_timestamp
from storage import add_transaction, transaction_exists, load_transactions
from settlement import settle_transaction



app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"status": "server running"})

@app.route("/create_intent", methods=["POST"])
def create_intent():
    data = request.json

    amount = data.get("amount")
    payer = data.get("payer")
    merchant = data.get("merchant")

    tx_id = generate_tx_id()

    if transaction_exists(tx_id):
        return jsonify({"error": "Duplicate transaction"}), 400

    tx = {
        "tx_id": tx_id,
        "payer_id": hash_id(payer),
        "merchant_id": hash_id(merchant),
        "amount": amount,
        "timestamp": current_timestamp(),
        "status": "PENDING"
    }

    add_transaction(tx)
    return jsonify(tx)

@app.route("/transactions", methods=["GET"])
def get_transactions():
    return jsonify(load_transactions())

@app.route("/settle", methods=["POST"])
def settle():
    data = request.json
    tx_id = data.get("tx_id")

    success, message = settle_transaction(tx_id)

    if success:
        return jsonify({"status": message})
    else:
        return jsonify({"error": message}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

