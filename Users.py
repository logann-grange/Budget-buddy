from Compte_bancaires import Compte_bancaire
from bdd_connector import connexion
import mysql.connector


class Users:
    def __init__(self, id_login):
        self.id = id_login
        self.mydb, self.cursor = connexion()
        self.cursor.execute("SELECT COUNT(*) FROM compte_bancaire WHERE login_id = %s", (id_login,))
        self.nombre_compte = self.cursor.fetchone()[0]
        self.list_compte = self.listage_compte(id_login, self.nombre_compte)
        self.historique = self.refresh_historique()
        
    def choix_compte(self, numero_compte=1):
        for compte in self.list_compte:
            if compte.numero_compte == numero_compte:
                return compte
        return None
    
    def listage_compte(self, id_login, nombre_compte):
        liste_compte = []
        self.cursor.execute(
            "SELECT id FROM compte_bancaire WHERE login_id = %s ORDER BY id",
            (id_login,),
        )
        rows = self.cursor.fetchall()
        for row in rows:
            liste_compte.append(Compte_bancaire(row[0], id_login))
        return liste_compte

    def refresh_historique(self):
        try:
            self.cursor.execute("SELECT * FROM transaction")
            return self.cursor.fetchall()
        except mysql.connector.Error:
            return []

    def ajouter_compte(self):
        """Cree un nouveau compte bancaire et l'ajoute a la liste de l'utilisateur."""
        import random
        while True:
            numero = "FR" + str(random.randint(10**15, 10**16 - 1))
            self.cursor.execute("SELECT * FROM compte_bancaire WHERE numero_compte = %s", (numero,))
            if not self.cursor.fetchone():
                break
        self.cursor.execute(
            "INSERT INTO compte_bancaire (login_id, numero_compte, solde) VALUES (%s, %s, %s)",
            (self.id, numero, 0.00)
        )
        new_account_id = self.cursor.lastrowid
        self.mydb.commit()
        # Rafraichit le nombre de comptes et la liste
        self.nombre_compte += 1
        self.list_compte.append(Compte_bancaire(new_account_id, self.id))
        return numero