# DB Kivételek Modul

## Áttekintés

Adatbázis kivételek modulja.

Ez a csomag tartalmazza az összes adatbázis-műveletekhez kapcsolódó kivételeket.

## Exportált Kivétel Osztályok

- [`DatabaseError`](db_error.md#databaseerror): Általános adatbázis hiba
- [`DBConnectionError`](db_error.md#dbconnectionerror): Adatbázis kapcsolat hiba
- [`TransactionError`](db_error.md#transactionerror): Tranzakció hiba

## Kivétel Hierarchia

```
NeuralAIException
└── DatabaseError
    ├── DBConnectionError
    └── TransactionError
```

## Használati Példák

### Alap adatbázis hiba kezelés

```python
from neural_ai.core.db.exceptions import DatabaseError, DBConnectionError

try:
    # Adatbázis művelet...
    pass
except DBConnectionError as e:
    print(f"Kapcsolódási hiba: {e}")
    print(f"Kapcsolati sztring: {e.connection_string}")
except DatabaseError as e:
    print(f"Adatbázis hiba: {e}")
    print(f"Részletek: {e.details}")
```

### Tranzakció hiba kezelése

```python
from neural_ai.core.db.exceptions import TransactionError
from neural_ai.core.db import get_db_session

async def update_data(data_id, new_value):
    async with get_db_session() as session:
        try:
            # Tranzakció indítása
            await session.begin()
            
            # Adatmódosítás...
            
            # Tranzakció commit
            await session.commit()
            
        except Exception as e:
            await session.rollback()
            raise TransactionError(
                message=f"Tranzakció sikertelen: {str(e)}",
                transaction_id=str(data_id)
            )
```

### Kapcsolódási hiba létrehozása

```python
from neural_ai.core.db.exceptions import DBConnectionError

def connect_to_database(connection_string):
    if not connection_string:
        raise DBConnectionError(
            message="Nincs megadva kapcsolati sztring",
            connection_string=connection_string
        )
    
    try:
        # Kapcsolódási próbálkozás...
        pass
    except Exception as e:
        raise DBConnectionError(
            message=f"Nem sikerült kapcsolódni az adatbázishoz: {str(e)}",
            connection_string=connection_string
        ) from e
```

## Kapcsolódó Dokumentáció

- [DB Error](db_error.md): Az összes kivétel osztály részletes leírása
- [DB Modul](../__init__.md)
- [Base Kivételek](../base/exceptions/base_error.md)