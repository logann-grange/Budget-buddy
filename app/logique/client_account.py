import customtkinter as ctk

class ClientAccount:
    def __init__(self, display, client):
        self.display = display
        self.frame = None
        self.client = client

    def afficher(self):
        self.frame = ctk.CTkFrame(self.display, width=1080, height=720, fg_color="transparent")
        self.frame.place(x=0, y=0)

        # Bouton retour
        back_button = ctk.CTkButton(self.frame, text="← Retour", command=self.retour_menu, 
                                    fg_color="red", hover_color="#FD4F4F", width=100, height=30)
        back_button.place(x=20, y=20)

        title_label = ctk.CTkLabel(self.frame, text=f"Compte de {self.client['nom']}", 
                                  font=("Helvetica", 32, "bold"))
        title_label.place(x=400, y=30)

        solde_frame = ctk.CTkFrame(self.frame, width=150, height=180, fg_color="white", border_width=2, border_color="white")
        solde_frame.place(x=20, y=120)
        
        solde_label = ctk.CTkLabel(solde_frame, text="Solde", font=("Helvetica", 16, "bold"), text_color="black")
        solde_label.place(x=10, y=10)
        
        solde_value = ctk.CTkLabel(solde_frame, text="0€", font=("Helvetica", 20, "bold"), text_color="red")
        solde_value.place(x=10, y=50)

        historique_button = ctk.CTkButton(self.frame, text="Historique\n\nOpérations\nrécentes...", 
                                         command=self.ouvrir_historique, 
                                         fg_color="white", text_color="black", 
                                         border_width=2, border_color="white",
                                         hover_color="#f0f0f0", font=("Helvetica", 12),
                                         width=150, height=400)
        historique_button.place(x=20, y=320)

        graphique_frame = ctk.CTkFrame(self.frame, width=850, height=580, fg_color="white", border_width=2, border_color="white")
        graphique_frame.place(x=190, y=120)
        
        graphique_label = ctk.CTkLabel(graphique_frame, text="Graphique", font=("Helvetica", 16, "bold"), text_color="black")
        graphique_label.place(x=10, y=10)
        
        graphique_placeholder = ctk.CTkLabel(graphique_frame, text="Graphique de dépenses", font=("Helvetica", 14), text_color="gray")
        graphique_placeholder.place(x=400, y=280)

    def ouvrir_historique(self):
        from app.logique.historique_client import HistoriqueClient
        self.frame.destroy()
        historique = HistoriqueClient(self.display, self.client)
        historique.afficher()

    def retour_menu(self):
        from app.graphique.menu_bank import MenuBank
        self.frame.destroy()
        menu = MenuBank(self.display)
        menu.afficher()
