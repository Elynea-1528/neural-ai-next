# ConfigLoader Implementation

**Modul:** [`neural_ai.core.config.implementations.config_loader`](neural_ai/core/config/implementations/config_loader.py:1)

**Felelősség:** SOPS titkosított és plain YAML fájlok betöltése.

## Áttekintés

A [`ConfigLoader`](neural_ai/core/config/implementations/config_loader.py:25) osztály implementálja az [`IConfigLoader`](neural_ai/core/config/interfaces/config_loader_interface.py:13) interfészt, és képes mind plain YAML, mind SOPS titkosított YAML fájlok betöltésére. A SOPS fájlokat a `sops -d` paranccsal dekódolja subprocess-en keresztül.

## Osztály Definíció

**Definíció:** [`ConfigLoader`](neural_ai/core/config/implementations/config_loader.py:25)

**Attributes:**
- `_logger` ([`LoggerInterface`](neural_ai/core/logger/interfaces/logger_interface.py:11) | None): Logger interfész (opcionális)
- `_sops_binary` (str): SOPS binary útvonala (default: "sops")

---

## Konstruktor

### `__init__(logger, sops_binary)`

**Definíció:** [`ConfigLoader.__init__()`](neural_ai/core/config/implementations/config_loader.py:57)

**Args:**
- `logger` ([`LoggerInterface`](neural_ai/core/logger/interfaces/logger_interface.py:11) | None): Logger interfész (opcionális)
- `sops_binary` (str): SOPS binary útvonala (default: "sops")

**Példa:**
```python
from neural_ai.core.config.factory import ConfigLoaderFactory
from neural_ai.core.logger.factory import LoggerFactory

# Alap használat
loader = ConfigLoaderFactory.create_loader()

# Custom SOPS binary
loader = ConfigLoaderFactory.create_loader(sops_binary="/usr/local/bin/sops")

# Logger-rel
logger = LoggerFactory.get_logger(__name__)
loader = ConfigLoaderFactory.create_loader(logger=logger)
```

---

## Publikus Metódusok

### `load_file(file_path: str) -> dict[str, Any]`

**Definíció:** [`ConfigLoader.load_file()`](neural_ai/core/config/implementations/config_loader.py:148)

Betölt egyetlen config fájlt (SOPS vagy plain YAML).

**Args:**
- `file_path` (str): Fájl útvonala (`.yaml` vagy `.yaml.sops`)

**Returns:**
- `dict[str, Any]`: Fájl tartalma dictionary formában

**Raises:**
- [`ConfigLoadError`](neural_ai/core/config/exceptions/config_error.py:31): Ha fájl nem található vagy betöltési hiba
- [`SOPSDecryptError`](neural_ai/core/config/exceptions/config_error.py:173): Ha SOPS dekódolás sikertelen

**Működés:**
1. Fájl létezés ellenőrzése
2. SOPS detektálás (`.yaml.sops` kiterjesztés)
3. Ha SOPS → [`_decrypt_sops_file()`](neural_ai/core/config/implementations/config_loader.py:91) hívás
4. Ha plain → `yaml.safe_load()` használat
5. Üres fájl kezelés (None → {})
6. Típus ellenőrzés (dict típus)

**Példa:**
```python
loader = ConfigLoaderFactory.create_loader()

# Plain YAML
config = loader.load_file("configs/database.yaml")
print(config["host"])  # "localhost"

# SOPS fájl
secrets = loader.load_file("configs/secrets.yaml.sops")
print(type(secrets))  # <class 'dict'>
```

---

### `load(config_dir: str) -> dict[str, Any]`

**Definíció:** [`ConfigLoader.load()`](neural_ai/core/config/implementations/config_loader.py:231)

Betölti az összes config fájlt egy könyvtárból namespace struktúrába.

**Args:**
- `config_dir` (str): Konfiguráció könyvtár útvonala

**Returns:**
- `dict[str, Any]`: Egyesített konfiguráció dictionary (namespace struktúra)

