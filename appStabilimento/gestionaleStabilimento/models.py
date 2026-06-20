# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# Le FK verso modelli con chiave primaria composta vanno messi campi semplici dentro Django a quanto pare

# Dove c'era una ForeignKey verso un modello con PK composta 
# (es. Abbonamento → Ombrellone, DettaglioOrdine → Catalogo), ora è un campo semplice. 
# Il vincolo di integrità referenziale resta nel database solo che Django non genererà automaticamente 
# il join. Per quelle relazioni dovremo filtrare a mano.

class Abbonamento(models.Model):
    pk = models.CompositePrimaryKey('codfila', 'numombrellone', 'anno')
    codfila = models.IntegerField(db_column='CodFila')
    numombrellone = models.IntegerField(db_column='NumOmbrellone')
    anno = models.TextField(db_column='Anno')  # Field name made lowercase. This field type is a guess.
    prezzo = models.DecimalField(db_column='Prezzo', max_digits=8, decimal_places=2)  # Field name made lowercase.
    sconto = models.FloatField(db_column='Sconto')  # Field name made lowercase.
    pagamento = models.CharField(db_column='Pagamento', max_length=1)  # Field name made lowercase.
    idcliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='IdCliente')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ABBONAMENTO'


class Catalogo(models.Model):
    pk = models.CompositePrimaryKey('partitaiva', 'codprodotto')
    codprodotto = models.ForeignKey('Prodotto', models.DO_NOTHING, db_column='CodProdotto')  # Field name made lowercase.
    partitaiva = models.ForeignKey('Fornitore', models.DO_NOTHING, db_column='PartitaIVA')  # Field name made lowercase.
    prezzounitario = models.DecimalField(db_column='PrezzoUnitario', max_digits=8, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'CATALOGO'


class Categoria(models.Model):
    codcategoria = models.AutoField(db_column='CodCategoria', primary_key=True)  # Field name made lowercase.
    nomecategoria = models.CharField(db_column='NomeCategoria', max_length=40)  # Field name made lowercase.
    descrizione = models.CharField(db_column='Descrizione', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'CATEGORIA'


class Cliente(models.Model):
    idcliente = models.AutoField(db_column='IdCliente', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=30)  # Field name made lowercase.
    cognome = models.CharField(db_column='Cognome', max_length=30)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    recapitotelefonico = models.CharField(db_column='RecapitoTelefonico', max_length=15)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'CLIENTE'


class DettaglioOrdine(models.Model):
    pk = models.CompositePrimaryKey('codordine', 'partitaiva', 'codprodotto')
    codordine = models.ForeignKey('Ordine', models.DO_NOTHING, db_column='CodOrdine')  # Field name made lowercase.
    partitaiva = models.CharField(db_column='PartitaIVA', max_length=11)
    codprodotto = models.IntegerField(db_column='CodProdotto')
    quantità = models.IntegerField(db_column='Quantità')  # Field name made lowercase.
    prezzoalmomento = models.DecimalField(db_column='PrezzoAlMomento', max_digits=8, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DETTAGLIO_ORDINE'


class Dipendente(models.Model):
    iddipendente = models.AutoField(db_column='IdDipendente', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=30)  # Field name made lowercase.
    cognome = models.CharField(db_column='Cognome', max_length=30)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    recapitotelefonico = models.CharField(db_column='RecapitoTelefonico', max_length=15)  # Field name made lowercase.
    codicefiscale = models.CharField(db_column='CodiceFiscale', max_length=16)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DIPENDENTE'


class Fila(models.Model):
    codfila = models.IntegerField(db_column='CodFila', primary_key=True)  # Field name made lowercase.
    tariffagiornaliera = models.DecimalField(db_column='TariffaGiornaliera', max_digits=8, decimal_places=2)  # Field name made lowercase.
    tariffastagionale = models.DecimalField(db_column='TariffaStagionale', max_digits=8, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'FILA'


class Fornitore(models.Model):
    partitaiva = models.CharField(db_column='PartitaIVA', primary_key=True, max_length=11)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=50)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    indirizzo = models.CharField(db_column='Indirizzo', max_length=60)  # Field name made lowercase.
    recapitotelefonico = models.CharField(db_column='RecapitoTelefonico', max_length=15)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'FORNITORE'


class Mansione(models.Model):
    codmansione = models.AutoField(db_column='CodMansione', primary_key=True)  # Field name made lowercase.
    nomemansione = models.CharField(db_column='NomeMansione', unique=True, max_length=40)  # Field name made lowercase.
    descrizione = models.CharField(db_column='Descrizione', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'MANSIONE'


class NoleggioLettino(models.Model):
    codnoleggio = models.AutoField(db_column='CodNoleggio', primary_key=True)  # Field name made lowercase.
    data = models.DateField(db_column='Data')  # Field name made lowercase.
    quantità = models.IntegerField(db_column='Quantità')  # Field name made lowercase.
    prezzototale = models.DecimalField(db_column='PrezzoTotale', max_digits=8, decimal_places=2)  # Field name made lowercase.
    pagamento = models.CharField(db_column='Pagamento', max_length=1)  # Field name made lowercase.
    idcliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='IdCliente')  # Field name made lowercase.
    tiponoleggio = models.ForeignKey('TariffeNoleggio', models.DO_NOTHING, db_column='TipoNoleggio')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'NOLEGGIO_LETTINO'


class Ombrellone(models.Model):
    pk = models.CompositePrimaryKey('codfila', 'numombrellone')
    codfila = models.ForeignKey(Fila, models.DO_NOTHING, db_column='CodFila')  # Field name made lowercase.
    numombrellone = models.IntegerField(db_column='NumOmbrellone')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'OMBRELLONE'


class Ordine(models.Model):
    codordine = models.AutoField(db_column='CodOrdine', primary_key=True)  # Field name made lowercase.
    dataordine = models.DateField(db_column='DataOrdine')  # Field name made lowercase.
    consegnaprevista = models.DateField(db_column='ConsegnaPrevista')  # Field name made lowercase.
    dataconsegna = models.DateField(db_column='DataConsegna', blank=True, null=True)  # Field name made lowercase.
    idproprietario = models.ForeignKey('Proprietario', models.DO_NOTHING, db_column='IdProprietario')  # Field name made lowercase.
    partitaiva = models.ForeignKey(Fornitore, models.DO_NOTHING, db_column='PartitaIVA')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ORDINE'


class Prenotazione(models.Model):
    codprenotazione = models.AutoField(db_column='CodPrenotazione', primary_key=True)  # Field name made lowercase.
    datainizio = models.DateField(db_column='DataInizio')  # Field name made lowercase.
    datafine = models.DateField(db_column='DataFine')  # Field name made lowercase.
    prezzo = models.DecimalField(db_column='Prezzo', max_digits=8, decimal_places=2)  # Field name made lowercase.
    sconto = models.FloatField(db_column='Sconto')  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pagamento = models.CharField(db_column='Pagamento', max_length=1)  # Field name made lowercase.
    idcliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='IdCliente')  # Field name made lowercase.
    codfila = models.IntegerField(db_column='CodFila')  # Field name made lowercase.
    numombrellone = models.IntegerField(db_column='NumOmbrellone')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'PRENOTAZIONE'


class Prodotto(models.Model):
    codprodotto = models.AutoField(db_column='CodProdotto', primary_key=True)  # Field name made lowercase.
    nomeprodotto = models.CharField(db_column='NomeProdotto', max_length=40)  # Field name made lowercase.
    quantitàmagazzino = models.IntegerField(db_column='QuantitàMagazzino')  # Field name made lowercase.
    quantitàminima = models.IntegerField(db_column='QuantitàMinima')  # Field name made lowercase.
    codcategoria = models.IntegerField(db_column='CodCategoria')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'PRODOTTO'


class Proprietario(models.Model):
    idproprietario = models.AutoField(db_column='IdProprietario', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=30)  # Field name made lowercase.
    cognome = models.CharField(db_column='Cognome', max_length=30)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    recapitotelefonico = models.CharField(db_column='RecapitoTelefonico', max_length=15)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'PROPRIETARIO'


class TariffeNoleggio(models.Model):
    tiponoleggio = models.CharField(db_column='TipoNoleggio', primary_key=True, max_length=15)  # Field name made lowercase.
    prezzo = models.DecimalField(db_column='Prezzo', max_digits=8, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'TARIFFE_NOLEGGIO'


class Turno(models.Model):
    pk = models.CompositePrimaryKey('iddipendente', 'data', 'orainizio')
    iddipendente = models.IntegerField(db_column='IdDipendente')  # Field name made lowercase.
    data = models.DateField(db_column='Data')  # Field name made lowercase.
    orainizio = models.TimeField(db_column='OraInizio')  # Field name made lowercase.
    orafine = models.TimeField(db_column='OraFine')  # Field name made lowercase.
    codmansione = models.IntegerField(db_column='CodMansione')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'TURNO'
