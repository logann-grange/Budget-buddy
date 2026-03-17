import mysql.connector

def connexion() :
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="banque",
    )

    cursor = mydb.cursor()

    return mydb, cursor