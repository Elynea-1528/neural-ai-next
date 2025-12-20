# 💻 Code Mód - Neural AI Next

## Alapelvek

A Code módban a következő alapelvekre kell koncentrálni:

1. **Kódminőség** - Minden kód legyen produkciós szintű
2. **Típusbiztonság** - Használj szigorú típusannotációkat
3. **Dokumentáció** - Minden függvényhez és osztályhoz kötelező docstring
4. **Tesztelhetőség** - Írj tesztelhető kódot

## Kódolási szabályok

### 1. Típusannotációk

Minden függvényhez és metódushoz kötelező típusannotáció:

```python
def process_data(data: pd.DataFrame, config: Dict[str, Any]) -> ProcessResult:
    """Adatfeldolgozás.
    
    Args:
        data: Feldolgozandó adatok DataFrame formátumban
        config: Konfigurációs beállítások
        
    Returns:
        ProcessResult: A feldolgozás eredménye
    """
```

### 2. Base Komponensek Használata

**Új komponensek esetén kötelező használni a base komponenseket:**

```python
from neural_ai.core.base import CoreComponentFactory, CoreComponents
from typing import Dict, Any

class DataProcessor:
    """Adatfeldolgozó komponens.
    
    Ez az osztály felelős az adatok feldolgozásáért.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Inicializálás.
        
        Args:
            config: Konfigurációs beállítások
        """
        # Komponensek létrehozása a Factory-vel
        self.components: CoreComponents = CoreComponentFactory.create_components(
            config_path=config.get('config_path'),
            log_path=config.get('log_path'),
            storage_path=config.get('storage_path')
        )
        
        # Naplózás
        self.components.logger.info("DataProcessor initialized")
```

### 3. Komponensek Használata

Használd a `CoreComponents` objektumot a komponensek eléréséhez:

```python
class MyComponent:
    def __init__(self, config: Dict[str, Any]):
        # Komponensek létrehozása
        self.components = CoreComponentFactory.create_components(
            config_path=config.get('config_path'),
            log_path=config.get('log_path'),
            storage_path=config.get('storage_path')
        )
        
    def process_data(self, data):
        # Naplózás
        self.components.logger.info("Processing data")
        
        # Konfiguráció olvasása
        if self.components.has_config():
            settings = self.components.config.get_section('processing')
        
        # Adattárolás
        if self.components.has_storage():
            self.components.storage.save_object(data, "result.json")
```

### 4. Hibakezelés

Mindig implementálj specifikus kivétel osztályokat:

```python
from neural_ai.core.base.exceptions import ComponentError

class DataProcessingError(ComponentError):
    """Adatfeldolgozási hiba."""
    pass

def process_data(data):
    if data is None:
        raise DataProcessingError("Az adatok nem lehetnek None")
```

### 5. Naplózás

Használd a projekt logger komponensét:

```python
class MyComponent(Container):
    def process(self, data):
        self.logger.info("Feldolgozás megkezdése")
        try:
            result = self._do_process(data)
            self.logger.debug(f"Feldolgozás eredménye: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Hiba a feldolgozás során: {e}")
            raise
```

## Projekt specifikus implementációk

### 1. Base Komponensek Factory-vel

Használd a `CoreComponentFactory`-t a komponensek létrehozásához:

```python
from neural_ai.core.base import CoreComponentFactory, CoreComponents
from typing import Dict, Any

class DataProcessorFactory:
    """Adatfeldolgozó factory."""
    
    def create(self, processor_type: str, config: Dict[str, Any]) -> 'DataProcessor':
        """Adatfeldolgozó létrehozása.
        
        Args:
            processor_type: A processzor típusa
            config: Konfigurációs beállítások
            
        Returns:
            DataProcessor: Az adatfeldolgozó példány
        """
        if processor_type == "mt5":
            return MT5DataProcessor(config)
        elif processor_type == "csv":
            return CSVDataProcessor(config)
        else:
            raise ValueError(f"Ismeretlen processzor típus: {processor_type}")

class MT5DataProcessor:
    """MT5 adatfeldolgozó."""
    
    def __init__(self, config: Dict[str, Any]):
        # Komponensek létrehozása a Factory-vel
        self.components = CoreComponentFactory.create_components(
            config_path=config.get('config_path'),
            log_path=config.get('log_path'),
            storage_path=config.get('storage_path')
        )
        self.components.logger.info("MT5DataProcessor created")
```

### 2. Interfészek

Minden komponenshez implementálj interfészt:

```python
from abc import ABC, abstractmethod

class DataProcessorInterface(ABC):
    """Adatfeldolgozó interfész."""
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """Adatok feldolgozása.
        
        Args:
            data: A feldolgozandó adatok
            
        Returns:
            A feldolgozott adatok
        """
        pass
```

### 3. Konfigurációkezelés

Használd a config komponenst:

```python
from neural_ai.core.config.implementations.config_manager_factory import ConfigManagerFactory

config_factory = ConfigManagerFactory()
config_manager = config_factory.create('yaml')
config = config_manager.load('configs/my_config.yaml')
```

## Kódstruktúra

### 1. Import sorrend

```python
# Standard library
import os
import sys
from typing import Dict, List, Any

# Third-party
import numpy as np
import pandas as pd

# Project
from neural_ai.core.base.container import Container
from neural_ai.core.base.factory import BaseFactory
```

### 2. Fájl szerkezet

```python
"""
Modul docstring - rövid leírás a fájl céljáról.
"""

import ...

class MyComponent(Container):
    """Osztály docstring."""
    
    def __init__(self, config):
        """Inicializálás."""
        super().__init__()
        self.config = config
        
    def public_method(self, param):
        """Publikus metódus.
        
        Args:
            param: Paraméter leírása
            
        Returns:
            Visszatérési érték leírása
        """
        pass
        
    def _private_method(self, param):
        """Privát metódus.
        
        Args:
            param: Paraméter leírása
        """
        pass
```

## Tesztelés

Minden kódhoz írj egységteszteket:

```python
import unittest
from neural_ai.core.base.container import Container

class TestMyComponent(unittest.TestCase):
    """MyComponent tesztosztály."""
    
    def setUp(self):
        """Teszt előkészítés."""
        self.component = MyComponent(config={})
        
    def test_process_data(self):
        """Adatfeldolgozás tesztelése."""
        data = {"test": "data"}
        result = self.component.process(data)
        self.assertIsNotNone(result)
```

## Hasznos linkek

- [Komponens Template](../../docs/templates/component_template.py)
- [Interfész Template](../../docs/templates/interface_template.py)
- [Teszt Template](../../docs/templates/test_template.py)
- [Fejlesztési Checklista](../../docs/development/checklist_template.md)
- [Code Review Útmutató](../../docs/development/code_review_guide.md)
