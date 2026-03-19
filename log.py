import customtkinter as ctk
from gestion_connexion import Auth

class Log:
    def __init__(self, display):
        self.display = display
        self.frame = None
        self.auth = Auth()

    def afficher(self):
        self.frame = ctk.CTkFrame(self.display, width=1080, height=720, fg_color="transparent")
        self.frame.place(x=0, y=0)

        self.label = ctk.CTkLabel(self.frame, text="Bonjour !", font=("Helvetica", 32))
        self.label.place(x=170, y=50)

        #===CONNEXION===#
        self.entry_mail = ctk.CTkEntry(self.frame, placeholder_text="Email...", width=200, height=40)
        self.entry_mail.place(x=170, y=300)

        self.entry_mdp = ctk.CTkEntry(self.frame, placeholder_text="Mot de passe...", show="*", width=200, height=40)
        self.entry_mdp.place(x=170, y=350)

        button = ctk.CTkButton(self.frame, text="Connectez-vous", command=self.changement_etat_connexion, fg_color="red", hover_color="#FD4F4F", width=200, height=20)
        button.place(x=170, y=450)

        #===INSCRIPTION===#
        self.entry_nom = ctk.CTkEntry(self.frame, placeholder_text="Nom...", width=200, height=40)
        self.entry_nom.place(x=710, y=200)

        self.entry_prenom = ctk.CTkEntry(self.frame, placeholder_text="Prenom...", width=200, height=40)
        self.entry_prenom.place(x=710, y=250)

        self.entry_mail_inscription = ctk.CTkEntry(self.frame, placeholder_text="Email...", width=200, height=40)
        self.entry_mail_inscription.place(x=710, y=300)

        self.entry_mdp_inscription = ctk.CTkEntry(self.frame, placeholder_text="Mot de passe...", show="*", width=200, height=40)
        self.entry_mdp_inscription.place(x=710, y=350)

        button2 = ctk.CTkButton(self.frame, text="Inscrivez-vous", command=self.changement_etat_inscription, fg_color="red", hover_color="#FD4F4F", width=200, height=20)
        button2.place(x=710, y=450)

    def verif_mail(self, mail):
        if "@" not in mail or "." not in mail:
            self.label.configure(text="Email Invalide", text_color="red")
            return False
        return True

    def changement_etat_connexion(self):
        from menu import Menu
        from menu_bank import MenuBank

        mail = self.entry_mail.get()
        mdp = self.entry_mdp.get()
        message, user = self.auth.se_connecter(mail, mdp)
        
        if user is None:
            self.label.configure(text=message, text_color="red")
            return
        
        self.frame.destroy()
        
        if "@labank.com" in mail:
            menu_bank = MenuBank(self.display)
            menu_bank.afficher()
        else:
            menu = Menu(self.display)
            menu.afficher(user)

    def changement_etat_inscription(self):
        from menu import Menu
        from menu_bank import MenuBank

        mail = self.entry_mail_inscription.get()
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        mdp = self.entry_mdp_inscription.get()

        message = self.auth.creer_compte(nom, prenom, mail, mdp)
        if message != "Compte créé avec succès.":
            self.label.configure(text=message, text_color="red")
            return
        
        message, user = self.auth.se_connecter(mail, mdp)
        
        
        self.frame.destroy()

        if "@labank.com" in mail:
            menu_bank = MenuBank(self.display)
            menu_bank.afficher()
        elif "@" in mail and "." in mail:
            menu = Menu(self.display)
            menu.afficher(user)