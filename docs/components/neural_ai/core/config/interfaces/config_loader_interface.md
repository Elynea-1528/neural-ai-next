# IConfigLoader Interface

**Modul:** [`neural_ai.core.config.interfaces.config_loader_interface`](neural_ai/core/config/interfaces/config_loader_interface.py:1)

**Felelősség:** Konfiguráció betöltő interfész SOPS és plain YAML fájlokhoz.

## Áttekintés

Az [`IConfigLoader`](neural_ai/core/config/interfaces/config_loader_interface.py:13) interfész definiálja a titkosított (SOPS) és titkosítatlan YAML konfigurációk egységes betöltésének contract-ját. Ez az interfész biztosítja, hogy minden konfiguráció betöltő implementáció konzisztens API-t nyújtson.

## Metódusok

### `load(config_dir: str) -> dict[str, Any]`

**Definíció:** [`IConfigLoader.load()`](neural_ai/core/config/interfaces/config_loader_interface.py:21)

Betölti az összes config fájlt egy könyvtárból namespace struktúrába.

**Args:**
- `config_dir` (str): Konfiguráció könyvtár útvonala

**Returns:**
- `dict[str, Any]`: Egyesített konfiguráció dictionary (namespace struktúra)

**Raises:**
- [`ConfigLoadError`](neural_ai/core/config/exceptions/config_error.py:31): Ha a könyvtár nem található
- [`SOPSDecryptError`](neural_ai/core/config/exceptions/config_error.py:173): Ha a SOPS dekódolás sikertelen

**Példa:**
```python
loader = ConfigLoaderFactory.create_loader()
config_dict = loader.load("configs/")
# {"database": {...}, "secrets": {...}, "logging": {...}}
```

---

### `load_file(file_path: str) -> dict[str, Any]`

**Definíció:** [`IConfigLoader.load_file()`](neural_ai/core/config/interfaces/config_loader_interface.py:39)

Betölt egyetlen config fájlt (SOPS vagy plain YAML).

**Args:**
- `file_path` (str): Fájl útvonala (`.yaml` vagy `.yaml.sops`)

**Returns:**
- `dict[str, Any]`: Fájl tartalma dictionary formában

**Raises:**
- [`ConfigLoadError`](neural_ai/core/config/exceptions/config_error.py:31): Ha fájl nem található
- [`SOPSDecryptError`](neural_ai/core/config/exceptions/config_error.py:173): Ha SOPS fájl dekódolása sikertelen

**Példa:**
```python
loader = ConfigLoaderFactory.create_loader()
secrets = loader.load_file("configs/secrets.yaml.sops")
# {"api_key": "...", "db_password": "..."}
```

---

## Implementációk

- [`ConfigLoader`](neural_ai/core/config/implementations/config_loader.py:25) - Alap implementáció SOPS támogatással

---

## Használati Forgatókönyvek

### 1. Bootstrap konfiguráció betöltés
A [`bootstrap_core()`](neural_ai/core/__init__.py:74) függvényben használatos a rendszer inicializációkor.

### 2. Dinamikus konfiguráció reload
Futásidejű config frissítés támogatása.

### 3. Teszt környezetek
Mock konfigurációk betöltése unit és integration tesztekben.

---

## Architektúra Szabályok

- ✅ **DDD Pattern:** Interface publikus, implementáció rejtett
- ✅ **Factory Pattern:** [`ConfigLoaderFactory.create_loader()`](neural_ai/core/config/factory.py:351) használat kötelező
- ✅ **SOPS Support:** Titkosított fájlok automatikus dekódolása
- ✅ **Dependency Injection:** Logger injektálás constructor-on keresztül

---

## Kapcsolódó Komponensek

- [`ConfigLoaderFactory`](neural_ai/core/config/factory.py:327) - Loader példányosítás factory pattern-nel
- [`YAMLConfigManager`](neural_ai/core/config/implementations/yaml_config_manager.py:176) - Config manager integráció
- [`bootstrap_core()`](neural_ai/core/__init__.py:74) - Rendszer inicializáció
- [`ConfigLoadError`](neural_ai/core/config/exceptions/config_error.py:31) - Betöltési hibák
- [`SOPSDecryptError`](neural_ai/core/config/exceptions/config_error.py:173) - SOPS dekódolási hibák

---

## Namespace Struktúra

A [`load()`](neural_ai/core/config/interfaces/config_loader_interface.py:21) metódus fájlneveket használ kulcsként:

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

## SOPS Támogatás

### Támogatott Formátumok
- `.yaml` / `.yml` - Plain YAML
- `.yaml.sops` / `.yml.sops` - SOPS titkosított YAML

### Automatikus Detektálás
A kiterjesztés alapján automatikusan eldönti, hogy SOPS dekódolás szükséges-e.

---

## Típusrendszer

Az interfész szigorú típusozást alkalmaz:
- **Input:** `str` (útvonalak)
- **Output:** `dict[str, Any]` (YAML tartalom)
- **Exceptions:** Typed error hierarchy

**Típus ellenőrzés:** Mypy/Pyright kompatibilis, `Any` használat minimalizálva.
