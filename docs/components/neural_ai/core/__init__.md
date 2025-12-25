# Neural-AI-Next Core Modul

## Áttekintés

A `neural_ai.core` modul a rendszer alapvető infrastrukturális komponenseit tartalmazza és inicializálja. Ez a modul biztosítja a core komponensek megfelelő sorrendű inicializálását, elkerülve a körkörös függőségeket.

## Fő Komponensek

A modul a következő alapvető rendszerkomponenseket kezeli:

- **Logger rendszer**: Alkalmazás naplózás
- **Konfiguráció kezelés**: Beállítások és konfigurációk kezelése
- **Adattárolás**: Fájl- és adattárolási műveletek
- **Adatbázis**: Adatbázis kapcsolat és session kezelés
- **Event Bus**: Eseményvezérelt architektúra
- **Hardver információk**: CPU feature-ök detektálása

## Verziókezelés

A modul dinamikus verziókezelést biztosít:

### get_version()

Dynamikusan betölti a csomag verzióját a `pyproject.toml`-ból.

```python
from neural_ai.core import get_version

version = get_version()
print(f"Neural-AI-Next verzió: {version}")
```

**Visszatérési érték**: 
- `str`: A csomag verziója vagy `"unknown"`, ha nem érhető el

### get_schema_version()

Visszaadja az aktuális séma verziót, amely a konfigurációs séma kompatibilitását biztosítja.

```python
from neural_ai.core import get_schema_version

schema_version = get_schema_version()
print(f"Séma verzió: {schema_version}")
```

**Visszatérési érték**:
- `str`: Az aktuális séma verzió (pl. `"1.0.0"`)

## Osztályok és Funkciók

### CoreComponents Osztály

A core komponensek tároló osztálya, amely biztosítja a hozzáférésüket az egész alkalmazásban.

```python
class CoreComponents:
    """Core komponensek tároló osztálya."""
    
    def __init__(
        self,
        config: ConfigManagerInterface,
        logger: LoggerInterface,
        storage: StorageInterface,
        database: DatabaseManager,
        event_bus: EventBus,
        hardware: HardwareInfo
    ) -> None:
        """Inicializálja a core komponenseket.
        
        Args:
            config: A konfiguráció kezelő példány
            logger: A logger példány
            storage: A tárhely kezelő példány
            database: Az adatbázis kezelő példány
            event_bus: Az esemény busz példány
            hardware: A hardver információ példány
        """
```

**Attribútumok:**

- `config`: A konfiguráció kezelő interfész
- `logger`: A logger interfész
- `storage`: A tárhely kezelő interfész
- `database`: Az adatbázis kezelő
- `event_bus`: Az esemény busz
- `hardware`: A hardver információk

### bootstrap_core Funkció

Bootstrap funkció a core komponensek inicializálásához. Ez a függvény biztosítja a core komponensek megfelelő sorrendű inicializálását.

```python
def bootstrap_core(
    config_path: Optional[str] = None,
    log_level: Optional[str] = None
) -> CoreComponents:
    """Bootstrap funkció a core komponensek inicializálásához.
    
    Args:
        config_path: Opcionális konfigurációs fájl útvonala
        log_level: Opcionális log szint beállítás
        
    Returns:
        A teljesen inicializált CoreComponents példány
    """
```

**Bootstrap folyamat (lépésenkénti inicializálás):**

1. **Hardware inicializálása** - Hardver információk lekérdezése
2. **Konfiguráció létrehozása** - Konfigurációs fájl betöltése
3. **Logger inicializálása** - Logger létrehozása a konfiggal
4. **Adatbázis inicializálása** - Adatbázis kapcsolat (Config+Logger)
5. **EventBus inicializálása** - Esemény busz (Config+Logger)
6. **Storage inicializálása** - Tárhely (Config+Logger+HardwareInfo)

**Példa használat:**

```python
from neural_ai.core import bootstrap_core

# Alapértelmezett inicializálás
core = bootstrap_core()

# Paraméterezett inicializálás
core = bootstrap_core(
    config_path="/path/to/config.yaml",
    log_level="DEBUG"
)

# Komponensek használata
core.logger.info("Alkalmazás elindult")
await core.database.initialize()
await core.event_bus.start()
```

### get_core_components Funkció

Globális core komponensek lekérdezése. Ez a függvény egy szingleton példányt ad vissza a core komponensekből.

```python
def get_core_components() -> CoreComponents:
    """Globális core komponensek lekérdezése.
    
    Returns:
        A globális CoreComponents példány
    """
```

**Példa használat:**

```python
from neural_ai.core import get_core_components

core = get_core_components()
core.logger.info("Komponens használatban")
```

## Függőségi Kezelés

