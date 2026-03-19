from Compte_bancaires import Compte_bancaire
from bdd_connector import connexion
import mysql.connector

mydb, cursor = connexion()

class Users:
    def __init__(self, id_login):
        self.id = id_login
        cursor.execute("SELECT COUNT(*) FROM compte_bancaire WHERE login_id = %s", (id_login,))
        self.nombre_compte = cursor.fetchone()[0]
        self.list_compte = self.listage_compte(id_login, self.nombre_compte)
        self.historique = self.refresh_historique()
        
    def choix_compte(self, numero_compte=1):
        for compte in self.list_compte:
            if compte.numero_compte == numero_compte:
                return compte
        return None
    
    def listage_compte(self, id_login, nombre_compte):
        liste_compte = []
        for i in range(nombre_compte):
            liste_compte.append(Compte_bancaire(i + 1, id_login))
        return liste_compte

    def refresh_historique(self):
        try:
            cursor.execute("SELECT * FROM transaction")
            return cursor.fetchall()
        except mysql.connector.Error:
            return []
