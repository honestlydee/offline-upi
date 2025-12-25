const API = "http://127.0.0.1:5000";

async function createPayment() {
    const amount = document.getElementById("amount").value;

    const res = await fetch(`${API}/create_intent`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            payer: "user@upi",
            merchant: "shop@upi",
            amount: Number(amount)
        })
    });

    const data = await res.json();
    document.getElementById("output").innerText =
        JSON.stringify(data, null, 2);
}

async function loadTransactions() {
    const res = await fetch(`${API}/transactions`);
    const data = await res.json();
    document.getElementById("transactions").innerText =
        JSON.stringify(data, null, 2);
}

async function settleTransaction() {
    const txId = document.getElementById("txid").value;

    const res = await fetch(`${API}/settle`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tx_id: txId })
    });

    const data = await res.json();
    alert(JSON.stringify(data));
}
