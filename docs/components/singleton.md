# Singleton Metaclass

## Áttekintés

A `SingletonMeta` egy metaklass, amely a singleton tervezési minta megvalósítását biztosítja Pythonban. Ez garantálja, hogy minden osztályból, ami ezt a metaklass-t használja, csak egyetlen példány létezzen az alkalmazás életciklusa során.

## Motiváció

A singleton minta használatának fő okai:

- **Erőforrás-kezelés**: Bizonyos erőforrásokhoz (adatbázis-kapcsolatok, konfigurációk, naplózók) csak egyetlen központi hozzáférési pont szükséges
- **Állapot-menedzsment**: Globális állapot következetes kezelése
- **Memóriahatékonyság**: Többszöri példányosítás elkerülése

## Implementáció

### Osztály definíció

```python
from typing import TypeVar

T = TypeVar('T')


class SingletonMeta(type):
    """Singleton minta megvalósítására szolgáló metaclass.
    
    Ez a metaclass biztosítja, hogy egy osztályból csak egy példány létezzen.
    A létrehozott példányokat egy osztályszintű szótárban tárolja, és minden
    következő példányosításnál ezt adja vissza.
    """
    
    _instances: dict[type, object] = {}
    
    def __call__(cls: type[T], *args: object, **kwargs: object) -> T:
        """Singleton példány létrehozása vagy visszaadása."""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
```

### Attribútumok

| Attribútum | Típus | Leírás |
|------------|-------|---------|
| `_instances` | `dict[type, object]` | Osztályszintű szótár, amely tárolja a singleton példányokat |

### Metódusok

#### `__call__(cls, *args, **kwargs) -> T`

Singleton példány létrehozása vagy visszaadása.

**Paraméterek:**
- `cls`: Az osztály, amelyből példányt szeretnénk létrehozni
- `*args`: Pozicionális argumentumok az osztály konstruktorához
- `**kwargs`: Kulcsszavas argumentumok az osztály konstruktorához

**Visszatérési érték:**
- A létrehozott vagy meglévő singleton példány

## Használat

### Alapvető példa

```python
class Database(metaclass=SingletonMeta):
    """Adatbázis kapcsolat kezelő osztály."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        print(f"Adatbázis kapcsolat létrehozva: {connection_string}")

# Első példányosítás
db1 = Database("sqlite:///mydb.db")
# Output: Adatbázis kapcsolat létrehozva: sqlite:///mydb.db

# Második példányosítás - ugyanazt a példányt kapjuk vissza
db2 = Database("postgresql://localhost/mydb")
# Nincs output, mert nem jön létre új példány

# Ellenőrzés
print(db1 is db2)  # True
print(db1.connection_string)  # 'sqlite:///mydb.db'
```

### Konfiguráció kezelés

```python
class Config(metaclass=SingletonMeta):
    """Alkalmazás konfiguráció kezelő."""
    
    def __init__(self):
        self.settings = {
            'debug': True,
            'log_level': 'INFO',
            'max_connections': 10
        }
    
    def get(self, key: str):
        return self.settings.get(key)

# Mindenhol ugyanaz a konfiguráció példány
config1 = Config()
config2 = Config()

assert config1 is config2
assert config1.get('debug') == config2.get('debug')
```

### Naplózó osztály

```python
class Logger(metaclass=SingletonMeta):
    """Egyszerűsített naplózó osztály."""
    
    def __init__(self, log_file: str = "app.log"):
        self.log_file = log_file
        self.logs = []
    
    def log(self, message: str):
        log_entry = f"[{datetime.now()}] {message}"
        self.logs.append(log_entry)
        print(log_entry)

logger1 = Logger("application.log")
logger2 = Logger("different.log")

# A második példányosítás figyelmen kívül hagyja az új log fájlnevet
print(logger1 is logger2)  # True
print(logger1.log_file)    # 'application.log'
```

## Type Hints és Type Safety

A `SingletonMeta` teljes mértékben támogatja a modern Python type hintseket:

- **Generikus típusok**: `TypeVar('T')` használata a visszatérési típus biztosításához
- **Strict type checking**: Nincs `Any` típus használat
- **Mypy kompatibilitás**: Teljes mértékben kompatibilis a mypy statikus elemzővel

