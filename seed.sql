-- ============================================================
-- Dati di esempio - Gestionale Stabilimento Balneare
-- Coerente con GestionaleStabilimento.ddl (MySQL)
-- Ordine di inserimento conforme ai vincoli di chiave esterna.
-- ============================================================
-- Note:
--  * Id cliente/dipendente/proprietario inseriti espliciti (1..N)
--    per rendere leggibili i riferimenti; le colonne sono comunque
--    auto_increment.
--  * Pagamento e' char(1): 'S' = saldato, 'N' = non saldato.
--  * Ogni ORDINE ha un unico FORNITORE: i DETTAGLIO_ORDINE usano
--    la stessa PartitaIVA dell'ordine (vincolo inespresso).
-- ============================================================

USE Gestionale;

-- ------------------------------------------------------------
-- FILA (file piu' vicine al mare = tariffe piu' alte)
-- TariffaStagionale = prezzo abbonamento annuale per la fila
-- ------------------------------------------------------------
INSERT INTO FILA (CodFila, TariffaGiornaliera, TariffaStagionale) VALUES
  (1, 25.00, 1300.00),
  (2, 22.00, 1150.00),
  (3, 20.00, 1000.00),
  (4, 18.00,  900.00),
  (5, 15.00,  750.00);

-- ------------------------------------------------------------
-- OMBRELLONE (6 ombrelloni per ciascuna delle 5 file = 30)
-- ------------------------------------------------------------
INSERT INTO OMBRELLONE (CodFila, NumOmbrellone) VALUES
  (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),
  (2,1),(2,2),(2,3),(2,4),(2,5),(2,6),
  (3,1),(3,2),(3,3),(3,4),(3,5),(3,6),
  (4,1),(4,2),(4,3),(4,4),(4,5),(4,6),
  (5,1),(5,2),(5,3),(5,4),(5,5),(5,6);

-- ------------------------------------------------------------
-- CLIENTE
-- ------------------------------------------------------------
INSERT INTO CLIENTE (IdCliente, Nome, Cognome, Email, RecapitoTelefonico) VALUES
  (1,'Marco','Bianchi','marco.bianchi@email.it','3331112233'),
  (2,'Laura','Rossi','laura.rossi@email.it','3332223344'),
  (3,'Giuseppe','Verdi','giuseppe.verdi@email.it','3343334455'),
  (4,'Anna','Esposito','anna.esposito@email.it','3354445566'),
  (5,'Francesco','Romano','francesco.romano@email.it','3365556677'),
  (6,'Chiara','Russo','chiara.russo@email.it','3376667788'),
  (7,'Luca','Ferrari','luca.ferrari@email.it','3387778899'),
  (8,'Sara','Conti','sara.conti@email.it','3398889900'),
  (9,'Matteo','Greco','matteo.greco@email.it','3401234567'),
  (10,'Giulia','Marino','giulia.marino@email.it','3412345678');

-- ------------------------------------------------------------
-- DIPENDENTE
-- ------------------------------------------------------------
INSERT INTO DIPENDENTE (IdDipendente, Nome, Cognome, Email, RecapitoTelefonico, CodiceFiscale) VALUES
  (1,'Paolo','Gallo','paolo.gallo@stab.it','3201112222','GLLPLA85M01H294K'),
  (2,'Elena','Costa','elena.costa@stab.it','3202223333','CSTLNE90A41F205Z'),
  (3,'Davide','Fontana','davide.fontana@stab.it','3203334444','FNTDVD88T10L378Q'),
  (4,'Martina','Serra','martina.serra@stab.it','3204445555','SRRMTN92E55G224W'),
  (5,'Simone','Rizzo','simone.rizzo@stab.it','3205556666','RZZSMN87B12C351Y'),
  (6,'Valentina','Lombardi','valentina.lombardi@stab.it','3206667777','LMBVNT95D60A662X');

-- ------------------------------------------------------------
-- PROPRIETARIO (Password = hash bcrypt di esempio, 60 caratteri)
-- ------------------------------------------------------------
INSERT INTO PROPRIETARIO (IdProprietario, Nome, Cognome, Email, RecapitoTelefonico, Password) VALUES
  (1,'Roberto','Mari','roberto.mari@stabilimento.it','3470001111','$2b$12$e0NRsT4xJ8wQ1vYpZ2bKuOeX7lM3nP9rS5tU6vW8yZ0aB1cD2eF3'),
  (2,'Federica','Mari','federica.mari@stabilimento.it','3470002222','$2b$12$e0NRsT4xJ8wQ1vYpZ2bKuOeX7lM3nP9rS5tU6vW8yZ0aB1cD2eF3'),
  (3,'Antonio','Sole','antonio.sole@stabilimento.it','3470003333','$2b$12$e0NRsT4xJ8wQ1vYpZ2bKuOeX7lM3nP9rS5tU6vW8yZ0aB1cD2eF3');

