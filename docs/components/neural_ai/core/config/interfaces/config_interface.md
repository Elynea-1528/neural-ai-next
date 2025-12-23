# ConfigManagerInterface

## Áttekintés

A `ConfigManagerInterface` egy absztrakt interfész, amely definiálja a konfigurációkezelők által implementálandó metódusokat. Ez az interfész biztosítja a konzisztens viselkedést a különböző konfigurációs implementációk között.

## Verziókezelés

- **Jelenlegi verzió:** 1.0.0
- **Séma verzió:** `schema_version` mező a konfigurációban
- **Kompatibilitás:** A verziókezelés biztosítja a konfigurációs séma kompatibilitását

## Osztály

```python
class ConfigManagerInterface(ABC)
```

## Metódusok

### `__init__`

```python
def __init__(self, filename: str | None = None) -> None
```

Inicializálja a konfigurációkezelőt.

**Paraméterek:**
- `filename` (str | None, opcionális): Konfigurációs fájl útvonala. Alapértelmezett: None

**Visszatérési érték:**
- `None`

---

### `get`

```python
def get(self, *keys: str, default: Any = None) -> Any
```

Érték lekérése a konfigurációból.

**Paraméterek:**
- `*keys` (str): Kulcsok sorozata a beágyazott konfigurációk eléréséhez
- `default` (Any, opcionális): Alapértelmezett érték, ha a kulcs nem létezik. Alapértelmezett: None

**Visszatérési érték:**
- `Any`: A lekérdezett érték vagy az alapértelmezett érték

---

### `get_section`

```python
def get_section(self, section: str) -> dict[str, Any]
```

Teljes konfigurációs szekció lekérése.

**Paraméterek:**
- `section` (str): A szekció neve

**Visszatérési érték:**
- `dict[str, Any]`: A szekció teljes tartalma

---

### `set`

```python
def set(self, *keys: str, value: Any) -> None
```

Érték beállítása a konfigurációban.

**Paraméterek:**
- `*keys` (str): Kulcsok sorozata a beágyazott konfigurációk eléréséhez
- `value` (Any): A beállítandó érték

**Visszatérési érték:**
- `None`

---

### `save`

```python
def save(self, filename: str | None = None) -> None
```

Konfiguráció mentése fájlba.

**Paraméterek:**
- `filename` (str | None, opcionális): A mentés helye. Ha None, az aktuális fájlnevet használja. Alapértelmezett: None

**Visszatérési érték:**
- `None`

---

### `load`

```python
def load(self, filename: str) -> None
```

Konfiguráció betöltése fájlból.

**Paraméterek:**
- `filename` (str): A betöltendő fájl útvonala

**Visszatérési érték:**
- `None`

---

### `validate`

```python
def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]
```

Konfiguráció validálása séma alapján.

**Paraméterek:**
- `schema` (dict[str, Any]): A validáláshoz használt séma

**Visszatérési érték:**
- `tuple[bool, dict[str, str] | None]`: 
  - `bool`: Igaz, ha a konfiguráció érvényes
  - `dict[str, str] | None`: Hibák szótára vagy None, ha nincs hiba

---

## Használati példa

```python
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager

# Interfész használata
config_manager: ConfigManagerInterface = YAMLConfigManager("config.yaml")

# Érték lekérése
value = config_manager.get("database", "host", default="localhost")

# Érték beállítása
config_manager.set("database", "port", value=5432)

# Konfiguráció mentése
config_manager.save()

# Validálás
schema = {
    "database": {
        "host": {"type": "str", "required": True},
        "port": {"type": "int", "min": 1, "max": 65535}
    }
}
is_valid, errors = config_manager.validate(schema)
```

## Implementációk

- [`YAMLConfigManager`](../implementations/yaml_config_manager.md): YAML fájl alapú konfigurációkezelő

## Függőségek

Ez az interfész nem rendelkezik külső függőségekkel, mivel egy tiszta interfész definíció. Az implementációk használhatnak logger vagy storage komponenseket a `core_dependencies.md`-ben leírtak szerint.

## Lásd még

- [Core Dependencies](../../../development/core_dependencies.md)
- [Config Implementations](../implementations/)