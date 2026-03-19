import re
import bcrypt
import random
from Users import Users
from bdd_connector import connexion

mydb, cursor = connexion()

class Auth:
        
    def creer_compte(self, nom, prenom, email, mot_de_passe):
        cursor.execute("SELECT * FROM login WHERE email = %s", (email,))
        login = cursor.fetchone()
        
        hashed_password = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())
        
        if nom=="" or prenom=="" or email=="" or mot_de_passe=="":
            return "Veuillez remplir tous les champs."
        elif len(mot_de_passe) < 10:
            return "Le mot de passe doit contenir au moins 10 caractères."
        elif not "@" in email or not "." in email:
            return "Veuillez entrer une adresse email valide."
        elif login:
            return "Cette adresse email est déjà utilisée."
        elif not nom.isalpha() or not prenom.isalpha():
            return "Le nom et le prénom doivent contenir uniquement des lettres."
        elif mot_de_passe.isdigit():
            return "Le mot de passe doit contenir des lettres et des chiffres."
        elif mot_de_passe.isalpha():
            return "Le mot de passe doit contenir des lettres et des chiffres."
        elif mot_de_passe.islower() or mot_de_passe.isupper():
            return "Le mot de passe doit contenir des lettres majuscules et minuscules."
        elif not re.search(r"[!@#$%^&*()-+_]", mot_de_passe):
            return "Le mot de passe doit contenir au moins un caractère spécial."
        else:
            sql = "INSERT INTO login (Nom, Prenom, Email, MDP) VALUES (%s, %s, %s, %s)"
            val = (nom, prenom, email, hashed_password)
            cursor.execute(sql, val)
            mydb.commit()
            numero_compte = self.generer_numero_compte()
            cursor.execute("INSERT INTO compte_bancaire (login_id, numero_compte, solde) VALUES (LAST_INSERT_ID(), %s, %s)",
            (numero_compte, 0.00))
            mydb.commit()
            return "Compte créé avec succès."
        
    def generer_numero_compte(self):
        while True:
            numero = "FR" + str(random.randint(10**15, 10**16 - 1))
            cursor.execute("SELECT * FROM compte_bancaire WHERE numero_compte = %s", (numero,))
            if not cursor.fetchone():
                return numero    
        
    def se_connecter(self, email, mot_de_passe):
        cursor.execute("SELECT * FROM login WHERE email = %s ", (email,))
        login = cursor.fetchone()
        if not login:
            return "Email ou mot de passe incorrect.", None
        
        
        if bcrypt.checkpw(mot_de_passe.encode('utf-8'), login[4].encode('utf-8')):
            user = Users(login[0])
            return "Connexion réussie.", user
        else:
            return "Mot de passe incorrect.", None


auth=Auth()
