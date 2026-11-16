# Tchaî - Système de Transactions Électroniques

**Projet réalisé dans le cadre du module "Chaîne des transactions" à Polytech Dijon.**

## Auteurs
*   **[Aurélien LITRA]** **aurelien_litra@etu.ube.fr**
*   **[Augustin PROTIN]** **augustin_prtin@etu.ube.fr**

---

## 📖 Description du Projet
L'objectif de ce projet est de concevoir un système de transactions électroniques garantissant l'intégrité des données, accessible via le protocole HTTP. Le système évolue de manière itérative, d'un simple registre de transactions (v1) vers un système sécurisé par chaînage cryptographique (façon blockchain) et signatures asymétriques (v4).

## 🛠️ Choix Techniques et Architecture

Conformément aux consignes du TP, voici la documentation de nos choix techniques :

*   **Langage de programmation :** Python 3
*   **Framework Web :** Flask 
*   **Stockage des données :** SQLite / Fichier JSON 
*   **Fonction de hachage :** SHA-256 

## 🚀 Installation et Lancement

1. Cloner le dépôt :
   ```bash
   git clone [URL_DE_VOTRE_DEPOT]
   cd TCHAI-Aurelien-LITRA-Augustin-PROTIN
   ```
2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Lancer le serveur (par défaut sur `http://127.0.0.1:5000`) :
   ```bash
   python tchai.py
   ```

---

## 📡 API HTTP (Fonctionnalités)

Le système expose les routes HTTP suivantes :

*   **(A1) Enregistrer une transaction :** `POST /transactions`
*   **(A2) Afficher toutes les transactions :** `GET /transactions` (Triées par ordre chronologique)
*   **(A3) Afficher les transactions d'une personne :** `GET /transactions/<personne>`
*   **(A4) Afficher le solde d'un compte :** `GET /solde/<personne>`
*   **(A5) Vérifier l'intégrité des données :** `GET /integrite` (Vérifie les hashs de la chaîne)

---

## ⚔️ Tests et Attaques (Évolution de la sécurité)

Cette section détaille les vulnérabilités identifiées et corrigées au cours des différentes versions du système, ainsi que les scripts disponibles dans le dossier `/tests`.

### Tchaî v1 : Attaque par modification (Exercice 4)
*   **Description de l'attaque :** Modification directe du montant d'une transaction dans la base de données/fichier.
*   **Script de test :** `tests/attack_v1_modify.py` ou description manuelle.
*   **Résultat :** L'attaque réussit car le système n'a aucun moyen de vérifier si les données ont été altérées a posteriori.

### Tchaî v2 : Attaque par suppression (Exercice 8)
*   **Description de l'attaque :** Suppression directe d'une ligne de transaction dans le registre. 
*   **Script de test :** `tests/attack_v2_delete.py`
*   **Résultat :** Bien que les transactions restantes aient des hashs valides, le système ne détecte pas le "trou" laissé par la suppression. Cela peut mener à une attaque de *double dépense*.
*   **Correction apportée (v3) :** Implémentation d'un chaînage où le hash de la transaction $i+1$ dépend du hash de la transaction $i$.

### Tchaî v3 : Attaque par falsification / Usurpation d'identité (Exercice 11)
*   **Description de l'attaque :** Ajout direct d'une transaction non autorisée (ex: de Alice vers l'Attaquant) en fin de chaîne, en calculant un hash valide.
*   **Script de test :** `tests/attack_v3_forge.py`
*   **Résultat :** La chaîne reste cryptographiquement valide du point de vue des hashs, mais la transaction est frauduleuse car l'expéditeur n'y a jamais consenti.
*   **Correction apportée (v4) :** Ajout de la cryptographie asymétrique (signatures numériques) pour garantir l'authenticité de l'expéditeur.
