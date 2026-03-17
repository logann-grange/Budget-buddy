from bdd_connector import connexion

mydb, cursor = connexion()

class Transaction() :

    def __init__(self, id, description, type, expediteur_id, receveur_id, montant, date):
        self.id = id
        self.description = description
        self.type = type
        self.expediteur = self.get_acount_from_id(expediteur_id)
        self.receveur = self.get_acount_from_id(receveur_id)
        self.montant = montant
        self.date = date

    def __str__(self):
        return f"{self.id} : {self.type} de {self.montant} de {self.expediteur} vers {self.receveur} le {self.date}"

    def add_to_bdd(self) :
        cursor.execute(f"INSERT INTO transaction (description, type, expediteur_id, receveur_id, montant, date) VALUES ('{self.description}', '{self.type}', {self.expediteur}, {self.receveur}, {self.montant}, '{self.date}');")
        mydb.commit()

            