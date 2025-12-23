# Storage Interfészek Csomag

## Áttekintés

Ez a csomag a tárolási réteg interfészeit tartalmazza, amelyek a különböző tárolási megoldások egységes kezelését teszik lehetővé.

## Interfészek

### StorageInterface

A tárolási műveletek alapvető interfésze.

**Metódusok:**
- `save(data: bytes, path: str) -> None`: Adatok mentése a megadott útvonalra
- `load(path: str) -> bytes`: Adatok betöltése a megadott útvonalról
- `exists(path: str) -> bool`: Ellenőrzi, hogy az útvonal létezik-e
- `delete(path: str) -> None`: Törli a megadott útvonalat

### StorageFactoryInterface

A tároló objektumok létrehozásáért felelős gyártó interfésze.

**Metódusok:**
- `register_storage(storage_type: str, storage_class: type[StorageInterface]) -> None`: Új tároló típus regisztrálása
- `get_storage(storage_type: str, base_path: str | Path | None, **kwargs) -> StorageInterface`: Tároló példány létrehozása

## Függőségek

- **Config**: A tárolási beállítások kezeléséhez
- **Logger**: A műveletek naplózásához

## Használat

```python
from neural_ai.core.storage.interfaces import StorageInterface, FactoryInterface
from neural_ai.core.config import ConfigInterface
from neural_ai.core.logger import LoggerInterface

# Interfész implementáció használata
class MyStorage(StorageInterface):
    def save(self, data: bytes, path: str) -> None:
        # Implementáció
        pass
    
    def load(self, path: str) -> bytes:
        # Implementáció
        pass
    
    def exists(self, path: str) -> bool:
        # Implementáció
        pass
    
    def delete(self, path: str) -> None:
        # Implementáció
        pass
```

## További Információk

- [Storage Interface](storage_interface.md) - Részletes leírás a tárolási interfészről
- [Factory Interface](factory_interface.md) - Részletes leírás a gyártó interfészről