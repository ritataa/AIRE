import tkinter as tk
from db.database import Database

class HomeView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        self.db = Database()

        # Intestazione principale
        tk.Label(self, text="Benvenuto in AIRE", font=("Arial", 28, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=(50, 10))
        tk.Label(self, text="Sistema di Monitoraggio Qualità dell'Aria a Milano", font=("Arial", 14), bg="#ffffff", fg="#7f8c8d").pack(pady=5)

        # Frame orizzontale per contenere le "Card" delle statistiche
        stats_frame = tk.Frame(self, bg="#ffffff")
        stats_frame.pack(pady=50)

        # Variabili di default in caso di errore
        tot_misurazioni = "N/D"
        tot_stazioni = "N/D"

        # Connessione al database per estrarre i conteggi in tempo reale
        conn = self.db.connect()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                # Conta tutte le righe della tabella misurazioni
                cursor.execute("SELECT COUNT(*) FROM misurazioni")
                # Formattiamo il numero con i puntini delle migliaia (es. 170.393)
                tot_misurazioni = f"{cursor.fetchone()[0]:,}".replace(',', '.')
                
                # Conta le centraline
                cursor.execute("SELECT COUNT(*) FROM stazioni")
                tot_stazioni = cursor.fetchone()[0]
            except Exception as e:
                print(f"Errore durante il caricamento delle statistiche: {e}")
            finally:
                cursor.close()

        # Disegna le Card chiamando la funzione di supporto
        self.crea_card(stats_frame, "📊", "Misurazioni Rilevate", str(tot_misurazioni), 0)
        self.crea_card(stats_frame, "📍", "Stazioni Monitorate", str(tot_stazioni), 1)

    def crea_card(self, parent, icona, titolo, valore, col):
        """Crea un riquadro grafico (Card) per visualizzare un singolo dato statistico."""
        card = tk.Frame(parent, bg="#ecf0f1", bd=0, highlightbackground="#bdc3c7", highlightthickness=1, padx=40, pady=20)
        card.grid(row=0, column=col, padx=30)
        
        tk.Label(card, text=icona, font=("Arial", 36), bg="#ecf0f1").pack()
        tk.Label(card, text=valore, font=("Arial", 24, "bold"), bg="#ecf0f1", fg="#2980b9").pack(pady=10)
        tk.Label(card, text=titolo, font=("Arial", 12), bg="#ecf0f1", fg="#34495e").pack()