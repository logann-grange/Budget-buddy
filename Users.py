import mysql.connector
import Compte_bancaires
from transaction import Transaction
from bdd_connector import connexion

mydb, cursor = connexion()

class Users:
    def __init__(self,id_login):
        self.id = id_login
        cursor.execute("SELECT  COUNT(*) FROM compte_bancaire WHERE id_login = %s", (id_login,))
        self.nombre_compte = cursor.fetchall()
        self.list_compte = self.listage_compte(id_login,self.nombre_compte[0][0])
        self.historique = self.refresh_historique()
        cursor.close()
        
    def choix_compte(self, numero_compte=1):
        for compte in self.comte_bancaire:
            if compte[2] == numero_compte:
                return compte
        return None
    
    def listage_compte(self, id_login,nombre_compte):
        liste_compte = []
        for i in range(nombre_compte):
            liste_compte.append(Compte_bancaires.Compte_bancaire(i+1, id_login))
        return liste_compte

    def refresh_historique(self) :
        cursor.execute(f"SELECT * FROM transaction WHERE id_expediteur = {self.id} OR id_receveur = {self.id};")
        return cursor.fetchall()
    

#TEST

user = Users(1)