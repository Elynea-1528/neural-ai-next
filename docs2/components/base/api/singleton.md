# Singleton API

## Áttekintés

Ez a dokumentum a Base komponens singleton mintájának API-ját dokumentálja. A singleton minta egy tervezési minta, amely biztosítja, hogy egy osztályból csak egy példány létezhessen, és globális hozzáférési pontot nyújtson hozzá.

## Metaclass: SingletonMeta

```python
class SingletonMeta(type):
    """Metaclass for implementing singleton pattern.

    This metaclass ensures that only one instance of a class exists.
    """
```

### Osztályváltozók

```python
_instances: Dict[type, Any] = {}
```

**Leírás:** Egy osztályszintű szótár, amely tárolja az összes singleton osztály példányait. A kulcs az osztály, az érték pedig a példány.

### __call__

```python
def __call__(cls, *args, **kwargs) -> Any:
    """Create or return the singleton instance."""
```

**Leírás:** Felülírja az osztály meghívását. Amikor egy singleton osztályt példányosítanak, ez a metódus ellenőrzi, hogy már létezik-e példány. Ha igen, visszaadja a meglévőt, ha nem, létrehozza az újat.

**Paraméterek:**
- `cls`: Az osztály, amelyet példányosítani kell
- `*args`: Pozicionális argumentumok
- `**kwargs`: Kulcsszavas argumentumok

**Visszatérési érték:**
- A singleton példány

**Példa:**
```python
from neural_ai.core.base.singleton import SingletonMeta

class MySingleton(metaclass=SingletonMeta):
    def __init__(self, name):
        self.name = name
        print(f"MySingleton létrehozva: {name}")

# Első példányosítás
instance1 = MySingleton("Első")
# Kiírja: "MySingleton létrehozva: Első"

# Második példányosítás (ugyanazt a példányt adja vissza)
instance2 = MySingleton("Második")
# Nem ír ki semmit, mert nem hoz létre új példányt

print(f"Azonos példány: {instance1 is instance2}")  # True
print(f"instance1 neve: {instance1.name}")  # "Első"
print(f"instance2 neve: {instance2.name}")  # "Első" (mert ugyanaz a példány)
```

## Használati módok

### 1. Alapvető singleton osztály

```python
from neural_ai.core.base.singleton import SingletonMeta

class ApplicationConfig(metaclass=SingletonMeta):
    """Alkalmazás konfiguráció singleton."""

    def __init__(self):
        self.settings = {
            'debug': True,
            'log_level': 'INFO',
            'database_url': 'sqlite:///app.db'
        }

    def get_setting(self, key):
        return self.settings.get(key)

    def set_setting(self, key, value):
        self.settings[key] = value

# Használat
config1 = ApplicationConfig()
config2 = ApplicationConfig()

print(f"Azonos konfiguráció: {config1 is config2}")  # True

# Beállítás módosítása
config1.set_setting('debug', False)

# A módosítás mindkét "példányban" látható
print(f"config2 debug mód: {config2.get_setting('debug')}")  # False
```

### 2. Singleton with arguments

```python
from neural_ai.core.base.singleton import SingletonMeta

class DatabaseConnection(metaclass=SingletonMeta):
    """Adatbázis kapcsolat singleton."""

    def __init__(self, host='localhost', port=5432):
        self.host = host
        self.port = port
        self.connection = None
        print(f"DatabaseConnection inicializálva: {host}:{port}")

    def connect(self):
        if self.connection is None:
            print(f"Kapcsolódás a {self.host}:{self.port} címhez")
            # Szimulált kapcsolódás
            self.connection = f"Connection to {self.host}:{self.port}"
        return self.connection

# Első példányosítás
db1 = DatabaseConnection(host='db.example.com', port=5432)
# Kiírja: "DatabaseConnection inicializálva: db.example.com:5432"

# Második példányosítás (figyelmen kívül hagyja az argumentumokat)
db2 = DatabaseConnection(host='other.example.com', port=3306)
# Nem ír ki semmit, és az argumentumokat figyelmen kívül hagyja

print(f"Azonos kapcsolat: {db1 is db2}")  # True
print(f"db2 host: {db2.host}")  # 'db.example.com' (az elsőből)
print(f"db2 port: {db2.port}")  # 5432 (az elsőből)

# Kapcsolódás
conn = db1.connect()
print(conn)  # "Connection to db.example.com:5432"
```

