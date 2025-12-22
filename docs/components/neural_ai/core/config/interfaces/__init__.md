# Konfiguráció Interfészek Csomag

## Áttekintés

Ez a dokumentáció a `neural_ai.core.config.interfaces` csomagot írja le, amely a konfigurációkezelő rendszer interfészeit tartalmazza.

## Cél

A csomag célja, hogy egységes interfészeket biztosítson a konfigurációkezeléshez, lehetővé téve a különböző implementációk cserélhetőségét és a függőség-inverzió elvét.

## Tartalom

### Interfészek

#### `ConfigManagerInterface`

A konfigurációkezelők alapvető műveleteit definiáló absztrakt interfész.

**Metódusok:**
- `__init__(filename: str | None = None) -> None`: Inicializálás
- `get(*keys: str, default: Any = None) -> Any`: Érték lekérése
- `get_section(section: str) -> dict[str, Any]`: Szekció lekérése
- `set(*keys: str, value: Any) -> None`: Érték beállítása
- `save(filename: str | None = None) -> None`: Konfiguráció mentése
- `load(filename: str) -> None`: Konfiguráció betöltése
- `validate(schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]`: Validálás

#### `ConfigManagerFactoryInterface`

A konfigurációkezelő factory-k által implementálandó absztrakt interfész.

**Metódusok:**
- `register_manager(extension: str, manager_class: type[ConfigManagerInterface]) -> None`: Manager regisztrálása
- `get_manager(filename: str, manager_type: str | None = None) -> ConfigManagerInterface`: Manager lekérése
- `create_manager(manager_type: str, *args: Any, **kwargs: Any) -> ConfigManagerInterface`: Manager létrehozása

## Használat

### Importálás

```python
from neural_ai.core.config.interfaces import (
    ConfigManagerInterface,
    ConfigManagerFactoryInterface,
)
```

### Példa Implementáció

```python
from neural_ai.core.config.interfaces import ConfigManagerInterface

class MyConfigManager(ConfigManagerInterface):
    def __init__(self, filename: str | None = None) -> None:
        super().__init__(filename)
        # Implementáció
    
    def get(self, *keys: str, default: Any = None) -> Any:
        # Implementáció
        pass
    
    # További metódusok implementációja...
```

## Függőségek

Ez a csomag nem rendelkezik külső függőségekkel a standard könyvtáron kívül, és a következőket importálja:

- `typing`: Típusanotációkhoz
- `abc`: Absztrakt osztályokhoz

## Architektúra

A csomag a következő architektúrai elveket követi:

1. **Függőség Inverzió**: Interfészeken keresztül történik a kommunikáció
2. **Nyílt-Zárt Elv**: Bővíthető, de nem módosítható
3. **Egyszeri Felelősség**: Minden interfész egyetlen feladatkörrel rendelkezik

## Jövőbeli Fejlesztések

- További konfigurációs formátumok támogatása (JSON, TOML, stb.)
- Validációs séma bővítése
- Konfiguráció változás események
- Dinamikus konfiguráció frissítés