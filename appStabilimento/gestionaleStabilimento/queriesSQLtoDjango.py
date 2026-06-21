"""
Modulo contenente tutte le operazioni SQL.
Ogni funzione usa connection.cursor() per eseguire query SQL pure,
con %s come placeholder (equivalente del ? generico).
"""

from django.db import connection


# =========================================================
# O.1 --- Inserimento di un cliente
# =========================================================
def inserisci_cliente(nome, cognome, email, recapito_telefonico):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO CLIENTE (Nome, Cognome, Email, RecapitoTelefonico) "
            "VALUES (%s, %s, %s, %s)",
            [nome, cognome, email, recapito_telefonico]
        )
        return cursor.lastrowid


# =========================================================
# O.2 --- Inserimento di una prenotazione
# =========================================================
def trova_cliente(nome, cognome, email):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT IdCliente FROM CLIENTE WHERE Nome = %s AND Cognome = %s AND Email = %s",
            [nome, cognome, email]
        )
        row = cursor.fetchone()
        return row[0] if row else None  # IdCliente oppure None se non trovato


def tariffa_giornaliera_fila(codfila):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT TariffaGiornaliera FROM FILA WHERE CodFila = %s",
            [codfila]
        )
        row = cursor.fetchone()
        return row[0] if row else None


def ombrellone_occupato_per_prenotazione(codfila, numombrellone, data_inizio, data_fine):
    """
    Ritorna True se l'ombrellone risulta già occupato (abbonamento annuale
    nell'anno di data_inizio, oppure prenotazione che si sovrappone).
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 1 FROM ABBONAMENTO A
            WHERE A.CodFila = %s AND A.NumOmbrellone = %s AND A.Anno = YEAR(%s)
            UNION
            SELECT 1 FROM PRENOTAZIONE P
            WHERE P.CodFila = %s AND P.NumOmbrellone = %s
            AND (%s <= P.DataFine AND %s >= P.DataInizio)
            """,
            [codfila, numombrellone, data_inizio,
             codfila, numombrellone,
             data_fine, data_inizio]
        )
        return cursor.fetchone() is not None


def inserisci_prenotazione(data_inizio, data_fine, prezzo, sconto, note,
                            idcliente, codfila, numombrellone):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO PRENOTAZIONE
                (DataInizio, DataFine, Prezzo, Sconto, Note, Pagamento, IdCliente, CodFila, NumOmbrellone)
            VALUES (%s, %s, %s, %s, %s, 'N', %s, %s, %s)
            """,
            [data_inizio, data_fine, prezzo, sconto, note, idcliente, codfila, numombrellone]
        )
        return cursor.lastrowid


# =========================================================
# O.3 --- Inserimento di un abbonamento
# =========================================================
def tariffa_stagionale_fila(codfila):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT TariffaStagionale FROM FILA WHERE CodFila = %s",
            [codfila]
        )
        row = cursor.fetchone()
        return row[0] if row else None


def ombrellone_occupato_per_abbonamento(codfila, numombrellone, anno):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 1 FROM ABBONAMENTO A
            WHERE A.CodFila = %s AND A.NumOmbrellone = %s AND A.Anno = %s
            UNION
            SELECT 1 FROM PRENOTAZIONE P
            WHERE P.CodFila = %s AND P.NumOmbrellone = %s AND YEAR(P.DataInizio) = %s
            """,
            [codfila, numombrellone, anno,
             codfila, numombrellone, anno]
        )
        return cursor.fetchone() is not None


def inserisci_abbonamento(codfila, numombrellone, anno, prezzo, sconto, idcliente):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO ABBONAMENTO (CodFila, NumOmbrellone, Anno, Prezzo, Sconto, Pagamento, IdCliente)
            VALUES (%s, %s, %s, %s, %s, 'N', %s)
            """,
            [codfila, numombrellone, anno, prezzo, sconto, idcliente]
        )
        return cursor.rowcount 


# =========================================================
# O.4 --- Inserimento del noleggio di un lettino
# =========================================================
def prezzo_tariffa_noleggio(tiponoleggio):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT Prezzo FROM TARIFFE_NOLEGGIO WHERE TipoNoleggio = %s",
            [tiponoleggio]
        )
        row = cursor.fetchone()
        return row[0] if row else None


def inserisci_noleggio_lettino(data, quantita, idcliente, tiponoleggio, prezzo):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO NOLEGGIO_LETTINO (Data, Quantità, Pagamento, IdCliente, TipoNoleggio, Prezzo)
            VALUES (%s, %s, 'N', %s, %s, %s)
            """,
            [data, quantita, idcliente, tiponoleggio, prezzo]
        )
        return cursor.lastrowid


