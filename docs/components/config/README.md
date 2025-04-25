# Neural AI - Config Komponens

## Áttekintés

A Config komponens felelős a Neural AI Next rendszer konfigurációs beállításainak kezeléséért. Biztosítja a különböző formátumú konfigurációs fájlok betöltését, validálását és a dinamikus konfiguráció kezelést.

## Főbb funkciók

- YAML és JSON konfigurációs fájlok kezelése
- Hierarchikus konfigurációs struktúra
- Séma alapú validáció
- Típusbiztos hozzáférés
- Környezeti változók integrációja
- Dinamikus konfiguráció módosítás
- Automatikus újratöltés támogatása

## Telepítés és függőségek

A komponens a Neural AI keretrendszer részeként települ.

### Függőségek
- PyYAML: YAML fájlok kezelése
- jsonschema: Séma validáció (opcionális)

## Használat

### 1. Alap használat

```python
from neural_ai.core.config.implementations import ConfigManagerFactory

# Konfiguráció betöltése
config = ConfigManagerFactory.get_manager("config.yaml")

# Értékek lekérése
host = config.get("database.host", default="localhost")
port = config.get("database.port", default=5432)

# Érték beállítása
config.set("logging.level", "DEBUG")
```

### 2. Séma validáció

```python
# Validációs séma definiálása
schema = {
    "database": {
        "type": "dict",
        "schema": {
            "host": {"type": "str"},
            "port": {"type": "int", "min": 1024, "max": 65535},
            "credentials": {
                "type": "dict",
                "schema": {
                    "username": {"type": "str"},
                    "password": {"type": "str"}
                }
            }
        }
    }
}

# Konfiguráció validálása
config = ConfigManagerFactory.get_manager("config.yaml", schema=schema)
```

### 3. Környezeti változók

```python
# Környezeti változók prioritással
db_url = config.get(
    "database.url",
    env_key="DB_URL",
    default="postgresql://localhost/db"
)
```

## Architektúra

A komponens felépítése:

```
neural_ai/core/config/
├── interfaces/
│   ├── config_interface.py     # Alap interfész
│   └── factory_interface.py    # Factory interfész
├── implementations/
│   ├── yaml_config_manager.py  # YAML implementáció
│   └── config_manager_factory.py # Factory osztály
└── exceptions.py              # Kivétel osztályok
```

### Főbb osztályok

1. **ConfigManagerInterface**
   - Konfiguráció lekérés és módosítás
   - Séma validáció
   - Környezeti változók kezelése

2. **YAMLConfigManager**
   - YAML fájlok kezelése
   - Hierarchikus konfiguráció
   - Automatikus újratöltés

3. **ConfigManagerFactory**
   - Megfelelő implementáció kiválasztása
   - Konfiguráció inicializálás
   - Validáció végrehajtás

## API gyorsreferencia

```python
# Factory használata
config = ConfigManagerFactory.get_manager("config.yaml")

# Érték lekérése
value = config.get("section.key", default="default")

# Szekció lekérése
section = config.get_section("database")

# Érték beállítása
config.set("section.key", "new_value")

# Konfiguráció mentése
config.save()
```

## Fejlesztői információk

### Új formátum hozzáadása

1. Implementálja a `ConfigManagerInterface`-t
2. Regisztrálja a formátumot a factory-ban:

```python
ConfigManagerFactory.register_manager(".ext", MyConfigManager)
```

### Validációs séma formátum

```python
{
    "key": {
        "type": str,       # Kötelező: str, int, float, bool, list, dict
        "optional": bool,  # Opcionális: True/False
        "choices": list,   # Opcionális: választható értékek
        "min": number,     # Opcionális: minimum érték (szám esetén)
        "max": number,     # Opcionális: maximum érték (szám esetén)
        "schema": dict     # Opcionális: beágyazott séma dict típus esetén
    }
}
```

## Tesztelés

```bash
# Unit tesztek futtatása
pytest tests/core/config/

# Lefedettség ellenőrzése
pytest --cov=neural_ai.core.config tests/core/config/
```

## Közreműködés

1. Fork létrehozása
2. Feature branch létrehozása (`git checkout -b feature/új_formátum`)
3. Változtatások commit-olása (`git commit -am 'Új formátum: xyz'`)
4. Branch feltöltése (`git push origin feature/új_formátum`)
5. Pull Request nyitása

## Licensz

MIT License - lásd a LICENSE fájlt a részletekért.

## További dokumentáció

- [API Dokumentáció](api.md)
- [Architektúra leírás](architecture.md)
- [Tervezési specifikáció](design_spec.md)
- [Példák](examples.md)
- [Fejlesztési checklist](development_checklist.md)
