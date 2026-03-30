# neural_ai/core/db/implementations/models.py

Adatbázis modellek a Neural AI Next rendszerhez.

Ez a modul definiálja az összes adatbázis táblát és modellt a rendszerben,
beleértve a DynamicConfig és LogEntry modelleket.

## Importok

```python
from typing import TYPE_CHECKING
from sqlalchemy import Boolean
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import mapped_column
from neural_ai.core.db.implementations.model_base import Base
```

## Osztály: `DynamicConfig(Base)`

Dinamikus konfigurációs értékek tárolására szolgáló modell.

Ez a modell tárolja a futás közben módosítható konfigurációs értékeket,
amelyek hot reload támogatással rendelkeznek.

Attributes:
    key: A konfigurációs kulcs (egyedi).
    value: A konfigurációs érték (JSON formátumban).
    value_type: Az érték típusa (int, float, str, bool, list, dict).
    category: A konfiguráció kategóriája (risk, strategy, trading, system).
    description: A konfiguráció leírása.
    is_active: A konfiguráció aktív-e.

### Metódusok

#### `__repr__()`

```python
def __repr__(self) -> str
```

Modell string reprezentációja.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `str`
- A modell rövid string reprezentációja.

## Osztály: `LogEntry(Base)`

Rendszer naplóbejegyzéseket tároló modell.

Ez a modell tárolja a rendszer által generált naplóbejegyzéseket
strukturált formában az adatbázisban.

Attributes:
    level: A napló szintje (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    logger_name: A logger neve.
    message: A naplóüzenet.
    module: A modul neve, ahonnan a napló született.
    function: A függvény neve, ahonnan a napló született.
    line_number: A sor száma, ahonnan a napló született.
    process_id: A folyamat azonosítója.
    thread_id: A szál azonosítója.
    exception_type: A kivétel típusa (ha van).
    exception_message: A kivétel üzenete (ha van).
    traceback: A traceback információ (ha van).
    extra_data: További egyéni adatok (JSON formátumban).

### Metódusok

#### `__tablename__()`

```python
def __tablename__(cls) -> str
```

LogEntries tábla neve.

**Paraméterek:**

- **`cls`**

**Visszatérési érték:**

- Típus: `str`
- A tábla neve string formátumban.

#### `__repr__()`

```python
def __repr__(self) -> str
```

Modell string reprezentációja.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `str`
- A modell rövid string reprezentációja.

---

**Forrásfájl:** [`neural_ai/core/db/implementations/models.py`](../../neural_ai/core/db/implementations/models.py)
