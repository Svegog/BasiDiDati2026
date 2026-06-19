-- *********************************************
-- * SQL MySQL generation                      
-- *--------------------------------------------
-- * DB-MAIN version: 11.0.2              
-- * Generator date: Sep 14 2021              
-- * Generation date: Fri Jun 19 13:07:35 2026 
-- * LUN file: Z:\home\marco\BasiDati\ProgettoBasi\ProgettoBasi.lun 
-- * Schema: SchemaLogico/1 
-- ********************************************* 


-- Database Section
-- ________________ 

DROP DATABASE IF EXISTS Gestionale;

CREATE DATABASE IF NOT EXISTS Gestionale;

use Gestionale;


-- Tables Section
-- _____________ 

create table ABBONAMENTO (
     CodFila int not null,
     NumOmbrellone int not null,
     Anno int not null,
     Prezzo decimal(8,2) not null,
     Sconto float(1) not null,
     Pagamento char not null,
     IdCliente int not null,
     constraint IDABBONAMENTO primary key (CodFila, NumOmbrellone, Anno));

create table CATALOGO (
     CodProdotto int not null,
     PartitaIVA char(11) not null,
     PrezzoUnitario decimal(8,2) not null,
     constraint IDFORNITURA primary key (PartitaIVA, CodProdotto));

create table CATEGORIA (
     CodCategoria int not null auto_increment,
     NomeCategoria varchar(40) not null,
     Descrizione varchar(255),
     constraint IDCATEGORIA primary key (CodCategoria));

create table CLIENTE (
     IdCliente int not null auto_increment,
     Nome varchar(30) not null,
     Cognome varchar(30) not null,
     Email varchar(50) not null,
     RecapitoTelefonico varchar(15) not null,
     constraint IDCLIENTE primary key (IdCliente));

create table DETTAGLIO_ORDINE (
     CodOrdine int not null,
     PartitaIVA char(11) not null,
     CodProdotto int not null,
     Quantità int not null,
     PrezzoAlMomento decimal(8,2) not null,
     constraint IDDettaglio_Ordine primary key (CodOrdine, PartitaIVA, CodProdotto));

create table DIPENDENTE (
     IdDipendente int not null auto_increment,
     Nome varchar(30) not null,
     Cognome varchar(30) not null,
     Email varchar(50) not null,
     RecapitoTelefonico varchar(15) not null,
     CodiceFiscale char(16) not null,
     constraint IDDIPENDENTE primary key (IdDipendente));

create table FILA (
     CodFila int not null,
     TariffaGiornaliera decimal(8,2) not null,
     TariffaStagionale decimal(8,2) not null,
     constraint IDFILA primary key (CodFila));

create table FORNITORE (
     PartitaIVA char(11) not null,
     Nome varchar(50) not null,
     Email varchar(50) not null,
     Indirizzo varchar(60) not null,
     RecapitoTelefonico varchar(15) not null,
     constraint IDFornitore_ID primary key (PartitaIVA));

create table MANSIONE (
     CodMansione int not null auto_increment,
     NomeMansione varchar(40) not null,
     Descrizione varchar(255),
     constraint IDMANSIONE_ID primary key (CodMansione),
     constraint IDMANSIONE_1 unique (NomeMansione));

create table NOLEGGIO_LETTINO (
     CodNoleggio int not null auto_increment,
     Data date not null,
     Quantità int not null,
     PrezzoTotale decimal(8,2) not null,
     Pagamento char not null,
     IdCliente int not null,
     TipoNoleggio varchar(15) not null,
     constraint IDNOLEGGIO_LETTINO primary key (CodNoleggio));

create table OMBRELLONE (
     CodFila int not null,
     NumOmbrellone int not null,
     constraint IDOMBRELLONE primary key (CodFila, NumOmbrellone));

create table ORDINE (
     CodOrdine int not null auto_increment,
     DataOrdine date not null,
     ConsegnaPrevista date not null,
     DataConsegna date,
     IdProprietario int not null,
     PartitaIVA char(11) not null,
     constraint IDOrdine primary key (CodOrdine));

create table PRENOTAZIONE (
     CodPrenotazione int not null auto_increment,
     DataInizio date not null,
     DataFine date not null,
     Prezzo decimal(8,2) not null,
     Sconto float(1) not null,
     Note varchar(255),
     Pagamento char not null,
     IdCliente int not null,
     CodFila int not null,
     NumOmbrellone int not null,
     constraint IDPRENOTAZIONE primary key (CodPrenotazione));

