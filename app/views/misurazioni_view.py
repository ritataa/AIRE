import tkinter as tk
from tkinter import ttk, messagebox
from db.database import Database

class MisurazioniView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#ffffff")
        self.db = Database()

        # Titolo
        tk.Label(self, text="Gestione Misurazioni", font=("Arial", 18, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=5)

        # --- ZONA FILTRI ---
        self.filtri_frame = tk.LabelFrame(self, text="Filtra Dati", bg="#2c3e50", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.filtri_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(self.filtri_frame, text="Stazione:", bg="#2c3e50").grid(row=0, column=0, padx=5, pady=5)
        self.combo_stazione = ttk.Combobox(self.filtri_frame, state="readonly", width=15)
        self.combo_stazione.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.filtri_frame, text="Inquinante:", bg="#2c3e50").grid(row=0, column=2, padx=5, pady=5)
        self.combo_inquinante = ttk.Combobox(self.filtri_frame, state="readonly", width=10)
        self.combo_inquinante.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.filtri_frame, text="Dal (YYYY-MM-DD):", bg="#2c3e50").grid(row=0, column=4, padx=5, pady=5)
        self.entry_data_inizio = ttk.Entry(self.filtri_frame, width=12)
        self.entry_data_inizio.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(self.filtri_frame, text="Al:", bg="#2c3e50").grid(row=0, column=6, padx=5, pady=5)
        self.entry_data_fine = ttk.Entry(self.filtri_frame, width=12)
        self.entry_data_fine.grid(row=0, column=7, padx=5, pady=5)

        tk.Button(self.filtri_frame, text="🔍 Applica", bg="#3498db", fg="black", command=lambda: self.carica_dati(usa_filtri=True)).grid(row=0, column=8, padx=10)
        tk.Button(self.filtri_frame, text="❌ Reset", bg="#ecf0f1", fg="black", command=self.reset_filtri).grid(row=0, column=9, padx=5)

        # --- TABELLA (Treeview) ---
        colonne = ("ID", "Data", "Valore", "Stazione", "Inquinante")
        self.tree = ttk.Treeview(self, columns=colonne, show="headings", height=10)

        for col in colonne:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=5)

        # --- ZONA CRUD (Form e Pulsanti) ---
        self.crud_frame = tk.Frame(self, bg="#ecf0f1", bd=1, relief="solid")
        self.crud_frame.pack(fill="x", padx=20, pady=5, ipady=5)

        tk.Label(self.crud_frame, text="Data (YYYY-MM-DD):", bg="#2c3e50").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_data = ttk.Entry(self.crud_frame)
        self.entry_data.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.crud_frame, text="Valore:", bg="#2c3e50").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.entry_valore = ttk.Entry(self.crud_frame)
        self.entry_valore.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(self.crud_frame, text="ID Stazione (es. 1):", bg="#2c3e50").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_stazione = ttk.Entry(self.crud_frame)
        self.entry_stazione.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.crud_frame, text="ID Inquinante (es. 1):", bg="#2c3e50").grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.entry_inquinante = ttk.Entry(self.crud_frame)
        self.entry_inquinante.grid(row=1, column=3, padx=10, pady=5)

        btn_frame = tk.Frame(self.crud_frame, bg="#ecf0f1")
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

        tk.Button(btn_frame, text="➕ Aggiungi", bg="#2ecc71", fg="black", command=self.aggiungi_record).pack(side="left", padx=10)
        tk.Button(btn_frame, text="✏️ Modifica Selezionata", bg="#f39c12", fg="black", command=self.modifica_record).pack(side="left", padx=10)
        tk.Button(btn_frame, text="🗑️ Elimina Selezionata", bg="#e74c3c", fg="black", command=self.elimina_record).pack(side="left", padx=10)

        # Inizializzazione dati
        self.popola_tendine()
        self.carica_dati()

    def popola_tendine(self):
        """Recupera i nomi di stazioni e inquinanti dal DB per i menu a tendina."""
        conn = self.db.connect()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT nome FROM stazioni ORDER BY nome")
                self.combo_stazione['values'] = ["Tutte"] + [r[0] for r in cursor.fetchall()]
                self.combo_stazione.current(0)

                cursor.execute("SELECT nome FROM inquinanti ORDER BY nome")
                self.combo_inquinante['values'] = ["Tutti"] + [r[0] for r in cursor.fetchall()]
                self.combo_inquinante.current(0)
            except Exception as e:
                print(f"Errore caricamento tendine: {e}")
            finally:
                cursor.close()

    def reset_filtri(self):
        """Svuota i campi filtro e ricarica tutti i dati."""
        self.combo_stazione.current(0)
        self.combo_inquinante.current(0)
        self.entry_data_inizio.delete(0, tk.END)
        self.entry_data_fine.delete(0, tk.END)
        self.carica_dati()

    def carica_dati(self, usa_filtri=False):
        """Carica i dati nella tabella, applicando i filtri se richiesto."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = self.db.connect()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            
            # Base della query
            query = """
                SELECT m.id, m.data_rilevazione, m.valore, s.nome, i.nome
                FROM misurazioni m
                JOIN stazioni s ON m.stazione_id = s.id
                JOIN inquinanti i ON m.inquinante_id = i.id
                WHERE 1=1
            """
            parametri = []

            # Costruzione dinamica della query in base ai filtri attivi
            if usa_filtri:
                staz = self.combo_stazione.get()
                if staz and staz != "Tutte":
                    query += " AND s.nome = %s"
                    parametri.append(staz)
                    
                inq = self.combo_inquinante.get()
                if inq and inq != "Tutti":
                    query += " AND i.nome = %s"
                    parametri.append(inq)
                    
                d_inizio = self.entry_data_inizio.get()
                if d_inizio:
                    query += " AND m.data_rilevazione >= %s"
                    parametri.append(d_inizio)
                    
                d_fine = self.entry_data_fine.get()
                if d_fine:
                    query += " AND m.data_rilevazione <= %s"
                    parametri.append(d_fine)

            # Aggiungiamo sempre un limite per non bloccare l'interfaccia
            query += " ORDER BY m.data_rilevazione DESC LIMIT 100"

            try:
                cursor.execute(query, tuple(parametri))
                for riga in cursor.fetchall():
                    self.tree.insert("", "end", values=riga)
            except Exception as e:
                messagebox.showerror("Errore query", f"Controlla il formato delle date inserite.\n{e}")
            finally:
                cursor.close()

    # --- METODI CRUD INVARIATI ---
    def elimina_record(self):
        selezione = self.tree.selection()
        if not selezione:
            messagebox.showwarning("Attenzione", "Seleziona prima una riga dalla tabella da eliminare!")
            return
        risposta = messagebox.askyesno("Conferma", "Sei sicuro di voler eliminare questa misurazione?")
        if risposta:
            id_record = self.tree.item(selezione[0])['values'][0]
            conn = self.db.connect()
            if conn and conn.is_connected():
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM misurazioni WHERE id = %s", (id_record,))
                    conn.commit()
                    messagebox.showinfo("Successo", "Record eliminato correttamente.")
                    self.carica_dati(usa_filtri=True) # Mantiene i filtri attivi dopo l'eliminazione
                except Exception as e:
                    messagebox.showerror("Errore", f"Impossibile eliminare: {e}")
                finally:
                    cursor.close()

    def aggiungi_record(self):
        data = self.entry_data.get()
        valore = self.entry_valore.get()
        staz = self.entry_stazione.get()
        inq = self.entry_inquinante.get()

        if not (data and valore and staz and inq):
            messagebox.showwarning("Attenzione", "Compila tutti i campi prima di aggiungere!")
            return

        conn = self.db.connect()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO misurazioni (data_rilevazione, valore, stazione_id, inquinante_id) VALUES (%s, %s, %s, %s)",
                    (data, valore, staz, inq)
                )
                conn.commit()
                messagebox.showinfo("Successo", "Nuova misurazione salvata!")
                self.carica_dati()
                
                self.entry_data.delete(0, tk.END)
                self.entry_valore.delete(0, tk.END)
                self.entry_stazione.delete(0, tk.END)
                self.entry_inquinante.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Errore DB", f"Controlla i formati inseriti.\n{e}")
            finally:
                cursor.close()

    def modifica_record(self):
        selezione = self.tree.selection()
        if not selezione:
            messagebox.showwarning("Attenzione", "Seleziona una riga dalla tabella per modificarla!")
            return

        id_record = self.tree.item(selezione[0])['values'][0]

        data = self.entry_data.get()
        valore = self.entry_valore.get()
        staz = self.entry_stazione.get()
        inq = self.entry_inquinante.get()

        if not (data and valore and staz and inq):
            messagebox.showwarning("Attenzione", "Compila tutti i campi con i nuovi valori per l'aggiornamento!")
            return

        conn = self.db.connect()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "UPDATE misurazioni SET data_rilevazione=%s, valore=%s, stazione_id=%s, inquinante_id=%s WHERE id=%s",
                    (data, valore, staz, inq, id_record)
                )
                conn.commit()
                messagebox.showinfo("Successo", "Misurazione aggiornata!")
                self.carica_dati(usa_filtri=True)
            except Exception as e:
                messagebox.showerror("Errore DB", f"Impossibile modificare.\n{e}")
            finally:
                cursor.close()