# Singleton Meta

## Áttekintés

A `SingletonMeta` egy metaklass, amely a singleton tervezési minta megvalósítását biztosítja. Ez a minta garantálja, hogy egy osztályból az alkalmazás életciklusa során csak egyetlen példány létezzen.

## Motiváció

A singleton minta hasznos olyan esetekben, amikor:
- Egy erőforráshoz (pl. adatbázis kapcsolat, konfiguráció) globális hozzáférésre van szükség
- Többszöri példányosítás költséges lenne
- Szeretnénk garantálni, hogy csak egyetlen példány osztozzon az állapoton

## Osztályok

### SingletonMeta

```python
class SingletonMeta(type):
    """Singleton minta megvalósítására szolgáló metaclass."""
    
    _instances: dict[type, object] = {}
```

**Attribútumok:**
- `_instances`: Osztályszintű szótár, amely tárolja a singleton példányokat. A kulcs az osztály, az érték pedig a létrehozott példány.

**Metódusok:**

#### `__call__(cls, *args, **kwargs) -> T`

Singleton példány létrehozása vagy visszaadása.

**Paraméterek:**
- `cls`: Az osztály, amelyből példányt szeretnénk létrehozni
- `*args`: Pozicionális argumentumok az osztály konstruktorához
- `**kwargs`: Kulcsszavas argumentumok az osztály konstruktorához

**Visszatérési érték:**
A létrehozott vagy meglévő singleton példány.

**Működés:**
1. Ellenőrzi, hogy az osztály szerepel-e már a `_instances` szótárban
2. Ha nem, létrehoz egy új példányt és eltárolja
3. Ha igen, a meglévő példányt adja vissza

## Használat

### Alapvető használat

```python
from neural_ai.core.base.singleton import SingletonMeta

class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = self._create_connection()
    
    def _create_connection(self):
        # Kapcsolat létrehozása
        pass

# Első példányosítás
db1 = DatabaseConnection("sqlite:///mydb.db")

# További példányosítások ugyanazt a példányt adják vissza
db2 = DatabaseConnection("postgresql://localhost/mydb")

assert db1 is db2  # True
assert db1.connection_string == "sqlite:///mydb.db"  # Az első érték marad
```

### Konfiguráció kezelés

```python
class ConfigManager(metaclass=SingletonMeta):
    def __init__(self, config_file: str = "config.yaml"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        # Konfiguráció betöltése
        pass
    
    def get(self, key: str):
        return self.config.get(key)

# Bárhol használhatjuk, mindig ugyanazt a példányt kapjuk
config1 = ConfigManager()
config2 = ConfigManager()

assert config1 is config2
```

### Logger implementáció

```python
class Logger(metaclass=SingletonMeta):
    def __init__(self, log_file: str = "app.log"):
        self.log_file = log_file
        self._setup_logger()
    
    def _setup_logger(self):
        # Logger beállítása
        pass
    
    def log(self, message: str):
        # Üzenet naplózása
        pass

# Globális logger használata
logger = Logger()
logger.log("Alkalmazás elindult")
```

## Előnyök

1. **Egyszeri példányosítás:** Garantálja, hogy csak egy példány létezik
2. **Globális hozzáférés:** Könnyű hozzáférés az egész alkalmazásban
3. **Lazy initialization:** A példány csak akkor jön létre, amikor először használják
4. **Erőforrás takarékosság:** Megelőzi a felesleges erőforrás-felhasználást

## Korlátozások

1. **Tesztelhetőség:** Nehezebb egységteszteket írni singleton osztályokra
2. **Párhuzamos hozzáférés:** Szálbiztonságot külön kell kezelni
3. **Függőségi injektálás:** Nehezebb a függőségek injektálása

## Szálbiztonság

Az alapvető implementáció nem szálbiztos. Többszálú környezetben szinkronizációt kell használni:

```python
import threading

class ThreadSafeSingletonMeta(type):
    _instances: dict[type, object] = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
```

## Tesztelés

A singleton osztályok tesztelésénél fontos figyelembe venni:

1. **Példányok törlése:** Tesztek között érdemes törölni a singleton példányokat
2. **Elkülönítés:** Minden teszt független legyen a többitől
3. **Mockolás:** Használjunk mock objektumokat a függőségek helyett

```python
# Teszteléskor érdemes lehet törölni a példányokat
class TestSingleton:
    def test_singleton_behavior(self):
        # Előző tesztek példányainak törlése
        if hasattr(MySingletonClass, '_instances'):
            MySingletonClass._instances.clear()
        
        # Teszt logika
        instance1 = MySingletonClass()
        instance2 = MySingletonClass()
        assert instance1 is instance2
```

## Kapcsolódó komponensek

- [`DIContainer`](container.md): Dependency injection konténer, amely támogatja a singleton életciklust
- [`LazyLoader`](lazy_loading.md): Késleltetett betöltést biztosító komponens
- [`CoreComponents`](core_components.md): Alap komponensek, amelyek singleton-ként működnek

## Hibaelhárítás

### Többszörös példányosítás problémája

**Probléma:** Több példány jön létre a vártnál.

**Megoldás:**
- Ellenőrizd, hogy mindenhol ugyanazt az osztályt használod-e
- Nézd át az öröklődési hierarchiát
- Használj metaklass-ot minden singleton osztályhoz

### Memóriaszivárgás

**Probléma:** A singleton példányok nem szabadulnak fel.

**Megoldás:**
- Implementálj egy `cleanup` metódust
- Használj gyenge referenciákat speciális esetekben
- Ügyelj a körkörös referenciákra

## Jövőbeli fejlesztések

1. **Szálbiztos implementáció:** Alapértelmezett szálbiztonság biztosítása
2. **Életciklus kezelés:** Explicit cleanup mechanizmus
3. **Konfigurálható viselkedés:** Lehessen kikapcsolni a singleton viselkedést teszteléshez
4. **Dependency injection integráció:** Jobb integráció a DI konténerrel

## Lásd még

- [Singleton tervezési minta](https://en.wikipedia.org/wiki/Singleton_pattern)
- [Python metaklass-ok](https://realpython.com/python-metaclasses/)
- [Dependency Injection](../container.md)