from bdd_connector import connexion
from Compte_bancaires import Compte_bancaire

mydb, cursor = connexion()

class Transaction() :

    def __init__(self, id, description, type, expediteur_id, receveur_id, montant, date):
        self.id = id
        self.description = self.make_description(description)
        self.type = type
        self.expediteur = self.get_acount_from_id(expediteur_id)
        self.receveur = self.get_acount_from_id(receveur_id)
        self.montant = montant
        self.date = date

    def __str__(self):
        return f"{self.id} : {self.type} de {self.montant} de {self.expediteur.numero_compte} vers {self.receveur.numero_compte} le {self.date}"

    def get_acount_from_id(self, id) :
        cursor.execute(f"SELECT * FROM Compte_bancaire WHERE id = {id};")
        transactions = cursor.fetchone()
        return Compte_bancaire(transactions[0], transactions[1])

    def add_to_bdd(self) :
        cursor.execute(f"INSERT INTO transaction (description, type, expediteur_id, receveur_id, montant, date) VALUES ('{self.description}', '{self.type}', {self.expediteur}, {self.receveur}, {self.montant}, '{self.date}');")
        mydb.commit()

    def make_description(self, description) :
        if description is None or description == "" :
            return f"{self.id} : {self.type} de {self.montant} de {self.expediteur.numero_compte} vers {self.receveur.numero_compte} le {self.date}"

            