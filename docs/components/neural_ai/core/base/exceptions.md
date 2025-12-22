# Kivételek - neural_ai.core.base.exceptions

## Áttekintés

Ez a modul definiálja az összes kivétel alaposztályait és a specifikus kivételeket a Neural AI Next projekt különböző komponenseihez (tárolás, konfiguráció, hálózat, stb.).

## Kivétel Hierarchia

```
NeuralAIException
├── StorageException
│   ├── StorageWriteError
│   ├── StorageReadError
│   ├── StoragePermissionError
│   ├── InsufficientDiskSpaceError
│   └── PermissionDeniedError
├── ConfigurationError
├── DependencyError
├── SingletonViolationError
├── ComponentNotFoundError
└── NetworkException
    ├── TimeoutError
    └── ConnectionError
```

## Alap Kivételek

### NeuralAIException

Az összes Neural AI Next kivétel közös alaposztálya.

**Leírás:**
Ez az osztály szolgál közös alapként az összes egyéni kivételnek a rendszerben. A kivételek hierarchiájának gyökerét képezi.

**Használat:**
```python
from neural_ai.core.base.exceptions import NeuralAIException

try:
    # Valami művelet
    pass
except NeuralAIException as e:
    print(f"Hiba történt: {e}")
```

## Tárolási Kivételek

### StorageException

Alap kivétel a tárolással kapcsolatos hibákhoz.

**Leírás:**
Ez a kivétel a fájlrendszerrel, adattárolással és azokhoz kapcsolódó műveletekkel kapcsolatos problémákra használatos.

### StorageWriteError

Akkor dobódik, ha a fájlírási művelet sikertelen.

**Leírás:**
Ez a kivétel konkrétan a fájlok írásakor fellépő hibákra vonatkozik, például amikor a rendszer nem tud adatokat írni a célfájlba.

**Használat:**
```python
from neural_ai.core.base.exceptions import StorageWriteError

try:
    with open("fajl.txt", "w") as f:
        f.write(adat)
except IOError as e:
    raise StorageWriteError(f"Nem sikerült írni a fájlba: {e}")
```

### StorageReadError

Akkor dobódik, ha a fájlolvasási művelet sikertelen.

**Leírás:**
Ez a kivétel a fájlok olvasásakor fellépő hibákra vonatkozik, például amikor a fájl nem található vagy sérült az adatszerkezet.

### StoragePermissionError

Akkor dobódik, ha jogosultsági problémák merülnek fel.

**Leírás:**
Ez a kivétel akkor dobódik, amikor a rendszer nem rendelkezik a szükséges jogosultságokkal a tárolási művelet végrehajtásához.

### InsufficientDiskSpaceError

Akkor dobódik, ha nincs elég lemezterület.

**Leírás:**
Ez a kivétel akkor dobódik, amikor a rendszer nem rendelkezik elegendő szabad lemezterülettel egy tárolási művelet végrehajtásához.

### PermissionDeniedError

Akkor dobódik, ha a jogosultság megtagadva.

**Leírás:**
Ez a kivétel akkor dobódik, amikor a rendszer hozzáférési jogosultságot próbál megadni vagy ellenőrizni, de a műveletet megtagadják.

## Konfigurációs Kivételek

### ConfigurationError

Akkor dobódik, ha a konfiguráció érvénytelen vagy hiányos.

**Leírás:**
Ez a kivétel a konfigurációs fájlok feldolgozásakor vagy a beállítások validálásakor fellépő problémákra használatos.

**Használat:**
```python
from neural_ai.core.base.exceptions import ConfigurationError

def validate_config(config: dict) -> None:
    if "required_key" not in config:
        raise ConfigurationError("A kötelező konfigurációs kulcs hiányzik")
```

## Függőségi Kivételek

### DependencyError

Akkor dobódik, ha szükséges függőségek nem elérhetőek.

**Leírás:**
Ez a kivétel akkor dobódik, amikor a rendszer valamelyik külső függősége (csomag, modul, szolgáltatás) nem érhető el vagy nem megfelelő.

## Tervezési Minta Kivételek

### SingletonViolationError

Akkor dobódik, ha a singleton minta megsérül.

**Leírás:**
Ez a kivétel akkor dobódik, amikor egy singleton osztályból többször próbálnak példányt létrehozni, ami a tervezési minta megsértését jelenti.

### ComponentNotFoundError

Akkor dobódik, ha egy komponens nem található a konténerben.

**Leírás:**
Ez a kivétel akkor dobódik, amikor a DI konténer nem találja a kért komponenst a regisztrált szolgáltatások között.

## Hálózati Kivételek

### NetworkException

Alap kivétel a hálózati hibákhoz.

**Leírás:**
Ez a kivétel a hálózati kommunikációval kapcsolatos problémákra használatos, mint például a kapcsolódási hibák vagy az időtúllépések.

### TimeoutError

Akkor dobódik, ha egy művelet időtúllépést okoz.

**Leírás:**
Ez a kivétel akkor dobódik, amikor egy hálózati művelet nem fejeződik be a várt időn belül, és időtúllépés következik be.

### ConnectionError

Akkor dobódik, ha a kapcsolódás sikertelen.

**Leírás:**
Ez a kivétel akkor dobódik, amikor a rendszer nem tud kapcsolódni egy távoli szerverhez vagy szolgáltatáshoz.

## Példák

### Példa 1: Alap kivétel kezelése

```python
from neural_ai.core.base.exceptions import (
    NeuralAIException,
    StorageWriteError,
    ConfigurationError
)

def process_data(data: str, config: dict) -> None:
    try:
        # Konfiguráció ellenőrzése
        if not config.get("enabled", False):
            raise ConfigurationError("A feldolgozás nincs engedélyezve")
        
        # Adatok mentése
        save_to_file(data)
        
    except NeuralAIException as e:
        logger.error(f"Neural AI hiba: {e}")
        raise
```

### Példa 2: Specifikus kivétel dobása

```python
from neural_ai.core.base.exceptions import (
    StorageReadError,
    ComponentNotFoundError
)

def load_component(component_id: str) -> Any:
    try:
        component = container.get(component_id)
        return component
    except KeyError:
        raise ComponentNotFoundError(
            f"A(z) {component_id} komponens nem található"
        )
```

### Példa 3: Kivétel láncolat

```python
from neural_ai.core.base.exceptions import (
    StorageException,
    StorageWriteError
)

def write_data_to_file(filename: str, data: str) -> None:
    try:
        with open(filename, "w") as f:
            f.write(data)
    except IOError as e:
        raise StorageWriteError(
            f"Failed to write to {filename}: {e}"
        ) from e
```

## Függőségek

Ez a modul nem rendelkezik külső függőségekkel, csak a Python standard library-t használja.

## Tesztelés

A kivételek tesztelése a `tests/core/base/test_exceptions.py` fájlban található. A tesztek lefedik:

- Minden kivétel osztály létrehozását
- Kivétel dobását és elkapását
- A kivétel hierarchia helyességét
- Öröklődési viszonyok ellenőrzését

Teszt futtatása:
```bash
pytest tests/core/base/test_exceptions.py -v
```

## Kapcsolódó Dokumentáció

- [Fejlesztői útmutató](../../../development/implementation_guide.md)
- [Hibakezelés](../../../development/error_handling.md)
- [DI Konténer](container.md)