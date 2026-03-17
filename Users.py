import mysql.connector
from Compte_bancaires import Compte_bancaire
import random

class Users:
    # Initialisation de la connexion à la base de données et récupération des comptes bancaires associés à l'utilisateur
    def __init__(self, id_login):
        self.connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="banque",
        )
        self.cursor = self.connexion.cursor()
        
        # Récupération du nombre de comptes bancaires associés à l'utilisateur connecté
        self.cursor.execute("SELECT COUNT(*) FROM compte_bancaire WHERE login_id = %s", (id_login,))
        self.nombre_compte = self.cursor.fetchall()
        self.listage_compte = self.listage_compte(id_login,self.nombre_compte[0][0])
        self.cursor.close()
        
    # Création d'un compte bancaire pour l'utilisateur connecté avec un solde initial de 0.00 euros   
    def créer_compte(self, id_login,solde_initial=0.00):
        self.cursor = self.connexion.cursor()
        numero_compte = self.generer_numero_compte()
        self.cursor.execute("INSERT INTO compte_bancaire (login_id, numero_compte, solde) VALUES (%s, %s, %s)",
        (id_login, numero_compte, solde_initial))
        self.connexion.commit()
        self.cursor.close()
    
    
    #Génération d'un numéro de compte unique pour chaque nouvel  compte bancaire créé   
    def generer_numero_compte(self):
        while True:
            numero = "FR" + str(random.randint(10**15, 10**16 - 1))
            self.cursor.execute("SELECT * FROM compte_bancaire WHERE numero_compte = %s", (numero,))
            if not self.cursor.fetchone():
                return numero        
    
    # Choix d'un compte bancaire parmi les comptes associés à l'utilisateur connecté en fonction du numéro de compte saisi
    def choix_compte(self, numero_compte=1):
        for compte in self.comte_bancaire:
            if compte[2] == numero_compte:
                return compte
        return None
    
    # Récupération de la liste des comptes bancaires associés à l'utilisateur connecté et création d'instances de la classe Compte_bancaire pour chaque compte récupéré
    def listage_compte(self, id_login,nombre_compte):
        liste_compte = []
        for i in range(nombre_compte):
            liste_compte.append(Compte_bancaire(i+1, id_login))
        return liste_compte            