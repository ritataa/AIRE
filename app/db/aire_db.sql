DROP DATABASE IF EXISTS aire_db;

CREATE DATABASE aire_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE aire_db;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS rilevamenti;
DROP TABLE IF EXISTS stazioni_rilevamento;
DROP TABLE IF EXISTS inquinanti;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE inquinanti (
    id_inquinante INT PRIMARY KEY,
    nome_inquinante VARCHAR(100) NOT NULL,
    valore_limite DECIMAL(10,2),
    unita_misura VARCHAR(50)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4;

CREATE TABLE stazioni_rilevamento (
    id_stazione INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    long_x_4326 DECIMAL(18,14),
    lat_y_4326 DECIMAL(18,14)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4;

CREATE TABLE rilevamenti (
    id_rilevamento VARCHAR(20) PRIMARY KEY,
    data_rilevamento DATE NOT NULL,
    orario TIME NOT NULL,
    id_inquinante INT NOT NULL,
    valore DECIMAL(10,2),
    id_stazione INT NOT NULL,

    INDEX idx_data (data_rilevamento),
    INDEX idx_orario (orario),
    INDEX idx_inquinante (id_inquinante),
    INDEX idx_stazione (id_stazione),

    CONSTRAINT fk_rilevamenti_inquinanti
        FOREIGN KEY (id_inquinante)
        REFERENCES inquinanti(id_inquinante),

    CONSTRAINT fk_rilevamenti_stazioni
        FOREIGN KEY (id_stazione)
        REFERENCES stazioni_rilevamento(id_stazione)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4;

LOAD DATA LOCAL INFILE '/Users/rita/Downloads/AIRE/db/pv_Inquinanti.csv'
INTO TABLE inquinanti
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@id_inquinante, @nome_inquinante, @valore_limite, @unita_misura)
SET
    id_inquinante = CAST(TRIM(@id_inquinante) AS UNSIGNED),
    nome_inquinante = TRIM(@nome_inquinante),
    valore_limite = CASE
        WHEN TRIM(@valore_limite) = '\\N' THEN NULL
        WHEN TRIM(@valore_limite) = '' THEN NULL
        ELSE CAST(REPLACE(TRIM(@valore_limite), ',', '.') AS DECIMAL(10,2))
    END,
    unita_misura = TRIM(@unita_misura);

SELECT 'record importati inquinanti' AS controllo, ROW_COUNT() AS righe_caricate;
SHOW WARNINGS;

LOAD DATA LOCAL INFILE '/Users/rita/Downloads/AIRE/db/pv_stazioni_rilevamento_CLEAN.csv'
INTO TABLE stazioni_rilevamento
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@id_stazione, @nome, @long_x_4326, @lat_y_4326)
SET
    id_stazione = CAST(TRIM(@id_stazione) AS UNSIGNED),
    nome = TRIM(@nome),
    long_x_4326 = CASE
        WHEN TRIM(@long_x_4326) = '\\N' THEN NULL
        WHEN TRIM(@long_x_4326) = '' THEN NULL
        ELSE CAST(REPLACE(TRIM(@long_x_4326), ',', '.') AS DECIMAL(18,14))
    END,
    lat_y_4326 = CASE
        WHEN TRIM(@lat_y_4326) = '\\N' THEN NULL
        WHEN TRIM(@lat_y_4326) = '' THEN NULL
        ELSE CAST(REPLACE(TRIM(@lat_y_4326), ',', '.') AS DECIMAL(18,14))
    END;

SELECT 'record importati stazioni' AS controllo, ROW_COUNT() AS righe_caricate;
SHOW WARNINGS;

LOAD DATA LOCAL INFILE '/Users/rita/Downloads/AIRE/db/pv_rilevamenti_arpa_unificati.csv'
INTO TABLE rilevamenti
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@id_rilevamento, @data_rilevamento, @orario, @id_inquinante, @valore, @id_stazione)
SET
    id_rilevamento = TRIM(@id_rilevamento),
    data_rilevamento = STR_TO_DATE(TRIM(@data_rilevamento), '%Y/%m/%d'),
    orario = STR_TO_DATE(TRIM(@orario), '%H:%i'),
    id_inquinante = CAST(TRIM(@id_inquinante) AS UNSIGNED),
    valore = CASE
        WHEN TRIM(@valore) = '\\N' THEN NULL
        WHEN TRIM(@valore) = '' THEN NULL
        ELSE CAST(REPLACE(TRIM(@valore), ',', '.') AS DECIMAL(10,2))
    END,
    id_stazione = CAST(TRIM(@id_stazione) AS UNSIGNED);

SELECT 'record importati rilevamenti' AS controllo, ROW_COUNT() AS righe_caricate;
SHOW WARNINGS;

SELECT 'inquinanti' AS tabella, COUNT(*) AS records
FROM inquinanti
UNION ALL
SELECT 'stazioni_rilevamento', COUNT(*)
FROM stazioni_rilevamento
UNION ALL
SELECT 'rilevamenti', COUNT(*)
FROM rilevamenti;

SELECT
    r.id_rilevamento,
    r.data_rilevamento,
    r.orario,
    i.nome_inquinante,
    r.valore,
    i.unita_misura,
    s.nome AS stazione
FROM rilevamenti r
JOIN inquinanti i
    ON r.id_inquinante = i.id_inquinante
JOIN stazioni_rilevamento s
    ON r.id_stazione = s.id_stazione
LIMIT 50;