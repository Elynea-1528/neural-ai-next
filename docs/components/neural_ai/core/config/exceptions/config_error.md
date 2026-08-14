# neural_ai/core/config/exceptions/config_error.py

Kivételek a konfigurációkezelő modulhoz.

Ez a modul definiálja a konfigurációkezelés során fellépő összes kivételt.
A kivételek hierarchikusan vannak szervezve, a ConfigError alaposztállyal
a gyökéren.

## Osztály: `ConfigError(Exception)`

Alap kivétel a konfigurációkezelő hibákhoz.

Ez az osztály szolgál közös alapként az összes konfigurációval
kapcsolatos kivételnek a rendszerben.

Attributes:
    message: A hibaüzenet részletes leírása.
    error_code: Opcionális hibakód a hibák kategorizálásához.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, error_code: str | None = None) -> None
```

Inicializálja a ConfigError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet részletes leírása.
- **`error_code`** (`str | None`) = `None`: Opcionális hibakód a hibák kategorizálásához.

**Visszatérési érték:**

- Típus: `None`

## Osztály: `ConfigLoadError(ConfigError)`

Konfiguráció betöltési hiba.

Akkor dobódik, ha a konfigurációs fájl betöltése sikertelen.
Ez tartalmazhat fájl nem található, olvasási hiba vagy formátum
hiba esetét is.

Attributes:
    file_path: Az érintett konfigurációs fájl elérési útja.
    original_error: Az eredeti kivétel, ami a hibát okozta.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, file_path: str | None = None, original_error: Exception | None = None) -> None
```

Inicializálja a ConfigLoadError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet részletes leírása.
- **`file_path`** (`str | None`) = `None`: Az érintett konfigurációs fájl elérési útja.
- **`original_error`** (`Exception | None`) = `None`: Az eredeti kivétel, ami a hibát okozta.

**Visszatérési érték:**

- Típus: `None`

## Osztály: `ConfigSaveError(ConfigError)`

Konfiguráció mentési hiba.

Akkor dobódik, ha a konfiguráció mentése sikertelen.
Ez tartalmazhat írási jogosultság hiányát, lemezterület hiányt
vagy egyéb I/O hibákat.

Attributes:
    file_path: A cél konfigurációs fájl elérési útja.
    original_error: Az eredeti kivétel, ami a hibát okozta.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, file_path: str | None = None, original_error: Exception | None = None) -> None
```

Inicializálja a ConfigSaveError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet részletes leírása.
- **`file_path`** (`str | None`) = `None`: A cél konfigurációs fájl elérési útja.
- **`original_error`** (`Exception | None`) = `None`: Az eredeti kivétel, ami a hibát okozta.

**Visszatérési érték:**

- Típus: `None`

## Osztály: `ConfigValidationError(ConfigError)`

Konfiguráció validációs hiba.

Akkor dobódik, ha a konfigurációs adatok érvénytelenek vagy
nem felelnek meg a várt sémának. Ez tartalmazhatja a kötelező
mezők hiányát, érvénytelen értékeket vagy típus eltéréseket.

Attributes:
    field_path: Az érintett konfigurációs mező elérési útja.
    invalid_value: Az érvénytelen érték, ami a hibát okozta.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, field_path: str | None = None, invalid_value: object | None = None) -> None
```

Inicializálja a ConfigValidationError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet részletes leírása.
- **`field_path`** (`str | None`) = `None`: Az érintett konfigurációs mező elérési útja.
- **`invalid_value`** (`object | None`) = `None`: Az érvénytelen érték, ami a hibát okozta.

**Visszatérési érték:**

- Típus: `None`

## Osztály: `ConfigTypeError(ConfigError)`

Típus hiba a konfigurációban.

Akkor dobódik, ha egy konfigurációs érték típusa nem megfelelő.
Ez specifikusabb, mint a ConfigValidationError, mivel kizárólag
a típus hibákra koncentrál.

Attributes:
    field_path: Az érintett konfigurációs mező elérési útja.
    expected_type: A várt típus neve.
    actual_type: A tényleges típus neve.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, field_path: str | None = None, expected_type: str | None = None, actual_type: str | None = None) -> None
```

Inicializálja a ConfigTypeError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet részletes leírása.
- **`field_path`** (`str | None`) = `None`: Az érintett konfigurációs mező elérési útja.
- **`expected_type`** (`str | None`) = `None`: A várt típus neve.
- **`actual_type`** (`str | None`) = `None`: A tényleges típus neve.

**Visszatérési érték:**

- Típus: `None`

## Osztály: `ConfigKeyError(ConfigError)`

Kulcs hiba a konfigurációban.

Akkor dobódik, ha egy konfigurációs kulcs nem található vagy
érvénytelen. Ez hasonlít a Python KeyError kivételéhez, de
specifikusan a konfigurációkra van szabva.

Attributes:
    key_path: A hiányzó vagy érvénytelen kulcs elérési útja.
    available_keys: A rendelkezésre álló kulcsok listája.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, key_path: str | None = None, available_keys: list[str] | None = None) -> None
```

Inicializálja a ConfigKeyError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet részletes leírása.
- **`key_path`** (`str | None`) = `None`: A hiányzó vagy érvénytelen kulcs elérési útja.
- **`available_keys`** (`list[str] | None`) = `None`: A rendelkezésre álló kulcsok listája.

**Visszatérési érték:**

- Típus: `None`

## Osztály: `SOPSDecryptError(ConfigLoadError)`

SOPS dekódolási hiba.

Akkor dobódik, ha a SOPS titkosított fájl dekódolása sikertelen.
Ez tartalmazhatja a SOPS binary hiányát, dekódolási hibákat vagy
érvénytelen SOPS fájl formátumot.

Attributes:
    file_path: A SOPS fájl elérési útja.
    sops_command: A futtatott SOPS parancs (debug célokra).
    exit_code: A SOPS parancs kilépési kódja.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, file_path: str | None = None, sops_command: str | None = None, exit_code: int | None = None) -> None
```

Inicializálja a SOPSDecryptError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet részletes leírása.
- **`file_path`** (`str | None`) = `None`: A SOPS fájl elérési útja.
- **`sops_command`** (`str | None`) = `None`: A futtatott SOPS parancs.
- **`exit_code`** (`int | None`) = `None`: A SOPS parancs kilépési kódja.

**Visszatérési érték:**

- Típus: `None`

**Példa használat:**

```python
try:
    loader.load_file("secrets.yaml.sops")
except SOPSDecryptError as e:
    print(f"Hiba: {e}")
    print(f"Fájl: {e.file_path}")
    print(f"Parancs: {e.sops_command}")
    print(f"Exit code: {e.exit_code}")
```

**SOPS Telepítési Útmutató:**

```bash
# Ubuntu/Debian
sudo apt install sops

# macOS
brew install sops

# Manual (Binary letöltés)
wget https://github.com/getsops/sops/releases/download/v3.8.1/sops-v3.8.1.linux.amd64
sudo mv sops-v3.8.1.linux.amd64 /usr/local/bin/sops
sudo chmod +x /usr/local/bin/sops
```

---

**Forrásfájl:** [`neural_ai/core/config/exceptions/config_error.py`](../../neural_ai/core/config/exceptions/config_error.py)
