# Adatbázis Modellek (`neural_ai.core.db.implementations.models`)

## Áttekintés

Ez a modul definiálja az összes adatbázis táblát és modellt a Neural AI Next rendszerben. A modellek SQLAlchemy ORM alapúak és a `Base` osztályból származnak, amely biztosítja a standardizált mezőket és metódusokat.

## Osztályok

### `DynamicConfig`

Dinamikus konfigurációs értékek tárolására szolgáló modell. Ez a modell tárolja a futás közben módosítható konfigurációs értékeket, amelyek hot reload támogatással rendelkeznek.

#### Attribútumok

| Név | Típus | Leírás |
|-----|-------|--------|
| `key` | `str` | A konfigurációs kulcs (egyedi, maximum 255 karakter) |
| `value` | `Any` | A konfigurációs érték (JSON formátumban) |
| `value_type` | `str` | Az érték típusa (int, float, str, bool, list, dict) |
| `category` | `str` | A konfiguráció kategóriája (risk, strategy, trading, system) |
| `description` | `str \| None` | A konfiguráció részletes leírása |
| `is_active` | `bool` | A konfiguráció aktív-e (alapértelmezett: True) |

#### Tábla információk

- **Táblanév:** `dynamic_configs`
- **Indexek:**
  - `idx_dynamic_config_category_active`: Összetett index a `category` és `is_active` mezőkre
  - `idx_dynamic_config_key_active`: Összetett index a `key` és `is_active` mezőkre
  - Egyedi index a `key` mezőre

#### Metódusok

##### `__repr__() -> str`

Modell string reprezentációja.

**Visszatérési érték:**
- `str`: A modell rövid string reprezentációja (pl. `<DynamicConfig(key='max_risk', value=0.05, type=float)>`)

---

### `LogEntry`

Rendszer naplóbejegyzéseket tároló modell. Ez a modell tárolja a rendszer által generált naplóbejegyzéseket strukturált formában az adatbázisban.

#### Attribútumok

| Név | Típus | Leírás |
|-----|-------|--------|
| `level` | `str` | A napló szintje (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `logger_name` | `str` | A logger neve |
| `message` | `str` | A naplóüzenet |
| `module` | `str \| None` | A modul neve, ahonnan a napló született |
| `function` | `str \| None` | A függvény neve, ahonnan a napló született |
| `line_number` | `int \| None` | A sor száma, ahonnan a napló született |
| `process_id` | `int \| None` | A folyamat azonosítója |
| `thread_id` | `int \| None` | A szál azonosítója |
| `exception_type` | `str \| None` | A kivétel típusa (ha van) |
| `exception_message` | `str \| None` | A kivétel üzenete (ha van) |
| `traceback` | `str \| None` | A traceback információ (ha van) |
| `extra_data` | `dict[str, Any] \| None` | További egyéni adatok (JSON formátumban) |

#### Tábla információk

- **Táblanév:** `log_entries`
- **Indexek:**
  - `idx_log_entries_level_created`: Összetett index a `level` és `created_at` mezőkre
  - `idx_log_entries_logger_created`: Összetett index a `logger_name` és `created_at` mezőkre
  - Egyedi indexek a `level` és `logger_name` mezőkre

#### Metódusok

##### `__repr__() -> str`

Modell string reprezentációja.

**Visszatérési érték:**
- `str`: A modell rövid string reprezentációja (pl. `<LogEntry(level='INFO', logger='core.db', message='Database connection established...')>`)

## Használati példa

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from neural_ai.core.db.implementations.models import DynamicConfig, LogEntry
from neural_ai.core.db.implementations.model_base import Base

# Adatbázis engine létrehozása
engine = create_engine("sqlite:///neural_ai.db")

# Táblák létrehozása
Base.metadata.create_all(engine)

# Munkamenet létrehozása
with Session(engine) as session:
    # Dinamikus konfiguráció létrehozása
    config = DynamicConfig(
        key="max_risk_per_trade",
        value=0.05,
        value_type="float",
        category="risk",
        description="Maximum risk per trade as percentage of account",
        is_active=True
    )
    session.add(config)
    
    # Naplóbejegyzés létrehozása
    log_entry = LogEntry(
        level="INFO",
        logger_name="trading.system",
        message="Trading system initialized successfully",
        module="trading",
        function="initialize",
        line_number=42,
        process_id=1234,
        thread_id=5678
    )
    session.add(log_entry)
    
    session.commit()
    
    # Adatok lekérdezése
    configs = session.query(DynamicConfig).filter_by(category="risk", is_active=True).all()
    logs = session.query(LogEntry).filter_by(level="INFO").all()
```

## Típusok és Biztonság

A modell erős típusosságot követel meg:

- Minden mezőnek definiált típusa van
- Az `Any` típus csak a `TYPE_CHECKING` blokkban szerepel
- Opcionális mezők esetén `| None` típus annotáció használatos
- A JSON mezők típusa explicit módon definiálva van (`dict[str, Any]`)

## Kapcsolódó dokumentáció

- [`model_base.md`](model_base.md) - Az alaposztály dokumentációja
- [`sqlalchemy_session.md`](sqlalchemy_session.md) - Munkamenet kezelés
- [SQLAlchemy ORM dokumentáció](https://docs.sqlalchemy.org/en/20/orm/)