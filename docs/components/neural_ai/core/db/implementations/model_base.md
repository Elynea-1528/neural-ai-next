# Model Base

## Áttekintés

Adatbázis modellek alaposztályai.

Ez a modul definiálja az összes adatbázis modell által használt alaposztályokat és segédosztályokat a Neural AI Next rendszerben.

## Osztályok

### `Base`

SQLAlchemy deklaratív alaposztály a modellekhez.

Ez az osztály biztosítja a standardizált mezőket és metódusokat az összes adatbázis modell számára.

#### Attribútumok

- `id`: Elsődleges kulcs minden modellhez.
- `created_at`: A rekord létrehozásának időpontja.
- `updated_at`: A rekord utolsó módosításának időpontja.

#### Osztályszintű Attribútumok

- `type_annotation_map`: Típusleképezés a datetime mezőkhöz

#### Oszlop Definíciók

##### `id`

Rekord elsődleges kulcsa.

- **Típus**: `Integer`
- **Elsődleges kulcs**: Igen
- **Autoincrement**: Igen
- **Nullable**: Nem

##### `created_at`

A rekord létrehozásának időpontja (UTC).

- **Típus**: `DateTime(timezone=True)`
- **Default**: `datetime.utcnow`
- **Nullable**: Nem

##### `updated_at`

A rekord utolsó módosításának időpontja (UTC).

- **Típus**: `DateTime(timezone=True)`
- **Default**: `datetime.utcnow`
- **Onupdate**: `datetime.utcnow`
- **Nullable**: Nem

#### Metódusok

##### `__tablename__`

Automatikus táblanév generálás a class névből.

A class nevet snake_case formátumba konvertálja és hozzáadja egy 's' végződést.

**Visszatérési érték:**
- `str`: A generált táblanév string formátumban.

**Példák:**
- `DynamicConfig` → `dynamicconfigs`
- `LogEntry` → `logentrys`

##### `to_dict()`

Modell átalakítása dictionary formátumba.

Az összes oszlop értékét dictionary formátumba konvertálja, datetime objektumokat ISO formátumú stringgé alakítja.

**Visszatérési érték:**
- `dict[str, Any]`: A modell adatait tartalmazó dictionary.

##### `__repr__()`

Modell string reprezentációja.

**Visszatérési érték:**
- `str`: A modell rövid string reprezentációja.

## Használati Példák

### Alap modell létrehozása

```python
from neural_ai.core.db.implementations.model_base import Base
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

class Product(Base):
    """Termék modell."""
    
    # A __tablename__ automatikusan generálódik: 'products'
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="A termék neve"
    )
    
    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        doc="A termék ára"
    )
    
    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
        doc="A termék leírása"
    )
```

### Modell használata

```python
from datetime import datetime
from neural_ai.core.db import get_db_session
from sqlalchemy import select

# Termék létrehozása
product = Product(
    name="Teszt Termék",
    price=99.99,
    description="Ez egy teszt termék"
)

# A Base osztály automatikusan hozzáadja:
# - id: autoincrement
# - created_at: aktuális idő
# - updated_at: aktuális idő

print(f"Termék ID: {product.id}")
print(f"Létrehozva: {product.created_at}")
print(f"Frissítve: {product.updated_at}")

# Dictionary formátumba konvertálás
product_dict = product.to_dict()
print(product_dict)
# {
#     'id': 1,
#     'name': 'Teszt Termék',
#     'price': 99.99,
#     'description': 'Ez egy teszt termék',
#     'created_at': '2024-01-01T12:00:00Z',
#     'updated_at': '2024-01-01T12:00:00Z'
# }

# String reprezentáció
print(repr(product))
# <Product(id=1)>
```

### Egyéni táblanév

```python
from neural_ai.core.db.implementations.model_base import Base
from sqlalchemy import Column, String

class User(Base):
    """Felhasználó modell egyéni táblanévvel."""
    
    __tablename__ = 'users'  # Egyéni táblanév
    
    username: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        doc="A felhasználónév"
    )
    
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        doc="Az email cím"
    )
```

### Öröklés használata

```python
from neural_ai.core.db.implementations.model_base import Base
from sqlalchemy import Column, String, Boolean

class TimestampedModel(Base):
    """Időbélyeggel ellátott modell bázisosztály."""
    
    __abstract__ = True  # Ez nem lesz saját tábla
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        doc="Aktív-e a rekord"
    )

class Category(TimestampedModel):
    """Kategória modell."""
    
    # A __tablename__ automatikusan generálódik: 'categorys'
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        doc="A kategória neve"
    )
    
    # Örökli a Base osztály összes mezőjét:
    # - id
    # - created_at
    # - updated_at
    # - is_active (a TimestampedModel-ből)
```

### Adatbázis műveletek

```python
from neural_ai.core.db import get_db_session
from sqlalchemy import select

async def get_all_products():
    """Összes termék lekérdezése."""
    async with get_db_session() as session:
        stmt = select(Product)
        result = await session.execute(stmt)
        products = result.scalars().all()
        
        # Dictionary formátumba konvertálás
        return [product.to_dict() for product in products]

async def get_product_by_id(product_id: int):
    """Termék lekérdezése ID alapján."""
    async with get_db_session() as session:
        stmt = select(Product).where(Product.id == product_id)
        result = await session.execute(stmt)
        product = result.scalar_one_or_none()
        
        if product:
            return product.to_dict()
        return None
```

## Előnyök

1. **Standardizált mezők**: Minden modell rendelkezik azonos alapmezőkkel (id, created_at, updated_at)
2. **Automatikus időbélyeg**: A létrehozási és módosítási idő automatikusan kezelésre kerül
3. **Dictionary konverzió**: Egyszerű adatok konvertálása dictionary formátumba
4. **Automatikus táblanév**: A táblanevek automatikusan generálódnak a class nevekből
5. **Típusbiztonság**: SQLAlchemy 2.0 style mapping használata típusbiztonság érdekében

## Kapcsolódó Dokumentáció

- [Modellek](models.md)
- [SQLAlchemy Session](sqlalchemy_session.md)
- [DB Implementációk](__init__.md)
- [DB Modul](../__init__.md)