import mysql.connector

def connexion() :
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "MohamedSwain-13010",
        database = "banque",
    )

    cursor = mydb.cursor()

    return mydb, cursor