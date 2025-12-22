# neural_ai.core.config

A Neural AI rendszer konfigurációs moduljának fő csomagja.

## Áttekintés

Ez a modul a konfigurációkezeléshez szükséges alapvető osztályokat, interfészeket és kivételeket exportálja. A modul célja, hogy egységes és típusbiztos interfészt nyújtson a konfigurációk kezeléséhez a Neural AI rendszerben.

## Komponensek

### Kivételek

- **ConfigError**: Alap konfigurációs kivétel osztály
- **ConfigKeyError**: Konfigurációs kulcs hibák kezelése
- **ConfigLoadError**: Konfiguráció betöltési hibák
- **ConfigSaveError**: Konfiguráció mentési hibák
- **ConfigTypeError**: Típus hibák a konfigurációban
- **ConfigValidationError**: Validációs hibák

### Interfészek

- **ConfigManagerInterface**: Konfigurációkezelő alapinterfész
- **ConfigManagerFactoryInterface**: Konfigurációkezelő gyártó interfész

### Implementációk

- **ConfigManagerFactory**: Konfigurációkezelő gyártó osztály
- **YAMLConfigManager**: YAML alapú konfigurációkezelő implementáció

## Használat

### Alapvető használat

```python
from neural_ai.core.config import ConfigManagerFactory, ConfigError

try:
    # Gyártó létrehozása
    factory = ConfigManagerFactory()
    
    # YAML konfigurációkezelő létrehozása
    config_manager = factory.create_manager('yaml')
    
    # Érték lekérdezése
    value = config_manager.get('database.host', 'localhost')
    
except ConfigError as e:
    print(f"Konfigurációs hiba: {e}")
```

### Konfigurációs kivételek kezelése

```python
from neural_ai.core.config import (
    ConfigError,
    ConfigKeyError,
    ConfigLoadError,
    ConfigValidationError
)

try:
    config_manager.load_config('config.yaml')
except ConfigLoadError as e:
    print(f"Betöltési hiba: {e}")
except ConfigValidationError as e:
    print(f"Validációs hiba: {e}")
```

## Függőségek

Ez a modul a következő komponensektől függ:

- **neural_ai.core.config.exceptions**: Konfigurációs kivételek
- **neural_ai.core.config.implementations**: Konfigurációkezelő implementációk
- **neural_ai.core.config.interfaces**: Konfigurációs interfészek

## Architektúra

A konfigurációs modul a következő architektúrai elveket követi:

1. **Dependency Injection**: A komponensek függőségeit injektáljuk
2. **Interface Segregation**: Külön interfészek a különböző szerepekre
3. **Factory Pattern**: Konfigurációkezelők gyártása
4. **Type Safety**: Típusbiztos műveletek

## További információk

- [Konfigurációs kivételek](exceptions.md)
- [Konfigurációkezelő interfész](interfaces/config_interface.md)
- [YAML konfigurációkezelő](implementations/yaml_config_manager.md)
- [Konfigurációkezelő gyártó](implementations/config_manager_factory.md)

## Verziótörténet

- **1.0.0**: Alap konfigurációs modul létrehozása