### 3. Thread-safe singleton

```python
from neural_ai.core.base.singleton import SingletonMeta
import threading
import time

class ThreadSafeLogger(metaclass=SingletonMeta):
    """Szálbiztos logger singleton."""

    def __init__(self):
        self.logs = []
        self.lock = threading.Lock()
        print("ThreadSafeLogger létrehozva")

    def log(self, message):
        with self.lock:
            timestamp = time.time()
            self.logs.append((timestamp, message))
            print(f"[{timestamp}] {message}")

def worker(thread_id, logger):
    """Munkás szál."""
    logger.log(f"Szál {thread_id} üzenet")

# Singleton létrehozása a főszálban
logger = ThreadSafeLogger()

# Több szál használja ugyanazt a logger példányt
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i, logger))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Összes log bejegyzés: {len(logger.logs)}")
```

## Speciális használati esetek

### 1. Singleton factory

```python
from neural_ai.core.base.singleton import SingletonMeta

class ComponentFactory(metaclass=SingletonMeta):
    """Komponens factory singleton."""

    def __init__(self):
        self.components = {}
        print("ComponentFactory létrehozva")

    def register_component(self, name, component_class):
        self.components[name] = component_class

    def create_component(self, name, *args, **kwargs):
        if name not in self.components:
            raise ValueError(f"Komponens nem található: {name}")
        return self.components[name](*args, **kwargs)

# Factory létrehozása és használata
factory1 = ComponentFactory()
factory1.register_component('logger', lambda: print("Logger created"))

factory2 = ComponentFactory()
factory2.register_component('database', lambda: print("Database created"))

# Mindkét factory ugyanaz, így mindkét komponens elérhető
print(f"Azonos factory: {factory1 is factory2}")  # True
print(f"Regisztrált komponensek: {list(factory1.components.keys())}")
# ['logger', 'database']
```

### 2. Singleton with lazy initialization

```python
from neural_ai.core.base.singleton import SingletonMeta

class ExpensiveResource(metaclass=SingletonMeta):
    """Drága erőforrás singleton lazy inicializálással."""

    def __init__(self):
        self._initialized = False
        self._resource = None

    def _initialize(self):
        """Lazy inicializálás."""
        if not self._initialized:
            print("Drága erőforrás inicializálása...")
            import time
            time.sleep(2)  # Szimulált drága művelet
            self._resource = "Inicializált erőforrás"
            self._initialized = True

    def get_resource(self):
        """Erőforrás lekérése (lazy)."""
        self._initialize()
        return self._resource

# Singleton létrehozása (még nem inicializálódik)
resource1 = ExpensiveResource()
print("Singleton létrehozva, de még nincs inicializálva")

# Erőforrás lekérése (most inicializálódik)
print("Első erőforrás lekérés:")
data1 = resource1.get_resource()
print(f"Erőforrás: {data1}")

# Második példány
resource2 = ExpensiveResource()
print("Második erőforrás lekérés (már inicializálva van):")
data2 = resource2.get_resource()
print(f"Erőforrás: {data2}")

print(f"Azonos erőforrás: {data1 is data2}")  # True
```

### 3. Singleton with cleanup

