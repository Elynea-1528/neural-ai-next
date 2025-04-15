# Konfiguráció Kezelő Komponens

## Áttekintés

A Konfiguráció Kezelő komponens a Neural AI Next rendszer központi konfigurációkezelő rendszere. Lehetővé teszi a különböző konfigurációs fájlok betöltését, validálását és kezelését egységes interfészen keresztül.

## Főbb funkciók

- YAML formátumú konfigurációs fájlok kezelése
- Hierarchikus konfiguráció támogatás
- Típus-biztos konfigurációs értékek
- Séma alapú validáció
- Alapértelmezett értékek kezelése
- Konfigurációk mentése és betöltése

## Telepítés és beállítás

A komponens a Neural AI Next rendszer része, külön telepítést nem igényel. A PyYAML függőség szükséges:

```bash
pip install pyyaml
```

## Használat

### 1. Alap használat

```python
from neural_ai.core.config.implementations import ConfigManagerFactory

# YAML konfiguráció betöltése
config = ConfigManagerFactory.get_manager("configs/app.yaml")

# Érték lekérése
host = config.get("database", "host", default="localhost")
port = config.get("database", "port", default=5432)

# Teljes szekció lekérése
db_config = config.get_section("database")

# Érték beállítása
config.set("logging", "level", "DEBUG")
config.save()
```

### 2. Validáció

```python
# Validációs séma definiálása
schema = {
    "database": {
        "host": {"type": "str"},
        "port": {
            "type": "int",
            "min": 1,
            "max": 65535
        },
        "timeout": {
            "type": "int",
            "min": 0,
            "optional": True
        }
    },
    "logging": {
        "level": {
            "type": "str",
            "choices": ["DEBUG", "INFO", "WARNING", "ERROR"]
        }
    }
}

# Konfiguráció validálása
is_valid, errors = config.validate(schema)
if not is_valid:
    print("Konfigurációs hibák:", errors)
```

### 3. Hierarchikus konfiguráció

```yaml
# configs/app.yaml
database:
  primary:
    host: localhost
    port: 5432
    credentials:
      username: admin
      password: secret
  replica:
    host: replica.db
    port: 5432
    credentials:
      username: reader
      password: readonly

logging:
  level: INFO
  handlers:
    console:
      enabled: true
      colored: true
    file:
      enabled: true
      path: logs/app.log
```

```python
# Beágyazott értékek elérése
primary_host = config.get("database", "primary", "host")
replica_creds = config.get("database", "replica", "credentials")
```

## Példák

További példák az `examples/config_usage.py` fájlban találhatók.

## Hibaelhárítás

### Gyakori problémák és megoldások

1. YAML szintaxis hiba
   ```python
   try:
       config = ConfigManagerFactory.get_manager("config.yaml")
   except ValueError as e:
       print(f"YAML hiba: {e}")
   ```

2. Hiányzó kötelező mező
   ```python
   schema = {"required_field": {"type": "str"}}
   is_valid, errors = config.validate(schema)
   # errors: {"required_field": "Required field is missing"}
   ```

3. Érvénytelen érték
   ```python
   schema = {"port": {"type": "int", "min": 1, "max": 65535}}
   config.set("port", -1)
   is_valid, errors = config.validate(schema)
   # errors: {"port": "Value must be >= 1"}
   ```

## További információk

- [API Dokumentáció](api_reference.md)
- [Technikai specifikáció](technical_spec.md)
- [Fejlesztői útmutató](CONTRIBUTING.md)
- [Változási napló](CHANGELOG.md)