create table PRODOTTO (
     CodProdotto int not null auto_increment,
     NomeProdotto char(40) not null,
     QuantitàMagazzino int not null,
     QuantitàMinima int not null,
     CodCategoria int not null,
     constraint IDProdotto_ID primary key (CodProdotto));

create table PROPRIETARIO (
     IdProprietario int not null auto_increment,
     Nome varchar(30) not null,
     Cognome varchar(30) not null,
     Email varchar(50) not null,
     RecapitoTelefonico varchar(15) not null,
     Password varchar(255) not null,
     constraint IDPROPRIETARIO primary key (IdProprietario));

create table TARIFFE_NOLEGGIO (
     TipoNoleggio varchar(15) not null,
     Prezzo decimal(8,2) not null,
     constraint IDTARIFFE_NOLEGGIO primary key (TipoNoleggio));

create table TURNO (
     IdDipendente int not null,
     Data date not null,
     OraInizio char(5) not null,
     OraFine char(5) not null,
     CodMansione int not null,
     constraint IDTURNO primary key (IdDipendente, Data, OraInizio));


-- Constraints Section
-- ___________________ 

alter table ABBONAMENTO add constraint FKSottoscrizione
     foreign key (IdCliente)
     references CLIENTE (IdCliente);

alter table ABBONAMENTO add constraint FKRiservazione
     foreign key (CodFila, NumOmbrellone)
     references OMBRELLONE (CodFila, NumOmbrellone);

alter table CATALOGO add constraint FKOfferta
     foreign key (PartitaIVA)
     references FORNITORE (PartitaIVA);

alter table CATALOGO add constraint FKRelativa
     foreign key (CodProdotto)
     references PRODOTTO (CodProdotto);

alter table DETTAGLIO_ORDINE add constraint FKDet_ORD
     foreign key (CodOrdine)
     references ORDINE (CodOrdine);

alter table DETTAGLIO_ORDINE add constraint FKDet_CAT
     foreign key (PartitaIVA, CodProdotto)
     references CATALOGO (PartitaIVA, CodProdotto);

-- Not implemented
-- alter table FORNITORE add constraint IDFornitore_CHK
--     check(exists(select * from CATALOGO
--                  where CATALOGO.PartitaIVA = PartitaIVA)); 

-- Not implemented
-- alter table MANSIONE add constraint IDMANSIONE_CHK
--     check(exists(select * from TURNO
--                  where TURNO.CodMansione = CodMansione)); 

alter table NOLEGGIO_LETTINO add constraint FKAcquisto
     foreign key (IdCliente)
     references CLIENTE (IdCliente);

alter table NOLEGGIO_LETTINO add constraint FKTipologia
     foreign key (TipoNoleggio)
     references TARIFFE_NOLEGGIO (TipoNoleggio);

alter table OMBRELLONE add constraint FKLocazione_ombrellone
     foreign key (CodFila)
     references FILA (CodFila);

alter table ORDINE add constraint FKInserimento
     foreign key (IdProprietario)
     references PROPRIETARIO (IdProprietario);

alter table ORDINE add constraint FKEmissione
     foreign key (PartitaIVA)
     references FORNITORE (PartitaIVA);

alter table PRENOTAZIONE add constraint FKRichiesta
     foreign key (IdCliente)
     references CLIENTE (IdCliente);

alter table PRENOTAZIONE add constraint FKRISERVAZIONE
     foreign key (CodFila, NumOmbrellone)
     references OMBRELLONE (CodFila, NumOmbrellone);

-- Not implemented
-- alter table PRODOTTO add constraint IDProdotto_CHK
--     check(exists(select * from CATALOGO
--                  where CATALOGO.CodProdotto = CodProdotto)); 

alter table PRODOTTO add constraint FKAppartenenza
     foreign key (CodCategoria)
     references CATEGORIA (CodCategoria);

alter table TURNO add constraint FKAssegnazione
     foreign key (IdDipendente)
     references DIPENDENTE (IdDipendente);

alter table TURNO add constraint FKSvolgimento
     foreign key (CodMansione)
     references MANSIONE (CodMansione);


-- Index Section
-- _____________ 