# =========================================================
# O.5 --- Registrazione nuovi dipendenti
# =========================================================
def inserisci_dipendente(nome, cognome, email, recapito_telefonico, codice_fiscale):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO DIPENDENTE (Nome, Cognome, Email, RecapitoTelefonico, CodiceFiscale)
            VALUES (%s, %s, %s, %s, %s)
            """,
            [nome, cognome, email, recapito_telefonico, codice_fiscale]
        )
        return cursor.lastrowid


# =========================================================
# O.6 --- Aggiunta di un nuovo turno di lavoro
# =========================================================
def trova_dipendente(nome, cognome, email):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT IdDipendente FROM DIPENDENTE WHERE Nome = %s AND Cognome = %s AND Email = %s",
            [nome, cognome, email]
        )
        row = cursor.fetchone()
        return row[0] if row else None


def trova_mansione(nomemansione):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT CodMansione FROM MANSIONE WHERE NomeMansione = %s",
            [nomemansione]
        )
        row = cursor.fetchone()
        return row[0] if row else None


def turno_sovrapposto(iddipendente, data, nuova_ora_inizio, nuova_ora_fine):
    """
    Verifica se il dipendente ha già un turno che si sovrappone
    con l'intervallo [nuova_ora_inizio, nuova_ora_fine].
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 1 FROM TURNO T
            WHERE T.IdDipendente = %s AND T.Data = %s
            AND (T.OraInizio < %s AND T.OraFine > %s)
            """,
            [iddipendente, data, nuova_ora_fine, nuova_ora_inizio]
        )
        return cursor.fetchone() is not None


def inserisci_turno(iddipendente, data, orainizio, orafine, codmansione):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO TURNO (IdDipendente, Data, OraInizio, OraFine, CodMansione)
            VALUES (%s, %s, %s, %s, %s)
            """,
            [iddipendente, data, orainizio, orafine, codmansione]
        )
        return cursor.rowcount


# =========================================================
# O.7 --- Inserimento di un ordine
# =========================================================
def inserisci_ordine(consegna_prevista, idproprietario, partitaiva):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO ORDINE (DataOrdine, ConsegnaPrevista, DataConsegna, IdProprietario, PartitaIVA)
            VALUES (CURDATE(), %s, NULL, %s, %s)
            """,
            [consegna_prevista, idproprietario, partitaiva]
        )
        return cursor.lastrowid


def inserisci_dettaglio_ordine(codordine, partitaiva, codprodotto, quantita):
    """
    Da chiamare per ciascun prodotto dell'ordine, subito dopo inserisci_ordine().
    Usa LAST_INSERT_ID() per recuperare il CodOrdine appena creato nella stessa connessione.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO DETTAGLIO_ORDINE (CodOrdine, PartitaIVA, CodProdotto, Quantità, PrezzoAlMomento)
            VALUES (%s, %s, %s, %s,
                   (SELECT C.PrezzoUnitario FROM CATALOGO C WHERE C.CodProdotto = %s AND C.PartitaIVA = %s))
            """,
            [codordine, partitaiva, codprodotto, quantita, codprodotto, partitaiva]
        )
        return cursor.rowcount


# =========================================================
# O.8 --- Aggiunta di un nuovo fornitore con catalogo prodotti
# =========================================================
def inserisci_fornitore(partitaiva, nome, email, indirizzo, recapito_telefonico):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO FORNITORE (PartitaIVA, Nome, Email, Indirizzo, RecapitoTelefonico)
            VALUES (%s, %s, %s, %s, %s)
            """,
            [partitaiva, nome, email, indirizzo, recapito_telefonico]
        )
        return cursor.rowcount


def inserisci_catalogo(codprodotto, partitaiva, prezzounitario):
    """Da chiamare per ciascun prodotto associato al fornitore."""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO CATALOGO (CodProdotto, PartitaIVA, PrezzoUnitario)
            VALUES (%s, %s, %s)
            """,
            [codprodotto, partitaiva, prezzounitario]
        )
        return cursor.rowcount


# =========================================================
# O.9 --- Registrazione consegna e aggiornamento giacenze
# =========================================================
def registra_consegna_ordine(codordine):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE ORDINE SET DataConsegna = CURDATE() WHERE CodOrdine = %s",
            [codordine]
        )
        return cursor.rowcount


def aggiorna_giacenze_da_ordine(codordine):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE PRODOTTO P
            JOIN DETTAGLIO_ORDINE DO ON P.CodProdotto = DO.CodProdotto
            SET P.QuantitàMagazzino = P.QuantitàMagazzino + DO.Quantità
            WHERE DO.CodOrdine = %s
            """,
            [codordine]
        )
        return cursor.rowcount


