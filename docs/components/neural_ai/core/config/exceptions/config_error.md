# Config Error Kivételek

## Áttekintés

Kivételek a konfigurációkezelő modulhoz.

Ez a modul definiálja a konfigurációkezelés során fellépő összes kivételt. A kivételek hierarchikusan vannak szervezve, a ConfigError alaposztállyal a gyökéren.

## Kivétel Osztályok

### `ConfigError`

Alap kivétel a konfigurációkezelő hibákhoz.

Ez az osztály szolgál közös alapként az összes konfigurációval kapcsolatos kivételnek a rendszerben.

#### Attribútumok

- `message`: A hibaüzenet részletes leírása.
- `error_code`: Opcionális hibakód a hibák kategorizálásához.

#### Metódusok

##### `__init__(message, error_code)`

Inicializálja a ConfigError kivételt.

**Paraméterek:**
- `message`: A hibaüzenet részletes leírása.
- `error_code`: Opcionális hibakód a hibák kategorizálásához.

### `ConfigLoadError`

Konfiguráció betöltési hiba.

Akkor dobódik, ha a konfigurációs fájl betöltése sikertelen. Ez tartalmazhat fájl nem található, olvasási hiba vagy formátum hiba esetét is.

#### Attribútumok

- `file_path`: Az érintett konfigurációs fájl elérési útja.
- `original_error`: Az eredeti kivétel, ami a hibát okozta.

#### Metódusok

##### `__init__(message, file_path, original_error)`

Inicializálja a ConfigLoadError kivételt.

**Paraméterek:**
- `message`: A hibaüzenet részletes leírása.
- `file_path`: Az érintett konfigurációs fájl elérési útja.
- `original_error`: Az eredeti kivétel, ami a hibát okozta.

### `ConfigSaveError`

Konfiguráció mentési hiba.

Akkor dobódik, ha a konfiguráció mentése sikertelen. Ez tartalmazhat írási jogosultság hiányát, lemezterület hiányt vagy egyéb I/O hibákat.

#### Attribútumok

- `file_path`: A cél konfigurációs fájl elérési útja.
- `original_error`: Az eredeti kivétel, ami a hibát okozta.

#### Metódusok

##### `__init__(message, file_path, original_error)`

Inicializálja a ConfigSaveError kivételt.

**Paraméterek:**
- `message`: A hibaüzenet részletes leírása.
- `file_path`: A cél konfigurációs fájl elérési útja.
- `original_error`: Az eredeti kivétel, ami a hibát okozta.

### `ConfigValidationError`

Konfiguráció validációs hiba.

Akkor dobódik, ha a konfigurációs adatok érvénytelenek vagy nem felelnek meg a várt sémának. Ez tartalmazhatja a kötelező mezők hiányát, érvénytelen értékeket vagy típus eltéréseket.

#### Attribútumok

- `field_path`: Az érintett konfigurációs mező elérési útja.
- `invalid_value`: Az érvénytelen érték, ami a hibát okozta.

#### Metódusok

##### `__init__(message, field_path, invalid_value)`

Inicializálja a ConfigValidationError kivételt.

**Paraméterek:**
- `message`: A hibaüzenet részletes leírása.
- `field_path`: Az érintett konfigurációs mező elérési útja.
- `invalid_value`: Az érvénytelen érték, ami a hibát okozta.

### `ConfigTypeError`

Típus hiba a konfigurációban.

Akkor dobódik, ha egy konfigurációs érték típusa nem megfelelő. Ez specifikusabb, mint a ConfigValidationError, mivel kizárólag a típus hibákra koncentrál.

#### Attribútumok

- `field_path`: Az érintett konfigurációs mező elérési útja.
- `expected_type`: A várt típus neve.
- `actual_type`: A tényleges típus neve.

#### Metódusok

##### `__init__(message, field_path, expected_type, actual_type)`

Inicializálja a ConfigTypeError kivételt.

**Paraméterek:**
- `message`: A hibaüzenet részletes leírása.
- `field_path`: Az érintett konfigurációs mező elérési útja.
- `expected_type`: A várt típus neve.
- `actual_type`: A tényleges típus neve.

### `ConfigKeyError`

Kulcs hiba a konfigurációban.

Akkor dobódik, ha egy konfigurációs kulcs nem található vagy érvénytelen. Ez hasonlít a Python KeyError kivételéhez, de specifikusan a konfigurációkra van szabva.

#### Attribútumok

- `key_path`: A hiányzó vagy érvénytelen kulcs elérési útja.
- `available_keys`: A rendelkezésre álló kulcsok listája.

#### Metódusok

##### `__init__(message, key_path, available_keys)`

Inicializálja a ConfigKeyError kivételt.

**Paraméterek:**
- `message`: A hibaüzenet részletes leírása.
- `key_path`: A hiányzó vagy érvénytelen kulcs elérési útja.
- `available_keys`: A rendelkezésre álló kulcsok listája.

## Kivétel Hierarchia

```
ConfigError
├── ConfigLoadError
├── ConfigSaveError
├── ConfigValidationError
├── ConfigTypeError
└── ConfigKeyError
```

## Használati Példák

### Fájl betöltési hiba kezelése

```python
from neural_ai.core.config.exceptions import ConfigLoadError

try:
    config_manager.load("nem_letezo_fajl.yml")
except ConfigLoadError as e:
    print(f"Hiba történt a fájl betöltésekor: {e}")
    print(f"Fájl elérési út: {e.file_path}")
    if e.original_error:
        print(f"Eredeti hiba: {e.original_error}")
```

### Validációs hiba létrehozása

```python
from neural_ai.core.config.exceptions import ConfigValidationError

def validate_database_config(config):
    port = config.get("database", "port")
    if port is None:
        raise ConfigValidationError(
            "Az adatbázis port kötelező mező",
            field_path="database.port",
            invalid_value=None
        )
    if port < 1 or port > 65535:
        raise ConfigValidationError(
            "Az adatbázis portnak 1 és 65535 között kell lennie",
            field_path="database.port",
            invalid_value=port
        )
```

### Típus hiba kezelése

```python
from neural_ai.core.config.exceptions import ConfigTypeError

def get_database_port(config):
    port = config.get("database", "port", default=5432)
    if not isinstance(port, int):
        raise ConfigTypeError(
            "Az adatbázis portnak egész számnak kell lennie",
            field_path="database.port",
            expected_type="int",
            actual_type=type(port).__name__
        )
    return port
```

### Kulcs hiba kezelése

```python
from neural_ai.core.config.exceptions import ConfigKeyError

def get_required_config(config, *keys):
    try:
        return config.get(*keys)
    except KeyError:
        available = list(config._config.keys())
        raise ConfigKeyError(
            f"A '{'.'.join(keys)}' kulcs nem található",
            key_path=".".join(keys),
            available_keys=available
        )
```

## Kapcsolódó Dokumentáció

- [Kivételek Modul](__init__.md)
- [Config Modul](../__init__.md)