```python
from neural_ai.core.base.singleton import SingletonMeta

class ManagedResource(metaclass=SingletonMeta):
    """Singleton erőforrás takarítással."""

    def __init__(self):
        self.resource = "Aktív erőforrás"
        print("ManagedResource létrehozva")

    def cleanup(self):
        """Erőforrás felszabadítása."""
        print("Erőforrás takarítása...")
        self.resource = None

    def __del__(self):
        """Destruktor."""
        if self.resource is not None:
            self.cleanup()

# Használat
resource = ManagedResource()
print(f"Erőforrás: {resource.resource}")

# Explicit takarítás
resource.cleanup()
print(f"Erőforrás takarítás után: {resource.resource}")

# Újra használat (még mindig ugyanaz a példány)
resource2 = ManagedResource()
print(f"Újra használat: {resource2.resource}")  # None
```

## Összehasonlítás más megvalósításokkal

### 1. Metaclass vs. __new__

```python
# Metaclass megvalósítás (ajánlott)
from neural_ai.core.base.singleton import SingletonMeta

class SingletonWithMeta(metaclass=SingletonMeta):
    def __init__(self, value):
        self.value = value

# __new__ megvalósítás (alternatíva)
class SingletonWithNew:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value):
        self.value = value

# Összehasonlítás
singleton1 = SingletonWithMeta("meta")
singleton2 = SingletonWithMeta("meta2")
print(f"Metaclass: {singleton1 is singleton2}")  # True
print(f"Metaclass érték: {singleton2.value}")  # "meta"

singleton3 = SingletonWithNew("new")
singleton4 = SingletonWithNew("new2")
print(f"__new__: {singleton3 is singleton4}")  # True
print(f"__new__ érték: {singleton4.value}")  # "new2" (mert újra inicializálódik)
```

### 2. Metaclass vs. decorator

```python
# Metaclass megvalósítás
from neural_ai.core.base.singleton import SingletonMeta

class SingletonWithMeta(metaclass=SingletonMeta):
    pass

# Decorator megvalósítás
def singleton_decorator(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton_decorator
class SingletonWithDecorator:
    pass

# Összehasonlítás
meta1 = SingletonWithMeta()
meta2 = SingletonWithMeta()
print(f"Metaclass: {meta1 is meta2}")  # True

decorator1 = SingletonWithDecorator()
decorator2 = SingletonWithDecorator()
print(f"Decorator: {decorator1 is decorator2}")  # True
```

## Thread safety

A SingletonMeta alapból szálbiztos, mivel az osztályszintű `_instances` szótár védett:

```python
from neural_ai.core.base.singleton import SingletonMeta
import threading

class ThreadSafeSingleton(metaclass=SingletonMeta):
    def __init__(self):
        import time
        time.sleep(0.1)  # Szimulált lassú inicializálás
        self.value = threading.current_thread().name

def create_singleton(results, thread_id):
    instance = ThreadSafeSingleton()
    results[thread_id] = (instance, instance.value)

# Több szál egyidejű példányosítása
results = {}
threads = []

for i in range(10):
    t = threading.Thread(target=create_singleton, args=(results, i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# Ellenőrzés, hogy minden szál ugyanazt a példányt kapta-e
first_instance = results[0][0]
all_same = all(instance is first_instance for instance, _ in results.values())

print(f"Minden szál ugyanazt a példányt kapta: {all_same}")  # True
print(f"Összes egyedi példány: {len(set(instance for instance, _ in results.values()))}")  # 1
```

## Korlátozások és figyelmeztetések

### 1. Konstruktor argumentumok

```python
from neural_ai.core.base.singleton import SingletonMeta

class ConfigurableSingleton(metaclass=SingletonMeta):
    def __init__(self, config_value):
        self.config_value = config_value

# Első példányosítás
singleton1 = ConfigurableSingleton("first")
print(f"Első érték: {singleton1.config_value}")  # "first"

# Második példányosítás (figyelmen kívül hagyja az argumentumokat)
singleton2 = ConfigurableSingleton("second")
print(f"Második érték: {singleton2.config_value}")  # "first" (nem "second")

print(f"Azonos példány: {singleton1 is singleton2}")  # True
```

