import mysql.connector
#from transaction import Transaction
from datetime import date

connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="banque",
        )
cursor = connexion.cursor()

class Compte_bancaire:
    def __init__(self,id,login_id):
        self.id = id
        self.login_id = login_id
        self.numero_compte = self.refresh_num()
        self.solde = self.refresh_solde()
        

    def get_acount_from_id(self, id) :
        #cursor.execute("SELECT * FROM Compte_bancaire WHERE id = %s;", id)
        cursor.execute(f"SELECT * FROM Compte_bancaire WHERE id = {id};")
        acount = cursor.fetchone()
        return Compte_bancaire(acount[0], acount[1])
    
    def refresh_num(self) :
        cursor.execute("SELECT numero_compte FROM compte_bancaire WHERE login_id = %s AND id = %s", (self.login_id, self.id,))
        return cursor.fetchone()[0]

    
    def refresh_solde(self) :
        cursor.execute("SELECT solde FROM compte_bancaire WHERE login_id = %s AND id = %s", (self.login_id, self.id,))
        return cursor.fetchone()[0]

    def transfert(self, id_receveur, montant) :
        # Calcule du nouveau prix et modification en BDD
        self.solde -= montant
        receveur = self.get_acount_from_id(id_receveur)
        receveur.solde += montant
        cursor.execute(f"UPDATE compte_bancaire SET solde = {self.solde} WHERE id = {self.id}")
        connexion.commit()
        cursor.execute(f"UPDATE compte_bancaire SET solde = {receveur.solde} WHERE id = {receveur.id}")
        connexion.commit()
        # Ajout dans la table transaction
        jour = date.today().strftime("%d/%m/%Y")
        cursor.execute(f"INSERT INTO transaction (type, description, expediteur_id, receveur_id, montant, date) VALUES ('transfert', '', {self.id}, {id_receveur}, {montant}, '{jour}')")
        connexion.commit()

    def depot(self, montant) :
        self.solde += montant
        cursor.execute(f"UPDATE compte_bancaire SET solde = {self.solde} WHERE id = {self.id}")
        connexion.commit()
        # Ajout dans la table transaction
        jour = date.today().strftime("%d/%m/%Y")
        print(jour)
        cursor.execute(f"INSERT INTO transaction (type, description, expediteur_id, receveur_id, montant, date) VALUES ('depot', '', {self.id}, {self.id}, {montant}, '{jour}')")
        connexion.commit()


    def retrait(self, montant) :
        self.solde -= montant
        cursor.execute(f"UPDATE compte_bancaire SET solde = {self.solde} WHERE id = {self.id}")
        connexion.commit()
        # Ajout dans la table transaction
        jour = date.today().strftime("%d/%m/%Y")
        cursor.execute(f"INSERT INTO transaction (type, description, expediteur_id, receveur_id, montant, date) VALUES ('retrait', '', {self.id}, {self.id}, {montant}, '{jour}')")
        connexion.commit()


#TEST :
cursor.execute("SELECT * FROM compte_bancaire WHERE id = 1")
result = cursor.fetchone() 
print("result : ", result)
compte = Compte_bancaire(result[0], result[1])
print("avant :", compte.solde)
#compte.depot(100)
compte.transfert(2, 200)
print("après :", compte.solde)