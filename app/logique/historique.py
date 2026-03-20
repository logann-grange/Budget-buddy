from app.logique.transaction import Transaction
from app.donnees.bdd_connector import connexion

mydb, cursor = connexion()

class Historique : 

    def __init__(self, login_id, transactions):
        self.transactions = transactions
        self.filter = ["", "", ""] #type, montant, date
        displayed_transaction = []
        self.display_transaction()

    def get_to_string(self) :
        str_historique = ""
        for transaction in self.transactions :
            str_historique += transaction.description + ";"
        return str_historique

    def display_transaction(self) :
        list_transaction = []
        for transaction in self.transactions :
            if (self.filter[0] in transaction.type or self.filter[0] == "")  and (self.filter[1] == str(transaction.montant) or self.filter[1] == "") and (self.filter[2] in str(transaction.date) or self.filter[2]=="") :
                list_transaction.append(transaction)

        self.displayed_transaction = list_transaction
                
    def charger_transactions(login_id):
        cursor.execute("SELECT id FROM compte_bancaire WHERE login_id = %s", (login_id,))
        ids_comptes = [row[0] for row in cursor.fetchall()]
        if not ids_comptes:
            return []
        placeholders = ",".join(["%s"] * len(ids_comptes))
        cursor.execute(
            f"SELECT id, description, type, expediteur_id, receveur_id, montant, date "
            f"FROM `transaction` "
            f"WHERE expediteur_id IN ({placeholders}) OR receveur_id IN ({placeholders}) "
            f"ORDER BY date DESC",
            ids_comptes + ids_comptes
        )
        rows = cursor.fetchall()
        transactions = []
        for row in rows:
            try:
                transactions.append(Transaction(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
            except Exception:
                pass
        return transactions
