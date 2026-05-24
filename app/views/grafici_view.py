import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib
# Forza il backend TkAgg per garantire l'embedding in Tkinter su macOS
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db.database import Database

class GraficiView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        self.db = Database()

        tk.Label(self, text="Analisi Grafica Inquinanti", font=("Arial", 18, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=10)
        tk.Button(self, text="🔄 Aggiorna Grafici", command=self.disegna_grafici, bg="#3498db", fg="black").pack(pady=5)

        self.grafici_frame = tk.Frame(self, bg="#ffffff")
        self.grafici_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.disegna_grafici()

    def disegna_grafici(self):
        for widget in self.grafici_frame.winfo_children():
            widget.destroy()

        conn = self.db.connect()
        if not conn or not conn.is_connected():
            messagebox.showerror("Errore", "Nessuna connessione al database.")
            return

        try:
            cursor = conn.cursor()

            # Query 1: Andamento PM10 (Nuovo Schema)
            cursor.execute("""
                SELECT r.data_rilevamento, r.valore 
                FROM rilevamenti r
                JOIN inquinanti i ON r.id_inquinante = i.id_inquinante
                WHERE i.nome_inquinante = 'PM10'
                ORDER BY r.data_rilevamento DESC
                LIMIT 30
            """)
            df_line = pd.DataFrame(cursor.fetchall(), columns=['data', 'valore'])
            print('DEBUG: fetched df_line rows:', len(df_line))
            if not df_line.empty:
                df_line['valore'] = df_line['valore'].astype(float)
                df_line = df_line.sort_values(by='data')

            # Query 2: Medie storiche (Nuovo Schema)
            cursor.execute("""
                SELECT i.nome_inquinante, AVG(r.valore) as media_valore
                FROM rilevamenti r
                JOIN inquinanti i ON r.id_inquinante = i.id_inquinante
                GROUP BY i.nome_inquinante
            """)
            df_bar = pd.DataFrame(cursor.fetchall(), columns=['nome', 'media_valore'])
            print('DEBUG: fetched df_bar rows:', len(df_bar))
            if not df_bar.empty:
                df_bar['media_valore'] = df_bar['media_valore'].astype(float)
            
            cursor.close()

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=100)
            fig.patch.set_facecolor('#ffffff')

            if not df_line.empty:
                ax1.plot(df_line['data'].astype(str), df_line['valore'], marker='o', color='#e74c3c', linestyle='-')
                ax1.set_title("Andamento PM10 (Ultime 30 rilevazioni)")
                ax1.tick_params(axis='x', rotation=45)
                ax1.set_ylabel("Valore (µg/m³)")
                ax1.grid(True, linestyle='--', alpha=0.7)
            else:
                ax1.text(0.5, 0.5, "Nessun dato PM10", ha='center')

            if not df_bar.empty:
                ax2.bar(df_bar['nome'], df_bar['media_valore'], color=['#3498db', '#2ecc71', '#f1c40f'])
                ax2.set_title("Media Storica per Inquinante")
                ax2.set_ylabel("Valore Medio")
                for index, value in enumerate(df_bar['media_valore']):
                    ax2.text(index, value + 0.5, f"{value:.1f}", ha='center')
            else:
                ax2.text(0.5, 0.5, "Nessun dato disponibile", ha='center')

            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.grafici_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile generare i grafici:\n{e}")