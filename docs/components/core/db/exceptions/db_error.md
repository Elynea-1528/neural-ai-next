# core/db/exceptions/db_error.py

Adatbázis-specifikus kivételek.

Ez a modul tartalmazza az összes adatbázis-műveletekhez kapcsolódó kivételeket.

## Osztályok

### `DatabaseError`

Általános adatbázis hiba.

### `DBConnectionError`

Adatbázis kapcsolat hiba.

### `TransactionError`

Tranzakció hiba.


## Függvények

### `__init__`

Inicializálja a TransactionError kivételt.

        Args:
            message: A hibaüzenet.
            transaction_id: A tranzakció azonosítója.


---

**Forrásfájl:** [`core/db/exceptions/db_error.py`](../../../neural_ai/core/db/exceptions/db_error.py)
