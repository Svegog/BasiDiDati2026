"""
Gestione della connessione al database MySQL.
Non serve modificare questo file.
"""
import mysql.connector
from flask import g
from config import DB_CONFIG


def get_db():
    """Restituisce una connessione MySQL attiva, riutilizzata per request."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = mysql.connector.connect(**DB_CONFIG)
    return db


def query_db(query, args=(), one=False, commit=False):
    """
    Esegue una query e restituisce i risultati come lista di dizionari.
    - one=True per ottenere una singola riga (o None)
    - commit=True per INSERT/UPDATE/DELETE
    """
    db = get_db()
    cur = db.cursor(dictionary=True)  # righe accessibili come dizionari (es. riga['nome'])
    cur.execute(query, args)

    if commit:
        db.commit()
        cur.close()
        return None

    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def close_db(exception=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
