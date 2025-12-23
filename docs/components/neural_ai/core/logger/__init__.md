# Logger Komponens - Fő Inicializációs Modul

## Áttekintés

A `neural_ai.core.logger.__init__` modul a Neural-AI-Next rendszer naplózási komponensének központi exportmodulja. Ez a modul biztosítja a logger komponens összes fontos osztályának, interfészének és kivételének egységes elérését. Emellett dinamikus verziókezelést is biztosít a projekt verzióinformációinak és konfigurációs séma verziójának nyomon követéséhez.

## Szerepkör és Feladat

### Fő Célok

1. **Központi Export**: Egyetlen import pontot biztosít a logger komponens összes almoduljához
2. **Típusbiztonság**: TYPE_CHECKING blokkal ellátott importok a körkörös függőségek elkerüléséért
3. **Verziókezelés**: Dinamikus verzióinformációk betöltése és sémaverzió nyomon követése
4. **Modularitás**: Jól szervezett és bővíthető szerkezet

### Exportált Komponensek

#### Interfészek

- **`LoggerInterface`**: A logger implementációk alapinterfésze
- **`LoggerFactoryInterface`**: A logger factory-k alapinterfésze

#### Implementációk

- **`DefaultLogger`**: Alapértelmezett logger implementáció
- **`ColoredLogger`**: Színes kimenetű logger implementáció
- **`RotatingFileLogger`**: Forgató logfájl-kezelő implementáció
- **`LoggerFactory`**: Logger példányok létrehozásáért felelős factory

#### Verzióinformációk

- **`__version__`**: A projekt aktuális verziószáma (dinamikusan betöltve)
- **`__schema_version__`**: A konfigurációs séma verziószáma

#### Kivételek

- **`LoggerError`**: Általános logger hiba alaposztály
- **`LoggerConfigurationError`**: Konfigurációs hibák kivétele
- **`LoggerInitializationError`**: Inicializálási hibák kivétele

## Használat

### Alapvető Importálás

```python
from neural_ai.core.logger import LoggerFactory, DefaultLogger
from neural_ai.core.logger import LoggerInterface, LoggerError
```

### Példa Használat

```python
# Alap logger létrehozása
from neural_ai.core.logger import DefaultLogger

logger = DefaultLogger()
logger.info("Alkalmazás indítása...")
logger.error("Hiba történt a feldolgozás során")
```

```python
# Factory használata logger létrehozásához
from neural_ai.core.logger import LoggerFactory

factory = LoggerFactory()
logger = factory.create_logger(logger_type="default")
logger.debug("Hibakeresési információ")
```

```python
# Kivételkezelés
from neural_ai.core.logger import LoggerConfigurationError

try:
    # Logger konfigurációja
    pass
except LoggerConfigurationError as e:
    print(f"Konfigurációs hiba: {e}")
```

```python
# Verzióinformációk elérése
import neural_ai.core.logger

print(f"Logger verzió: {neural_ai.core.logger.__version__}")
print(f"Séma verzió: {neural_ai.core.logger.__schema_version__}")
```

## Technikai Döntések

### TYPE_CHECKING Blokk

A modul `TYPE_CHECKING` blokkot használ a típusellenőrzésekhez, hogy elkerülje a körkörös import problémákat:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces import LoggerInterface
    # ... egyéb típusdefiníciók
```

Ez biztosítja, hogy a típusellenőrző eszközök (mint a mypy) látják a típusokat, de a futási időben ne legyenek körkörös függőségek.

### Függőségi Injektálás

A logger komponensek függőségi injektálást használnak a konfiguráció és egyéb komponensek esetén:

```python
class DefaultLogger:
    def __init__(self, config: Optional[ConfigInterface] = None):
        self._config = config or DefaultConfig()
```

Ez lehetővé teszi a lazításos betöltést és a tesztelhetőséget.

### Verziókezelés

A modul dinamikusan tölti be a projekt verzióinformációit az `importlib.metadata` segítségével:

```python
from importlib import metadata

try:
    _version: str = metadata.version("neural-ai-next")
except metadata.PackageNotFoundError:
    _version = "1.0.0"  # Fallback verzió

__version__: Final[str] = _version
__schema_version__: Final[str] = "1.0"
```

Ez biztosítja, hogy a verziószám mindig szinkronban legyen a `pyproject.toml` fájllal, és lehetővé teszi a konfigurációs séma verzióellenőrzését a kompatibilitás érdekében.

## Kapcsolódó Komponensek

- **Interfészek**: [`neural_ai.core.logger.interfaces`](interfaces/__init__.md)
- **Implementációk**: [`neural_ai.core.logger.implementations`](implementations/__init__.md)
- **Kivételek**: [`neural_ai.core.logger.exceptions`](exceptions.md)
- **Formázók**: [`neural_ai.core.logger.formatters`](formatters/logger_formatters.md)

## Fejlesztési Jegyzetek

### Bővíthetőség

Új logger implementációk hozzáadásakor:

1. Implementáld a `LoggerInterface`-t
2. Add hozzá az implementációt az `implementations` mappához
3. Regisztráld az új implementációt a `LoggerFactory`-ban
4. Add hozzá az exportot ehhez az `__init__.py` fájlhoz

### Tesztelés

A modulhoz tartozó tesztek a `tests/core/logger/test___init__.py` fájlban találhatók. A tesztek ellenőrzik:

- Az összes exportált osztály és interfész importálhatóságát
- Az interfészek nem példányosíthatóságát
- A TYPE_CHECKING blokk helyes működését

### Linter Szabályok

- **Ruff**: 0 hiba szükséges
- **MyPy**: 0 hiba szükséges, szigorú típusellenőrzés
- **Pytest**: 100% coverage kötelező

## Hibaelhárítás

### Gyakori Hibák

1. **Körkörös Import**: Ha körkörös import hibát észlelsz, ellenőrizd, hogy minden típusimport a `TYPE_CHECKING` blokkban van-e
2. **Hiányzó Export**: Új komponens hozzáadásakor ne felejtsd el hozzáadni az `__all__` listához

### Debug mód

A logger komponensek támogatják a debug módot:

```python
logger = DefaultLogger(debug=True)
logger.set_level("DEBUG")
```

## Jövőbeli Fejlesztések

- [ ] Aszinkron logger implementációk
- [ ] Strukturált logging támogatás
- [ ] Metrikák integrációja
- [ ] Napló aggregáció és elemzés

## Lásd Még

- [Fejlesztői Dokumentáció](../../../../development/core_dependencies.md)
- [Logger Architektúra](overview.md)
- [Tesztelési Útmutató](../../../../development/implementation_guide.md)