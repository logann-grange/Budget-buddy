import mysql.connector
import Compte_bancaires

class Users:
    def __init__(self,id_login):
        self.connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="banque",
        )
        self.cursor = self.connexion.cursor()
        self.cursor.execute("SELECT  COUNT(*) FROM compte_bancaire WHERE id_login = %s", (id_login,))
        self.nombre_compte = self.cursor.fetchall()
        self.listage_compte = self.listage_compte(id_login,self.nombre_compte[0][0])
        self.cursor.close()
        
        
        
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