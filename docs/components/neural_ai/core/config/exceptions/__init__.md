# Config Kivételek Modul

## Áttekintés

Kivételek a konfigurációkezelő modulhoz.

Ez a modul exportálja az összes konfigurációkezelési kivétel osztályt.

## Exportált Kivétel Osztályok

- [`ConfigError`](config_error.md#configerror): Alap konfigurációs kivétel osztály
- [`ConfigLoadError`](config_error.md#configloaderror): Konfiguráció betöltési hiba
- [`ConfigSaveError`](config_error.md#configsaveerror): Konfiguráció mentési hiba
- [`ConfigValidationError`](config_error.md#configvalidationerror): Konfiguráció validációs hiba
- [`ConfigTypeError`](config_error.md#configtypeerror): Típus hiba a konfigurációban
- [`ConfigKeyError`](config_error.md#configkeyerror): Kulcs hiba a konfigurációban

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

### Alap kivétel kezelés

```python
from neural_ai.core.config.exceptions import ConfigError, ConfigLoadError

try:
    config_manager.load("config.yml")
except ConfigLoadError as e:
    print(f"Betöltési hiba: {e}")
    print(f"Fájl: {e.file_path}")
except ConfigError as e:
    print(f"Általános konfigurációs hiba: {e}")
```

### Validációs hiba kezelése

```python
from neural_ai.core.config.exceptions import ConfigValidationError

try:
    is_valid, errors = config_manager.validate(schema)
    if not is_valid:
        raise ConfigValidationError(
            "Érvénytelen konfiguráció",
            field_path="database.port",
            invalid_value=-1
        )
except ConfigValidationError as e:
    print(f"Validációs hiba: {e}")
    print(f"Mező: {e.field_path}")
    print(f"Érvénytelen érték: {e.invalid_value}")
```

### Típus hiba kezelése

```python
from neural_ai.core.config.exceptions import ConfigTypeError

try:
    port = config_manager.get("database", "port")
    if not isinstance(port, int):
        raise ConfigTypeError(
            "A portnak egész számnak kell lennie",
            field_path="database.port",
            expected_type="int",
            actual_type=type(port).__name__
        )
except ConfigTypeError as e:
    print(f"Típushiba: {e}")
    print(f"Várt típus: {e.expected_type}")
    print(f"Kapott típus: {e.actual_type}")
```

## Kapcsolódó Dokumentáció

- [Config Error](config_error.md): Az összes kivétel osztály részletes leírása
- [Config Modul](../__init__.md)