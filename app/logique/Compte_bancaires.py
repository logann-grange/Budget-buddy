from app.donnees.bdd_connector import connexion
from datetime import date


class Compte_bancaire:
    def __init__(self,id,login_id):
        self.mydb, self.cursor = connexion()
        self.id = id
        self.login_id = login_id
        self.numero_compte = self.refresh_num()
        self.solde = self.refresh_solde()
        

    def get_acount_from_id(self, id) :
        #cursor.execute("SELECT * FROM Compte_bancaire WHERE id = %s;", id)
        self.cursor.execute("SELECT * FROM Compte_bancaire WHERE id = %s", (id,))
        acount = self.cursor.fetchone()
        return Compte_bancaire(acount[0], acount[1])
    
    def refresh_num(self) :
        self.cursor.execute("SELECT numero_compte FROM compte_bancaire WHERE login_id = %s AND id = %s", (self.login_id, self.id,))
        return self.cursor.fetchone()[0]

    
    def refresh_solde(self) :
        self.cursor.execute("SELECT solde FROM compte_bancaire WHERE login_id = %s AND id = %s", (self.login_id, self.id,))
        return float(self.cursor.fetchone()[0])

    def transfert(self, id_receveur, montant) :
        # Calcule du nouveau prix et modification en BDD
        self.solde -= montant
        self.cursor.execute("SELECT solde FROM compte_bancaire WHERE id = %s", (id_receveur,))
        solde_receveur = float(self.cursor.fetchone()[0]) + float(montant)
        self.cursor.execute(f"UPDATE compte_bancaire SET solde = {self.solde} WHERE id = {self.id}")
        self.mydb.commit()
        self.cursor.execute(f"UPDATE compte_bancaire SET solde = {solde_receveur} WHERE id = {id_receveur}")
        self.mydb.commit()
        # Ajout dans la table transaction
        jour = date.today().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO `transaction` (type, description, expediteur_id, receveur_id, montant, date) VALUES (%s, %s, %s, %s, %s, %s)",
            ("transfert", "", self.id, id_receveur, montant, jour)
        )
        self.mydb.commit()
    
    def depot(self, montant) :
        self.solde += montant
        self.cursor.execute(f"UPDATE compte_bancaire SET solde = {self.solde} WHERE id = {self.id}")
        self.mydb.commit()
        # Ajout dans la table transaction
        jour = date.today().strftime("%Y-%m-%d %H:%M:%S")
        print(jour)
        self.cursor.execute(
            "INSERT INTO `transaction` (type, description, expediteur_id, receveur_id, montant, date) VALUES (%s, %s, %s, %s, %s, %s)",
            ("depot", "", self.id, self.id, montant, jour)
        )
        self.mydb.commit()


    def retrait(self, montant) :
        self.solde -= montant
        self.cursor.execute(f"UPDATE compte_bancaire SET solde = {self.solde} WHERE id = {self.id}")
        self.mydb.commit()
        # Ajout dans la table transaction
        jour = date.today().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO `transaction` (type, description, expediteur_id, receveur_id, montant, date) VALUES (%s, %s, %s, %s, %s, %s)",
            ("retrait", "", self.id, self.id, montant, jour)
        )
        self.mydb.commit()


# #TEST :
# self.cursor.execute("SELECT * FROM compte_bancaire WHERE id = 1")
# result = self.cursor.fetchone() 
# print("result : ", result)
# compte = Compte_bancaire(result[0], result[1])
# print("avant :", compte.solde)
# #compte.depot(100)
# compte.transfert(2, 200)
# print("après :", compte.solde)