# CoreComponents

## Áttekintés

A `CoreComponents` osztály az alap komponensek gyűjteménye lusta betöltéssel. Ez az osztály egy egységes interfészt biztosít a rendszer alap komponenseinek eléréséhez, és automatikusan kezeli a függőségeket a mögöttes DI konténer segítségével.

## Komponensek

Az osztály a következő komponenseket támogatja:

- **config**: Konfiguráció kezelő (`ConfigManagerInterface`)
- **logger**: Naplózó komponens (`LoggerInterface`)
- **storage**: Tároló komponens (`StorageInterface`)
- **database**: Adatbázis komponens (`DatabaseManager`)
- **event_bus**: Esemény busz (`EventBusInterface`)
- **hardware**: Hardver információ (`HardwareInterface`)

## Inicializálás

### Konténerrel

```python
from neural_ai.core.base.implementations.component_bundle import CoreComponents
from neural_ai.core.base.implementations.di_container import DIContainer

# Létező konténer használata
container = DIContainer()
components = CoreComponents(container)
```

### Konténer nélkül

```python
# Új konténer létrehozása automatikusan
components = CoreComponents()
```

## Komponens elérés

Minden komponens property-n keresztül érhető el, amely lusta betöltést használ:

```python
# Konfiguráció elérése
config = components.config
if config:
    value = config.get("key")

# Logger elérése
logger = components.logger
if logger:
    logger.info("Hello World")

# Storage elérése
storage = components.storage
if storage:
    storage.save_dataframe(df, "data.parquet")
```

## Komponens beállítás (teszteléshez)

A komponenseket manuálisan is be lehet állítani, főleg tesztelés céljából:

```python
from unittest.mock import MagicMock

# Mock komponensek létrehozása
mock_config = MagicMock()
mock_logger = MagicMock()
mock_storage = MagicMock()

# Komponensek beállítása
components.set_config(mock_config)
components.set_logger(mock_logger)
components.set_storage(mock_storage)
```

## Komponens ellenőrzés

### Egyéni ellenőrzés

```python
# Egyes komponensek ellenőrzése
has_config = components.has_config()  # True/False
has_logger = components.has_logger()
has_storage = components.has_storage()
# stb.
```

### Teljes validálás

```python
# Minden komponens ellenőrzése
is_valid = components.validate()  # True, ha minden komponens megvan
```

A `validate()` metódus ellenőrzi, hogy minden szükséges komponens (config, logger, storage, database, event_bus, hardware) elérhető-e.

## Példa: Teljes használat

```python
from neural_ai.core.base.implementations.component_bundle import CoreComponents
from neural_ai.core.base.factory import CoreComponentFactory
import tempfile

# Komponensek létrehozása
with tempfile.TemporaryDirectory() as temp_dir:
    components = CoreComponentFactory.create_components(
        config_path=f"{temp_dir}/config.yml",
        log_path=f"{temp_dir}/app.log",
        storage_path=f"{temp_dir}/storage"
    )

    # Komponensek használata
    if components.has_config():
        config = components.config
        app_name = config.get("app_name")

    if components.has_logger():
        logger = components.logger
        logger.info(f"Application started: {app_name}")

    if components.has_storage():
        storage = components.storage
        # Adatok mentése
        # storage.save_dataframe(df, "data.parquet")

    # Validálás
    if components.validate():
        print("All components are ready!")
    else:
        print("Some components are missing!")
```

## Függőség kezelés

A `CoreComponents` a mögöttes `DIContainer`-t használja a függőségek kezelésére. A komponensek property-ként vannak elérhetővé téve, és csak akkor töltődnek be, amikor először használják őket (lusta betöltés).

## Tesztelés

A modul tesztelése a `tests/core/base/implementations/test_component_bundle.py` fájlban található. A tesztek 100% statement coverage-t érnek el, és minden komponens lekérdezését, beállítását és validálását tesztelik.

### Teszt példa

```python
from neural_ai.core.base.implementations.component_bundle import CoreComponents
from unittest.mock import MagicMock

def test_component_access():
    components = CoreComponents()
    
    # Kezdetben nincs komponens
    assert components.config is None
    assert not components.has_config()
    
    # Komponens beállítása
    mock_config = MagicMock()
    components.set_config(mock_config)
    
    # Most már elérhető
    assert components.config is mock_config
    assert components.has_config()
```

## DI Konténer integráció

A `CoreComponents` osztály a `CoreComponentFactory`-vel együttműködve biztosítja a komponensek egységes létrehozását és kezelését. A factory a konténerbe regisztrálja a komponenseket, majd a `CoreComponents` ezeket lusta betöltéssel éri el.

Ez a megoldás lehetővé teszi:

1. **Modularitást**: Minden komponens függetlenül fejleszthető és tesztelhető.
2. **Lusta betöltést**: A drága erőforrások csak akkor töltődnek be, amikor szükség van rájuk.
3. **DI-t**: A függőségek injektálhatók, ami tesztelhetőséget biztosít.
4. **Egységes interfészt**: Minden komponens ugyanúgy érhető el property-n keresztül.