# =========================================================
# O.10 --- Visualizzazione dipendenti in turno per data
# =========================================================
def dipendenti_in_turno(data):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT D.Nome, D.Cognome, M.NomeMansione, T.OraInizio, T.OraFine
            FROM TURNO T
            JOIN DIPENDENTE D ON T.IdDipendente = D.IdDipendente
            JOIN MANSIONE M ON T.CodMansione = M.CodMansione
            WHERE T.Data = %s
            ORDER BY OraInizio
            """,
            [data]
        )
        return cursor.fetchall()  # lista di tuple


# =========================================================
# O.11 --- Verifica disponibilità ombrelloni per intervallo
# =========================================================
def ombrelloni_disponibili(data_inizio, data_fine):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT O.CodFila, O.NumOmbrellone
            FROM OMBRELLONE O
            WHERE NOT EXISTS (
                SELECT 1 FROM ABBONAMENTO A
                WHERE A.CodFila = O.CodFila AND A.NumOmbrellone = O.NumOmbrellone
                AND A.Anno = YEAR(%s)
            )
            AND NOT EXISTS (
                SELECT 1 FROM PRENOTAZIONE P
                WHERE P.CodFila = O.CodFila AND P.NumOmbrellone = O.NumOmbrellone
                AND (P.DataInizio <= %s AND P.DataFine >= %s))
            ORDER BY O.CodFila, O.NumOmbrellone
            """,
            [data_inizio, data_fine, data_inizio]
        )
        return cursor.fetchall()


# =========================================================
# O.12 --- Controllo giacenze magazzino
# =========================================================
def prodotti_sotto_scorta():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT CodProdotto, NomeProdotto, QuantitàMagazzino, QuantitàMinima,
              (QuantitàMinima - QuantitàMagazzino) AS QuantitàMancante
            FROM PRODOTTO
            WHERE QuantitàMagazzino < QuantitàMinima
            ORDER BY QuantitàMancante DESC
            """
        )
        return cursor.fetchall()


# =========================================================
# O.13 --- Visualizzazione storico cliente
# =========================================================
def storico_cliente(idcliente):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 'Prenotazione' AS TIPO, DataInizio, DataFine, Prezzo
            FROM PRENOTAZIONE
            WHERE IdCliente = %s AND DataFine < CURDATE()

            UNION ALL

            SELECT 'Abbonamento' AS TIPO, Anno AS DataInizio, NULL AS DataFine, Prezzo
            FROM ABBONAMENTO
            WHERE IdCliente = %s

            UNION ALL

            SELECT 'Noleggio Lettini' AS TIPO, Data AS DataInizio, NULL AS DataFine, PrezzoTotale AS Prezzo
            FROM NOLEGGIO_LETTINO
            WHERE IdCliente = %s AND Data < CURDATE()
            """,
            [idcliente, idcliente, idcliente]
        )
        return cursor.fetchall()


# =========================================================
# O.14 --- Modifica tariffa lettini
# =========================================================
def modifica_tariffa_noleggio(prezzo, tiponoleggio):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE TARIFFE_NOLEGGIO SET Prezzo = %s WHERE TipoNoleggio = %s",
            [prezzo, tiponoleggio]
        )
        return cursor.rowcount


# =========================================================
# O.15 --- Modifica prezzi per fila
# =========================================================
def modifica_prezzi_fila(tariffa_giornaliera, tariffa_stagionale, codfila):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE FILA SET TariffaGiornaliera = %s, TariffaStagionale = %s WHERE CodFila = %s",
            [tariffa_giornaliera, tariffa_stagionale, codfila]
        )
        return cursor.rowcount


# =========================================================
# O.16 --- Aggiornamento prezzi catalogo di un fornitore
# =========================================================
def aggiorna_prezzo_catalogo(prezzounitario, partitaiva, codprodotto):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE CATALOGO SET PrezzoUnitario = %s WHERE PartitaIVA = %s AND CodProdotto = %s",
            [prezzounitario, partitaiva, codprodotto]
        )
        return cursor.rowcount


# =========================================================
# O.17 --- Aggiornamento giacenze dopo inventario
# =========================================================
def aggiorna_giacenza_prodotto(quantita_magazzino, codprodotto):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE PRODOTTO SET QuantitàMagazzino = %s WHERE CodProdotto = %s",
            [quantita_magazzino, codprodotto]
        )
        return cursor.rowcount


# =========================================================
# O.18 --- Inserimento conferma pagamento
# =========================================================
def conferma_pagamento_prenotazione(codprenotazione):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE PRENOTAZIONE SET Pagamento = 'S' WHERE CodPrenotazione = %s",
            [codprenotazione]
        )
        return cursor.rowcount


def conferma_pagamento_abbonamento(codfila, numombrellone, anno):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE ABBONAMENTO SET Pagamento = 'S' WHERE CodFila = %s AND NumOmbrellone = %s AND Anno = %s",
            [codfila, numombrellone, anno]
        )
        return cursor.rowcount


def conferma_pagamento_noleggio(codnoleggio):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE NOLEGGIO_LETTINO SET Pagamento = 'S' WHERE CodNoleggio = %s",
            [codnoleggio]
        )
        return cursor.rowcount
    
# =========================================================
# Nuova Op Temporanea --- Check Catalogo per fornitore
# =========================================================
def ottieni_catalogo_fornitore(partitaiva):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT C.CodProdotto, C.PrezzoUnitario FROM CATALOGO C
            WHERE C.PartitaIVA = %s
            """,
            [partitaiva]
        )
        return cursor.fetchall()