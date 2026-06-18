-- ============================================================
-- SCHEMA DATABASE - Gestionale Bagno Spiaggia (documentazione)
-- ============================================================
-- NOTA: con Django questo script NON va eseguito a mano.
-- Le tabelle vengono create automaticamente dalle migrations
-- (python manage.py migrate), generate a partire da bagno/models.py
--
-- Questo file resta utile come documentazione dello schema logico
-- da allegare alla relazione, e per creare il database vuoto.
-- ============================================================

CREATE DATABASE IF NOT EXISTS bagno_db CHARACTER SET utf8mb4;
USE bagno_db;

-- ------------------------------------------------------------
-- Le tabelle sottostanti vengono generate da Django (vedi models.py)
-- Strutture equivalenti per riferimento/relazione:
-- ------------------------------------------------------------

-- Tabella: Cliente
-- inserisci codice preso dallo schema logico (CREATE TABLE Cliente ...)


-- Tabella: Ombrellone
-- inserisci codice preso dallo schema logico (CREATE TABLE Ombrellone ...)


-- Tabella: Prenotazione
-- inserisci codice preso dallo schema logico (CREATE TABLE Prenotazione ...)


-- ------------------------------------------------------------
-- Aggiungi qui le altre tabelle del tuo schema logico
-- (una sezione per ogni entità, da riportare anche in models.py)
-- ------------------------------------------------------------