## Tesztelés

A singleton minta tesztelése különleges figyelmet igényel, mivel az osztály állapota megmarad a tesztesetek között.

### Tesztelési stratégiák

1. **Példány egyediség ellenőrzése**
2. **Állapot megőrzésének ellenőrzése**
3. **Többszálú környezetben való viselkedés**

### Példa teszt

```python
import pytest
from neural_ai.core.base.singleton import SingletonMeta


class TestSingleton:
    def test_singleton_creates_only_one_instance(self):
        class TestClass(metaclass=SingletonMeta):
            def __init__(self, value: int):
                self.value = value
        
        instance1 = TestClass(42)
        instance2 = TestClass(100)
        
        assert instance1 is instance2
        assert instance1.value == 42  # Az első érték marad meg
        assert instance2.value == 42
    
    def test_different_classes_create_different_instances(self):
        class ClassA(metaclass=SingletonMeta):
            pass
        
        class ClassB(metaclass=SingletonMeta):
            pass
        
        instance_a = ClassA()
        instance_b = ClassB()
        
        assert instance_a is not instance_b
```

## Előnyök és Hátrányok

### Előnyök

✅ **Kontrollált hozzáférés**: Egyetlen hozzáférési pont az erőforráshoz
✅ **Memóriahatékonyság**: Csak egy példány létezik
✅ **Globális állapot**: Könnyű állapotkezelés
✅ **Lazy initialization**: A példány csak akkor jön létre, amikor először szükség van rá

### Hátrányok

❌ **Tesztelési nehézségek**: Nehéz mockolni vagy cserélni
❌ **Többszálú környezet**: Külön óvintézkedéseket igényel
❌ **Túlságos kötöttség**: Globális állapot függőségeket okozhat
❌ **Életciklus kezelés**: Nehéz lehet a példányt explicit módon felszabadítani

## Alternatívák és Best Practices

### Dependency Injection

A singleton helyett érdemes lehet dependency injection-t használni:

```python
class Database:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

# Alkalmazás szinten egy példány
db_instance = Database("sqlite:///mydb.db")

# Injektálás a függő osztályokba
class UserService:
    def __init__(self, database: Database):
        self.database = database
```

### Modul szintű singleton

Pythonban a modulok alapból singleton-ként viselkednek:

```python
# config.py
class Config:
    def __init__(self):
        self.settings = {...}

config = Config()

# main.py
from config import config  # Mindenhol ugyanaz a példány
```

## Teljesítmény és Biztonság

### Többszálú biztonság

Alapvető implementáció nem biztonságos több szál esetén:

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

### Memória hatékonyság

- **Kis memóriafootprint**: Csak egy példány
- **Lazy loading**: Csak első hozzáféréskor jön létre
- **Automatikus felszabadítás**: A Python GC kezeli

## Kapcsolódó komponensek

- [`Container`](container.md): Dependency injection tároló
- [`Factory`](base_factory.md): Objektum létrehozási minta
- [`Lazy Loading`](lazy_loading.md): Lustán betöltő komponens

## API Referencia

Lásd: [`neural_ai.core.base.singleton`](../../neural_ai/core/base/singleton.py)

## Hibaelhárítás

### Gyakori problémák

1. **Importálási problémák**: Ügyeljünk a körkörös importokra
2. **Tesztelési problémák**: Minden teszt előtt érdemes resetelni a singletonokat
3. **Többszálú környezet**: Használjunk lock mechanizmust

### Debugolás

```python
# Singleton példányok listázása
print(SingletonMeta._instances)

# Példány törlése (csak teszteléshez!)
if SomeClass in SingletonMeta._instances:
    del SingletonMeta._instances[SomeClass]
```

## Jövőbeli fejlesztések

- [ ] Többszálú biztonság beépítése
- [ ] WeakReference alapú implementáció
- [ ] Konfigurálható életciklus kezelés
- [ ] Tesztbarát reset mechanizmus

## Lásd még

- [Singleton tervezési minta](https://en.wikipedia.org/wiki/Singleton_pattern)
- [Python Metaclasses](https://realpython.com/python-metaclasses/)
- [Dependency Injection vs Singleton](../development/dependency_injection.md)