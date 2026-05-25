# AIRE

Applicazione desktop in Python per consultare e gestire i dati sulle rilevazioni di qualità dell'aria.

## Versioni consigliate da installare

Le versioni sotto sono quelle già presenti nel virtualenv del progetto e sono quelle consigliate per avviare il programma senza sorprese:

- Python 3.14.5
- MySQL Server 8.0.x o compatibile
- mysql-connector-python 9.7.0
- pandas 3.0.3
- matplotlib 3.10.9
- numpy 2.4.6
- pillow 12.2.0

Le dipendenze transitive vengono installate automaticamente con `pip` e non vanno scaricate a mano.

## Prerequisiti su macOS

- Python 3.14.5 installato da python.org o tramite il tuo gestore preferito
- Tkinter disponibile con l'installazione di Python
- MySQL Server avviato in locale

## Preparazione dell'ambiente

Da terminale, nella cartella del progetto:

```bash
cd /Users/rita/Downloads/AIRE
python3.14 -m venv venv
source venv/bin/activate
pip install mysql-connector-python==9.7.0 pandas==3.0.3 matplotlib==3.10.9 numpy==2.4.6 pillow==12.2.0
```

Se il comando `python3.14` non è disponibile, usa il Python 3.14.5 installato sul sistema.

## Database

Il programma usa un database MySQL chiamato `aire_db`.

1. Avvia MySQL in locale.
2. Crea il database importando il file `app/db/aire_db.sql`.
3. Verifica le credenziali in `app/db/database.py`:
   - host: `localhost`
   - database: `aire_db`
   - user: `root`
   - password: vuota

Nota: il file SQL contiene percorsi assoluti per il caricamento dei CSV. Se hai spostato la cartella del progetto, aggiorna quei percorsi prima di importare i dati.

## Avvio del programma

La cartella `app` deve essere la directory di lavoro, perché i moduli vengono importati con percorsi relativi.

```bash
cd /Users/rita/Downloads/AIRE/app
python main.py
```

## Struttura essenziale

- `app/main.py` avvia l'interfaccia grafica
- `app/views/` contiene le schermate dell'applicazione
- `app/db/database.py` gestisce la connessione a MySQL
- `app/db/aire_db.sql` crea schema e tabelle

## Se qualcosa non parte

- Controlla che MySQL sia acceso
- Controlla che il database `aire_db` esista
- Controlla che il virtualenv sia attivo
- Controlla che i CSV usati dal file SQL siano nel percorso corretto
