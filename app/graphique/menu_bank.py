import customtkinter as ctk

# Liste des clients de la banque
CLIENTS = []

class MenuBank:
    def __init__(self, display):
        self.display = display
        self.frame = None

    def afficher(self):
        self.frame = ctk.CTkFrame(self.display, width=1080, height=720, fg_color="transparent")
        self.frame.place(x=0, y=0)
        title_label = ctk.CTkLabel(self.frame, text="Profils suivis", font=("Helvetica", 32, "bold"))
        title_label.place(x=400, y=30)

        # Bouton déconnecter
        logout_button = ctk.CTkButton(self.frame, text="Déconnecter", command=self.deconnecter, fg_color="red", hover_color="#FD4F4F", width=100, height=30)
        logout_button.place(x=950, y=30)

        scrollable_frame = ctk.CTkScrollableFrame(self.frame, width=1000, height=600, fg_color="transparent")
        scrollable_frame.place(x=40, y=100)

        # Afficher les clients dans le frame scrollable (3 par ligne)
        clients_per_row = 3
        for i in range(0, len(CLIENTS), clients_per_row):
            row_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
            row_frame.pack(pady=15)
            
            for j in range(clients_per_row):
                if i + j < len(CLIENTS):
                    client = CLIENTS[i + j]
                    card = ctk.CTkButton(row_frame, text=f"{client['nom']}\n\n{client['solde']}", 
                                       command=lambda c=client: self.ouvrir_compte_client(c),
                                       fg_color="white", text_color="black", 
                                       border_width=2, border_color="white",
                                       hover_color="#f0f0f0", font=("Helvetica", 14),
                                       width=250, height=220)
                    card.pack(side="left", padx=15)


    def ouvrir_compte_client(self, client):
        from app.logique.client_account import ClientAccount
        self.frame.destroy()
        compte = ClientAccount(self.display, client)
        compte.afficher()

    def deconnecter(self):
        from app.commun.log import Log
        self.frame.destroy()
        log = Log(self.display)
        log.afficher()
