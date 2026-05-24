import tkinter as tk
from tkinter import ttk, messagebox
from db.database import Database

class StazioniView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        self.db = Database()

        tk.Label(self, text="Anagrafica Stazioni di Rilevamento", font=("Arial", 18, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=10)
        tk.Label(self, text="Elenco delle centraline con coordinate geografiche reali.", bg="#ffffff", font=("Arial", 11), fg="#7f8c8d").pack(pady=5)

        # Tabella aggiornata con i nuovi campi del DB
        colonne = ("ID Stazione", "Nome Centralina", "Longitudine (X)", "Latitudine (Y)")
        self.tree = ttk.Treeview(self, columns=colonne, show="headings", height=15)

        for col in colonne:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        self.carica_stazioni()

    def carica_stazioni(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = self.db.connect()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                # Query aggiornata con i nuovi nomi delle colonne
                cursor.execute("SELECT id_stazione, nome, long_x_4326, lat_y_4326 FROM stazioni_rilevamento ORDER BY id_stazione")
                for riga in cursor.fetchall():
                    self.tree.insert("", "end", values=riga)
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile caricare le stazioni:\n{e}")
            finally:
                cursor.close()