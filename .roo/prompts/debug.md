# 🪲 Debug Mód - Neural AI Next

## Alapelvek

A Debug módban a következő alapelvekre kell koncentrálni:

1. **Rendszeres megközelítés** - Mindig kövess egy logikus hibakeresési folyamatot
2. **Naplózás** - Használd a projekt logger komponensét hibák nyomon követéséhez
3. **Típusellenőrzés** - Ellenőrizd a típusokat és az annotációkat
4. **Tesztelés** - Írj reprodukálható teszteseteket

## Hibakeresési folyamat

### 1. Hiba reprodukálása

Első lépés mindig a hiba reprodukálása:

```python
# Hozz létre egy minimális tesztesetet
def test_error_reproduction():
    """Hiba reprodukálása."""
    from neural_ai.core.base import CoreComponentFactory
    
    class TestComponent:
        def __init__(self):
            # Komponensek létrehozása
            self.components = CoreComponentFactory.create_minimal()
            
        def problematic_method(self, data):
            # Ide írd a hibás kódot
            return data.process()
    
    component = TestComponent()
    try:
        component.problematic_method(None)
    except Exception as e:
        print(f"Hiba történt: {type(e).__name__}: {e}")
```

### 2. Naplózás implementálása

Használd a projekt logger komponensét:

```python
from neural_ai.core.base import CoreComponentFactory, CoreComponents

class DebuggableComponent:
    def __init__(self, config: Dict[str, Any]):
        # Komponensek létrehozása
        self.components: CoreComponents = CoreComponentFactory.create_components(
            config_path=config.get('config_path'),
            log_path=config.get('log_path'),
            storage_path=config.get('storage_path')
        )
        
    def process_data(self, data):
        self.components.logger.info("Adatfeldolgozás megkezdése")
        self.components.logger.debug(f"Bemeneti adatok: {data}")
        
        try:
            result = self._do_processing(data)
            self.components.logger.info("Feldolgozás sikeres")
            return result
        except Exception as e:
            self.components.logger.error(f"Hiba a feldolgozás során: {e}")
            self.components.logger.exception("Kivétel részletei:")
            raise
```

### 3. Típusellenőrzés

Használd a MyPy-t típushibák ellenőrzéséhez:

```bash
# Futtasd a MyPy-t a projektben
mypy neural_ai/
```

Javítsd a típushibákat:

```python
from typing import Dict, Any, Optional

def process_data(data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Adatok feldolgozása.
    
    Args:
        data: Feldolgozandó adatok vagy None
        
    Returns:
        Feldolgozott adatok
        
    Raises:
        ValueError: Ha az adatok None-ok
    """
    if data is None:
        raise ValueError("Az adatok nem lehetnek None")
    
    return {k: v for k, v in data.items() if v is not None}
```

## Projekt specifikus hibakeresés

### 1. Base komponensek hibakeresése

```python
from neural_ai.core.base import CoreComponentFactory, CoreComponents

class MyComponent:
    def __init__(self, config: Dict[str, Any]):
        # Komponensek létrehozása
        self.components = CoreComponentFactory.create_components(
            config_path=config.get('config_path'),
            log_path=config.get('log_path'),
            storage_path=config.get('storage_path')
        )
        
        # Függőségek ellenőrzése
        self._validate_dependencies()
        
    def _validate_dependencies(self):
        """Függőségek ellenőrzése."""
        # Config ellenőrzése
        if not self.components.has_config():
            raise RuntimeError("Config komponens hiányzik")
        self.components.logger.debug("Config komponens elérhető")
        
        # Logger ellenőrzése
        if not self.components.has_logger():
            raise RuntimeError("Logger komponens hiányzik")
        self.components.logger.debug("Logger komponens elérhető")
        
        # Storage ellenőrzése
        if not self.components.has_storage():
            raise RuntimeError("Storage komponens hiányzik")
        self.components.logger.debug("Storage komponens elérhető")
```

### 2. Konfigurációs hibák

```python
from neural_ai.core.config.implementations.config_manager_factory import ConfigManagerFactory
from neural_ai.core.config.exceptions import ConfigError

def load_and_validate_config(config_path: str) -> Dict[str, Any]:
    """Konfiguráció betöltése és validálása.
    
    Args:
        config_path: A konfigurációs fájl elérési útja
        
    Returns:
        A betöltött konfiguráció
        
    Raises:
        ConfigError: Ha a konfiguráció érvénytelen
    """
    try:
        factory = ConfigManagerFactory()
        config_manager = factory.create('yaml')
        config = config_manager.load(config_path)
        
        # Validáció
        required_keys = ['database', 'logging', 'storage']
        for key in required_keys:
            if key not in config:
                raise ConfigError(f"Hiányzó kötelező kulcs: {key}")
        
        return config
        
    except FileNotFoundError:
        raise ConfigError(f"Konfigurációs fájl nem található: {config_path}")
    except Exception as e:
        raise ConfigError(f"Hiba a konfiguráció betöltésekor: {e}")
```

