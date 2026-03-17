import mysql.connector
import re
import bcrypt
import random
from Users import Users

class Auth:
    # Initialisation de la connexion à la base de données
    def __init__(self):
        self.connexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="banque",
        )
        self.cursor = self.connexion.cursor()
    # Création d'un compte utilisateur avec validation des champs et du mot de passe    
    def creer_compte(self, nom, prenom, email, mot_de_passe):
        self.cursor.execute("SELECT * FROM login WHERE email = %s", (email,))
        login = self.cursor.fetchone()
        # Hashage du mot de passe avant de le stocker dans la base de données
        hashed_password = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())
        # Validation des champs et du mot de passe selon les critères spécifiés
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
        elif mot_de_passe.isdigit() or mot_de_passe.isalpha():
            return "Le mot de passe doit contenir des lettres et des chiffres." 
        elif mot_de_passe.islower() or mot_de_passe.isupper():
            return "Le mot de passe doit contenir des lettres majuscules et minuscules."
        elif not re.search(r"[!@#$%^&*()-+_]", mot_de_passe):
            return "Le mot de passe doit contenir au moins un caractère spécial."
        else:
            # Insertion du nouvel utilisateur dans la base de données
            sql = "INSERT INTO login (Nom, Prenom, Email, MDP) VALUES (%s, %s, %s, %s)"
            val = (nom, prenom, email, hashed_password)
            self.cursor.execute(sql, val)
            self.connexion.commit()
            numero_compte = self.generer_numero_compte()
            self.cursor.execute("INSERT INTO compte_bancaire (login_id, numero_compte, solde) VALUES (LAST_INSERT_ID(), %s, %s)",
            (numero_compte, 0.00))
            self.connexion.commit()
            self.cursor.close()
            return "Compte créé avec succès."
    
    # Génération d'un numéro de compte unique pour chaque nouvel utilisateur
    def generer_numero_compte(self):
        while True:
            numero = "FR" + str(random.randint(10**15, 10**16 - 1))
            self.cursor.execute("SELECT * FROM compte_bancaire WHERE numero_compte = %s", (numero,))
            if not self.cursor.fetchone():
                return numero    
    # Vérification des informations de connexion de l'utilisateur et retour des comptes associés en cas de succès 
    def se_connecter(self, email, mot_de_passe):
        self.cursor.execute("SELECT * FROM login WHERE email = %s ", (email,))
        login = self.cursor.fetchone()
        if not login:
            return "Email ou mot de passe incorrect.", None
        
        # Vérification du mot de passe en comparant le mot de passe saisi avec le mot de passe hashé stocké dans la base de données
        if bcrypt.checkpw(mot_de_passe.encode('utf-8'), login[4].encode('utf-8')):
            User=Users(login[0])
            # Récupération des comptes bancaires associés à l'utilisateur connecté
            return "Connexion réussie.", User.listage_compte
        else:
            return "Mot de passe incorrect.", None


auth=Auth()
success, comptes = auth.se_connecter("john.doe@example.com", "Motdepasse123!")
print(success)
print(comptes)