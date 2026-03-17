import mysql.connector
from Compte_bancaires import Compte_bancaire
import random

class Users:
    def __init__(self, id_login):
        self.connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="banque",
        )
        self.cursor = self.connexion.cursor()
        self.cursor.execute("SELECT COUNT(*) FROM compte_bancaire WHERE login_id = %s", (id_login,))
        self.nombre_compte = self.cursor.fetchall()
        self.listage_compte = self.listage_compte(id_login,self.nombre_compte[0][0])
        self.cursor.close()
        
        
    def créer_compte(self, id_login,solde_initial=0.00):
        self.cursor = self.connexion.cursor()
        numero_compte = self.generer_numero_compte()
        self.cursor.execute("INSERT INTO compte_bancaire (login_id, numero_compte, solde) VALUES (%s, %s, %s)",
        (id_login, numero_compte, solde_initial))
        self.connexion.commit()
        self.cursor.close()
        
    def generer_numero_compte(self):
        while True:
            numero = "FR" + str(random.randint(10**15, 10**16 - 1))
            self.cursor.execute("SELECT * FROM compte_bancaire WHERE numero_compte = %s", (numero,))
            if not self.cursor.fetchone():
                return numero        
    
    
    def choix_compte(self, numero_compte=1):
        for compte in self.comte_bancaire:
            if compte[2] == numero_compte:
                return compte
        return None
    
    def listage_compte(self, id_login,nombre_compte):
        liste_compte = []
        for i in range(nombre_compte):
            liste_compte.append(Compte_bancaire(i+1, id_login))
        return liste_compte            