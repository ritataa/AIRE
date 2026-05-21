import tkinter as tk
from tkinter import ttk, messagebox
from db.database import Database

class SuperamentiView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        self.db = Database()

        # Titoli e descrizioni
        tk.Label(self, text="Superamenti Limiti UE", font=("Arial", 18, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=10)
        tk.Label(self, text="Elenco delle rilevazioni in cui il valore dell'inquinante ha superato la soglia di legge.", 
                 bg="#ffffff", fg="#2c3e50", font=("Arial", 12)).pack(pady=5)

        # Pulsante di aggiornamento
        tk.Button(self, text="🔄 Ricarica Dati", command=self.carica_dati, bg="#3498db", fg="black", font=("Arial", 10, "bold")).pack(pady=10)

        # Tabella
        colonne = ("Data", "Stazione", "Inquinante", "Valore Rilevato", "Limite UE")
        self.tree = ttk.Treeview(self, columns=colonne, show="headings", height=20)

        for col in colonne:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Carica automaticamente all'apertura
        self.carica_dati()

    def carica_dati(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = self.db.connect()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            
            # La magia è qui: filtriamo direttamente da DB usando >
            query = """
                SELECT m.data_rilevazione, s.nome, i.nome, m.valore, i.limite_ue
                FROM misurazioni m
                JOIN stazioni s ON m.stazione_id = s.id
                JOIN inquinanti i ON m.inquinante_id = i.id
                WHERE m.valore > i.limite_ue
                ORDER BY m.data_rilevazione DESC
                LIMIT 200
            """
            try:
                cursor.execute(query)
                for riga in cursor.fetchall():
                    self.tree.insert("", "end", values=riga)
            except Exception as e:
                messagebox.showerror("Errore query", f"Impossibile caricare i superamenti:\n{e}")
            finally:
                cursor.close()