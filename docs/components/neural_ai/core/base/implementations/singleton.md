# Singleton - Singleton Metaclass

## Áttekintés

Ez a modul egy metaclass-t biztosít, amely garantálja, hogy minden osztályból, ami ezt a metaclass-t használja, csak egyetlen példány létezzen az alkalmazás életciklusa során. Ez a singleton tervezési minta szabványos Python implementációja.

## Osztályok

### `SingletonMeta`

**Hely:** [`neural_ai.core.base.implementations.singleton:13`](neural_ai/core/base/implementations/singleton.py:13)

Singleton minta megvalósítására szolgáló metaclass. Ez a metaclass biztosítja, hogy egy osztályból csak egy példány létezzen. A létrehozott példányokat egy osztályszintű szótárban tárolja, és minden következő példányosításnál ezt adja vissza.

#### Attribútumok

- `_instances: dict[type, object]` - Osztályszintű szótár, amely tárolja a singleton példányokat. A kulcs az osztály, az érték pedig a létrehozott példány.

#### Metódusok

##### `__call__(cls: type[T], *args: object, **kwargs: object) -> T`
Singleton példány létrehozása vagy visszaadása.

Ha az osztály még nem szerepel a `_instances` szótárban, létrehoz egy új példányt és eltárolja. Ellenkező esetben a meglévő példányt adja vissza.

**Paraméterek:**
- `cls`: Az osztály, amelyből példányt szeretnénk létrehozni
- `*args`: Pozicionális argumentumok az osztály konstruktorához
- `**kwargs`: Kulcsszavas argumentumok az osztály konstruktorához

**Visszatérési érték:** A létrehozott vagy meglévő singleton példány

## Használat

### Alap használat

```python
from neural_ai.core.base.implementations.singleton import SingletonMeta

class MyClass(metaclass=SingletonMeta):
    def __init__(self, value: int):
        self.value = value

# Első példányosítás
obj1 = MyClass(42)
print(obj1.value)  # 42

# Második példányosítás - ugyanazt a példányt kapjuk vissza
obj2 = MyClass(100)
print(obj2.value)  # 42 (nem 100!)

# Ellenőrzés, hogy tényleg ugyanaz a példány
print(obj1 is obj2)  # True
```

### Adatbázis kapcsolat

```python
from neural_ai.core.base.implementations.singleton import SingletonMeta
import sqlite3

class Database(metaclass=SingletonMeta):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = sqlite3.connect(connection_string)
        print(f"Adatbázis kapcsolat létrehozva: {connection_string}")
    
    def query(self, sql: str):
        return self.connection.execute(sql).fetchall()

# Első kapcsolat létrehozása
db1 = Database("sqlite:///mydb.db")
# Kimenet: "Adatbázis kapcsolat létrehozva: sqlite:///mydb.db"

# Második "példányosítás" - ugyanazt a kapcsolatot kapjuk
db2 = Database("postgresql://localhost/mydb")
# Nincs kimenet, mert nem jön létre új kapcsolat

print(db1 is db2)  # True
print(db1.connection_string)  # "sqlite:///mydb.db"
print(db2.connection_string)  # "sqlite:///mydb.db" (nem a postgres!)
```

### Konfiguráció kezelő

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

# Bárhol a kódban, mindig ugyanazt a példányt kapjuk
config2 = ConfigManager("different_config.yml")  # Figyelmen kívül hagyja az új fájlt

print(config1 is config2)  # True
print(config1.config_file)  # "app_config.yml"
print(config2.config_file)  # "app_config.yml"
```

### Logger osztály

```python
from neural_ai.core.base.implementations.singleton import SingletonMeta
import logging

class AppLogger(metaclass=SingletonMeta):
    def __init__(self, name: str = "app", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Handler beállítása
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

# Különböző modulokban
logger1 = AppLogger(name="my_app")
logger2 = AppLogger(name="different_app")  # Ugyanaz a logger

logger1.info("Üzenet az első loggertől")
logger2.error("Hiba a második loggertől")  # Mindkettő ugyanahhoz a logger példányhoz ír
```

## Fontos megjegyzések

### Konstruktor paraméterek

A singleton minta miatt az első példányosításnál megadott paraméterek maradnak érvényben. A későbbi példányosításoknál megadott paramétereket figyelmen kívül hagyjuk.

```python
class Example(metaclass=SingletonMeta):
    def __init__(self, value: str):
        self.value = value

obj1 = Example("első")
obj2 = Example("második")

print(obj1.value)  # "első"
print(obj2.value)  # "első" (nem "második"!)
```

### Öröklés

A singleton minta öröklődik, de minden alosztály külön singleton lesz:

```python
class BaseClass(metaclass=SingletonMeta):
    pass

class ChildClass(BaseClass):
    pass

base1 = BaseClass()
base2 = BaseClass()
child1 = ChildClass()
child2 = ChildClass()

print(base1 is base2)  # True
print(child1 is child2)  # True
print(base1 is child1)  # False - különböző osztályok
```

### Szálbiztosság

Ez az alap implementáció nem szálbiztos. Ha szálbiztos singletonra van szükséged, használd a szálzárást:

```python
import threading

class ThreadSafeSingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
```

## Függőségek

- `typing.TypeVar` - Generikus típusokhoz
- `typing.cast` - Típus konverzióhoz

## Előnyök

1. **Egyetlen példány:** Garantálja, hogy egy osztályból csak egy példány létezik
2. **Globális hozzáférés:** Könnyű hozzáférés az alkalmazás bármely pontjáról
3. **Erőforrás takarékosság:** Megelőzi a felesleges erőforrás felhasználást
4. **Konzisztencia:** Biztosítja, hogy mindenhol ugyanazt a példányt használjuk

## Korlátozások

1. **Tesztelés nehézség:** A singletonok nehezen tesztelhetőek, mert globális állapotot tartanak
2. **Függőség rejtés:** Elrejti az osztály függőségeit
3. **Párhuzamos hozzáférés:** Alap implementáció nem szálbiztos

## Alternatívák

- **Dependency Injection:** Használj DI konténert a példányok kezelésére
- **Modul szintű változók:** Pythonban a modulok is singletonok
- **Borg minta:** Minden példány megosztja az állapotot, de külön példányok

## Kapcsolódó dokumentáció

- [DI Container](neural_ai/core/base/implementations/di_container.md) - Ahol a singleton pattern ellenőrzése történik
- [Core Component Factory](neural_ai/core/base/factory.md) - Ahol a SingletonMeta használatos
- [Component Bundle](neural_ai/core/base/implementations/component_bundle.md) - Komponens életciklus kezelés