import tkinter as tk
from tkinter import ttk, messagebox
from db.database import Database

class StazioniView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        self.db = Database()

        # Titolo della sezione
        tk.Label(self, text="Anagrafica Stazioni di Rilevamento", font=("Arial", 18, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=10)
        tk.Label(self, text="Elenco delle centraline di monitoraggio della qualità dell'aria dislocate a Milano.", 
                 bg="#ffffff", font=("Arial", 11), fg="#7f8c8d").pack(pady=5)

        # Tabella per visualizzare le stazioni
        colonne = ("ID Stazione", "Nome Centralina", "Coordinate Geografiche")
        self.tree = ttk.Treeview(self, columns=colonne, show="headings", height=15)

        for col in colonne:
            self.tree.heading(col, text=col)
            if col == "Coordinate Geografiche":
                self.tree.column(col, width=250, anchor="center")
            else:
                self.tree.column(col, width=150, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Carica i dati all'apertura
        self.carica_stazioni()

    def carica_stazioni(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = self.db.connect()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT id, nome, zona_geografica FROM stazioni ORDER BY id")
                for riga in cursor.fetchall():
                    self.tree.insert("", "end", values=riga)
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile caricare le stazioni:\n{e}")
            finally:
                cursor.close()