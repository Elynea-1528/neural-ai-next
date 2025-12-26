# Component Bundle Implementáció

## Áttekintés

Core komponensek gyűjtemény.

## Osztályok

### `LazyLoader[T]`

Drága erőforrások lusta betöltője.

#### Metódusok

##### `__init__(loader_func)`

Lustabetöltő inicializálása.

**Paraméterek:**
- `loader_func`: A függvény, amely az erőforrás betöltését végzi.

##### `_load()`

Betölti az erőforrást, ha még nincs betöltve.

**Visszatérési érték:**
- `T`: A betöltött erőforrás.

##### `__call__()`

Visszaadja a betöltött erőforrást.

**Visszatérési érték:**
- `T`: A betöltött erőforrás.

##### `is_loaded` property

Ellenőrzi, hogy az erőforrás betöltődött-e.

**Visszatérési érték:**
- `bool`: True, ha az erőforrás betöltve van, különben False.

##### `reset()`

Visszaállítja a betöltőt, hogy kirakja az erőforrást.

Ez a metódus visszaállítja a betöltő állapotát, lehetővé téve az erőforrás újbóli betöltését.

### `CoreComponents`

Alap komponensek lusta betöltéssel.

#### Metódusok

##### `__init__(container)`

Alap komponensek inicializálása.

**Paraméterek:**
- `container`: Egy függőséginjektáló konténer példány. Ha nincs megadva, új konténert hoz létre.

##### `config` property

Konfiguráció kezelő komponens lekérése.

**Visszatérési érték:**
- `ConfigManagerInterface | None`: A konfiguráció kezelő példánya, vagy None ha nincs regisztrálva.

##### `logger` property

Naplózó komponens lekérése.

**Visszatérési érték:**
- `LoggerInterface | None`: A naplózó példánya, vagy None ha nincs regisztrálva.

##### `storage` property

Tároló komponens lekérése.

**Visszatérési érték:**
- `StorageInterface | None`: A tároló példánya, vagy None ha nincs regisztrálva.

##### `database` property

Adatbázis komponens lekérése.

**Visszatérési érték:**
- `DatabaseManager | None`: Az adatbázis példánya, vagy None ha nincs regisztrálva.

##### `event_bus` property

Esemény busz komponens lekérése.

**Visszatérési érték:**
- `EventBus | None`: Az esemény busz példánya, vagy None ha nincs regisztrálva.

##### `hardware` property

Hardver információ komponens lekérése.

**Visszatérési érték:**
- `HardwareInfo | None`: A hardver információ példánya, vagy None ha nincs regisztrálva.

##### `set_config(config)`

Beállítja a konfiguráció komponenst (csak teszteléshez).

**Paraméterek:**
- `config`: A konfiguráció kezelő implementáció példánya.

##### `set_logger(logger)`

Beállítja a naplózó komponenst (csak teszteléshez).

**Paraméterek:**
- `logger`: A naplózó implementáció példánya.

##### `set_storage(storage)`

Beállítja a tároló komponenst (csak teszteléshez).

**Paraméterek:**
- `storage`: A tároló implementáció példánya.

##### `set_database(database)`

Beállítja az adatbázis komponenst (csak teszteléshez).

**Paraméterek:**
- `database`: Az adatbázis implementáció példánya.

##### `set_event_bus(event_bus)`

Beállítja az esemény busz komponenst (csak teszteléshez).

**Paraméterek:**
- `event_bus`: Az esemény busz implementáció példánya.

##### `set_hardware(hardware)`

Beállítja a hardver információ komponenst (csak teszteléshez).

**Paraméterek:**
- `hardware`: A hardver információ implementáció példánya.

##### `has_config()`

Ellenőrzi, hogy van-e config komponens.

**Visszatérési érték:**
- `bool`: True ha van config komponens, False ha nincs

##### `has_logger()`

Ellenőrzi, hogy van-e logger komponens.

**Visszatérési érték:**
- `bool`: True ha van logger komponens, False ha nincs

##### `has_storage()`

Ellenőrzi, hogy van-e storage komponens.

**Visszatérési érték:**
- `bool`: True ha van storage komponens, False ha nincs

##### `has_database()`

Ellenőrzi, hogy van-e database komponens.

**Visszatérési érték:**
- `bool`: True ha van database komponens, False ha nincs

##### `has_event_bus()`

Ellenőrzi, hogy van-e event_bus komponens.

**Visszatérési érték:**
- `bool`: True ha van event_bus komponens, False ha nincs

##### `has_hardware()`

Ellenőrzi, hogy van-e hardware komponens.

**Visszatérési érték:**
- `bool`: True ha van hardware komponens, False ha nincs

##### `validate()`

Ellenőrzi, hogy minden szükséges komponens megvan-e.

**Visszatérési érték:**
- `bool`: True ha minden komponens megvan, False ha valamelyik hiányzik

## Használati Példák

### Alap komponensek létrehozása

```python
from neural_ai.core.base.implementations.component_bundle import CoreComponents
from neural_ai.core.base.implementations.di_container import DIContainer

# Konténer létrehozása
container = DIContainer()

# Core komponensek létrehozása
components = CoreComponents(container=container)

# Komponensek használata
if components.has_logger():
    logger = components.logger
    logger.info("Alkalmazás elindult")
```

### Komponensek beállítása teszteléshez

```python
from neural_ai.core.logger.implementations import DefaultLogger
from neural_ai.core.config.implementations import YamlConfigManager

# Teszt komponensek létrehozása
test_logger = DefaultLogger(name="test")
test_config = YamlConfigManager("test_config.yml")

# Komponensek beállítása
components = CoreComponents()
components.set_logger(test_logger)
components.set_config(test_config)

# Ellenőrzés
assert components.has_logger()
assert components.has_config()
assert components.validate()
```

## Kapcsolódó Dokumentáció

- [CoreComponentFactory](../factory.md)
- [DIContainer](di_container.md)
- [LazyLoader](lazy_loader.md)
- [Base Modul](../__init__.md)