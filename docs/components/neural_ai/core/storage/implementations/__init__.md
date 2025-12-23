# Storage Implementációk Modul

## Áttekintés

Ez a modul a tárolási komponens implementációit tartalmazza. A storage implementációk felelősek az adatok perzisztens tárolásáért és kezeléséért.

## Exportált Osztályok és Funkciók

### `FileStorage`

Fájl alapú tárolási implementáció. Az adatokat fájlrendszerben tárolja, biztosítva a perzisztenciát.

**Jellemzők:**
- Fájl alapú adattárolás
- Adatok olvasása és írása
- Hibakezelés és validáció

**Használat:**
```python
from neural_ai.core.storage.implementations import FileStorage

storage = FileStorage()
data = storage.read("data.json")
storage.write("output.json", data)
```

### `StorageFactory`

Storage implementációk létrehozásáért felelős gyár osztály.

**Jellemzők:**
- Típus alapú objektum létrehozás
- Konfigurálható storage implementációk
- Dependency injection támogatás

**Használat:**
```python
from neural_ai.core.storage.implementations import StorageFactory

factory = StorageFactory()
storage = factory.create_storage("file")
```

## Függőségek

A storage implementációk a következő komponensekre támaszkodnak:

- **Logger**: Műveletek naplózásához
- **Config**: Konfigurációs beállításokhoz

## Implementációs Részletek

### Függőség Injektálás

A storage implementációk a core függőségi injektálási mintát követik:

```python
class FileStorage:
    def __init__(
        self,
        config: Optional[ConfigInterface] = None,
        logger: Optional[LoggerInterface] = None
    ):
        self._config = config or DefaultConfig()
        self._logger = logger or NullLogger()
```

### Típusbiztonság

Minden osztály és metódus szigorú típusannotációkkal rendelkezik, biztosítva a fordítási hibák elkerülését.

## Hibakezelés

A storage műveletek a következő kivételeket dobhatják:

- `StorageError`: Általános tárolási hiba
- `FileNotFoundError`: Fájl nem található
- `PermissionError`: Nincs megfelelő jogosultság

## Tesztelés

A modul tesztelése a `tests/core/storage/implementations/` mappában található.

**Tesztesetek:**
- Importok ellenőrzése
- Típusannotációk validálása
- Dokumentáció ellenőrzése
- Körkörös importok vizsgálata

## Fejlesztési Jó Gyakorlatok

1. **Típusbiztonság**: Mindig használj szigorú típusannotációkat
2. **Dokumentáció**: A docstring-ek magyar nyelven, Google style formátumban
3. **Hibakezelés**: Minden műveletnél implementáld a megfelelő hibakezelést
4. **Tesztelés**: 100% coverage kötelező a tesztekben