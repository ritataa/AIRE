import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db.database import Database

class GraficiView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        self.db = Database()

        # Titolo della sezione
        tk.Label(self, text="Analisi Grafica Inquinanti", font=("Arial", 18, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=10)

        # Pulsante di aggiornamento
        tk.Button(self, text="🔄 Aggiorna Grafici", command=self.disegna_grafici, bg="#3498db", fg="black").pack(pady=5)

        # Frame che conterrà il canvas di matplotlib
        self.grafici_frame = tk.Frame(self, bg="#ffffff")
        self.grafici_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Disegna i grafici in automatico all'apertura
        self.disegna_grafici()

    def disegna_grafici(self):
        # 1. Pulisce i grafici precedenti per evitare sovrapposizioni
        for widget in self.grafici_frame.winfo_children():
            widget.destroy()

        conn = self.db.connect()
        if not conn or not conn.is_connected():
            messagebox.showerror("Errore", "Nessuna connessione al database.")
            return

        try:
            cursor = conn.cursor()

            # --- Dati per Grafico 1: Andamento PM10 ---
            cursor.execute("""
                SELECT m.data_rilevazione, m.valore 
                FROM misurazioni m
                JOIN inquinanti i ON m.inquinante_id = i.id
                WHERE i.nome = 'PM10'
                ORDER BY m.data_rilevazione DESC
                LIMIT 30
            """)
            df_line = pd.DataFrame(cursor.fetchall(), columns=['data', 'valore'])
            if not df_line.empty:
                # FORZIAMO LA CONVERSIONE IN FLOAT
                df_line['valore'] = df_line['valore'].astype(float)
                df_line = df_line.sort_values(by='data')

            # --- Dati per Grafico 2: Media valori per inquinante ---
            cursor.execute("""
                SELECT i.nome, AVG(m.valore) as media_valore
                FROM misurazioni m
                JOIN inquinanti i ON m.inquinante_id = i.id
                GROUP BY i.nome
            """)
            df_bar = pd.DataFrame(cursor.fetchall(), columns=['nome', 'media_valore'])
            if not df_bar.empty:
                # FORZIAMO LA CONVERSIONE IN FLOAT
                df_bar['media_valore'] = df_bar['media_valore'].astype(float)
            
            cursor.close()

            # --- 2. Creazione della Figura Matplotlib ---
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=100)
            fig.patch.set_facecolor('#ffffff')

            # Plot 1: Line Chart
            if not df_line.empty:
                ax1.plot(df_line['data'].astype(str), df_line['valore'], marker='o', color='#e74c3c', linestyle='-')
                ax1.set_title("Andamento PM10 (ultime 30 rilevazioni)")
                ax1.tick_params(axis='x', rotation=45)
                ax1.set_ylabel("Valore (µg/m³)")
                ax1.grid(True, linestyle='--', alpha=0.7)
            else:
                ax1.text(0.5, 0.5, "Nessun dato PM10", ha='center')

            # Plot 2: Bar Chart
            if not df_bar.empty:
                ax2.bar(df_bar['nome'], df_bar['media_valore'], color=['#3498db', '#2ecc71', '#f1c40f'])
                ax2.set_title("Media Storica per Inquinante")
                ax2.set_ylabel("Valore Medio")
                for index, value in enumerate(df_bar['media_valore']):
                    # Ora value è un float, quindi la somma con 0.5 funziona perfettamente
                    ax2.text(index, value + 0.5, f"{value:.1f}", ha='center')
            else:
                ax2.text(0.5, 0.5, "Nessun dato disponibile", ha='center')

            fig.tight_layout()

            # --- 3. Integrazione in Tkinter ---
            canvas = FigureCanvasTkAgg(fig, master=self.grafici_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile generare i grafici:\n{e}")