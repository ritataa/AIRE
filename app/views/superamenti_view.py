import tkinter as tk
from tkinter import ttk, messagebox
from db.database import Database

class SuperamentiView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        self.db = Database()

        tk.Label(self, text="Superamenti Limiti UE", font=("Arial", 18, "bold"),bg="#ffffff", fg="#2c3e50").pack(pady=10)
        tk.Label(self, text="Rilevamenti che hanno superato la soglia critica stabilita dall'Unione Europea.", bg="#ffffff", fg="#2c3e50", font=("Arial", 12)).pack(pady=5)

        tk.Button(self, text="🔄 Ricarica Dati", command=self.carica_dati, bg="#e74c3c", fg="black", font=("Arial", 10, "bold")).pack(pady=10)

        colonne = ("Data", "Stazione", "Inquinante", "Valore Rilevato", "Limite UE")
        self.tree = ttk.Treeview(self, columns=colonne, show="headings", height=20)

        for col in colonne:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        self.carica_dati()

    def carica_dati(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = self.db.connect()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            
            # Query riscritta con il nuovo schema
            query = """
                SELECT r.data_rilevamento, s.nome, i.nome_inquinante, r.valore, i.valore_limite
                FROM rilevamenti r
                JOIN stazioni_rilevamento s ON r.id_stazione = s.id_stazione
                JOIN inquinanti i ON r.id_inquinante = i.id_inquinante
                WHERE r.valore > i.valore_limite
                ORDER BY r.data_rilevamento DESC
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