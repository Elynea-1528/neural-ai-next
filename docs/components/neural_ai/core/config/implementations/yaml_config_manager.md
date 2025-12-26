# YAMLConfigManager

## Áttekintés

YAML alapú konfigurációkezelő implementáció.

## Adat Osztályok

### `ValidationContext`

Séma validációs kontextus.

Ez az osztály tartalmazza a validációs folyamat során szükséges adatokat.

#### Attribútumok

- `path`: Az aktuális validációs útvonal
- `errors`: A validációs hibák gyűjteménye
- `value`: Az ellenőrizendő érték
- `schema`: A validációs séma

## Osztályok

### `YAMLConfigManager`

YAML fájlokat kezelő konfigurációkezelő.

A konfigurációk mentésekor automatikusan hozzáadja a schema_version-t, és betöltéskor ellenőrzi a kompatibilitást.

#### Osztályszintű Attribútumok

- `_TYPE_MAP`: Típusleképezés a validációhoz
- `_CURRENT_SCHEMA_VERSION`: A jelenlegi séma verziója

#### Metódusok

##### `__init__(filename, logger, storage)`

Inicializálja a YAML konfigurációkezelőt.

**Paraméterek:**
- `filename`: Konfigurációs fájl útvonala (opcionális)
- `logger`: Logger interfész a naplózásra (opcionális)
- `storage`: Storage interfész a perzisztens tárolásra (opcionális)

##### `_get_current_schema_version()`

Visszaadja a jelenlegi séma verzióját.

**Visszatérési érték:**
- `str`: A jelenlegi séma verziója

##### `_check_schema_compatibility(loaded_version)`

Ellenőrzi a betöltött séma kompatibilitását.

**Paraméterek:**
- `loaded_version`: A betöltött konfiguráció séma verziója

**Visszatérési érték:**
- `bool`: True ha kompatibilis, False egyébként

##### `_ensure_dict(data)`

Adatok dictionary típusának biztosítása.

**Paraméterek:**
- `data`: Ellenőrizendő adatok

**Visszatérési érték:**
- `dict[str, Any]`: Az adatok dictionary formátumban

**Kivételek:**
- `ConfigLoadError`: Ha az adatok nem None és nem dictionary

##### `get(*keys, default)`

Érték lekérése a konfigurációból.

**Paraméterek:**
- `*keys`: A konfigurációs kulcsok hierarchiája
- `default`: Alapértelmezett érték, ha a kulcs nem található

**Visszatérési érték:**
- `Any`: A konfigurációs érték vagy az alapértelmezett érték

##### `get_section(section)`

Teljes konfigurációs szekció lekérése.

**Paraméterek:**
- `section`: A szekció neve

**Visszatérési érték:**
- `dict[str, Any]`: A szekció konfigurációs adatai

**Kivételek:**
- `KeyError`: Ha a szekció nem található

##### `set(*keys, value)`

Érték beállítása a konfigurációban.

**Paraméterek:**
- `*keys`: A konfigurációs kulcsok hierarchiája
- `value`: A beállítandó érték

**Kivételek:**
- `ValueError`: Ha nincs kulcs megadva vagy érvénytelen hierarchia

##### `save(filename)`

Aktuális konfiguráció mentése fájlba.

A konfiguráció mentésekor automatikusan hozzáadja a schema_version-t, hogy a jövőbeli betöltések kompatibilitást ellenőrizhessenek.

**Paraméterek:**
- `filename`: A mentési fájl neve (opcionális, alapértelmezett az eredeti fájlnév)

**Kivételek:**
- `ValueError`: Ha nincs fájlnév megadva vagy mentési hiba történik

##### `load(filename)`

Konfiguráció betöltése fájlból.

A betöltés során ellenőrzi a séma verzió kompatibilitást, ha a fájl tartalmaz verzióinformációt.

**Paraméterek:**
- `filename`: A betöltendő fájl neve

**Kivételek:**
- `ConfigLoadError`: Ha a fájl nem található vagy betöltési hiba történik

##### `validate(schema)`

Konfiguráció validálása séma alapján.

**Paraméterek:**
- `schema`: A validációs séma definíció

**Visszatérési érték:**
- `tuple[bool, dict[str, str] | None]`: (sikeres-e a validáció, hibák dictionary vagy None)

## Használati Példák

### Alap konfiguráció kezelés

```python
from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager

# Konfigurációkezelő létrehozása
config = YAMLConfigManager("config.yml")

# Érték lekérése
host = config.get("database", "host", default="localhost")
port = config.get("database", "port", default=5432)

# Érték beállítása
config.set("database", "host", "192.168.1.100")
config.set("database", "port", 5433)

# Konfiguráció mentése
config.save()
```

### Szekció kezelés

```python
# Teljes szekció lekérése
try:
    database_config = config.get_section("database")
    print(f"Host: {database_config.get('host')}")
    print(f"Port: {database_config.get('port')}")
except KeyError as e:
    print(f"Szekció nem található: {e}")
```

### Validáció használata

```python
# Validációs séma definiálása
schema = {
    "database": {
        "type": "dict",
        "schema": {
            "host": {"type": "str", "optional": False},
            "port": {"type": "int", "min": 1, "max": 65535, "optional": False},
            "username": {"type": "str", "optional": False},
            "password": {"type": "str", "optional": True}
        }
    },
    "logging": {
        "type": "dict",
        "schema": {
            "level": {"type": "str", "choices": ["DEBUG", "INFO", "WARNING", "ERROR"]},
            "file": {"type": "str", "optional": True}
        }
    }
}

# Validáció végrehajtása
is_valid, errors = config.validate(schema)
if not is_valid:
    print("Validációs hibák:")
    for path, error in errors.items():
        print(f"  {path}: {error}")
```

### Séma verzió kezelés

```python
# A konfiguráció automatikusan hozzáadja a séma verziót mentéskor
config.save("my_config.yml")

# Betöltéskor ellenőrzi a kompatibilitást
config.load("my_config.yml")
# Ha a verzió eltér, figyelmeztetést naplóz
```

## Séma Definíció

A validációs séma a következő mezőket támogatja:

- `type`: Az elvárt típus (`str`, `int`, `float`, `bool`, `list`, `dict`)
- `optional`: Ha True, a mező hiányában nem keletkezik hiba (alapértelmezett: False)
- `choices`: Az elfogadható értékek listája
- `min`: Minimális érték (számokhoz)
- `max`: Maximális érték (számokhoz)
- `schema`: Beágyazott séma definíció (dict típushoz)

## Kapcsolódó Dokumentáció

- [Config Implementációk Modul](__init__.md)
- [ConfigManagerInterface](../interfaces/config_interface.md)
- [Config Modul](../__init__.md)