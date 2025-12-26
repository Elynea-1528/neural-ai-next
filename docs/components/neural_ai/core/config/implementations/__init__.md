# Config Implementációk Modul

## Áttekintés

Konfigurációkezelő implementációk.

Ez a modul tartalmazza a különböző konfigurációkezelő implementációkat, köztük a YAML alapú konfigurációkezelőt és a hozzá tartozó factory osztályt.

A modul a következő fő komponenseket exportálja:

- `ConfigManagerFactory`: Factory osztály konfigurációkezelők létrehozásához
- `YAMLConfigManager`: YAML fájlokat kezelő konfigurációkezelő implementáció

## Verziókezelés

A modul támogatja a konfigurációs sémák verziókezelését. Minden konfigurációs fájl tartalmazhat egy 'schema_version' mezőt, amely a séma verzióját határozza meg. Ez lehetővé teszi a verziók közötti migrációkat és kompatibilitás-ellenőrzést.

## Modul Változók

- `__version__`: A modul verziója (dinamikusan betöltve a pyproject.toml-ből)
- `SCHEMA_VERSION`: A konfigurációs séma aktuális verziója

## Használati Példa

```python
from neural_ai.core.config.implementations import ConfigManagerFactory

factory = ConfigManagerFactory()
config = factory.get_manager("config.yaml")
value = config.get("database", "host")
schema_version = config.get("schema_version", default="1.0.0")
```

## Kapcsolódó Dokumentáció

- [YAMLConfigManager](yaml_config_manager.md)
- [Config Modul](../__init__.md)