**Raises:**
- [`ConfigLoadError`](neural_ai/core/config/exceptions/config_error.py:31): Ha könyvtár nem található
- [`SOPSDecryptError`](neural_ai/core/config/exceptions/config_error.py:173): Ha SOPS dekódolás sikertelen

**Működés:**
1. Könyvtár létezés ellenőrzése
2. `.yaml`, `.yml`, `.yaml.sops`, `.yml.sops` fájlok listázása
3. Minden fájl → [`load_file()`](neural_ai/core/config/implementations/config_loader.py:148) hívás
4. Fájlnév → kulcs konverzió (kiterjesztés nélkül)
5. Namespace struktúra építés

**Példa:**
```python
loader = ConfigLoaderFactory.create_loader()
config = loader.load("configs/")

print(config.keys())
# dict_keys(['database', 'secrets', 'logging'])

print(config["database"]["host"])
# "localhost"
```

**Namespace Struktúra:**
```
configs/
├── database.yaml → {"database": {...}}
├── secrets.yaml.sops → {"secrets": {...}}
└── logging.yaml → {"logging": {...}}

Result: {
  "database": {...},
  "secrets": {...},
  "logging": {...}
}
```

---

## Privát Metódusok

### `_is_sops_file(file_path: str) -> bool`

**Definíció:** [`ConfigLoader._is_sops_file()`](neural_ai/core/config/implementations/config_loader.py:71)

Ellenőrzi, hogy SOPS fájlról van-e szó.

**Args:**
- `file_path` (str): Fájl útvonala

**Returns:**
- `bool`: True ha SOPS fájl, False egyébként

**Logika:**
```python
return file_path.endswith(".yaml.sops") or file_path.endswith(".yml.sops")
```

**Példa:**
```python
loader._is_sops_file("config.yaml.sops")  # True
loader._is_sops_file("config.yaml")       # False
```

---

### `_decrypt_sops_file(file_path: str) -> str`

**Definíció:** [`ConfigLoader._decrypt_sops_file()`](neural_ai/core/config/implementations/config_loader.py:91)

SOPS fájl dekódolása subprocess-el.

**Args:**
- `file_path` (str): SOPS fájl útvonala

**Returns:**
- `str`: Dekódolt YAML tartalom (string)

**Raises:**
- [`SOPSDecryptError`](neural_ai/core/config/exceptions/config_error.py:173): Ha dekódolás sikertelen

**Működés:**
1. `subprocess.run([self._sops_binary, "-d", file_path])` futtatás
2. `capture_output=True` → stdout/stderr rögzítés
3. `timeout=30` → 30 másodperc max
4. `check=True` → CalledProcessError ha nem nulla exit code

**Hibakezelés:**

| Hiba | Exception | Üzenet |
|:-----|:----------|:-------|
| `CalledProcessError` | [`SOPSDecryptError`](neural_ai/core/config/exceptions/config_error.py:173) | "SOPS dekódolás sikertelen: {stderr}" |
| `FileNotFoundError` | [`SOPSDecryptError`](neural_ai/core/config/exceptions/config_error.py:173) | "SOPS binary nem található: {sops_binary}" |
| `TimeoutExpired` | [`SOPSDecryptError`](neural_ai/core/config/exceptions/config_error.py:173) | "SOPS dekódolás timeout (30s): {file_path}" |

**Példa:**
```python
content = loader._decrypt_sops_file("secrets.yaml.sops")
print(type(content))  # <class 'str'>
```

---

## Technikai Részletek

### SOPS Dekódolás

**Parancs:** `sops -d <file_path>`

**Timeout:** 30 másodperc

**Követelmény:** A `sops` binárisnak telepítve kell lennie a rendszer PATH-jában.

**Támogatott fájl formátumok:**
- `.yaml.sops` - SOPS titkosított YAML
- `.yml.sops` - SOPS titkosított YML
- `.yaml` / `.yml` - Plain YAML

---

### Namespace Struktúra

A [`load()`](neural_ai/core/config/implementations/config_loader.py:231) metódus a fájlneveket használja kulcsként:

