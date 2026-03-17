import mysql.connector


# Classe représentant un compte bancaire avec des méthodes pour récupérer les informations du compte et afficher les détails du compte
class Compte_bancaire:
    def __init__(self,id,login_id):
        self.connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="banque",
        )
        self.cursor = self.connexion.cursor()
        # Récupération du numéro de compte et du solde du compte bancaire en fonction de l'identifiant de connexion et de l'identifiant du compte
        self.cursor.execute("SELECT numero_compte FROM compte_bancaire WHERE login_id = %s AND id = %s", (login_id,id,))
        self.numero_compte = self.cursor.fetchone()[0]
        # Récupération du solde du compte bancaire en fonction de l'identifiant de connexion et de l'identifiant du compte
        self.cursor.execute("SELECT solde FROM compte_bancaire WHERE login_id = %s AND id = %s", (login_id,id,))
        self.solde = self.cursor.fetchone()[0]

    def __repr__(self):
        return f"Compte_bancaire(numero_compte='{self.numero_compte}', solde={self.solde})"

    def __str__(self):
        return f"Compte {self.numero_compte} | Solde: {self.solde}"
        