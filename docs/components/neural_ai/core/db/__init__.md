# neural_ai/core/db/__init__.py

Adatbázis modul a Neural AI Next rendszerhez.

Ez a modul biztosítja az adatbázis kapcsolat kezelést, modelleket és session
factory-t az aszinkron adatbázis műveletekhez.

DDD Szabály:
    Csak Factory + Exceptions exportáltak.
    Az implementációk (Base, models, DatabaseManager, session függvények) NEM exportáltak.
    Ezeket közvetlenül a DatabaseFactory vagy az implementations modulból kell importálni.

Megjegyzés:
    A modul jelenleg nem rendelkezik interfészekkel (interfaces/ üres).
    Ez egy későbbi fázisban kerül kialakításra (DatabaseInterface, SessionInterface).

## Importok

```python
from neural_ai.core.db.exceptions import DatabaseError
from neural_ai.core.db.exceptions import DBConnectionError
from neural_ai.core.db.exceptions import TransactionError
from neural_ai.core.db.factory import DatabaseFactory
```

## Konstansok

- **`__all__`**
: `['DatabaseFactory', 'DatabaseError', 'DBConnectionError', 'TransactionError']`


---

**Forrásfájl:** [`neural_ai/core/db/__init__.py`](../../neural_ai/core/db/__init__.py)