### 3. MT5 Collector hibakeresés

```python
from neural_ai.core.base import CoreComponentFactory, CoreComponents

class MT5Collector:
    def __init__(self, config: Dict[str, Any]):
        # Komponensek létrehozása
        self.components = CoreComponentFactory.create_components(
            config_path=config.get('config_path'),
            log_path=config.get('log_path'),
            storage_path=config.get('storage_path')
        )
        self.config = config
        
    def collect_data(self, symbol: str, timeframe: str) -> Dict[str, Any]:
        """Adatgyűjtés MT5-ből.
        
        Args:
            symbol: A szimbólum neve
            timeframe: Az időkeret
            
        Returns:
            Az összegyűjtött adatok
        """
        self.components.logger.info(f"Adatgyűjtés indítása: {symbol}, {timeframe}")
        
        try:
            # Kapcsolódás ellenőrzése
            if not self._check_connection():
                raise ConnectionError("Nincs kapcsolat az MT5-tel")
            
            # Adatlekérdezés
            data = self._fetch_data(symbol, timeframe)
            
            # Adatvalidáció
            if not self._validate_data(data):
                raise ValueError("Az adatok érvénytelenek")
            
            self.components.logger.info("Adatgyűjtés sikeres")
            return data
            
        except Exception as e:
            self.components.logger.error(f"Hiba az adatgyűjtés során: {e}")
            self.components.logger.exception("Kivétel részletei:")
            raise
```

## Hibakeresési eszközök

### 1. Naplózási szintek

```python
# Állítsd be a naplózási szintet
import logging

logging.basicConfig(level=logging.DEBUG)

# Vagy használd a projekt loggerét
from neural_ai.core.logger.implementations.logger_factory import LoggerFactory

factory = LoggerFactory()
logger = factory.create('default', log_level='DEBUG')
logger.debug("Részletes hibakeresési információ")
```

### 2. Assert használata

```python
def process_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Adatok feldolgozása.
    
    Args:
        data: A feldolgozandó adatok
        
    Returns:
        Feldolgozott adatok
    """
    # Előfeltételek ellenőrzése
    assert data is not None, "Az adatok nem lehetnek None"
    assert isinstance(data, dict), "Az adatoknak szótárnak kell lennie"
    assert 'required_field' in data, "Hiányzó kötelező mező"
    
    # Feldolgozás
    result = {}
    for key, value in data.items():
        assert value is not None, f"Érvénytelen érték a {key} kulcsnál"
        result[key] = value * 2
    
    # Utófeltételek ellenőrzése
    assert len(result) > 0, "Az eredmény nem lehet üres"
    
    return result
```

### 3. Profilozás

```python
import cProfile
import pstats

def profile_function(func, *args, **kwargs):
    """Függvény profilozása.
    
    Args:
        func: A profilozandó függvény
        *args: Pozíciós argumentumok
        **kwargs: Kulcsszavas argumentumok
    """
    profiler = cProfile.Profile()
    profiler.enable()
    
    result = func(*args, **kwargs)
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 leglassabb függvény
    
    return result
```

## Hibajelentési sablon

Amikor hibát találsz, használd ezt a sablont:

```markdown
## Hiba leírása

### Környezet
- Python verzió: 3.10+
- Operációs rendszer: Linux
- Komponens: [komponens neve]

### Hiba reprodukálása
1. Lépés
2. Lépés
3. Lépés

### Várt viselkedés
Mit kellett volna látni

### Tényleges viselkedés
Mit láttunk helyette

### Naplók
```
[ide másold a releváns naplóbejegyzéseket]
```

### Hibakeresési lépések
- [ ] Hiba reprodukálva
- [ ] Naplózás implementálva
- [ ] Típusellenőrzés elvégezve
- [ ] Teszteset létrehozva
```

## Hasznos linkek

- [Hibakezelési Útmutató](../../docs/development/error_handling.md)
- [Logger Komponens API](../../docs/components/logger/api.md)
- [Tesztelési Template](../../docs/templates/test_template.py)
- [MT5 Hibakeresési Útmutató](../../neural_ai/experts/mt5/TESTING_GUIDE_HU.md)
