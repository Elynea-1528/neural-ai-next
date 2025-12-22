# Kivételek - neural_ai.core.config.exceptions

## Áttekintés

Ez a modul definiálja a konfigurációkezelés során fellépő összes kivételt. A kivételek hierarchikusan vannak szervezve, a [`ConfigError`](#configerror) alaposztállyal a gyökéren, amelyből az összes többi specifikus kivétel származik.

## Kivétel Hierarchia

```
ConfigError (Exception)
├── ConfigLoadError
├── ConfigSaveError
├── ConfigValidationError
├── ConfigTypeError
└── ConfigKeyError
```

## Alap Kivételek

### ConfigError

Az összes konfigurációkezelő kivétel közös alaposztálya.

**Leírás:**
Ez az osztály szolgál közös alapként az összes konfigurációval kapcsolatos kivételnek a rendszerben. A kivételek hierarchiájának gyökerét képezi.

**Attribútumok:**
- `error_code`: Opcionális hibakód a hibák kategorizálásához.

**Használat:**
```python
from neural_ai.core.config.exceptions import ConfigError

try:
    # Valami konfigurációs művelet
    config.load("config.yaml")
except ConfigError as e:
    print(f"Konfigurációs hiba: {e}")
    if e.error_code:
        print(f"Hibakód: {e.error_code}")
```

## Betöltési Kivételek

### ConfigLoadError

Akkor dobódik, ha a konfigurációs fájl betöltése sikertelen.

**Leírás:**
Ez a kivétel a konfigurációs fájlok betöltése során fellépő hibákra használatos. Ez tartalmazhat fájl nem található, olvasási hiba vagy formátum hiba esetét is.

**Attribútumok:**
- `file_path`: Az érintett konfigurációs fájl elérési útja.
- `original_error`: Az eredeti kivétel, ami a hibát okozta.

**Használat:**
```python
from neural_ai.core.config.exceptions import ConfigLoadError

try:
    with open(config_file, "r") as f:
        config_data = yaml.safe_load(f)
except FileNotFoundError as e:
    raise ConfigLoadError(
        f"A konfigurációs fájl nem található: {config_file}",
        file_path=config_file,
        original_error=e
    )
except yaml.YAMLError as e:
    raise ConfigLoadError(
        f"Érvénytelen YAML formátum: {config_file}",
        file_path=config_file,
        original_error=e
    )
```

## Mentési Kivételek

### ConfigSaveError

Akkor dobódik, ha a konfiguráció mentése sikertelen.

**Leírás:**
Ez a kivétel a konfigurációk mentése során fellépő hibákra használatos. Ez tartalmazhat írási jogosultság hiányát, lemezterület hiányt vagy egyéb I/O hibákat.

**Attribútumok:**
- `file_path`: A cél konfigurációs fájl elérési útja.
- `original_error`: Az eredeti kivétel, ami a hibát okozta.

**Használat:**
```python
from neural_ai.core.config.exceptions import ConfigSaveError

try:
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)
except PermissionError as e:
    raise ConfigSaveError(
        f"Nincs írási jogosultság: {config_file}",
        file_path=config_file,
        original_error=e
    )
except OSError as e:
    raise ConfigSaveError(
        f"Lemezterület hiba: {config_file}",
        file_path=config_file,
        original_error=e
    )
```

## Validációs Kivételek

### ConfigValidationError

Akkor dobódik, ha a konfigurációs adatok érvénytelenek vagy nem felelnek meg a várt sémának.

**Leírás:**
Ez a kivétel a konfigurációs adatok validálása során fellépő problémákra használatos. Ez tartalmazhatja a kötelező mezők hiányát, érvénytelen értékeket vagy formátum eltéréseket.

**Attribútumok:**
- `field_path`: Az érintett konfigurációs mező elérési útja.
- `invalid_value`: Az érvénytelen érték, ami a hibát okozta.

**Használat:**
```python
from neural_ai.core.config.exceptions import ConfigValidationError

def validate_database_config(config: dict) -> None:
    if "database" not in config:
        raise ConfigValidationError(
            "Az adatbázis konfiguráció hiányzik",
            field_path="database"
        )
    
    db_config = config["database"]
    if "host" not in db_config:
        raise ConfigValidationError(
            "Az adatbázis hoszt hiányzik",
            field_path="database.host"
        )
    
    if not isinstance(db_config.get("port"), int):
        raise ConfigValidationError(
            "Az adatbázis portnak egész számnak kell lennie",
            field_path="database.port",
            invalid_value=db_config.get("port")
        )
```

## Típus Kivételek

### ConfigTypeError

Akkor dobódik, ha egy konfigurációs érték típusa nem megfelelő.

**Leírás:**
Ez a kivétel specifikusabb, mint a [`ConfigValidationError`](#configvalidationerror), mivel kizárólag a típus hibákra koncentrál. Akkor használatos, amikor egy konfigurációs érték típusa nem egyezik meg a várt típussal.

**Attribútumok:**
- `field_path`: Az érintett konfigurációs mező elérési útja.
- `expected_type`: A várt típus neve.
- `actual_type`: A tényleges típus neve.

**Használat:**
```python
from neural_ai.core.config.exceptions import ConfigTypeError

def validate_port_config(port_value: object) -> None:
    if not isinstance(port_value, int):
        raise ConfigTypeError(
            "A port értéknek egész számnak kell lennie",
            field_path="server.port",
            expected_type="int",
            actual_type=type(port_value).__name__
        )
    
    if not (1 <= port_value <= 65535):
        raise ConfigValidationError(
            "A port értéknek 1 és 65535 között kell lennie",
            field_path="server.port",
            invalid_value=port_value
        )
```

## Kulcs Kivételek

### ConfigKeyError

Akkor dobódik, ha egy konfigurációs kulcs nem található vagy érvénytelen.

**Leírás:**
Ez a kivétel hasonlít a Python `KeyError` kivételéhez, de specifikusan a konfigurációkra van szabva. Akkor használatos, amikor egy konfigurációs kulcs nem található a konfigurációban.

**Attribútumok:**
- `key_path`: A hiányzó vagy érvénytelen kulcs elérési útja.
- `available_keys`: A rendelkezésre álló kulcsok listája.

**Használat:**
```python
from neural_ai.core.config.exceptions import ConfigKeyError

def get_config_value(config: dict, key_path: str) -> object:
    keys = key_path.split(".")
    current = config
    
    try:
        for key in keys:
            current = current[key]
        return current
    except KeyError:
        available = list(config.keys())
        raise ConfigKeyError(
            f"A(z) '{key_path}' konfigurációs kulcs nem található",
            key_path=key_path,
            available_keys=available
        )
```

## Példák

### Példa 1: Alap kivétel kezelése

```python
from neural_ai.core.config.exceptions import (
    ConfigError,
    ConfigLoadError,
    ConfigValidationError
)

def load_and_validate_config(config_path: str) -> dict:
    try:
        # Konfiguráció betöltése
        config = load_config_file(config_path)
        
        # Konfiguráció validálása
        validate_config_schema(config)
        
        return config
        
    except ConfigLoadError as e:
        logger.error(f"Konfiguráció betöltési hiba: {e}")
        logger.error(f"Fájl: {e.file_path}")
        raise
        
    except ConfigValidationError as e:
        logger.error(f"Konfiguráció validációs hiba: {e}")
        logger.error(f"Mező: {e.field_path}")
        if e.invalid_value:
            logger.error(f"Érvénytelen érték: {e.invalid_value}")
        raise
        
    except ConfigError as e:
        logger.error(f"Egyéb konfigurációs hiba: {e}")
        raise
```

### Példa 2: Specifikus kivétel dobása

```python
from neural_ai.core.config.exceptions import (
    ConfigTypeError,
    ConfigKeyError
)

def process_server_config(config: dict) -> None:
    # Kulcs ellenőrzés
    if "server" not in config:
        raise ConfigKeyError(
            "A 'server' konfigurációs szakasz hiányzik",
            key_path="server",
            available_keys=list(config.keys())
        )
    
    server_config = config["server"]
    
    # Típus ellenőrzés
    if "port" in server_config:
        port = server_config["port"]
        if not isinstance(port, int):
            raise ConfigTypeError(
                "A port értéknek egész számnak kell lennie",
                field_path="server.port",
                expected_type="int",
                actual_type=type(port).__name__
            )
```

### Példa 3: Kivétel láncolat

```python
from neural_ai.core.config.exceptions import (
    ConfigLoadError,
    ConfigValidationError
)

def load_config_file(config_path: str) -> dict:
    try:
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)
            
        if config_data is None:
            raise ConfigValidationError(
                "A konfigurációs fájl üres",
                field_path=None
            )
            
        return config_data
        
    except FileNotFoundError as e:
        raise ConfigLoadError(
            f"A konfigurációs fájl nem található: {config_path}",
            file_path=config_path,
            original_error=e
        ) from e
        
    except yaml.YAMLError as e:
        raise ConfigLoadError(
            f"Érvénytelen YAML formátum: {config_path}",
            file_path=config_path,
            original_error=e
        ) from e
```

### Példa 4: Hibakódok használata

```python
from neural_ai.core.config.exceptions import (
    ConfigError,
    ConfigLoadError,
    ConfigSaveError
)

def handle_config_error(error: ConfigError) -> None:
    """Konfigurációs hibák kezelése hibakód alapján."""
    
    if error.error_code == "CONFIG_LOAD_ERROR":
        print("Betöltési hiba történt")
        if isinstance(error, ConfigLoadError) and error.file_path:
            print(f"Fájl: {error.file_path}")
            
    elif error.error_code == "CONFIG_SAVE_ERROR":
        print("Mentési hiba történt")
        if isinstance(error, ConfigSaveError) and error.file_path:
            print(f"Fájl: {error.file_path}")
            
    elif error.error_code == "CONFIG_VALIDATION_ERROR":
        print("Validációs hiba történt")
        
    else:
        print(f"Ismeretlen konfigurációs hiba: {error}")
```

## Függőségek

Ez a modul nem rendelkezik külső függőségekkel, csak a Python standard library-t használja. A típus hint-ekhez a `typing` modult használja.

## Tesztelés

A kivételek tesztelése a [`tests/core/config/test_exceptions.py`](../../../tests/core/config/test_exceptions.py) fájlban található. A tesztek lefedik:

- Minden kivétel osztály létrehozását és inicializálását
- Kivétel dobását és elkapását
- A kivétel hierarchia helyességét
- Öröklődési viszonyok ellenőrzését
- Attribútumok helyes beállítását
- Kivétel láncolatot

Teszt futtatása:
```bash
pytest tests/core/config/test_exceptions.py -v
```

Coverage ellenőrzés:
```bash
pytest tests/core/config/test_exceptions.py --cov=neural_ai.core.config.exceptions --cov-report=term-missing
```

## Kapcsolódó Dokumentáció

- [Fejlesztői útmutató](../../../development/implementation_guide.md)
- [Hibakezelés](../../../development/error_handling.md)
- [Konfigurációkezelő interfész](interfaces/config_interface.md)
- [YAML Konfigurációkezelő](implementations/yaml_config_manager.md)
- [Konfigurációkezelő gyár](implementations/config_manager_factory.md)