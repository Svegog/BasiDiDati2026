Punti diversi rispetto alla progettazione con Flask:
- Step 3: con Django non si scrivono le CREATE TABLE a mano in Workbench, basta creare il database vuoto
- Step 5-6: modelli Python (models.py) al posto del DDL manuale, con db_table per mantenere i nomi tabella coerenti con lo schema DbMain, e migrations che generano le tabelle automaticamente
- Step 6: admin panel automatico, un vantaggio specifico di Django
- Step 7: mostro entrambe le strade per le query, ORM Django e SQL puro con connection.cursor(), utile se vuoi restare più fedele alle query già tradotte da DbMain invece di usare l'ORM
