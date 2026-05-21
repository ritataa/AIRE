-- Creazione del database (se non esiste già)
CREATE DATABASE IF NOT EXISTS aire_db;
USE aire_db;

-- 1. Tabella Inquinanti
CREATE TABLE IF NOT EXISTS inquinanti (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    limite_ue DECIMAL(10, 2) COMMENT 'Limite massimo consentito dall UE'
);

-- 2. Tabella Stazioni
CREATE TABLE IF NOT EXISTS stazioni (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    zona_geografica VARCHAR(100)
);

-- 3. Tabella Misurazioni
CREATE TABLE IF NOT EXISTS misurazioni (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_rilevazione DATE NOT NULL,
    valore DECIMAL(10, 2) NOT NULL,
    stazione_id INT NOT NULL,
    inquinante_id INT NOT NULL,
    FOREIGN KEY (stazione_id) REFERENCES stazioni(id) ON DELETE CASCADE,
    FOREIGN KEY (inquinante_id) REFERENCES inquinanti(id) ON DELETE CASCADE
);

-- Inserimento di base per gli inquinanti più comuni
INSERT IGNORE INTO inquinanti (nome, limite_ue) VALUES 
('PM10', 50.00),
('PM2.5', 25.00),
('NO2', 40.00);