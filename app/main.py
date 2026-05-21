import tkinter as tk
from tkinter import ttk
from db.database import Database
from views.misurazioni_view import MisurazioniView
from views.grafici_view import GraficiView
from views.superamenti_view import SuperamentiView
from views.home_view import HomeView
from views.stazioni_view import StazioniView

class AireApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configurazione base della finestra
        self.title("AIRE - Qualità dell'Aria a Milano")
        self.geometry("900x600")
        self.configure(bg="#f4f4f4")

        self.setup_ui()

    def setup_ui(self):
        # Frame per il Menu laterale
        self.sidebar = tk.Frame(self, bg="#2c3e50", width=200)
        self.sidebar.pack(side="left", fill="y")

        # Frame per l'Area principale centrale
        self.main_area = tk.Frame(self, bg="#ffffff")
        self.main_area.pack(side="right", fill="both", expand=True)

        # Titolo del menu
        tk.Label(self.sidebar, text="Menu AIRE", fg="white", bg="#2c3e50", 
                 font=("Arial", 16, "bold")).pack(pady=20)

        # Pulsanti di navigazione richiesti dalla consegna
        buttons = ["Home", "Misurazioni", "Grafici", "Superamenti", "Stazioni"]
        
        for btn_text in buttons:
            # Usiamo una lambda per passare il nome corretto al comando
            btn = tk.Button(self.sidebar, text=btn_text, bg="#34495e", fg="black", 
                            font=("Arial", 12),
                            command=lambda t=btn_text: self.change_view(t))
            btn.pack(fill="x", pady=5, padx=10)

        # Apre la Home di default all'avvio
        self.change_view("Home")

    def change_view(self, view_name):
        # 1. Distruggiamo tutti i widget attualmente presenti nell'area centrale
        for widget in self.main_area.winfo_children():
            widget.destroy()

        # 2. Carichiamo la vista corrispondente al pulsante cliccato

        if view_name == "Home":
            vista = HomeView(self.main_area)
            vista.pack(fill="both", expand=True)

        elif view_name == "Misurazioni":
            vista = MisurazioniView(self.main_area)
            vista.pack(fill="both", expand=True)

        elif view_name == "Grafici":
            vista = GraficiView(self.main_area)
            vista.pack(fill="both", expand=True)

        elif view_name == "Superamenti":
            vista = SuperamentiView(self.main_area)
            vista.pack(fill="both", expand=True)
        
        elif view_name == "Stazioni":
            vista = StazioniView(self.main_area)
            vista.pack(fill="both", expand=True)

        else:
            # Per le altre schermate non ancora create, mostriamo un testo provvisorio
            tk.Label(self.main_area, text=f"Schermata '{view_name}' in costruzione 🛠️", 
                     bg="#ffffff", font=("Arial", 16)).pack(pady=100)
        print(f"Hai cliccato per aprire la vista: {view_name}")

if __name__ == "__main__":
    # Testiamo la connessione all'avvio
    db = Database()
    db.connect()

    app = AireApp()
    app.mainloop()

    # Chiudiamo la connessione quando chiudiamo la finestra
    db.close()