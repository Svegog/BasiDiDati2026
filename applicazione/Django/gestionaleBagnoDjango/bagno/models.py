"""
============================================================
MODELLI DJANGO - Gestionale Bagno Spiaggia
============================================================
Ogni classe corrisponde a una tabella del tuo schema logico.
Sostituisci/aggiungi campi secondo le CREATE TABLE della tua
relazione (vedi schema.sql incluso nel progetto).

IMPORTANTE: il nome in `db_table` deve corrispondere esattamente
al nome di tabella usato nel tuo schema logico/DDL, così le query
in SQL puro (views.py) e il pannello admin restano coerenti.
============================================================
"""
from django.db import models


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    # ------------------------------------------------------------
    # Aggiungi qui altri campi secondo il tuo schema logico, es:
    # email = models.CharField(max_length=100, blank=True, null=True)
    # ------------------------------------------------------------

    class Meta:
        db_table = 'Cliente'  # nome tabella esatto dello schema logico

    def __str__(self):
        return f"{self.nome} {self.cognome}"


class Ombrellone(models.Model):
    id_ombrellone = models.AutoField(primary_key=True)
    numero = models.IntegerField()
    fila = models.CharField(max_length=10, blank=True, null=True)
    stato = models.CharField(max_length=20, blank=True, null=True)

    # ------------------------------------------------------------
    # Aggiungi qui altri campi secondo il tuo schema logico
    # ------------------------------------------------------------

    class Meta:
        db_table = 'Ombrellone'

    def __str__(self):
        return f"Ombrellone {self.numero}"


class Prenotazione(models.Model):
    id_prenotazione = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    id_ombrellone = models.ForeignKey(Ombrellone, on_delete=models.CASCADE, db_column='id_ombrellone')
    data_inizio = models.DateField()
    data_fine = models.DateField()

    # ------------------------------------------------------------
    # Aggiungi qui altri campi secondo il tuo schema logico
    # ------------------------------------------------------------

    class Meta:
        db_table = 'Prenotazione'

    def __str__(self):
        return f"Prenotazione #{self.id_prenotazione}"


# ============================================================
# AGGIUNGI QUI LE ALTRE ENTITÀ DEL TUO SCHEMA LOGICO
# (una classe per tabella, seguendo lo stesso schema sopra)
# ============================================================
