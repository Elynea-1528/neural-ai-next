# Storage Interfészek

## Áttekintés

Ez a csomag a tárolási réteg interfészeit tartalmazza, amelyek a különböző tárolási megoldások egységes kezelését teszik lehetővé. Az interfészek lehetővé teszik a függőség injektálást, ami a komponensek laza csatolását és egyszerű tesztelését eredményezi.

## Elérhető Interfészek

### [`StorageInterface`](storage_interface.md)
Alapvető tárolási műveletek (mentés, betöltés, törlés)

### [`StorageFactoryInterface`](factory_interface.md)
Tároló objektumok létrehozásáért felelős gyártó

## Használat

### Alapvető Példa

```python
from neural_ai.core.storage.interfaces import StorageInterface
from neural_ai.core.config import ConfigManagerInterface
from neural_ai.core.logger import LoggerInterface

class MyStorage(StorageInterface):
    def __init__(
        self,
        config: ConfigManagerInterface,
        logger: LoggerInterface
    ):
        self._config = config
        self._logger = logger
    
    def save_dataframe(self, df, path, **kwargs):
        # Implementáció
        pass
    
    def load_dataframe(self, path, **kwargs):
        # Implementáció
        pass
    
    # További metódusok implementációja...
```

### Factory Használata

```python
from neural_ai.core.storage.interfaces import StorageFactoryInterface
from neural_ai.core.storage.interfaces import StorageInterface

class MyStorageFactory(StorageFactoryInterface):
    @classmethod
    def register_storage(cls, storage_type, storage_class):
        # Implementáció
        pass
    
    @classmethod
    def get_storage(cls, storage_type="file", base_path=None, **kwargs):
        # Implementáció
        pass
```

## Függőség Injektálás

Az interfészek használatának fő előnye a függőség injektálás (Dependency Injection), ami lehetővé teszi:

1. **Laza csatolás**: A komponensek nem függenek konkrét implementációktól
2. **Könnyű tesztelés**: Mock objektumokkal egyszerű a tesztelés
3. **Bővíthetőség**: Új tárolási megoldások egyszerű hozzáadása

### Példa DI-re

```python
from neural_ai.core.storage.interfaces import StorageInterface
from neural_ai.core.logger.interfaces import LoggerInterface
from neural_ai.core.config.interfaces import ConfigManagerInterface

class DatabaseStorage(StorageInterface):
    def __init__(
        self,
        logger: LoggerInterface,
        config: ConfigManagerInterface,
        connection_string: str
    ):
        self._logger = logger
        self._config = config
        self._connection_string = connection_string
    
    def save_dataframe(self, df, path, **kwargs):
        # Naplózás a logger interfészen keresztül
        self._logger.info(f"DataFrame mentése: {path}")
        
        # Konfiguráció lekérdezése
        timeout = self._config.get("storage.timeout", default=30)
        
        # Adatbázis mentés implementációja
        # ...
```

## Tesztelés

Az interfészek használatával egyszerű a tesztelés:

```python
import unittest
from unittest.mock import Mock
from neural_ai.core.storage.interfaces import StorageInterface

class TestMyComponent(unittest.TestCase):
    def setUp(self):
        # Mock storage létrehozása
        self.mock_storage = Mock(spec=StorageInterface)
        
        # Komponens létrehozása a mockkal
        self.component = MyComponent(storage=self.mock_storage)
    
    def test_save_data(self):
        # Mock konfigurálása
        self.mock_storage.save_dataframe.return_value = None
        
        # Teszt végrehajtása
        self.component.save_data()
        
        # Assert
        self.mock_storage.save_dataframe.assert_called_once()
```

## Exportált Interfészek

A modul a következő interfészeket exportálja:

- `StorageInterface`: Alapvető tárolási műveletek
- `StorageFactoryInterface`: Tároló objektumok létrehozásáért felelős gyártó

## Best Practices

1. **Interfész használata**: Mindig az interfészt importáljuk, ne a konkrét implementációt
2. **Típusjelzés**: Használjuk a típusjelzéseket az interfészekre
3. **DI konténer**: Használjunk DI konténert a függőségek kezeléséhez
4. **Tesztelés**: Mockoljuk az interfészeket a tesztelés során
