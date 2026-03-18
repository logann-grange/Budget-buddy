import customtkinter as ctk

class Historique:
    def __init__(self, display):
        self.display = display
        self.frame = None

    def afficher(self):
        self.frame = ctk.CTkFrame(self.display, width=1080, height=720, fg_color="transparent")
        self.frame.place(x=0, y=0)

        back_button = ctk.CTkButton(self.frame, text="← Retour", command=self.retour_menu, fg_color="red", hover_color="#FD4F4F", width=100, height=30)
        back_button.place(x=20, y=20)

        title_label = ctk.CTkLabel(self.frame, text="Historique détaillé", font=("Helvetica", 32, "bold"))
        title_label.place(x=400, y=30)

        depenses_frame = ctk.CTkFrame(self.frame, width=500, height=600, fg_color="white", border_width=2, border_color="white")
        depenses_frame.place(x=20, y=100)

        depenses_label = ctk.CTkLabel(depenses_frame, text="de -X€ date raison", font=("Helvetica", 18, "bold"), text_color="red")
        depenses_label.place(x=20, y=20)

        depenses_text = ctk.CTkLabel(depenses_frame,
            text="",
            font=("Helvetica", 12), text_color="black", justify="left")
        depenses_text.place(x=20, y=70)

        revenus_frame = ctk.CTkFrame(self.frame, width=500, height=600, fg_color="white", border_width=2, border_color="white")
        revenus_frame.place(x=540, y=100)

        revenus_label = ctk.CTkLabel(revenus_frame, text="a +X€ date", font=("Helvetica", 18, "bold"), text_color="green")
        revenus_label.place(x=20, y=20)

        revenus_text = ctk.CTkLabel(revenus_frame,
            text="",
            font=("Helvetica", 12), text_color="black", justify="left")
        revenus_text.place(x=20, y=70)

    def retour_menu(self):
        from menu import Menu
        self.frame.destroy()
        menu = Menu(self.display)
        menu.afficher()
