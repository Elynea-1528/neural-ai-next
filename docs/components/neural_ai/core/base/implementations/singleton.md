# Singleton Implementáció

## Áttekintés

Singleton metaclass megvalósítása a singleton tervezési minta biztosításához.

Ez a modul egy metaclass-t biztosít, amely garantálja, hogy minden osztályból, ami ezt a metaclass-t használja, csak egyetlen példány létezzen az alkalmazás életciklusa során.

## Osztályok

### `SingletonMeta`

Singleton minta megvalósítására szolgáló metaclass.

Ez a metaclass biztosítja, hogy egy osztályból csak egy példány létezzen. A létrehozott példányokat egy osztályszintű szótárban tárolja, és minden következő példányosításnál ezt adja vissza.

#### Attribútumok

- `_instances`: Osztályszintű szótár, amely tárolja a singleton példányokat. A kulcs az osztály, az érték pedig a létrehozott példány.

#### Metódusok

##### `__call__(cls, *args, **kwargs)`

Singleton példány létrehozása vagy visszaadása.

Ha az osztály még nem szerepel a _instances szótárban, létrehoz egy új példányt és eltárolja. Ellenkező esetben a meglévő példányt adja vissza.

**Paraméterek:**
- `cls`: Az osztály, amelyből példányt szeretnénk létrehozni.
- `*args`: Pozicionális argumentumok az osztály konstruktorához.
- `**kwargs`: Kulcsszavas argumentumok az osztály konstruktorához.

**Visszatérési érték:**
- `T`: A létrehozott vagy meglévő singleton példány.

## Használati Példák

### Alap singleton használat

```python
from neural_ai.core.base.implementations.singleton import SingletonMeta

class MyClass(metaclass=SingletonMeta):
    def __init__(self, value: int):
        self.value = value

# Első példányosítás
obj1 = MyClass(42)

# Második példányosítás - ugyanazt a példányt kapjuk vissza
obj2 = MyClass(100)

# Ellenőrzés
print(obj1 is obj2)  # True
print(obj1.value)    # 42 (az első érték marad)
print(obj2.value)    # 42 (ugyanaz az objektum)
```

### Adatbázis kezelő singleton

```python
from neural_ai.core.base.implementations.singleton import SingletonMeta

class Database(metaclass=SingletonMeta):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = self._create_connection()
        print(f"Adatbázis kapcsolat létrejött: {connection_string}")
    
    def _create_connection(self):
        # Szimulált kapcsolat létrehozás
        return f"Connection to {self.connection_string}"

# Első példányosítás
db1 = Database("sqlite:///mydb.db")
# Kiírja: "Adatbázis kapcsolat létrejött: sqlite:///mydb.db"

# Második példányosítás - nem hoz létre új kapcsolatot
db2 = Database("postgresql://localhost/mydb")
# Nem ír ki semmit, mert ugyanazt a példányt adja vissza

print(db1 is db2)  # True
print(db1.connection_string)  # "sqlite:///mydb.db"
print(db2.connection_string)  # "sqlite:///mydb.db" (az első marad)
```

### Konfiguráció kezelő singleton

```python
from neural_ai.core.base.implementations.singleton import SingletonMeta
import yaml

class ConfigManager(metaclass=SingletonMeta):
    def __init__(self, config_file: str = "config.yml"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def get(self, key: str, default=None):
        return self.config.get(key, default)

# Első példányosítás
config1 = ConfigManager("app_config.yml")

# További példányosítások
config2 = ConfigManager("different_config.yml")
config3 = ConfigManager()

# Mind ugyanazt a példányt adják vissza
print(config1 is config2 is config3)  # True
print(config1.config_file)  # "app_config.yml" (az első marad)
```

### Logger singleton

```python
from neural_ai.core.base.implementations.singleton import SingletonMeta
import logging

class Logger(metaclass=SingletonMeta):
    def __init__(self, name: str = "app", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def error(self, message: str):
        self.logger.error(message)

# Használat
logger1 = Logger(name="my_app")
logger2 = Logger(name="different_app")  # Ugyanazt kapjuk vissza

logger1.info("Ez egy információ")  # A my_app logger írja ki
logger2.error("Ez egy hiba")       # Ugyanaz a logger írja ki
```

## Fontos Megjegyzések

### Konstruktor paraméterek

A singleton minta miatt az első példányosításnál megadott paraméterek maradnak érvényben. A későbbi példányosításoknál megadott paramétereket figyelmen kívül hagyjuk.

```python
class Service(metaclass=SingletonMeta):
    def __init__(self, host: str = "localhost"):
        self.host = host

service1 = Service("api.example.com")
service2 = Service("other.example.com")

print(service1.host)  # "api.example.com"
print(service2.host)  # "api.example.com" (nem "other.example.com")
```

### Szálbiztonság

Az alapvető `SingletonMeta` implementáció nem szálbiztos. Ha szálbiztos singletonra van szükséged, használd a `RLock`-ot a `__call__` metódusban:

```python
import threading
from typing import TypeVar, cast

T = TypeVar("T")

class ThreadSafeSingletonMeta(type):
    _instances: dict[type, object] = {}
    _lock = threading.RLock()
    
    def __call__(cls: type[T], *args: object, **kwargs: object) -> T:
        with cls._lock:
            if cls not in cls._instances:  # type: ignore[attr-defined]
                instance = super().__call__(*args, **kwargs)  # type: ignore[misc]
                cls._instances[cls] = instance  # type: ignore[attr-defined]
        return cast(T, cls._instances[cls])  # type: ignore[attr-defined]
```

### Tesztelés

A singleton osztályok tesztelésekor fontos, hogy a tesztesetek között reseteld a singleton állapotát:

```python
import unittest

class TestSingleton(unittest.TestCase):
    def tearDown(self):
        # Reseteljük a singleton állapotát
        if hasattr(MySingletonClass, '_instances'):
            MySingletonClass._instances.clear()
    
    def test_singleton_pattern(self):
        obj1 = MySingletonClass()
        obj2 = MySingletonClass()
        self.assertIs(obj1, obj2)
```

## Előnyök

1. **Egyetlen példány:** Garantálja, hogy egy osztályból csak egy példány létezik.

2. **Globális hozzáférés:** A singleton példány globálisan elérhető az alkalmazásban.

3. **Lusta inicializálás:** A példány csak az első hozzáféréskor jön létre.

4. **Erőforrás takarékosság:** Megakadályozza a felesleges erőforrás-felhasználást.

## Kapcsolódó Dokumentáció

- [Component Bundle](component_bundle.md)
- [DI Container](di_container.md)
- [Lazy Loader](lazy_loader.md)
- [Base Modul](../__init__.md)