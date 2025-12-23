# Neural-AI-Next Core Modul

## Áttekintés

A `neural_ai.core` modul a rendszer alapvető infrastrukturális komponenseit tartalmazza és inicializálja. Ez a modul biztosítja a core komponensek megfelelő sorrendű inicializálását, elkerülve a körkörös függőségeket.

## Fő Komponensek

A modul a következő alapvető rendszerkomponenseket kezeli:

- **Logger rendszer**: Alkalmazás naplózás
- **Konfiguráció kezelés**: Beállítások és konfigurációk kezelése
- **Adattárolás**: Fájl- és adattárolási műveletek

## Osztályok és Funkciók

### CoreComponents Osztály

A core komponensek tároló osztálya, amely biztosítja a hozzáférésüket az egész alkalmazásban.

```python
class CoreComponents:
    """Core komponensek tároló osztálya."""
    
    def __init__(
        self,
        config: ConfigInterface,
        logger: LoggerInterface,
        storage: StorageInterface
    ) -> None:
        """Inicializálja a core komponenseket.
        
        Args:
            config: A konfiguráció kezelő példány
            logger: A logger példány
            storage: A tárhely kezelő példány
        """
```

**Attribútumok:**

- `config`: A konfiguráció kezelő interfész
- `logger`: A logger interfész
- `storage`: A tárhely kezelő interfész

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

**Bootstrap folyamat:**

1. Alap konfiguráció létrehozása
2. Logger inicializálása a konfiggal
3. Konfig frissítése a valódi loggerrel
4. Storage inicializálása

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
config_value = core.config.get("database.host")
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
Config → Logger → Storage
   ↑         ↓        ↓
   └─────────┴────────┘
```

## Publikus API

A modul a következő elemeket exportálja:

```python
__all__ = [
    "CoreComponents",
    "bootstrap_core", 
    "get_core_components",
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

### Tesztelés

```python
from neural_ai.core import CoreComponents
from unittest.mock import Mock

# Mock objektumokkal
mock_config = Mock()
mock_logger = Mock()
mock_storage = Mock()

components = CoreComponents(
    config=mock_config,
    logger=mock_logger,
    storage=mock_storage
)
```

## Fejlesztési Szempontok

### Típusbiztonság

- Minden függvény és metódus típusozott
- `TYPE_CHECKING` blokkok használata a körkörös importok elkerülésére
- Nincs `Any` típus használat

### Dokumentáció

- Minden osztály és függvény magyar nyelvű docstringgel rendelkezik
- Google style docstring formátum
- Példakódok a dokumentációban

### Tesztelés

- 100% tesztlefedettség kötelező
- Mock objektumok használata a függőségek teszteléséhez
- Unit és integrációs tesztek

## Kapcsolódó Dokumentáció

- [Core Függőségi Analízis](../development/core_dependencies.md)
- [Konfiguráció Kezelés](./config/__init__.md)
- [Logger Rendszer](./logger/__init__.md)
- [Tárhely Kezelés](./storage/__init__.md)

## Verzió Történet

- **v1.0**: Alapvető core inicializálás és függőségi injektálás implementálva
- **v1.1**: Bootstrap folyamat és szingleton pattern hozzáadva
- **v2.0**: Teljes refaktorálás TYPE_CHECKING és DI használatával