**Figyelmeztetés:** A singleton minta miatt a második példányosításnál megadott argumentumokat figyelmen kívül hagyjuk, mert már létezik egy példány.

### 2. Öröklés

```python
from neural_ai.core.base.singleton import SingletonMeta

class BaseSingleton(metaclass=SingletonMeta):
    def __init__(self):
        print(f"BaseSingleton inicializálva")

class DerivedSingleton(BaseSingleton):
    def __init__(self):
        super().__init__()
        print(f"DerivedSingleton inicializálva")

# Használat
base1 = BaseSingleton()
base2 = BaseSingleton()
print(f"Base azonos: {base1 is base2}")  # True

derived1 = DerivedSingleton()
derived2 = DerivedSingleton()
print(f"Derived azonos: {derived1 is derived2}")  # True

# Fontos: Base és Derived különböző singleton-ok
print(f"Base és Derived azonos: {base1 is derived1}")  # False
```

## Hibakezelés

### SingletonViolationError

```python
from neural_ai.core.base.singleton import SingletonMeta
from neural_ai.core.base.exceptions import SingletonViolationError

class StrictSingleton(metaclass=SingletonMeta):
    def __init__(self):
        # Manuális ellenőrzés
        if hasattr(self.__class__, '_instance_created'):
            raise SingletonViolationError("Singleton már létezik")
        self.__class__._instance_created = True

# Első példányosítás
singleton1 = StrictSingleton()

# Második példányosítás (kivételt dob)
try:
    singleton2 = StrictSingleton()
except SingletonViolationError as e:
    print(f"Singleton megsértése: {e}")
```

## Teljesítmény optimalizációk

### 1. Gyors hozzáférés

```python
from neural_ai.core.base.singleton import SingletonMeta
import time

class FastSingleton(metaclass=SingletonMeta):
    def __init__(self):
        self.data = list(range(1000000))

# Első hozzáférés (létrehozza a példányt)
start_time = time.time()
singleton1 = FastSingleton()
end_time = time.time()
print(f"Első hozzáférés ideje: {end_time - start_time:.4f} másodperc")

# Második hozzáférés (azonnal visszaadja a meglévőt)
start_time = time.time()
singleton2 = FastSingleton()
end_time = time.time()
print(f"Második hozzáférés ideje: {end_time - start_time:.6f} másodperc")

print(f"Azonos példány: {singleton1 is singleton2}")  # True
```

### 2. Memóriahatékonyság

```python
from neural_ai.core.base.singleton import SingletonMeta
import sys

class MemoryIntensiveSingleton(metaclass=SingletonMeta):
    def __init__(self):
        self.large_data = [i for i in range(10**7)]  # 10 millió elem

# Csak egy példány létezik, akkor is, ha többször "példányosítjuk"
singleton1 = MemoryIntensiveSingleton()
size1 = sys.getsizeof(singleton1.large_data)

singleton2 = MemoryIntensiveSingleton()
size2 = sys.getsizeof(singleton2.large_data)

print(f"Memóriahasználat: {size1} bájt")
print(f"Ugyanaz az adat: {singleton1.large_data is singleton2.large_data}")  # True
print(f"Összes memóriahasználat: {size1} bájt (nem {size1 * 2})")
```

## Kapcsolódó dokumentáció

- [API Áttekintés](overview.md)
- [CoreComponentFactory API](factory.md) - Singleton használata a Factory-ben
- [DIContainer API](container.md) - Singleton ellenőrzés a konténerben
- [Architektúra áttekintés](../architecture/overview.md)
- [Tervezési minták](../../development/implementation_guide.md)

## Példák

- [Alap használati példák](../examples/basic_usage.md)
- [Haladó példák](../examples/advanced_usage.md)
- [Tesztelési példák](../examples/testing.md)

---

**Dokumentum verzió:** 1.0
**Utolsó frissítés:** 2025-12-19
**Metaclass:** SingletonMeta
