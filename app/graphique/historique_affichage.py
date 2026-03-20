import customtkinter as ctk
from app.logique.historique import Historique

class Historique_affichage:
    def __init__(self, display):
        self.display = display
        self.frame = None
        self.user = None
 
    def afficher(self, user):
        self.user = user
 
        # Charge les transactions et crée l'objet Historique comme prévu par ton collègue
        transactions = Historique.charger_transactions(user.id)
        self.historique = Historique(user.id, transactions)
 
        self.frame = ctk.CTkFrame(self.display, width=1080, height=720, fg_color="transparent")
        self.frame.place(x=0, y=0)
 
        # --- Header ---
        ctk.CTkButton(self.frame, text="<- Retour", command=self.retour_menu,
                      fg_color="red", hover_color="#FD4F4F", width=100, height=30).place(x=20, y=20)
        ctk.CTkLabel(self.frame, text="Historique détaillé", font=("Helvetica", 28, "bold")).place(x=350, y=15)
 
        # --- Barre de filtres ---
        filtre_frame = ctk.CTkFrame(self.frame, width=1040, height=50, fg_color="#222")
        filtre_frame.place(x=20, y=60)
 
        ctk.CTkLabel(filtre_frame, text="Type :", font=("Helvetica", 12), text_color="white").place(x=10, y=12)
        self.entry_type = ctk.CTkEntry(filtre_frame, placeholder_text="depot / retrait / transfert", width=200, height=28)
        self.entry_type.place(x=60, y=10)
 
        ctk.CTkLabel(filtre_frame, text="Montant :", font=("Helvetica", 12), text_color="white").place(x=280, y=12)
        self.entry_montant = ctk.CTkEntry(filtre_frame, placeholder_text="Ex : 100.0", width=120, height=28)
        self.entry_montant.place(x=350, y=10)
 
        ctk.CTkLabel(filtre_frame, text="Date :", font=("Helvetica", 12), text_color="white").place(x=490, y=12)
        self.entry_date = ctk.CTkEntry(filtre_frame, placeholder_text="Ex : 2025-01", width=150, height=28)
        self.entry_date.place(x=540, y=10)
 
        ctk.CTkButton(filtre_frame, text="Filtrer", command=self.appliquer_filtre,
                      fg_color="red", hover_color="#FD4F4F", width=80, height=28).place(x=710, y=10)
        ctk.CTkButton(filtre_frame, text="Reset", command=self.reset_filtre,
                      fg_color="#555", hover_color="#777", width=80, height=28).place(x=800, y=10)
 
        # --- Colonnes ---
        depenses_frame = ctk.CTkFrame(self.frame, width=500, height=560, fg_color="white",
                                      border_width=2, border_color="white")
        depenses_frame.place(x=20, y=125)
        ctk.CTkLabel(depenses_frame, text="Dépenses / Transferts sortants",
                     font=("Helvetica", 14, "bold"), text_color="red").place(x=10, y=10)
        self.scroll_dep = ctk.CTkScrollableFrame(depenses_frame, width=470, height=490, fg_color="white")
        self.scroll_dep.place(x=10, y=45)
 
        revenus_frame = ctk.CTkFrame(self.frame, width=500, height=560, fg_color="white",
                                     border_width=2, border_color="white")
        revenus_frame.place(x=550, y=125)
        ctk.CTkLabel(revenus_frame, text="Revenus / Transferts entrants",
                     font=("Helvetica", 14, "bold"), text_color="green").place(x=10, y=10)
        self.scroll_rev = ctk.CTkScrollableFrame(revenus_frame, width=470, height=490, fg_color="white")
        self.scroll_rev.place(x=10, y=45)
 
        self._afficher_transactions()
 
    def appliquer_filtre(self):
        self.historique.filter[0] = self.entry_type.get().strip()
        self.historique.filter[1] = self.entry_montant.get().strip()
        self.historique.filter[2] = self.entry_date.get().strip()
        self.historique.display_transaction()
        self._afficher_transactions()
 
    def reset_filtre(self):
        self.entry_type.delete(0, "end")
        self.entry_montant.delete(0, "end")
        self.entry_date.delete(0, "end")
        self.historique.filter = ["", "", ""]
        self.historique.display_transaction()
        self._afficher_transactions()
 
    def _afficher_transactions(self):
        ids_comptes = [c.id for c in self.user.list_compte]
 
        for widget in self.scroll_dep.winfo_children():
            widget.destroy()
        for widget in self.scroll_rev.winfo_children():
            widget.destroy()
 
        depenses = [t for t in self.historique.displayed_transaction
                    if t.type in ("retrait", "transfert") and t.expediteur.id in ids_comptes]
        revenus  = [t for t in self.historique.displayed_transaction
                    if t.type == "depot" or
                    (t.type == "transfert" and t.receveur.id in ids_comptes
                     and t.expediteur.id not in ids_comptes)]
 
        if not depenses:
            ctk.CTkLabel(self.scroll_dep, text="Aucune dépense.", text_color="gray",
                         font=("Helvetica", 12)).pack(anchor="w", pady=4)
        for t in depenses:
            ctk.CTkLabel(self.scroll_dep,
                         text=f"-{t.montant:.2f}€   {t.date}   {t.type}",
                         text_color="red", font=("Helvetica", 12), anchor="w"
                         ).pack(anchor="w", pady=2, padx=5)
 
        if not revenus:
            ctk.CTkLabel(self.scroll_rev, text="Aucun revenu.", text_color="gray",
                         font=("Helvetica", 12)).pack(anchor="w", pady=4)
        for t in revenus:
            ctk.CTkLabel(self.scroll_rev,
                         text=f"+{t.montant:.2f}€   {t.date}   {t.type}",
                         text_color="green", font=("Helvetica", 12), anchor="w"
                         ).pack(anchor="w", pady=2, padx=5)
    def retour_menu(self):
        from app.graphique.menu import Menu
        self.frame.destroy()
        menu = Menu(self.display)
        menu.afficher(self.user)
