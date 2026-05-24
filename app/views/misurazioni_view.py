import tkinter as tk
from tkinter import ttk, messagebox
import time
from db.database import Database

class MisurazioniView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        self.db = Database()

        tk.Label(self, text="Gestione Rilevamenti", font=("Arial", 18, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=5)

        # --- ZONA FILTRI ---
        self.filtri_frame = tk.LabelFrame(self, text="Filtra Dati", bg="#ffffff", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.filtri_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(self.filtri_frame, text="Stazione:", bg="#ffffff", fg="#2c3e50").grid(row=0, column=0, padx=5, pady=5)
        self.combo_stazione = ttk.Combobox(self.filtri_frame, state="readonly", width=15)
        self.combo_stazione.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.filtri_frame, text="Inquinante:", bg="#ffffff", fg="#2c3e50").grid(row=0, column=2, padx=5, pady=5)
        self.combo_inquinante = ttk.Combobox(self.filtri_frame, state="readonly", width=10)
        self.combo_inquinante.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.filtri_frame, text="Dal:", bg="#ffffff", fg="#2c3e50").grid(row=0, column=4, padx=5, pady=5)
        self.entry_data_inizio = ttk.Entry(self.filtri_frame, width=12)
        self.entry_data_inizio.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(self.filtri_frame, text="Al:", bg="#ffffff", fg="#2c3e50").grid(row=0, column=6, padx=5, pady=5)
        self.entry_data_fine = ttk.Entry(self.filtri_frame, width=12)
        self.entry_data_fine.grid(row=0, column=7, padx=5, pady=5)

        tk.Button(self.filtri_frame, text="🔍 Applica", bg="#3498db", fg="black", command=lambda: self.carica_dati(usa_filtri=True)).grid(row=0, column=8, padx=10)
        tk.Button(self.filtri_frame, text="❌ Reset", bg="#ecf0f1", fg="black", command=self.reset_filtri).grid(row=0, column=9, padx=5)

        # --- TABELLA (Aggiunta colonna Orario) ---
        colonne = ("ID Rilevamento", "Data", "Orario", "Valore", "Stazione", "Inquinante")
        self.tree = ttk.Treeview(self, columns=colonne, show="headings", height=10)

        for col in colonne:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=5)

        # --- ZONA CRUD ---
        self.crud_frame = tk.Frame(self,bg="#ffffff", bd=1, relief="solid")
        self.crud_frame.pack(fill="x", padx=20, pady=5, ipady=5)

        tk.Label(self.crud_frame, text="Data (YYYY-MM-DD):", bg="#ffffff", fg="#2c3e50").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_data = ttk.Entry(self.crud_frame)
        self.entry_data.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.crud_frame, text="Orario (HH:MM):", bg="#ffffff", fg="#2c3e50").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.entry_orario = ttk.Entry(self.crud_frame)
        self.entry_orario.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(self.crud_frame, text="Valore Rilevato:", bg="#ffffff", fg="#2c3e50").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_valore = ttk.Entry(self.crud_frame)
        self.entry_valore.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.crud_frame, text="ID Stazione:", bg="#ffffff", fg="#2c3e50").grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.entry_stazione = ttk.Entry(self.crud_frame)
        self.entry_stazione.grid(row=1, column=3, padx=10, pady=5)

        tk.Label(self.crud_frame, text="ID Inquinante:", bg="#ffffff", fg="#2c3e50").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_inquinante = ttk.Entry(self.crud_frame)
        self.entry_inquinante.grid(row=2, column=1, padx=10, pady=5)

        btn_frame = tk.Frame(self.crud_frame, bg="#ffffff", fg="#2c3e50")
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)

        tk.Button(btn_frame, text="➕ Aggiungi", bg="#2ecc71", fg="black", command=self.aggiungi_record).pack(side="left", padx=10)
        tk.Button(btn_frame, text="✏️ Modifica Selezionata", bg="#f39c12", fg="black", command=self.modifica_record).pack(side="left", padx=10)
        tk.Button(btn_frame, text="🗑️ Elimina Selezionata", bg="#e74c3c", fg="black", command=self.elimina_record).pack(side="left", padx=10)

        self.popola_tendine()
        self.carica_dati()

    def popola_tendine(self):
        conn = self.db.connect()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT nome FROM stazioni_rilevamento ORDER BY nome")
                self.combo_stazione['values'] = ["Tutte"] + [r[0] for r in cursor.fetchall()]
                self.combo_stazione.current(0)

                cursor.execute("SELECT nome_inquinante FROM inquinanti ORDER BY nome_inquinante")
                self.combo_inquinante['values'] = ["Tutti"] + [r[0] for r in cursor.fetchall()]
                self.combo_inquinante.current(0)
            except Exception as e:
                print(f"Errore tendine: {e}")
            finally:
                cursor.close()

    def reset_filtri(self):
        self.combo_stazione.current(0)
        self.combo_inquinante.current(0)
        self.entry_data_inizio.delete(0, tk.END)
        self.entry_data_fine.delete(0, tk.END)
        self.carica_dati()

    def carica_dati(self, usa_filtri=False):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = self.db.connect()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            
            query = """
                SELECT r.id_rilevamento, r.data_rilevamento, r.orario, r.valore, s.nome, i.nome_inquinante
                FROM rilevamenti r
                JOIN stazioni_rilevamento s ON r.id_stazione = s.id_stazione
                JOIN inquinanti i ON r.id_inquinante = i.id_inquinante
                WHERE 1=1
            """
            parametri = []

            if usa_filtri:
                staz = self.combo_stazione.get()
                if staz and staz != "Tutte":
                    query += " AND s.nome = %s"
                    parametri.append(staz)
                    
                inq = self.combo_inquinante.get()
                if inq and inq != "Tutti":
                    query += " AND i.nome_inquinante = %s"
                    parametri.append(inq)
                    
                d_inizio = self.entry_data_inizio.get()
                if d_inizio:
                    query += " AND r.data_rilevamento >= %s"
                    parametri.append(d_inizio)
                    
                d_fine = self.entry_data_fine.get()
                if d_fine:
                    query += " AND r.data_rilevamento <= %s"
                    parametri.append(d_fine)

            query += " ORDER BY r.data_rilevamento DESC, r.orario DESC LIMIT 100"

            try:
                cursor.execute(query, tuple(parametri))
                for riga in cursor.fetchall():
                    # Trasformiamo l'orario in stringa leggibile HH:MM prima di inserirlo nel Treeview
                    riga_lista = list(riga)
                    if riga_lista[2]:
                        # Converte timedelta o time in formato stringa
                        tot_seconds = int(riga_lista[2].total_seconds()) if hasattr(riga_lista[2], 'total_seconds') else 0
                        hours = tot_seconds // 3600
                        minutes = (tot_seconds % 3600) // 60
                        riga_lista[2] = f"{hours:02d}:{minutes:02d}"
                    self.tree.insert("", "end", values=riga_lista)
            except Exception as e:
                messagebox.showerror("Errore query", f"Impossibile caricare i rilevamenti.\n{e}")
            finally:
                cursor.close()

    def elimina_record(self):
        selezione = self.tree.selection()
        if not selezione:
            messagebox.showwarning("Attenzione", "Seleziona prima una riga da eliminare!")
            return
        risposta = messagebox.askyesno("Conferma", "Vuoi eliminare questo rilevamento?")
        if risposta:
            id_record = self.tree.item(selezione[0])['values'][0]
            conn = self.db.connect()
            if conn and conn.is_connected():
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM rilevamenti WHERE id_rilevamento = %s", (id_record,))
                    conn.commit()
                    messagebox.showinfo("Successo", "Rilevamento eliminato correttamente.")
                    self.carica_dati(usa_filtri=True)
                except Exception as e:
                    messagebox.showerror("Errore", f"Impossibile eliminare: {e}")
                finally:
                    cursor.close()

    def aggiungi_record(self):
        data = self.entry_data.get()
        orario = self.entry_orario.get()
        valore = self.entry_valore.get()
        staz = self.entry_stazione.get()
        inq = self.entry_inquinante.get()

        if not (data and orario and valore and staz and inq):
            messagebox.showwarning("Attenzione", "Compila tutti i campi prima di aggiungere!")
            return

        # Generazione automatica di un ID stringa unico basato sul timestamp corrente
        id_nuovo = f"RIL_{int(time.time() * 1000)}"[:20]

        conn = self.db.connect()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO rilevamenti (id_rilevamento, data_rilevamento, orario, valore, id_stazione, id_inquinante) VALUES (%s, %s, %s, %s, %s, %s)",
                    (id_nuovo, data, orario, valore, staz, inq)
                )
                conn.commit()
                messagebox.showinfo("Successo", "Rilevamento inserito!")
                self.carica_dati()
                
                self.entry_data.delete(0, tk.END)
                self.entry_orario.delete(0, tk.END)
                self.entry_valore.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Errore DB", f"Impossibile inserire il record.\n{e}")
            finally:
                cursor.close()

    def modifica_record(self):
        selezione = self.tree.selection()
        if not selezione:
            messagebox.showwarning("Attenzione", "Seleziona prima una riga da modificare!")
            return

        id_record = self.tree.item(selezione[0])['values'][0]
        data = self.entry_data.get()
        orario = self.entry_orario.get()
        valore = self.entry_valore.get()
        staz = self.entry_stazione.get()
        inq = self.entry_inquinante.get()

        if not (data and orario and valore and staz and inq):
            messagebox.showwarning("Attenzione", "Compila tutti i campi per effettuare la modifica!")
            return

        conn = self.db.connect()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "UPDATE rilevamenti SET data_rilevamento=%s, orario=%s, valore=%s, id_stazione=%s, id_inquinante=%s WHERE id_rilevamento=%s",
                    (data, orario, valore, staz, inq, id_record)
                )
                conn.commit()
                messagebox.showinfo("Successo", "Rilevamento modificato con successo!")
                self.carica_dati(usa_filtri=True)
            except Exception as e:
                messagebox.showerror("Errore DB", f"Impossibile modificare il record.\n{e}")
            finally:
                cursor.close()