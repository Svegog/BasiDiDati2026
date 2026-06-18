#!/usr/bin/env python
"""Utility a riga di comando di Django per attivit&agrave; amministrative."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestionale_bagno.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossibile importare Django. Sei sicuro che sia installato e "
            "disponibile nella variabile d'ambiente PYTHONPATH? Hai dimenticato "
            "di attivare il virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
