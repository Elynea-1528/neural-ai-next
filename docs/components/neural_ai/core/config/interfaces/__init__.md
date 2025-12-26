# Config Interfészek Modul

## Áttekintés

Konfigurációkezelő interfészek.

Ez a modul tartalmazza a konfigurációkezelő komponens interfészeit, beleértve a ConfigManagerInterface és ConfigManagerFactoryInterface osztályokat.

A modul biztosítja a konfigurációkezeléshez szükséges alapvető interfészeket, amelyek lehetővé teszik a különböző konfigurációs formátumok és tárolási módok egységes kezelését.

## Exportált Interfészek

- [`ConfigManagerInterface`](config_interface.md): Konfigurációkezelő interfész
- [`ConfigManagerFactoryInterface`](factory_interface.md): Konfigurációkezelő factory interfész

## Használati Példa

```python
from neural_ai.core.config.interfaces import ConfigManagerInterface
from typing import Any

class MyCustomConfigManager(ConfigManagerInterface):
    def __init__(self, filename: str | None = None):
        self._config = {}
        self._filename = filename
        if filename:
            self.load(filename)
    
    def get(self, *keys: str, default: Any = None) -> Any:
        # Egyéni implementáció
        pass
    
    def get_section(self, section: str) -> dict[str, Any]:
        # Egyéni implementáció
        pass
    
    def set(self, *keys: str, value: Any) -> None:
        # Egyéni implementáció
        pass
    
    def save(self, filename: str | None = None) -> None:
        # Egyéni implementáció
        pass
    
    def load(self, filename: str) -> None:
        # Egyéni implementáció
        pass
    
    def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]:
        # Egyéni implementáció
        pass
```

## Kapcsolódó Dokumentáció

- [ConfigManagerInterface](config_interface.md)
- [ConfigManagerFactoryInterface](factory_interface.md)
- [Config Modul](../__init__.md)