import mysql.connector
from mysql.connector import Error
# Active: 1773930107655@@localhost@3306@aire_db
class Database:
    _instance = None

    def __new__(cls):
        # Implementazione del pattern Singleton
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        """Stabilisce o recupera la connessione al database aire_db."""
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host='localhost',
                    database='aire_db', # Il nome richiesto dalla consegna
                    user='root',        # Modifica con il tuo username di MySQL
                    password=''     # Modifica con la tua password di MySQL
                )
                if self.connection.is_connected():
                    print("Connessione al database MySQL 'aire_db' avvenuta con successo!")
            except Error as e:
                print(f"Errore durante la connessione a MySQL: {e}")
        
        return self.connection

    def close(self):
        """Chiude la connessione in modo sicuro."""
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            print("Connessione a MySQL chiusa.")