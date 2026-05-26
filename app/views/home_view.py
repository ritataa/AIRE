import tkinter as tk
from db.database import Database

class HomeView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        self.db = Database()

        self.build_ui()
        self.after(0, self.load_stats)

    def build_ui(self):
        tk.Label(
            self,
            text="Benvenuto in AIRE",
            font=("Arial", 28, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(pady=(50, 10))

        tk.Label(
            self,
            text="Sistema di Monitoraggio Qualità dell'Aria a Milano",
            font=("Arial", 14),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(pady=5)

        self.stats_frame = tk.Frame(self, bg="#ffffff")
        self.stats_frame.pack(pady=50)

        self.rilevamenti_value = tk.Label(
            self.stats_frame,
            text="Caricamento...",
            font=("Arial", 24, "bold"),
            bg="#ecf0f1",
            fg="#2980b9",
            padx=40,
            pady=20
        )
        self.rilevamenti_value.grid(row=0, column=0, padx=30)

        self.stazioni_value = tk.Label(
            self.stats_frame,
            text="Caricamento...",
            font=("Arial", 24, "bold"),
            bg="#ecf0f1",
            fg="#2980b9",
            padx=40,
            pady=20
        )
        self.stazioni_value.grid(row=0, column=1, padx=30)

        # Etichette descrittive sotto i valori
        self.rilevamenti_text = tk.Label(
            self.stats_frame,
            text="Misurazioni Totali",
            font=("Arial", 12),
            bg="#ffffff",
            fg="#34495e"
        )
        self.rilevamenti_text.grid(row=1, column=0, pady=(10,0))

        self.stazioni_text = tk.Label(
            self.stats_frame,
            text="Stazioni di Rilevamento",
            font=("Arial", 12),
            bg="#ffffff",
            fg="#34495e"
        )
        self.stazioni_text.grid(row=1, column=1, pady=(10,0))

    def load_stats(self):
        try:
            conn = self.db.connect()
            if not conn or not conn.is_connected():
                self.rilevamenti_value.config(text="N/D")
                self.stazioni_value.config(text="N/D")
                return

            cursor = conn.cursor(buffered=True)
            try:
                cursor.execute("SELECT COUNT(*) FROM rilevamenti")
                risultato_ril = cursor.fetchone()
                if risultato_ril:
                    formatted = f"{risultato_ril[0]:,}".replace(",", ".")
                    self.rilevamenti_value.config(text=formatted)
                    # Aggiorna anche il testo descrittivo con il valore
                    self.rilevamenti_text.config(text=f"Misurazioni Totali")

                cursor.execute("SELECT COUNT(*) FROM stazioni_rilevamento")
                risultato_staz = cursor.fetchone()
                if risultato_staz:
                    count_staz = risultato_staz[0]
                    self.stazioni_value.config(text=str(count_staz))
                    self.stazioni_text.config(text=f"Stazioni di Rilevamento")
            finally:
                cursor.close()

        except Exception as e:
            print(f"Errore caricamento HomeView: {e}")
            self.rilevamenti_value.config(text="N/D")
            self.stazioni_value.config(text="N/D")

            
    def crea_card(self, parent, icona, titolo, valore, col):
        card = tk.Frame(parent, bg="#ecf0f1", bd=0, highlightbackground="#bdc3c7", highlightthickness=1, padx=40, pady=20)
        card.grid(row=0, column=col, padx=30)
        
        tk.Label(card, text=icona, font=("Arial", 36), bg="#ecf0f1").pack()
        tk.Label(card, text=valore, font=("Arial", 24, "bold"), bg="#ecf0f1", fg="#2980b9").pack(pady=10)
        tk.Label(card, text=titolo, font=("Arial", 12), bg="#ecf0f1", fg="#34495e").pack()