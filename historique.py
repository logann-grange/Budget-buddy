from transaction import Transaction

class Historique : 

    def __init__(self, login_id, transactions):
        self.transactions = transactions
        self.filter = ["", "", ""] #type, montant, date
        displayed_transaction = []
        self.display_transaction()

    def get_to_string(self) :
        str_historique = ""
        for transaction in self.transactions :
            str_historique += transaction.description + ";"
        return str_historique

    def display_transaction(self) :
        list_transaction = []
        for transaction in self.transactions :
            if transaction.type == (self.filter[0] in transaction.type or self.filter[0] == "")  and (self.filter[1] == transaction.montant or self.filter[1] == "") and (self.filter[2] in transaction.date or self.filter[2]=="") :
                list_transaction.append(transaction)

        self.displayed_transaction = list_transaction
                
                

