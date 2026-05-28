## **PROPOSTA DI PROGETTO**
### **LEGENDA**
Nella prima proposta qua sotto:
- I nomi in **grassetto** indicano i possibili nomi da utilizzare per le entità
- I nomi in *corsivo* indicano i possibili nomi da utilizzare per gli attributi

Il contenuto del seguente README è una breve descrizione del dominio applicativo, che andrà poi sviluppato in:
- Schema E/R
- Schema logico
- DB fisico (da decidere le modalità)
- Applicazione (semplice, minimale ma necessaria)

### **PROPOSTA: DA PERFEZIONARE**
L'obiettivo del progetto è realizzare un gestionale che venga utilizzato dai vari proprietari dello stabilimento, per il monitoraggio delle funzioni essenziali di un bagno.
L'idea è realizzare uno strumento ausiliario per le funzioni essenziali di uno stabilimento balneare, che i proprietari possano consultare.

Il progetto non si occupa di interazioni utente -> stabilimento in quanto le informazioni che vengono trattate sono rivolte ai proprietari.

Il **proprietario** o i proprietari (che in questo testo prenderanno il nome di proprietario al singolare per semplicità) possono effettuare l'accesso al gestionale tramite *credenziali* (nome, cognome, email, password).

Il proprietario può inserire **clienti** (nome, cognome, numeroTelefono, email) nel gestionale, in modo che possa assegnarli a degli **ombrelloni**, a dei **lettini** oppure proporli un **abbonamento** calcolato su base di durata e posizione (che per semplicità mostrerà solo il prezzo, non gestendo il pagamento).

Degli ombrelloni è necessario memorizzarsi posizione, numeroLettini, numeroSedie, mentre il prezzo verrà calcolato in base alla richiesta del cliente, in quanto *informazioni* (come dataInizio e dataFine) che legano ombrelloni e clienti sono conservate nelle **prenotazioni**.

Il proprietario può gestire i turni dei **dipendenti**, in modo da visualizzare in determinate giornate la forza lavoro disponibile, modificando i **turni** per riempire la giornata.

Sarà inoltre possibile verificare la disponibilità in **magazzino**, effettuando se necessario ordini per singoli o gruppi di prodotti (per semplicità il pagamento degli ordini sarà effettuato alla consegna, e una volta aggiunto un ordine il contenuto sarà aggiunto al magazzino).

### **OPERAZIONI: DA PERFEZIONARE**
Le `funzionalità` offerte dal gestionale per il proprietario sono:
- Inserimento di un cliente (in caso di clienti abituali)
- Inserimento di prenotazioni o abbonamenti relativi a lettini o ombrelloni
- Registrazione di nuovi dipendenti
- Registrazione turni di lavoro di dipendenti
- Inserimento di un ordine relativo alle forniture
- Aggiunta, rimozione o modifica di prodotti, fornitori, clienti o dipendenti
- Inserimento o modifica di prezzi (riferiti a lettini, sedie e prodotti in magazzino)

Inoltre è possibile `consultare`:
- Lettini o ombrelloni disponibili
- Dipendenti al lavoro per un determinato giorno
- Orari di uno specifico dipendente
- Mancanze in magazzino totali o per uno specifico prodotto

sconto = ScaleFactor × (1 - e^(-k × durata)) 