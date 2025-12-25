# neural_ai/__init__.py

## Áttekintés

Ez a modul a Neural-AI-Next projekt fő inicializációs pontja. Felelős a projekt verzióinformációinak, konfigurációs séma verziójának és alapvető publikus API-jának exportálásáért.

## Verziókezelés

A modul dinamikusan tölti be a projekt verziószámát az `importlib.metadata` segítségével a `pyproject.toml` fájlból. Ez biztosítja, hogy a verzió mindig szinkronban legyen a projekt konfigurációjával.

### Verzió lekérdezése

```python
import neural_ai

print(f"Neural-AI-Next verzió: {neural_ai.__version__}")
print(f"Konfigurációs séma verzió: {neural_ai.__schema_version__}")
```

## Konfigurációs Séma Verzió

A `__schema_version__` változó a konfigurációs séma verziószámát tartalmazza. Ez kritikus fontosságú a kompatibilitás ellenőrzéséhez és a migrációs folyamatok automatizálásához a 10. fejezet szerint.

### Sémaverzió használata

```python
import neural_ai
from neural_ai.core.config import ConfigManager

config = ConfigManager()
current_schema = neural_ai.__schema_version__

if config.schema_version != current_schema:
    print(f"Figyelmeztetés: A konfigurációs séma elavult!")
    print(f"Aktuális: {config.schema_version}, Szükséges: {current_schema}")
    # Automatikus migráció indítása
    config.migrate_schema(current_schema)
```

## Publikus API

### Verzió információk

```python
__version__: Final[str]
```

A projekt aktuális verziószáma (pl. "0.5.0"). A verziószámot a `pyproject.toml`-ból tölti be dinamikusan.

```python
__schema_version__: Final[str]
```

A konfigurációs séma verziószáma (pl. "1.0"). Ezt a verziót használja a rendszer a konfigurációs fájlok kompatibilitásának ellenőrzéséhez.

### Exportok

```python
__all__: Final[list[str]]
```

A modul által exportált publikus szimbólumok listája. Jelenleg a következőket tartalmazza:

- `__version__`: Projekverzió
- `__schema_version__`: Konfigurációs séma verziója

## Függőségek

Ez a modul minimalizált függőségekkel rendelkezik:

- **Python 3.8+**: Az `importlib.metadata` modul használatához
- **importlib_metadata** (opcionális): Python 3.8 alatti verziókhoz

A tényleges funkcionalitás a `neural_ai.core` modulban található, amely a következő komponenseket tartalmazza:

- **Config**: Konfigurációkezelés
- **Logger**: Naplózási rendszer
- **Storage**: Adattárolási réteg

## Típusozás

A modul szigorú típusozást használ a `typing.Final` annotációval, hogy megakadályozza a véletlen módosításokat:

```python
from typing import Final

__version__: Final[str] = "0.5.0"
__schema_version__: Final[str] = "1.0"
```

Ez biztosítja, hogy a verzióinformációk futási időben ne módosulhassanak véletlenül.

## Használati Példák

### Alapvető inicializálás

```python
import neural_ai

# Verzió ellenőrzése
print(f"Neural-AI-Next {neural_ai.__version__}")

# Sémaverzió ellenőrzése
print(f"Konfigurációs séma: {neural_ai.__schema_version__}")
```

### Konfiguráció betöltése verzióellenőrzéssel

```python
import neural_ai
from neural_ai.core import bootstrap_core

# Core komponensek inicializálása
core = bootstrap_core()

# Sémaverzió ellenőrzése
if core.config.schema_version != neural_ai.__schema_version__:
    print("Konfigurációs séma migrálása szükséges!")
    core.config.migrate(neural_ai.__schema_version__)
```

### Telepítés ellenőrzése

```python
import neural_ai

def check_installation():
    """Ellenőrzi a Neural-AI-Next telepítését."""
    try:
        version = neural_ai.__version__
        print(f"Sikeres telepítés: Neural-AI-Next {version}")
        return True
    except Exception as e:
        print(f"Hiba a telepítés ellenőrzésekor: {e}")
        return False
```

## Fejlesztői Jegyzetek

### Verziószámozás Stratégia

A projekt a [Semantic Versioning](https://semver.org/) elveit követi:

- **Major** (1.0.0): Kompatibilitástörő változtatások
- **Minor** (0.5.0): Új funkciók, visszafelé kompatibilis
- **Patch** (0.4.1): Hibajavítások

### Sémaverzió kezelés

A konfigurációs séma verziószámozása független a projekt verziószámától:

- A sémaverzió csak akkor változik, ha a konfigurációs struktúra módosul
- A migrációs szkriptek automatikusan frissítik a régi konfigurációkat
- A sémaverzió ellenőrzése minden alkalommal megtörténik, amikor a rendszer betölti a konfigurációt

## Jövőbeli Fejlesztések

- **Alapértelmezett konfiguráció exportálása**: A leggyakrabban használt konfigurációs beállítások közvetlen elérése
- **Gyors inicializáló függvények**: Egysoros inicializálás a leggyakoribb használati esetekhez
- **Publikus API bővítése**: A leggyakrabban használt komponensek közvetlen importálása
- **Telepítés ellenőrző eszközök**: További helper funkciók a környezet ellenőrzéséhez

## Hibaelhárítás

### Hiba: "PackageNotFoundError"

**Ok**: A `neural-ai-next` csomag nincs telepítve a környezetben.

**Megoldás**:
```bash
pip install -e .
```

vagy

```bash
conda env update -f environment.yml
```

### Hiba: "ModuleNotFoundError: No module named 'importlib_metadata'"

**Ok**: Python 3.8 alatti verzió használata.

**Megoldás**:
```bash
pip install importlib-metadata
```

## Lásd még

- [`neural_ai.core`](../core/__init__.md): A core komponensek dokumentációja
- [`pyproject.toml`](../../../pyproject.toml): Projekverzió konfigurációja
- [Fejlesztési útmutató](../../development/implementation_guide.md): Részletes implementációs információk