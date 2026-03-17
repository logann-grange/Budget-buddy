import mysql.connector

class Compte_bancaire:
    def __init__(self,id,login_id):
        self.connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="banque",
        )
        self.cursor = self.connexion.cursor()
        self.cursor.execute("SELECT numero_compte FROM compte_bancaire WHERE id_login = %s AND id = %s", (login_id,id,))
        self.numero_compte = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT solde FROM compte_bancaire WHERE id_login = %s AND id = %s", (login_id,id,))
        self.solde = self.cursor.fetchone()[0]
        