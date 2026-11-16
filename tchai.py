from flask import Flask, request, jsonify
import time
import json
import os

app = Flask(__name__)

# Nom du fichier texte qui servira de base de données
FICHIER_DONNEES = "transactions.json"

def charger_transactions():
    """Charge les transactions depuis le fichier s'il existe."""
    if os.path.exists(FICHIER_DONNEES):
        with open(FICHIER_DONNEES, "r") as f:
            return json.load(f)
    return []

def sauvegarder_transactions():
    """Sauvegarde la liste actuelle des transactions dans le fichier."""
    with open(FICHIER_DONNEES, "w") as f:
        json.dump(transactions, f, indent=4)

# Initialisation de la liste au démarrage du serveur
transactions = charger_transactions()


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
    
    sauvegarder_transactions()
    
    return jsonify({"message": "Transaction enregistrée", "transaction": transaction}), 201

# (A2) Afficher toutes les transactions
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


if __name__ == '__main__':
    app.run(debug=True, port=5000)