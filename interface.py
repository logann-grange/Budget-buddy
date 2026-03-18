import customtkinter as ctk
from log import *
from menu import *
from menu_bank import *

LOG = "log"
MENU = "menu"
MENU_BANK = "menu_bank"
HISTORIQUE = "historique"

#===GERE TOUT LE FONCTIONNEMENT DE L'INTERFACE===#

if __name__ == "__main__":

    etat = LOG

    ctk.set_appearance_mode("dark")

    app = ctk.CTk()
    app.title("OUR Bank")
    app.geometry("1080x720")

    j = Log(app)
    menu = Menu(app)
    menu_bank = MenuBank(app)

    if etat == LOG:
        j.afficher()
    elif etat == MENU:
        menu.afficher()
    elif etat == MENU_BANK:
        menu_bank.afficher()

    app.protocol("WM_DELETE_WINDOW", app.destroy)

    app.mainloop()