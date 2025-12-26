# Neural AI Core Config Modul

## Áttekintés

Konfigurációs modul a Neural AI rendszerhez.

Ez a modul a konfigurációkezeléshez szükséges alapvető osztályokat, interfészeket és kivételeket exportálja.

A modul a következő komponenseket tartalmazza:

- **Kivételek**: Konfigurációs hibakezelés speciális kivétel osztályokkal
- **Interfészek**: Konfigurációkezelő és gyártó interfészek
- **Implementációk**: YAML alapú konfigurációkezelés és gyártó osztály

## Komponensek

- `ConfigError`: Alap konfigurációs kivétel osztály
- `ConfigKeyError`: Konfigurációs kulcs hibák
- `ConfigLoadError`: Konfiguráció betöltési hibák
- `ConfigSaveError`: Konfiguráció mentési hibák
- `ConfigTypeError`: Típus hibák a konfigurációban
- `ConfigValidationError`: Validációs hibák
- `ConfigManagerFactory`: Konfigurációkezelő gyártó
- `YAMLConfigManager`: YAML alapú konfigurációkezelő
- `ConfigManagerInterface`: Konfigurációkezelő interfész
- `ConfigManagerFactoryInterface`: Gyártó interfész

## Használati Példa

```python
from neural_ai.core.config import ConfigManagerFactory, ConfigError

try:
    factory = ConfigManagerFactory()
    config_manager = factory.create_manager('yaml')
    value = config_manager.get('database.host', 'localhost')
except ConfigError as e:
    print(f"Konfigurációs hiba: {e}")
```

## Kapcsolódó Dokumentáció

- [Kivételek](exceptions/)
- [Interfészek](interfaces/)
- [Implementációk](implementations/)
- [Config Manager Factory](factory.md)