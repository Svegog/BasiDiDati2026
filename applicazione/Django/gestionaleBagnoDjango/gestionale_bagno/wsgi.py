"""
Configurazione WSGI per il progetto gestionale_bagno.
Non serve modificare questo file.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestionale_bagno.settings')

application = get_wsgi_application()