-- ------------------------------------------------------------
-- MANSIONE
-- ------------------------------------------------------------
INSERT INTO MANSIONE (CodMansione, NomeMansione, Descrizione) VALUES
  (1,'Bagnino','Sorveglianza spiaggia e operazioni di salvataggio'),
  (2,'Cassiere','Gestione cassa, prenotazioni e pagamenti'),
  (3,'Addetto pulizie','Pulizia spiaggia, servizi e aree comuni'),
  (4,'Manutentore','Manutenzione ombrelloni, lettini e strutture'),
  (5,'Barista','Servizio bar e punto ristoro'),
  (6,'Receptionist','Accoglienza clienti e informazioni');

-- ------------------------------------------------------------
-- TURNO (PK = IdDipendente, Data, OraInizio -> ammessi turni spezzati)
-- ------------------------------------------------------------
INSERT INTO TURNO (IdDipendente, Data, OraInizio, OraFine, CodMansione) VALUES
  (1,'2026-06-19','08:00','14:00',1),
  (1,'2026-06-19','14:00','20:00',1),
  (2,'2026-06-19','09:00','17:00',2),
  (3,'2026-06-19','07:00','13:00',3),
  (4,'2026-06-19','10:00','18:00',5),
  (5,'2026-06-20','08:00','14:00',1),
  (6,'2026-06-20','09:00','13:00',6),
  (2,'2026-06-20','14:00','20:00',2);

-- ------------------------------------------------------------
-- CATEGORIA
-- ------------------------------------------------------------
INSERT INTO CATEGORIA (CodCategoria, NomeCategoria, Descrizione) VALUES
  (1,'Bevande','Bibite, acqua e bevande per il bar'),
  (2,'Snack','Snack dolci e salati'),
  (3,'Pulizia','Materiale per pulizia e igiene'),
  (4,'Attrezzatura','Attrezzatura da spiaggia'),
  (5,'Cancelleria','Materiale di cancelleria e ufficio');

-- ------------------------------------------------------------
-- PRODOTTO (alcuni sotto la soglia minima -> utili per la query O5)
-- ------------------------------------------------------------
INSERT INTO PRODOTTO (CodProdotto, NomeProdotto, `QuantitàMagazzino`, `QuantitàMinima`, CodCategoria) VALUES
  (1,'Acqua naturale 1.5L',200,100,1),
  (2,'Coca Cola lattina 33cl',40,80,1),       -- sotto soglia
  (3,'Aranciata bottiglia 50cl',150,60,1),
  (4,'Patatine classiche',30,50,2),           -- sotto soglia
  (5,'Snack salati misti',90,40,2),
  (6,'Detergente multiuso 5L',12,20,3),       -- sotto soglia
  (7,'Sacchi spazzatura 100L',100,30,3),
  (8,'Sdraio di ricambio',8,15,4),            -- sotto soglia
  (9,'Teli mare con logo',60,25,4),
  (10,'Blocchetti ricevute',70,20,5);

-- ------------------------------------------------------------
-- FORNITORE
-- ------------------------------------------------------------
INSERT INTO FORNITORE (PartitaIVA, Nome, Email, Indirizzo, RecapitoTelefonico) VALUES
  ('01234567890','Bibite Adriatiche Srl','ordini@bibiteadriatiche.it','Via del Porto 12, Cesenatico','0541111222'),
  ('09876543210','SnackPoint Spa','info@snackpoint.it','Via Emilia 200, Rimini','0541333444'),
  ('11223344556','PuliMare Forniture','vendite@pulimare.it','Via Mazzini 5, Cesena','0547555666'),
  ('99887766554','Spiaggia e Co','commerciale@spiaggiaeco.it','Viale Roma 88, Rimini','0541777888');

