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
        self.cursor.execute("SELECT numero_compte FROM compte_bancaire WHERE login_id = %s AND id = %s", (login_id,id,))
        self.numero_compte = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT solde FROM compte_bancaire WHERE login_id = %s AND id = %s", (login_id,id,))
        self.solde = self.cursor.fetchone()[0]

    def __repr__(self):
        return f"Compte_bancaire(numero_compte='{self.numero_compte}', solde={self.solde})"

    def __str__(self):
        return f"Compte {self.numero_compte} | Solde: {self.solde}"
        