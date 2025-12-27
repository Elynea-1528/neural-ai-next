# Model Base - Adatbázis Modellek Alaposztálya

## Áttekintés

A `model_base.py` modul definiálja az összes adatbázis modell által használt alaposztályokat és segédosztályokat a Neural AI Next rendszerben. Ez az osztály biztosítja a standardizált mezőket és metódusokat az összes adatbázis modell számára.

## Osztályok

### Base

SQLAlchemy deklaratív alaposztály a modellekhez.

#### Attribútumok

- **`id`**: `Mapped[int]` - Elsődleges kulcs minden modellhez. Autoincrement és nem nullázható.
- **`created_at`**: `Mapped[datetime]` - A rekord létrehozásának időpontja (UTC). Automatikusan beállítódik a létrehozáskor.
- **`updated_at`**: `Mapped[datetime]` - A rekord utolsó módosításának időpontja (UTC). Automatikusan frissül módosításkor.

#### Metódusok

##### `__tablename__`

Automatikus táblanév generálás a class névből.

A class nevet snake_case formátumba konvertálja és hozzáadja egy 's' végződést.

**Példák:**
- `DynamicConfig` → `dynamic_configs`
- `ConfigEntry` → `configs`

**Visszatérési érték:** A generált táblanév string formátumban.

##### `to_dict()`

Modell átalakítása dictionary formátumba.

Az összes oszlop értékét dictionary formátumba konvertálja, datetime objektumokat ISO formátumú stringgé alakítja.

**Visszatérési érték:** A modell adatait tartalmazó dictionary.

**Példa:**
```python
{
    "id": 1,
    "name": "Test",
    "value": 42,
    "created_at": "2025-12-27T00:00:00+00:00",
    "updated_at": "2025-12-27T00:00:00+00:00"
}
```

##### `__repr__()`

Modell string reprezentációja.

**Visszatérési érték:** A modell rövid string reprezentációja.

**Példa:** `<TestModel(id=1)>`

## Használat

### Alapvető példa

```python
from neural_ai.core.db.implementations.model_base import Base
from sqlalchemy import Column, String, Integer

class User(Base):
    """Felhasználói modell."""
    
    username: str = Column(String(50), nullable=False)
    email: str = Column(String(100), nullable=False)
    age: int = Column(Integer, nullable=True)
```

### Példa a metódusok használatára

```python
# Modell létrehozása
user = User(username="john_doe", email="john@example.com", age=30)

# Adatbázisba mentés
session.add(user)
session.commit()

# Dictionary formátumba konvertálás
user_dict = user.to_dict()
print(user_dict)
# {
#     "id": 1,
#     "username": "john_doe",
#     "email": "john@example.com",
#     "age": 30,
#     "created_at": "2025-12-27T00:00:00+00:00",
#     "updated_at": "2025-12-27T00:00:00+00:00"
# }

# String reprezentáció
print(repr(user))
# <User(id=1)>
```

## Technikai részletek

### Időbélyeg kezelés

A `created_at` és `updated_at` mezők automatikusan kezelik az időbélyegeket:

- **`created_at`**: Beállítódik a rekord létrehozásakor, és soha nem változik.
- **`updated_at`**: Beállítódik a létrehozáskor, és minden módosításkor automatikusan frissül.

Az időbélyegek UTC időzónában tárolódnak a `datetime.now(timezone.utc)` használatával, ami biztosítja a konzisztens időkezelést.

### Táblanév generálás

Az automatikus táblanév generálás a következő szabályokat követi:

1. A class név kisbetűssé alakítása
2. A "config" és "entry" szavak eltávolítása
3. Többes számú végződés hozzáadása ('s')

### Típusosság

A modul szigorú típusosságot követ:

- Minden mezőnek van típus annotációja
- A `Dict[str, Any]` típus használata a dictionary visszatérési értékeknél
- A `TYPE_CHECKING` blokk használata a körkörös importok elkerülésére

## Kapcsolódó dokumentáció

- [Architektúra szabványok](../../../development/architecture_standards.md)
- [Adatbázis factory](../factory.md)
- [SQLAlchemy session implementáció](sqlalchemy_session.md)
- [Modellek implementációja](models.md)

## Verzió történet

- **v1.0**: Kezdeti implementáció a deprecated `datetime.utcnow()` használatával
- **v2.0**: Refaktorálva a `datetime.now(timezone.utc)` használatára, típusosság javítása