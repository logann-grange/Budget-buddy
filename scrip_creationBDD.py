import mysql.connector

def creer_bdd():
    connexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",    
    )
    cursor = connexion.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS banque")
    cursor.execute("USE banque")
    cursor.execute("""CREATE TABLE IF NOT EXISTS login (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    Nom VARCHAR(255) NOT NULL,
                    Prenom VARCHAR(255) NOT NULL,
                    Email VARCHAR(255) NOT NULL UNIQUE,
                    MDP VARCHAR(255) NOT NULL
                    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS compte_bancaire (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    login_id INT NOT NULL,
                    numero_compte VARCHAR(255) NOT NULL UNIQUE,
                    solde DECIMAL(10, 2) NOT NULL,
                    FOREIGN KEY (login_id) REFERENCES login(id)
                    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    type varchar(255) NOT NULL,
                    description text NOT NULL,
                    montant DECIMAL(10, 2) NOT NULL,
                    date DATETIME NOT NULL,
                    )""")
    connexion.commit()
    cursor.close()