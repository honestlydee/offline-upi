from flask import Flask, request, jsonify
from flask_cors import CORS

from crypto import generate_tx_id, hash_id, current_timestamp
from storage import add_transaction, transaction_exists, load_transactions
from settlement import settle_transaction

app = Flask(__name__)
CORS(app)


# ------------------------
# Health check
# ------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "server running"})


# ------------------------
# Create payment intent
# ------------------------
@app.route("/create_intent", methods=["POST"])
def create_intent():
    try:
        data = request.get_json(force=True)

        if not data:
            return jsonify({"error": "Invalid JSON body"}), 400

        amount = data.get("amount")
        payer = data.get("payer")
        merchant = data.get("merchant")

        if amount is None or payer is None or merchant is None:
            return jsonify({"error": "Missing required fields"}), 400

        try:
            amount = int(amount)
        except ValueError:
            return jsonify({"error": "Amount must be a number"}), 400

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
        return jsonify(tx), 200

    except Exception as e:
        print("CREATE_INTENT ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500


# ------------------------
# Fetch all transactions
# ------------------------
@app.route("/transactions", methods=["GET"])
def get_transactions():
    try:
        return jsonify(load_transactions()), 200
    except Exception as e:
        print("GET_TRANSACTIONS ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500


# ------------------------
# Settle transaction
# ------------------------
@app.route("/settle", methods=["POST"])
def settle():
    try:
        data = request.get_json(force=True)

        if not data or "tx_id" not in data:
            return jsonify({"error": "tx_id is required"}), 400

        tx_id = data.get("tx_id")

        success, message = settle_transaction(tx_id)

        if success:
            return jsonify({"status": message}), 200
        else:
            return jsonify({"error": message}), 400

    except Exception as e:
        print("SETTLE ERROR:", e)
        return jsonify({"error": "Internal server error"}), 500


# ------------------------
# Entry point (Render)
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
