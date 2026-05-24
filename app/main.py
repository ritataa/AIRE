import tkinter as tk
import traceback

# Importiamo il database
from db.database import Database

class AireApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AIRE - Modalità Acchiappa Errori")
        self.geometry("900x600")
        
        # Sfondo grigio chiaro fisso
        self.configure(bg="#cccccc")
        self.setup_ui()

    def setup_ui(self):
        self.sidebar = tk.Frame(self, bg="#2c3e50", width=200)
        self.sidebar.pack(side="left", fill="y")

        # Area principale con sfondo bianco, se diventa nera significa che sta collassando!
        self.main_area = tk.Frame(self, bg="#ffffff")
        self.main_area.pack(side="left", fill="both", expand=True)

        tk.Label(self.sidebar, text="Menu AIRE", fg="white", bg="#2c3e50", font=("Arial", 16, "bold")).pack(pady=20)

        buttons = ["Home", "Misurazioni", "Grafici", "Superamenti", "Stazioni"]
        for btn_text in buttons:
            btn = tk.Button(self.sidebar, text=btn_text, bg="#34495e", fg="black", font=("Arial", 12),
                            command=lambda t=btn_text: self.change_view(t))
            btn.pack(fill="x", pady=5, padx=10)

        self.change_view("Home")

    def change_view(self, view_name):
        for widget in self.main_area.winfo_children():
            widget.destroy()
            
        self.update_idletasks()

        # IL TRUCCO È QUI: Proviamo a caricare la schermata, se fallisce mostriamo l'errore a video!
        try:
            if view_name == "Home":
                from views.home_view import HomeView
                vista = HomeView(self.main_area)
                vista.pack(fill="both", expand=True)
                
            elif view_name == "Misurazioni":
                from views.misurazioni_view import MisurazioniView
                vista = MisurazioniView(self.main_area)
                vista.pack(fill="both", expand=True)
                
            elif view_name == "Grafici":
                from views.grafici_view import GraficiView
                vista = GraficiView(self.main_area)
                vista.pack(fill="both", expand=True)
                
            elif view_name == "Superamenti":
                from views.superamenti_view import SuperamentiView
                vista = SuperamentiView(self.main_area)
                vista.pack(fill="both", expand=True)
                
            elif view_name == "Stazioni":
                from views.stazioni_view import StazioniView
                vista = StazioniView(self.main_area)
                vista.pack(fill="both", expand=True)

        except Exception as e:
            # Se c'è un errore, disegna uno sfondo nero con scritte rosse giganti!
            errore_completo = traceback.format_exc()
            error_frame = tk.Frame(self.main_area, bg="black")
            error_frame.pack(fill="both", expand=True)
            
            tk.Label(error_frame, text="⚠️ ERRORE CRITICO TROVATO ⚠️", fg="red", bg="black", font=("Arial", 18, "bold")).pack(pady=20)
            tk.Label(error_frame, text=errore_completo, fg="yellow", bg="black", font=("Courier", 12), justify="left").pack(padx=20, pady=10)
            print("Errore critico catturato!")

if __name__ == "__main__":
    app = AireApp()
    app.mainloop()