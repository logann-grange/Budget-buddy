import customtkinter as ctk
import matplotlib; matplotlib.use("TkAgg"); from matplotlib import pyplot as plt, dates as mdates; from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from collections import defaultdict
 

class Menu:
    def __init__(self, display):
        self.display = display
        self.frame = None
        self.user = None
        self.compte_actif = None
        self.modal = None
 
    def afficher(self, user):
        self.user = user
        self.compte_actif = self.user.list_compte[0] if self.user.list_compte else None
 
        self.frame = ctk.CTkFrame(self.display, width=1080, height=720, fg_color="transparent")
        self.frame.place(x=0, y=0)
 
        # --- Header ---
        self.label = ctk.CTkLabel(self.frame, text="Bonjour !", font=("Helvetica", 32, "bold"))
        self.label.place(x=600, y=50)
 
        logout_button = ctk.CTkButton(self.frame, text="Déconnecter", command=self.deconnecter,
                                      fg_color="red", hover_color="#FD4F4F", width=100, height=30)
        logout_button.place(x=950, y=30)
 
        # --- Dropdown sélecteur de compte ---
        noms_comptes = [f"Compte {i+1} — {c.numero_compte}" for i, c in enumerate(self.user.list_compte)]
        if not noms_comptes:
            noms_comptes = ["Aucun compte"]
 
        self.dropdown_compte = ctk.CTkOptionMenu(
            self.frame,
            values=noms_comptes,
            command=self.changer_compte,
            width=300, height=35,
            fg_color="#333333", button_color="red", button_hover_color="#FD4F4F"
        )
        self.dropdown_compte.place(x=20, y=75)
 
        # --- Bloc solde ---
        solde_frame = ctk.CTkFrame(self.frame, width=150, height=180, fg_color="white", border_width=2, border_color="white")
        solde_frame.place(x=20, y=120)
 
        ctk.CTkLabel(solde_frame, text="Solde", font=("Helvetica", 16, "bold"), text_color="black").place(x=10, y=10)
 
        solde_affiche = f"{self.compte_actif.solde}€" if self.compte_actif else "0€"
        self.solde_value = ctk.CTkLabel(solde_frame, text=solde_affiche, font=("Helvetica", 20, "bold"), text_color="red")
        self.solde_value.place(x=10, y=50)
 
        numero_affiche = self.compte_actif.numero_compte if self.compte_actif else ""
        self.numero_label = ctk.CTkLabel(solde_frame, text=numero_affiche, font=("Helvetica", 9), text_color="gray")
        self.numero_label.place(x=10, y=100)
 
        # --- Boutons actions ---
        for i, (texte, cmd) in enumerate([
            ("Depot",     self.ouvrir_depot),
            ("Retrait",   self.ouvrir_retrait),
            ("Transfert", self.ouvrir_transfert),
        ]):
            ctk.CTkButton(self.frame, text=texte, command=cmd,
                          fg_color="red", hover_color="#FD4F4F",
                          width=150, height=40, font=("Helvetica", 13)
                          ).place(x=20, y=320 + i * 60)
 
        # --- Nouveau compte ---
        ctk.CTkButton(self.frame, text="+ Nouveau compte", command=self.ouvrir_nouveau_compte,
                      fg_color="#333333", hover_color="#555555",
                      width=150, height=40, font=("Helvetica", 12)
                      ).place(x=20, y=510)
 
        # --- Historique ---
        ctk.CTkButton(self.frame, text="Historique\n\nOperations\nrecentes...",
                      command=self.ouvrir_historique,
                      fg_color="white", text_color="black",
                      border_width=2, border_color="white",
                      hover_color="#f0f0f0", font=("Helvetica", 12),
                      width=150, height=120
                      ).place(x=20, y=570)
 
        # --- Graphique ---
        self.graphique_frame = ctk.CTkFrame(self.frame, width=850, height=580, fg_color="white", border_width=2, border_color="white")
        self.graphique_frame.place(x=190, y=120)
        ctk.CTkLabel(self.graphique_frame, text="Graphique", font=("Helvetica", 16, "bold"), text_color="black").place(x=10, y=10)
        self._afficher_graphique()
 
    # ------------------------------------------------------------------ #
    #  Dropdown                                                             #
    # ------------------------------------------------------------------ #
 
    def changer_compte(self, choix):
        index = self.dropdown_compte.cget("values").index(choix)
        ancien = self.user.list_compte[index]     
        self.compte_actif = self.user.list_compte[index].__class__(ancien.id, ancien.login_id)
        self.user.list_compte[index] = self.compte_actif
        self.solde_value.configure(text=f"{self.compte_actif.solde}€")
        self.numero_label.configure(text=self.compte_actif.numero_compte)
        self._afficher_graphique()
 
    # ------------------------------------------------------------------ #
    #  Helpers modaux                                                       #
    # ------------------------------------------------------------------ #
 
    def _fermer_modal(self):
        if self.modal:
            if hasattr(self.modal, "overlay"):
                self.modal.overlay.destroy()
            self.modal.destroy()
            self.modal = None
 
    def _creer_modal(self, titre, hauteur=220):
        self._fermer_modal()
        overlay = ctk.CTkFrame(self.frame, width=1080, height=720, fg_color="#000000")
        overlay.place(x=0, y=0)
        overlay.bind("<Button-1>", lambda e: self._fermer_modal())
 
        self.modal = ctk.CTkFrame(self.frame, width=380, height=hauteur, fg_color="#1a1a1a", border_width=1, border_color="#444")
        self.modal.place(x=(1080 - 380) // 2, y=(720 - hauteur) // 2)
        self.modal.overlay = overlay
 
        ctk.CTkLabel(self.modal, text=titre, font=("Helvetica", 18, "bold")).place(x=20, y=15)
        ctk.CTkButton(self.modal, text="X", width=30, height=30,
                      fg_color="transparent", hover_color="#333",
                      command=self._fermer_modal, font=("Helvetica", 14)
                      ).place(x=335, y=10)
        return self.modal
 
    def _rafraichir_solde(self):
    
        self.solde_value.configure(text=f"{self.compte_actif.solde}€")
 
    # ------------------------------------------------------------------ #
    #  Modal Depot                                                          #
    # ------------------------------------------------------------------ #
 
    def ouvrir_depot(self):
        if not self.compte_actif:
            return
        modal = self._creer_modal("Depot")
        ctk.CTkLabel(modal, text="Montant (EUR)", font=("Helvetica", 13)).place(x=20, y=65)
        entry = ctk.CTkEntry(modal, placeholder_text="Ex : 200", width=340, height=40)
        entry.place(x=20, y=95)
        msg = ctk.CTkLabel(modal, text="", font=("Helvetica", 12))
        msg.place(x=20, y=145)
 
        def valider():
            try:
                montant = float(entry.get().replace(",", "."))
                if montant <= 0:
                    raise ValueError
            except ValueError:
                msg.configure(text="Montant invalide.", text_color="red")
                return
            self.compte_actif.depot(montant)
            self._rafraichir_solde()
            self._afficher_graphique()
            msg.configure(text=f"+{montant}EUR deposes avec succes.", text_color="green")
 
        ctk.CTkButton(modal, text="Confirmer", command=valider,
                      fg_color="red", hover_color="#FD4F4F", width=340, height=40).place(x=20, y=165)
 
    # ------------------------------------------------------------------ #
    #  Modal Retrait                                                        #
    # ------------------------------------------------------------------ #
 
    def ouvrir_retrait(self):
        if not self.compte_actif:
            return
        modal = self._creer_modal("Retrait")
        ctk.CTkLabel(modal, text="Montant (EUR)", font=("Helvetica", 13)).place(x=20, y=65)
        entry = ctk.CTkEntry(modal, placeholder_text="Ex : 50", width=340, height=40)
        entry.place(x=20, y=95)
        msg = ctk.CTkLabel(modal, text="", font=("Helvetica", 12))
        msg.place(x=20, y=145)
 
        def valider():
            try:
                montant = float(entry.get().replace(",", "."))
                if montant <= 0:
                    raise ValueError
            except ValueError:
                msg.configure(text="Montant invalide.", text_color="red")
                return
            if montant > self.compte_actif.solde:
                msg.configure(text="Solde insuffisant.", text_color="red")
                return
            self.compte_actif.retrait(montant)
            self._rafraichir_solde()
            self._afficher_graphique()
            msg.configure(text=f"-{montant}EUR retires avec succes.", text_color="green")
 
        ctk.CTkButton(modal, text="Confirmer", command=valider,
                      fg_color="red", hover_color="#FD4F4F", width=340, height=40).place(x=20, y=165)
 
    # ------------------------------------------------------------------ #
    #  Modal Transfert                                                      #
    # ------------------------------------------------------------------ #
 
    def ouvrir_transfert(self):
        if not self.compte_actif:
            return
        modal = self._creer_modal("Transfert", hauteur=270)
        ctk.CTkLabel(modal, text="Numero de compte receveur (FR...)", font=("Helvetica", 13)).place(x=20, y=60)
        entry_numero = ctk.CTkEntry(modal, placeholder_text="Ex : FR1234567890123456", width=340, height=40)
        entry_numero.place(x=20, y=90)
        ctk.CTkLabel(modal, text="Montant (EUR)", font=("Helvetica", 13)).place(x=20, y=140)
        entry_montant = ctk.CTkEntry(modal, placeholder_text="Ex : 100", width=340, height=40)
        entry_montant.place(x=20, y=165)
        msg = ctk.CTkLabel(modal, text="", font=("Helvetica", 12))
        msg.place(x=20, y=215)
 
        def valider():
            from bdd_connector import connexion
            numero = entry_numero.get().strip()
            try:
                montant = float(entry_montant.get().replace(",", "."))
                if montant <= 0:
                    raise ValueError
            except ValueError:
                msg.configure(text="Montant invalide.", text_color="red")
                return
            if numero == self.compte_actif.numero_compte:
                msg.configure(text="Impossible vers le meme compte.", text_color="red")
                return
            if montant > self.compte_actif.solde:
                msg.configure(text="Solde insuffisant.", text_color="red")
                return
            # Recherche de l'ID interne a partir du numero de compte
            _, cur = connexion()
            cur.execute("SELECT id FROM compte_bancaire WHERE numero_compte = %s", (numero,))
            row = cur.fetchone()
            if not row:
                msg.configure(text="Numero de compte introuvable.", text_color="red")
                return
            id_receveur = row[0]
            self.compte_actif.transfert(id_receveur, montant)
            self._rafraichir_solde()
            self._afficher_graphique()
            msg.configure(text=f"Transfert de {montant}EUR effectue.", text_color="green")
 
        ctk.CTkButton(modal, text="Confirmer", command=valider,
                      fg_color="red", hover_color="#FD4F4F", width=340, height=40).place(x=20, y=225)
 
    # ------------------------------------------------------------------ #
    #  Modal Nouveau compte                                                 #
    # ------------------------------------------------------------------ #
 
    def ouvrir_nouveau_compte(self):
        modal = self._creer_modal("Nouveau compte bancaire", hauteur=180)
        ctk.CTkLabel(modal, text="Creer un nouveau compte associe\na votre profil ?", font=("Helvetica", 13)).place(x=20, y=60)
        feedback = ctk.CTkLabel(modal, text="", font=("Helvetica", 12))
        feedback.place(x=20, y=115)
 
        def confirmer():
            numero = self.user.ajouter_compte()
            noms_comptes = [f"Compte {i+1} — {c.numero_compte}" for i, c in enumerate(self.user.list_compte)]
            self.dropdown_compte.configure(values=noms_comptes)
            feedback.configure(text=f"Compte {numero} cree !", text_color="green")
 
        ctk.CTkButton(modal, text="Confirmer", command=confirmer,
                      fg_color="red", hover_color="#FD4F4F", width=340, height=40).place(x=20, y=125)
 
 
    def _afficher_graphique(self):
        from bdd_connector import connexion
        # Nettoyage du frame
        for widget in self.graphique_frame.winfo_children():
            widget.destroy()
 
        # Récupération des transactions du compte actif
        _, cur = connexion()
        cur.execute(
            "SELECT date, type, montant FROM `transaction` "
            "WHERE expediteur_id = %s OR receveur_id = %s ORDER BY date ASC",
            (self.compte_actif.id, self.compte_actif.id)
        )
        rows = cur.fetchall()
 
        # Construction de la figure avec 2 sous-graphiques
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.2, 5.3), facecolor="white")
        fig.subplots_adjust(hspace=0.45, left=0.1, right=0.97, top=0.93, bottom=0.1)
 
        if not rows:
            ax1.text(0.5, 0.5, "Aucune transaction", ha="center", va="center",
                     transform=ax1.transAxes, fontsize=12, color="gray")
            ax2.text(0.5, 0.5, "Aucune transaction", ha="center", va="center",
                     transform=ax2.transAxes, fontsize=12, color="gray")
        else:
            dates, types, montants = zip(*rows)
            dates = [d if isinstance(d, datetime) else datetime.strptime(str(d), "%Y-%m-%d %H:%M:%S") for d in dates]
 
            # --- Courbe solde cumulé ---
            solde_initial = self.compte_actif.solde
            # On reconstitue le solde en partant de la fin
            deltas = []
            for t, m in zip(types, montants):
                m = float(m)
                if t == "depot" or t == "transfert" and True:
                    deltas.append(m if t == "depot" else -m)
                elif t == "retrait":
                    deltas.append(-m)
                else:
                    deltas.append(-m)
            # Calcul du solde de départ
            solde_debut = solde_initial - sum(deltas)
            soldes = [solde_debut]
            for d in deltas:
                soldes.append(soldes[-1] + d)
            soldes_plot = soldes[1:]  # on aligne avec les dates
 
            ax1.plot(dates, soldes_plot, color="red", linewidth=2, marker="o", markersize=3)
            ax1.fill_between(dates, soldes_plot, alpha=0.1, color="red")
            ax1.set_title("Évolution du solde", fontsize=11, fontweight="bold", color="#222")
            ax1.set_ylabel("Solde (€)", fontsize=9)
            ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%y"))
            ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
            fig.autofmt_xdate(rotation=30)
            ax1.grid(axis="y", linestyle="--", alpha=0.4)
            ax1.spines[["top", "right"]].set_visible(False)
 
            # --- Barres par type ---
            totaux = defaultdict(float)
            for t, m in zip(types, montants):
                totaux[t] += float(m)
 
            couleurs = {"depot": "#2ecc71", "retrait": "#e74c3c", "transfert": "#3498db"}
            labels = list(totaux.keys())
            valeurs = [totaux[l] for l in labels]
            colors = [couleurs.get(l, "#999") for l in labels]
 
            bars = ax2.bar(labels, valeurs, color=colors, width=0.4, edgecolor="white")
            ax2.set_title("Total par type d'opération", fontsize=11, fontweight="bold", color="#222")
            ax2.set_ylabel("Montant (€)", fontsize=9)
            ax2.grid(axis="y", linestyle="--", alpha=0.4)
            ax2.spines[["top", "right"]].set_visible(False)
            for bar, val in zip(bars, valeurs):
                ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(valeurs) * 0.02,
                         f"{val:.2f}€", ha="center", va="bottom", fontsize=9, fontweight="bold")
 
        canvas = FigureCanvasTkAgg(fig, master=self.graphique_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)
 
 
    # ------------------------------------------------------------------ #
    #  Navigation                                                           #
    # ------------------------------------------------------------------ #
 
    def ouvrir_historique(self):
        from historique_affichage import Historique_affichage
        self._fermer_modal()
        self.frame.destroy()
        historique_ = Historique_affichage(self.display)
        historique_.afficher(self.user)
 
    def deconnecter(self):
        from log import Log
        self._fermer_modal()
        self.frame.destroy()
        log = Log(self.display)
        log.afficher()