# Neural AI - Konfigurációs Komponens

## Áttekintés

A konfigurációs komponens felelős a rendszer különböző beállításainak kezeléséért. Támogatja a YAML formátumú konfigurációs fájlok betöltését, validálását és módosítását.

## Főbb funkciók

- YAML konfigurációs fájlok kezelése
- Hierarchikus konfigurációs struktúra
- Séma alapú validáció
- Típus biztonságos hozzáférés
- Dinamikus konfiguráció módosítás

## Telepítés

A komponens a Neural AI keretrendszer részeként települ. Külön telepítést nem igényel.

## Használat

### Alap használat

```python
from neural_ai.core.config.implementations import ConfigManagerFactory

# Konfiguráció betöltése
config = ConfigManagerFactory.get_manager("config.yaml")

# Érték lekérése
host = config.get("database", "host", default="localhost")
port = config.get("database", "port", default=5432)

# Érték beállítása
config.set("logging", "level", value="DEBUG")

# Konfiguráció mentése
config.save()
```

### Séma validáció

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
valid, errors = config.validate(schema)
if not valid:
    print("Validation errors:", errors)
```

## API Dokumentáció

### ConfigManagerFactory

Factory osztály a konfigurációkezelők létrehozásához.

```python
@classmethod
def get_manager(cls, filename: str, **kwargs: Any) -> ConfigManagerInterface:
    """Megfelelő konfigurációkezelő példány létrehozása.

    Args:
        filename: Konfigurációs fájl neve
        **kwargs: További paraméterek a kezelő számára

    Returns:
        ConfigManagerInterface: Konfigurációkezelő példány

    Raises:
        ValueError: Ha nem található megfelelő kezelő
    """
```

### YAMLConfigManager

YAML fájlok kezelésére szolgáló implementáció.

```python
def get(self, *keys: str, default: Any = None) -> Any:
    """Érték lekérése a konfigurációból.

    Args:
        *keys: Kulcsok útvonala
        default: Alapértelmezett érték ha nem található

    Returns:
        Any: A konfigurációs érték vagy az alapértelmezett érték
    """

def set(self, *keys: str, value: Any) -> None:
    """Érték beállítása a konfigurációban.

    Args:
        *keys: Kulcsok útvonala
        value: Az új érték

    Raises:
        ValueError: Ha érvénytelen az útvonal
    """
```

## Fejlesztői információk

### Új konfigurációkezelő hozzáadása

1. Implementáld a `ConfigManagerInterface`-t
2. Regisztráld a kezelőt a `ConfigManagerFactory`-ban:

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
pytest tests/core/config/
```

## Közreműködés

1. Fork létrehozása
2. Feature branch létrehozása (`git checkout -b feature/új_funkcio`)
3. Változtatások commit-olása (`git commit -am 'Új funkció: xyz'`)
4. Branch feltöltése (`git push origin feature/új_funkcio`)
5. Pull Request nyitása

## Licensz

MIT License - lásd a LICENSE fájlt a részletekért.
