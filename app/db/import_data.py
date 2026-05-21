import pandas as pd
import mysql.connector
from database import Database
import os

def importa_dati():
    # Otteniamo i percorsi assoluti dei file considerando che lo script viene lanciato dalla root del progetto
    base_path = os.getcwd()
    file_inquinanti = os.path.join(base_path, 'pv_Inquinanti.csv')
    file_stazioni = os.path.join(base_path, 'pv_stazioni_rilevamento_CLEAN.csv')
    file_rilevamenti = os.path.join(base_path, 'pv_rilevamenti_arpa_unificati.csv')

    # Connessione al database
    db = Database()
    conn = db.connect()
    
    if not conn or not conn.is_connected():
        print("Impossibile connettersi al DB per l'importazione.")
        return

    cursor = conn.cursor()

    try:
        # Svuotiamo le tabelle prima di importare (per evitare duplicati se lo lanci più volte)
        print("Pulizia delle tabelle in corso...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE misurazioni;")
        cursor.execute("TRUNCATE TABLE stazioni;")
        cursor.execute("TRUNCATE TABLE inquinanti;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        # --- 1. Importiamo gli Inquinanti ---
        print("Importazione Inquinanti...")
        # Aggiunto decimal=',' per convertire in automatico le virgole in punti
        df_inq = pd.read_csv(file_inquinanti, sep=';', encoding='latin1', decimal=',')
        
        df_inq.columns = df_inq.columns.str.strip()

        for index, row in df_inq.iterrows():
            sql = "INSERT INTO inquinanti (id, nome, limite_ue) VALUES (%s, %s, %s)"
            # Se il limite non è numerico o manca, mettiamo NULL
            valore_limite = row['Valore_limite'] if pd.notna(row['Valore_limite']) else None
            cursor.execute(sql, (row['ID_inquinante'], row['Nome_inquinante'].strip(), valore_limite))

            
        # --- 2. Importiamo le Stazioni ---
        print("Importazione Stazioni...")
        df_staz = pd.read_csv(file_stazioni)
        for index, row in df_staz.iterrows():
            # Uniamo le coordinate nella colonna 'zona_geografica'
            zona = f"Lon: {row['LONG_X_4326']}, Lat: {row['LAT_Y_4326']}"
            sql = "INSERT INTO stazioni (id, nome, zona_geografica) VALUES (%s, %s, %s)"
            cursor.execute(sql, (row['ID_Stazione'], row['nome'], zona))

    # --- 3. Importiamo le Misurazioni ---
        print("Importazione Misurazioni (potrebbe richiedere qualche secondo)...")
        
        # 1. Proviamo a leggere con il punto e virgola, se non va usiamo la virgola
        df_mis = pd.read_csv(file_rilevamenti, sep=';')
        if len(df_mis.columns) == 1:
            df_mis = pd.read_csv(file_rilevamenti, sep=',')
            
        # 2. Pulizia degli spazi invisibili nelle intestazioni
        df_mis.columns = df_mis.columns.str.strip()

        # 3. Se la colonna è letta come testo, sostituiamo le virgole con i punti
        if df_mis['valore'].dtype == 'object':
            # Convertiamo tutto in stringa, puliamo gli spazi estremi e cambiamo la virgola
            df_mis['valore'] = df_mis['valore'].astype(str).str.strip().str.replace(',', '.')
            
        # 4. LA MAGIA DI PANDAS: Forziamo la conversione a numero. 
        # Tutto ciò che è 'sporco' (come '\N') diventerà NaN senza far crashare il programma.
        df_mis['valore'] = pd.to_numeric(df_mis['valore'], errors='coerce')
        
        # 5. Rimuoviamo definitivamente tutte le righe vuote/sporche
        df_mis = df_mis.dropna(subset=['valore'])

        # Prepariamo i dati per una INSERZIONE DI MASSA (molto più veloce)
        dati_misurazioni = []
        for index, row in df_mis.iterrows():
            dati_misurazioni.append((
                row['_data_'], 
                row['valore'], 
                row['id_stazione'], 
                row['id_inquinante']
            ))
        
        sql_mis = """INSERT INTO misurazioni 
                     (data_rilevazione, valore, stazione_id, inquinante_id) 
                     VALUES (%s, %s, %s, %s)"""
                     
        cursor.executemany(sql_mis, dati_misurazioni)
        
        # Usiamo executemany per inserirli tutti in un colpo
        cursor.executemany(sql_mis, dati_misurazioni)

        # Salviamo i cambiamenti nel database
        conn.commit()
        print(f"Importazione completata con successo! Inserite {cursor.rowcount} misurazioni.")

    except Exception as e:
        print(f"Si è verificato un errore: {e}")
        conn.rollback() # Annulla in caso di errore
    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    importa_dati()