**Konverziós szabályok:**
- `database.yaml` → `"database"`
- `secrets.yaml.sops` → `"secrets"` (`.yaml.sops` eltávolítva)
- `logging.yml` → `"logging"`

**Implementáció:**
```python
key = Path(filename).stem  # "database.yaml.sops" → "database.yaml"
if key.endswith(".yaml"):
    key = key[:-5]  # "database.yaml" → "database"
```

---

## Hibakezelés

### 1. SOPS binary hiányzik

**Exception:** [`SOPSDecryptError`](neural_ai/core/config/exceptions/config_error.py:173)

**Üzenet:** "SOPS binary nem található: sops"

**Megoldás:** Telepítsd a SOPS-t: https://github.com/getsops/sops

```bash
# Ubuntu/Debian
sudo apt install sops

# macOS
brew install sops

# Binary letöltés
wget https://github.com/getsops/sops/releases/download/v3.8.1/sops-v3.8.1.linux.amd64
mv sops-v3.8.1.linux.amd64 /usr/local/bin/sops
chmod +x /usr/local/bin/sops
```

### 2. SOPS dekódolás sikertelen

**Exception:** [`SOPSDecryptError`](neural_ai/core/config/exceptions/config_error.py:173)

**Attribútumok:**
- `exit_code`: SOPS kilépési kód
- `sops_command`: Futtatott parancs
- `file_path`: SOPS fájl útvonala

**Példa:**
```python
try:
    loader.load_file("secrets.yaml.sops")
except SOPSDecryptError as e:
    print(f"SOPS hiba: {e}")
    print(f"Exit code: {e.exit_code}")
    print(f"Parancs: {e.sops_command}")
```

### 3. Fájl nem található

**Exception:** [`ConfigLoadError`](neural_ai/core/config/exceptions/config_error.py:31)

**Üzenet:** "Config fájl nem található: {file_path}"

### 4. Érvénytelen YAML

**Exception:** [`ConfigLoadError`](neural_ai/core/config/exceptions/config_error.py:31)

**Üzenet:** "Config fájl betöltése sikertelen: {yaml_error}"

---

## Teljesítmény

| Művelet | Idő | Megjegyzés |
|:--------|:----|:-----------|
| Plain YAML | ~1-5 ms / fájl | `yaml.safe_load()` overhead |
| SOPS dekódolás | ~50-200 ms / fájl | Subprocess overhead |
| Könyvtár betöltés | Szekvenciális | Párhuzamos verzió jövőbeli fejlesztés |

---

## Korlátok

1. **SOPS dependency:** A `sops` binárisnak telepítve kell lennie
2. **Timeout:** 30 sec max SOPS dekódoláshoz
3. **Sync only:** Aszinkron verzió nincs implementálva
4. **Szekvenciális:** Könyvtár betöltés nem párhuzamos

---

## Kapcsolódó Komponensek

- [`IConfigLoader`](neural_ai/core/config/interfaces/config_loader_interface.py:13) - Interface definíció
- [`ConfigLoaderFactory`](neural_ai/core/config/factory.py:327) - Factory pattern
- [`YAMLConfigManager.load_dict()`](neural_ai/core/config/implementations/yaml_config_manager.py:713) - Integration pont
- [`ConfigLoadError`](neural_ai/core/config/exceptions/config_error.py:31) - Betöltési hibák
- [`SOPSDecryptError`](neural_ai/core/config/exceptions/config_error.py:173) - SOPS dekódolási hibák

---

## Architektúra Szabályok

- ✅ **DDD Pattern:** Implementáció rejtett, csak factory-n keresztül elérhető
- ✅ **Interface Segregation:** [`IConfigLoader`](neural_ai/core/config/interfaces/config_loader_interface.py:13) implementáció
- ✅ **Dependency Injection:** Logger injektálás constructor-on keresztül
- ✅ **Error Handling:** Typed exceptions, exception chaining (`from e`)
- ✅ **Type Safety:** Strict typing, `cast()` használat
