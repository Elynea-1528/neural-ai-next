# DB Error Kivételek

## Áttekintés

Adatbázis-specifikus kivételek.

Ez a modul tartalmazza az összes adatbázis-műveletekhez kapcsolódó kivételeket.

## Kivétel Osztályok

### `DatabaseError`

Általános adatbázis hiba.

Ez az osztály az összes adatbázis-specifikus kivétel alaposztálya. A `NeuralAIException` osztályból származik.

#### Attribútumok

- `message`: A hibaüzenet.
- `details`: Opcionális részletes leírás a hibáról.

#### Metódusok

##### `__init__(message, details)`

Inicializálja a DatabaseError kivételt.

**Paraméterek:**
- `message`: A hibaüzenet.
- `details`: Opcionális részletes leírás a hibáról.

### `DBConnectionError`

Adatbázis kapcsolat hiba.

Akkor dobódik, ha probléma merül fel az adatbázishoz való kapcsolódás során.

#### Attribútumok

- `message`: A hibaüzenet.
- `connection_string`: Az adatbázis kapcsolati sztringje.

#### Metódusok

##### `__init__(message, connection_string)`

Inicializálja a DBConnectionError kivételt.

**Paraméterek:**
- `message`: A hibaüzenet.
- `connection_string`: Az adatbázis kapcsolati sztringje.

### `TransactionError`

Tranzakció hiba.

Akkor dobódik, ha probléma merül fel egy adatbázis tranzakció során (pl. rollback, commit hiba).

#### Attribútumok

- `message`: A hibaüzenet.
- `transaction_id`: A tranzakció azonosítója.

#### Metódusok

##### `__init__(message, transaction_id)`

Inicializálja a TransactionError kivételt.

**Paraméterek:**
- `message`: A hibaüzenet.
- `transaction_id`: A tranzakció azonosítója.

## Kivétel Hierarchia

```
NeuralAIException
└── DatabaseError
    ├── DBConnectionError
    └── TransactionError
```

## Használati Példák

### Kapcsolódási hiba kezelése

```python
from neural_ai.core.db.exceptions import DBConnectionError
from neural_ai.core.db import get_database_url

def validate_database_connection():
    try:
        db_url = get_database_url()
        # Kapcsolódási próbálkozás...
        
    except Exception as e:
        raise DBConnectionError(
            message=f"Nem sikerült kapcsolódni az adatbázishoz: {str(e)}",
            connection_string=db_url
        ) from e
```

### Tranzakció hiba kezelése

```python
from neural_ai.core.db.exceptions import TransactionError
from neural_ai.core.db import get_db_session
from sqlalchemy import update
from neural_ai.core.db.implementations.models import DynamicConfig

async def update_config_safe(config_id, new_value):
    """Biztonságos konfiguráció frissítés tranzakcióban."""
    async with get_db_session() as session:
        try:
            # Tranzakció indítása
            await session.begin()
            
            # Frissítés végrehajtása
            stmt = (
                update(DynamicConfig)
                .where(DynamicConfig.id == config_id)
                .values(value=new_value)
            )
            result = await session.execute(stmt)
            
            if result.rowcount == 0:
                raise TransactionError(
                    message=f"Konfiguráció nem található: {config_id}",
                    transaction_id=str(config_id)
                )
            
            # Tranzakció commit
            await session.commit()
            
        except Exception as e:
            # Rollback ha hiba történt
            await session.rollback()
            
            if isinstance(e, TransactionError):
                raise
            
            raise TransactionError(
                message=f"Tranzakció sikertelen: {str(e)}",
                transaction_id=str(config_id)
            ) from e
```

### Általános adatbázis hiba

```python
from neural_ai.core.db.exceptions import DatabaseError
from neural_ai.core.db import get_db_session
from sqlalchemy import select
from neural_ai.core.db.implementations.models import LogEntry

async def get_recent_logs(limit: int = 100):
    """Legutóbbi naplóbejegyzések lekérdezése."""
    try:
        async with get_db_session() as session:
            stmt = select(LogEntry).order_by(LogEntry.created_at.desc()).limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()
            
    except Exception as e:
        raise DatabaseError(
            message=f"Naplóbejegyzések lekérdezése sikertelen: {str(e)}",
            details=f"Limit: {limit}"
        ) from e
```

### Hiba láncolás

```python
from neural_ai.core.db.exceptions import DatabaseError, DBConnectionError

async def execute_query(query):
    """Lekérdezés végrehajtása hiba láncolással."""
    try:
        # Adatbázis művelet...
        pass
        
    except DBConnectionError as e:
        # Kapcsolódási hiba továbbadása
        raise
        
    except Exception as e:
        # Általános adatbázis hiba
        raise DatabaseError(
            message=f"Lekérdezés végrehajtása sikertelen: {str(e)}",
            details=f"Query: {str(query)}"
        ) from e
```

### Tesztelési forgatókönyv

```python
import pytest
from neural_ai.core.db.exceptions import DBConnectionError, TransactionError

def test_database_connection_error():
    """Teszteli a kapcsolódási hibák kezelését."""
    with pytest.raises(DBConnectionError) as exc_info:
        connect_to_database("invalid_connection_string")
    
    assert exc_info.value.connection_string == "invalid_connection_string"
    assert "Nem sikerült kapcsolódni" in str(exc_info.value.message)

def test_transaction_rollback():
    """Teszteli a tranzakció rollback-jét."""
    with pytest.raises(TransactionError) as exc_info:
        update_config_safe(999, "invalid_value")
    
    assert exc_info.value.transaction_id == "999"
    assert "sikertelen" in str(exc_info.value.message)
```

## Hibakezelési Stratégia

### 1. Specifikus hibák használata

Mindig a legspecifikusabb kivétel osztályt használd a hibák jelzésére:

```python
# Rossz
raise Exception("Adatbázis hiba")

# Jó
raise DBConnectionError("Nem sikerült kapcsolódni", connection_string=db_url)
```

### 2. Hiba láncolás

Használd a `from` kulcsszót a hibák láncolásához:

```python
try:
    # Adatbázis művelet...
except Exception as e:
    raise DatabaseError("Adatbázis hiba") from e
```

### 3. Részletes információk

Add meg a releváns információkat a kivétel attribútumokban:

```python
raise DBConnectionError(
    message="Kapcsolódási időtúllépés",
    connection_string=db_url
)
```

## Kapcsolódó Dokumentáció

- [Kivételek Modul](__init__.md)
- [DB Modul](../__init__.md)
- [Base Kivételek](../base/exceptions/base_error.md)