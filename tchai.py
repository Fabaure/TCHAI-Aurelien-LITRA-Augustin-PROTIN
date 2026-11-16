from flask import Flask, request, jsonify
import time
import json

app = Flask(__name__)

transactions = []

# (A1) Enregistrer une transaction
@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    
    transaction = {
        "P1": data.get("P1"),
        "P2": data.get("P2"),
        "t": time.time(),
        "a": data.get("a")
    }
    transactions.append(transaction)
    
    return jsonify({"message": "Transaction enregistrée", "transaction": transaction}), 201

# (A2) Afficher toutes les transactions (ordre chronologique)
@app.route('/transactions', methods=['GET'])
def get_all_transactions():
    return jsonify(transactions), 200

# (A3) Afficher les transactions liées à une personne
@app.route('/transactions/<personne>', methods=['GET'])
def get_person_transactions(personne):
    person_txs = [tx for tx in transactions if tx["P1"] == personne or tx["P2"] == personne]
    return jsonify(person_txs), 200

# (A4) Afficher le solde du compte d'une personne
@app.route('/solde/<personne>', methods=['GET'])
def get_balance(personne):
    solde = 0
    for tx in transactions:
        if tx["P2"] == personne:
            solde += tx["a"] 
        elif tx["P1"] == personne:
            solde -= tx["a"]
            
    return jsonify({"personne": personne, "solde": solde}), 200


def save_transactions_to_file(transactions, filename="transactions.txt"):
    with open(filename, "w") as f:
        f.write(str(transactions))


if __name__ == '__main__':
    app.run(debug=True, port=5000)

