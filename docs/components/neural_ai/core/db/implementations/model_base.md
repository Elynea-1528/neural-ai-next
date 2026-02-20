# neural_ai/core/db/implementations/model_base.py

Adatbázis modellek alaposztályai.

Ez a modul definiálja az összes adatbázis modell által használt alaposztályokat
és segédosztályokat a Neural AI Next rendszerben.

## Importok

```python
from datetime import UTC
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import mapped_column
```

## Osztály: `Base(DeclarativeBase)`

SQLAlchemy deklaratív alaposztály a modellekhez.

Ez az osztály biztosítja a standardizált mezőket és metódusokat
az összes adatbázis modell számára.

Attributes:
    id: Elsődleges kulcs minden modellhez.
    created_at: A rekord létrehozásának időpontja.
    updated_at: A rekord utolsó módosításának időpontja.

### Metódusok

#### `__tablename__()`

```python
def __tablename__(cls) -> str
```

Automatikus táblanév generálás a class névből. A class nevet snake_case formátumba konvertálja és hozzáadja egy 's' végződést. Például: DynamicConfig -> dynamic_configs

**Paraméterek:**

- **`cls`**

**Visszatérési érték:**

- Típus: `str`
- A generált táblanév string formátumban.

#### `to_dict()`

```python
def to_dict(self) -> dict[str, object]
```

Modell átalakítása dictionary formátumba. Az összes oszlop értékét dictionary formátumba konvertálja, datetime objektumokat ISO formátumú stringgé alakítja.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, object]`
- A modell adatait tartalmazó dictionary.

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

**Forrásfájl:** [`neural_ai/core/db/implementations/model_base.py`](../../neural_ai/core/db/implementations/model_base.py)