A modul a `docs/development/core_dependencies.md` dokumentumban leírtakat követve kezeli a függőségeket:

### Körkörös Függőségek Megoldása

A modul a következő módszereket alkalmazza a körkörös függőségek elkerülésére:

1. **Függőségi Injektálás**: Minden komponens opcionális függőségeket kap
2. **TYPE_CHECKING Blokkok**: Típusok késleltetett betöltése
3. **Bootstrap Folyamat**: Komponensek sorrendben történő inicializálása

### Függőségi Gráf

```
Hardware → Config → Logger → Database
                                    ↓
EventBus ←──────────────────────────┘
                                    ↓
Storage ←───────────────────────────┘
```

## Publikus API

A modul a következő elemeket exportálja:

```python
__all__ = [
    "CoreComponents",
    "bootstrap_core", 
    "get_core_components",
    "get_version",
    "get_schema_version",
]
```

## Használati Példák

### Alapvető Inicializálás

```python
from neural_ai.core import bootstrap_core, get_core_components

# Alkalmazás indításkor
core = bootstrap_core()

# Bárhol az alkalmazásban
core = get_core_components()
logger = core.logger
config = core.config
storage = core.storage
database = core.database
event_bus = core.event_bus
hardware = core.hardware
```

### Speciális Konfiguráció

```python
from neural_ai.core import bootstrap_core

# Egyedi konfigurációval
core = bootstrap_core(
    config_path="config/production.yaml",
    log_level="WARNING"
)

# Komponensek használata
logger = core.logger
logger.info("Alkalmazás konfigurálva")
```

### Verzió Információk

```python
from neural_ai.core import get_version, get_schema_version

# Verzió információk lekérdezése
package_version = get_version()
schema_version = get_schema_version()

print(f"Package: {package_version}")
print(f"Schema: {schema_version}")
```

### Tesztelés

```python
from neural_ai.core import CoreComponents
from unittest.mock import Mock

# Mock objektumokkal
mock_config = Mock()
mock_logger = Mock()
mock_storage = Mock()
mock_database = Mock()
mock_event_bus = Mock()
mock_hardware = Mock()

components = CoreComponents(
    config=mock_config,
    logger=mock_logger,
    storage=mock_storage,
    database=mock_database,
    event_bus=mock_event_bus,
    hardware=mock_hardware
)
```

### Main.py Egyszerűsített Használata

```python
#!/usr/bin/env python3
import asyncio
from neural_ai.core import bootstrap_core

async def main():
    """Fő alkalmazás belépési pont."""
    # Core komponensek inicializálása
    components = bootstrap_core()

    # EventBus indítása
    await components.event_bus.start()

    # Adatbázis inicializálása
    await components.database.initialize()

    # Örök futás
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
```

## Fejlesztési Szempontok

### Típusbiztonság

- Minden függvény és metódus típusozott
- `TYPE_CHECKING` blokkok használata a körkörös importok elkerülésére
- Nincs `Any` típus használat
- Szigorú `mypy` ellenőrzés (0 hiba)

### Kódminőség

- `ruff` linter használata (0 hiba)
- 100% tesztlefedettség kötelező
- Magyar nyelvű docstringek (Google style)
- Pylance hiba mentesség

### Verziókezelés

- Dinamikus verzióbetöltés `importlib.metadata` segítségével
- Séma verzió ellenőrzés a konfiguráció kompatibilitásához
- Verzió információk elérhetőek a publikus API-n keresztül

### Dokumentáció

- Minden osztály és függvény magyar nyelvű docstringgel rendelkezik
- Google style docstring formátum
- Példakódok a dokumentációban
- Részletes függőségi dokumentáció

### Tesztelés

- 100% tesztlefedettség kötelező
- Mock objektumok használata a függőségek teszteléséhez
- Unit és integrációs tesztek
- Verzió függvények külön tesztelése

## Kapcsolódó Dokumentáció

- [Core Függőségi Analízis](../development/core_dependencies.md)
- [Konfiguráció Kezelés](./config/__init__.md)
- [Logger Rendszer](./logger/__init__.md)
- [Tárhely Kezelés](./storage/__init__.md)
- [Adatbázis Kezelés](./db/__init__.md)
- [Event Bus](./events/__init__.md)
- [Hardver Információk](./utils/__init__.md)

## Verzió Történet

- **v1.0**: Alapvető core inicializálás és függőségi injektálás implementálva
- **v1.1**: Bootstrap folyamat és szingleton pattern hozzáadva
- **v2.0**: Teljes refaktorálás TYPE_CHECKING és DI használatával
- **v2.1**: Verziókezelés hozzáadva (`get_version`, `get_schema_version`)
- **v3.0**: Core bootstrap refaktor - Database, EventBus, Hardware integráció