-- ------------------------------------------------------------
-- CATALOGO (il prodotto 2 e' venduto da due fornitori diversi)
-- ------------------------------------------------------------
INSERT INTO CATALOGO (PartitaIVA, CodProdotto, PrezzoUnitario) VALUES
  ('01234567890',1,0.40),
  ('01234567890',2,0.55),
  ('01234567890',3,0.50),
  ('09876543210',2,0.60),
  ('09876543210',4,0.80),
  ('09876543210',5,1.20),
  ('11223344556',6,14.50),
  ('11223344556',7,3.20),
  ('99887766554',8,22.00),
  ('99887766554',9,8.50),
  ('99887766554',10,2.10);

-- ------------------------------------------------------------
-- ORDINE (ogni ordine ha UN solo fornitore)
-- ------------------------------------------------------------
INSERT INTO ORDINE (CodOrdine, DataOrdine, ConsegnaPrevista, DataConsegna, IdProprietario, PartitaIVA) VALUES
  (1,'2026-06-01','2026-06-05','2026-06-05',1,'01234567890'),  -- consegnato
  (2,'2026-06-10','2026-06-14',NULL,1,'09876543210'),          -- in attesa
  (3,'2026-06-12','2026-06-16','2026-06-16',2,'11223344556'),  -- consegnato
  (4,'2026-06-15','2026-06-19',NULL,3,'99887766554');          -- in attesa

-- ------------------------------------------------------------
-- DETTAGLIO_ORDINE (PartitaIVA = quella dell'ordine; coppia presente in CATALOGO)
-- ------------------------------------------------------------
INSERT INTO DETTAGLIO_ORDINE (CodOrdine, PartitaIVA, CodProdotto, `Quantità`, PrezzoAlMomento) VALUES
  (1,'01234567890',1,100,0.40),
  (1,'01234567890',2,80,0.55),
  (1,'01234567890',3,60,0.50),
  (2,'09876543210',4,60,0.80),
  (2,'09876543210',5,40,1.20),
  (3,'11223344556',6,20,14.50),
  (3,'11223344556',7,50,3.20),
  (4,'99887766554',8,15,22.00),
  (4,'99887766554',9,30,8.50),
  (4,'99887766554',10,40,2.10);

-- ------------------------------------------------------------
-- TARIFFE_NOLEGGIO
-- ------------------------------------------------------------
INSERT INTO TARIFFE_NOLEGGIO (TipoNoleggio, Prezzo) VALUES
  ('Mattina',8.00),
  ('Pomeriggio',8.00),
  ('Giornata',14.00);

-- ------------------------------------------------------------
-- NOLEGGIO_LETTINO (PrezzoTotale = Prezzo tariffa * Quantita')
-- ------------------------------------------------------------
INSERT INTO NOLEGGIO_LETTINO (Data, `Quantità`, PrezzoTotale, Pagamento, IdCliente, TipoNoleggio) VALUES
  ('2026-06-15',2,28.00,'S',1,'Giornata'),
  ('2026-06-16',1, 8.00,'S',2,'Mattina'),
  ('2026-06-16',2,16.00,'N',3,'Pomeriggio'),
  ('2026-06-17',4,56.00,'S',4,'Giornata'),
  ('2026-06-18',2,28.00,'S',5,'Giornata');

-- ------------------------------------------------------------
-- PRENOTAZIONE (periodi non sovrapposti sullo stesso ombrellone)
-- ------------------------------------------------------------
INSERT INTO PRENOTAZIONE (DataInizio, DataFine, Prezzo, Sconto, Note, Pagamento, IdCliente, CodFila, NumOmbrellone) VALUES
  ('2026-06-20','2026-06-27',175.00,0,NULL,'S',1,1,1),
  ('2026-06-20','2026-06-25',125.00,0,NULL,'S',2,1,2),
  ('2026-07-01','2026-07-10',198.00,0.1,NULL,'N',3,2,1),
  ('2026-07-01','2026-07-05',125.00,0,'Stesso ombrellone della prima prenotazione ma periodo diverso','S',4,1,1),
  ('2026-06-22','2026-06-29',160.00,0,NULL,'S',5,3,3),
  ('2026-08-01','2026-08-15',330.00,0.15,'Aggiunto un lettino extra','N',6,2,4);

-- ------------------------------------------------------------
-- ABBONAMENTO (PK = CodFila, NumOmbrellone, Anno)
-- ------------------------------------------------------------
INSERT INTO ABBONAMENTO (CodFila, NumOmbrellone, Anno, Prezzo, Sconto, Pagamento, IdCliente) VALUES
  (1,5,2026,1300.00,0,'S',7),
  (1,6,2026,1300.00,0.1,'S',8),
  (2,6,2026,1150.00,0,'N',9);
