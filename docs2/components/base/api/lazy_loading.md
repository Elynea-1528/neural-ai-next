# Lazy Loading API

## Áttekintés

Ez a dokumentum a Base komponens lazy loading mechanizmusának API-ját dokumentálja. A lazy loading (lustabetöltés) egy optimalizációs technika, amely lehetővé teszi, hogy a drága erőforrások csak akkor töltődjenek be, amikor valóban szükség van rájuk.

## Osztály: LazyLoader

```python
class LazyLoader(Generic[T]):
    """Lazy loader for expensive resources."""
```

### Konstruktor

```python
def __init__(self, loader_func: Callable[[], T]) -> None:
    """Initialize lazy loader.

    Args:
        loader_func: Function to call when loading the resource
    """
```

**Leírás:** Létrehoz egy új LazyLoader példányt a megadott betöltő függvénnyel.

**Paraméterek:**
- `loader_func`: A függvény, amely betölti az erőforrást. Ennek a függvénynek vissza kell térnie a betöltött erőforrással.

**Visszatérési érték:**
- Egy új `LazyLoader` példány

**Példa:**
```python
from neural_ai.core.base.lazy_loading import LazyLoader
import time

def load_expensive_config():
    """Drága konfiguráció betöltése."""
    print("Konfiguráció betöltése...")
    time.sleep(2)  # Szimulált drága művelet
    return {"setting": "value", "timeout": 30}

# Lazy loader létrehozása
config_loader = LazyLoader(load_expensive_config)
print("Lazy loader létrehozva, de a konfiguráció még nincs betöltve")
```

### _load

```python
def _load(self) -> T:
    """Load the resource if not already loaded."""
```

**Leírás:** Belső metódus az erőforrás betöltéséhez. Szálbiztos művelet, amely biztosítja, hogy az erőforrás csak egyszer töltődjön be.

**Visszatérési érték:**
- A betöltött erőforrás

**Megjegyzés:** Ez egy belső metódus, általában nem kell közvetlenül használni. Ehelyett használd a `__call__` metódust.

### __call__

```python
def __call__(self) -> T:
    """Get the loaded resource."""
```

**Leírás:** Visszaadja a betöltött erőforrást. Ha az erőforrás még nincs betöltve, először meghívja a betöltő függvényt.

**Visszatérési érték:**
- A betöltött erőforrás

**Példa:**
```python
from neural_ai.core.base.lazy_loading import LazyLoader

def load_database_connection():
    print("Adatbázis kapcsolat létrehozása...")
    return DatabaseConnection()

# Lazy loader létrehozása
db_loader = LazyLoader(load_database_connection)

# Erőforrás használata (csak most töltődik be)
print("Első hozzáférés:")
connection = db_loader()  # Kiírja: "Adatbázis kapcsolat létrehozása..."
print(f"Betöltve: {db_loader.is_loaded}")  # True

# Második hozzáférés (már betöltve van)
print("Második hozzáférés:")
connection2 = db_loader()  # Nem ír ki semmit, már betöltve van
print(f"Azonos objektum: {connection is connection2}")  # True
```

### is_loaded

```python
@property
def is_loaded(self) -> bool:
    """Check if the resource is loaded."""
```

**Leírás:** Visszaadja az erőforrás betöltöttségi állapotát.

**Visszatérési érték:**
- `True`, ha az erőforrás betöltve van
- `False`, ha még nincs betöltve

**Példa:**
```python
from neural_ai.core.base.lazy_loading import LazyLoader

def load_config():
    return {"setting": "value"}

loader = LazyLoader(load_config)

print(f"Kezdeti állapot: {loader.is_loaded}")  # False

# Erőforrás használata
config = loader()

print(f"Használat után: {loader.is_loaded}")  # True
```

### reset

```python
def reset(self) -> None:
    """Reset the loader to unload the resource."""
```

**Leírás:** Visszaállítja a betöltőt az alaphelyzetbe, kitéve a betöltött erőforrást. Ez hasznos lehet tesztelés során vagy ha újra szeretnénk tölteni az erőforrást.

**Példa:**
```python
from neural_ai.core.base.lazy_loading import LazyLoader

def load_settings():
    print("Beállítások betöltése...")
    return {"theme": "dark", "language": "hu"}

loader = LazyLoader(load_settings)

# Első betöltés
print("Első betöltés:")
settings1 = loader()
print(f"Betöltve: {loader.is_loaded}")  # True

# Reset
print("\nReset:")
loader.reset()
print(f"Betöltve: {loader.is_loaded}")  # False

# Újra betöltés
print("\nÚjra betöltés:")
settings2 = loader()
print(f"Betöltve: {loader.is_loaded}")  # True
```

## Dekorátor: lazy_property

```python
def lazy_property(func: Callable[..., T]) -> property:
    """Decorator for lazy-loaded properties."""
```

**Leírás:** Egy dekorátor, amely lazy-loaded property-t hoz létre. A property értéke csak az első hozzáféréskor számolódik ki, majd gyorsítótárba kerül.

**Paraméterek:**
- `func`: A függvény, amely kiszámolja a property értékét

**Visszatérési érték:**
- Egy property objektum lazy loadinggel

**Példa:**
```python
from neural_ai.core.base.lazy_loading import lazy_property
import time

class ExpensiveDataProcessor:
    def __init__(self, data):
        self._data = data

    @lazy_property
    def processed_data(self):
        """Drága adatfeldolgozás - csak egyszer fut le."""
        print("Adatok feldolgozása...")
        time.sleep(3)  # Szimulált drága művelet
        return [x * 2 for x in self._data]

    @lazy_property
    def statistics(self):
        """Statisztikák számítása - csak egyszer fut le."""
        print("Statisztikák számítása...")
        time.sleep(2)
        return {
            'count': len(self._data),
            'sum': sum(self._data),
            'avg': sum(self._data) / len(self._data)
        }

# Használat
processor = ExpensiveDataProcessor(list(range(1000000)))

print("Első hozzáférés a processed_data-hoz:")
data1 = processor.processed_data  # Kiírja: "Adatok feldolgozása..." és vár 3 másodpercet
print(f"Adatok száma: {len(data1)}")

print("\nMásodik hozzáférés a processed_data-hoz:")
data2 = processor.processed_data  # Nem ír ki semmit, azonnal visszaadja
print(f"Azonos adatok: {data1 is data2}")  # True

print("\nElső hozzáférés a statistics-hoz:")
stats1 = processor.statistics  # Kiírja: "Statisztikák számítása..." és vár 2 másodpercet
print(f"Statisztikák: {stats1}")

print("\nMásodik hozzáférés a statistics-hoz:")
stats2 = processor.statistics  # Nem ír ki semmit, azonnal visszaadja
print(f"Azonos statisztikák: {stats1 is stats2}")  # True
```

## Használati minták

### 1. Alapvető lazy loading

```python
from neural_ai.core.base.lazy_loading import LazyLoader
import time

def load_application_config():
    """Alkalmazás konfigurációjának betöltése."""
    print("Konfiguráció betöltése fájlból...")
    time.sleep(2)  # Szimulált fájl I/O
    return {
        'database': {'host': 'localhost', 'port': 5432},
        'logging': {'level': 'INFO', 'file': 'app.log'},
        'cache': {'enabled': True, 'ttl': 3600}
    }

# Lazy loader létrehozása
config_loader = LazyLoader(load_application_config)

print("Alkalmazás indítása...")
print("Konfiguráció még nincs betöltve")

# Amikor először szükség van a konfigurációra
print("\nElső konfiguráció hozzáférés:")
config = config_loader()  # Most töltődik be
print(f"Adatbázis hoszt: {config['database']['host']}")

# Későbbi hozzáférések már gyorsak
print("\nKésőbbi hozzáférés:")
config2 = config_loader()  # Azonnal visszaadja
print(f"Gyorsítótárban: {config is config2}")
```

### 2. Lazy loading több erőforrással

```python
from neural_ai.core.base.lazy_loading import LazyLoader
import time

class ResourceManager:
    def __init__(self):
        # Több erőforrás lazy loader-e
        self._config_loader = LazyLoader(self._load_config)
        self._database_loader = LazyLoader(self._load_database)
        self._cache_loader = LazyLoader(self._load_cache)

    def _load_config(self):
        print("Konfiguráció betöltése...")
        time.sleep(1)
        return {"setting": "value"}

    def _load_database(self):
        print("Adatbázis kapcsolat létrehozása...")
        time.sleep(2)
        return DatabaseConnection()

    def _load_cache(self):
        print("Gyorsítótár inicializálása...")
        time.sleep(1)
        return Cache()

    @property
    def config(self):
        return self._config_loader()

    @property
    def database(self):
        return self._database_loader()

    @property
    def cache(self):
        return self._cache_loader()

# Használat
manager = ResourceManager()

print("Alkalmazás indítása...")
print("Még egyik erőforrás sincs betöltve")

# Csak a szükséges erőforrások betöltése
print("\nKonfiguráció használata:")
config = manager.config  # Most töltődik be a konfiguráció

print("\nAdatbázis használata:")
db = manager.database  # Most töltődik be az adatbázis kapcsolat

# A cache-re még nincs szükség, így az nem töltődik be
print(f"\nÁllapotok:")
print(f"Config betöltve: {manager._config_loader.is_loaded}")
print(f"Database betöltve: {manager._database_loader.is_loaded}")
print(f"Cache betöltve: {manager._cache_loader.is_loaded}")
```

### 3. Lazy property használata

```python
from neural_ai.core.base.lazy_loading import lazy_property
import time

class DataAnalyzer:
    def __init__(self, dataset):
        self.dataset = dataset

    @lazy_property
    def mean(self):
        """Átlag számítása - csak egyszer."""
        print("Átlag számítása...")
        time.sleep(1)
        return sum(self.dataset) / len(self.dataset)

    @lazy_property
    def variance(self):
        """Variancia számítása - csak egyszer."""
        print("Variancia számítása...")
        time.sleep(1)
        mean = self.mean  # Használhatjuk a másik lazy property-t
        return sum((x - mean) ** 2 for x in self.dataset) / len(self.dataset)

    @lazy_property
    def std_dev(self):
        """Szórás számítása - csak egyszer."""
        print("Szórás számítása...")
        time.sleep(1)
        return self.variance ** 0.5

# Használat
data = list(range(1, 1000001))
analyzer = DataAnalyzer(data)

print("Adatok betöltve, de statisztikák még nincsenek kiszámolva")

print("\nÁtlag lekérése:")
avg = analyzer.mean  # Most számolódik ki

print("\nVariancia lekérése:")
var = analyzer.variance  # Most számolódik ki (és használja az átlagot)

print("\nSzórás lekérése:")
std = analyzer.std_dev  # Most számolódik ki (és használja a varianciát)

print(f"\nEredmények:")
print(f"Átlag: {avg}")
print(f"Variancia: {var}")
print(f"Szórás: {std}")

# Második hozzáférések már gyorsak
print("\nMásodik hozzáférések (már gyorsítótárból):")
avg2 = analyzer.mean  # Azonnal
var2 = analyzer.variance  # Azonnal
std2 = analyzer.std_dev  # Azonnal
```

### 4. Tesztelés lazy loader reseteléssel

```python
from neural_ai.core.base.lazy_loading import LazyLoader
import time

def create_expensive_resource():
    """Drága erőforrás létrehozása."""
    print("Erőforrás létrehozása...")
    time.sleep(2)
    return {"id": id( object()), "data": "expensive"}

# Lazy loader létrehozása
loader = LazyLoader(create_expensive_resource)

print("=== 1. Teszt futtatása ===")
resource1 = loader()
print(f"Resource ID: {resource1['id']}")
print(f"Betöltve: {loader.is_loaded}")

print("\n=== Reset ===")
loader.reset()
print(f"Betöltve: {loader.is_loaded}")

print("\n=== 2. Teszt futtatása ===")
resource2 = loader()
print(f"Resource ID: {resource2['id']}")
print(f"Betöltve: {loader.is_loaded}")

print(f"\n=== Összehasonlítás ===")
print(f"Különböző erőforrások: {resource1['id'] != resource2['id']}")
```

### 5. Thread safe használat

```python
from neural_ai.core.base.lazy_loading import LazyLoader
import threading
import time

def load_shared_resource():
    """Megosztott erőforrás betöltése."""
    print(f"Erőforrás betöltése a {threading.current_thread().name} szálban")
    time.sleep(1)
    return {"loaded_by": threading.current_thread().name, "timestamp": time.time()}

# Lazy loader létrehozása
shared_loader = LazyLoader(load_shared_resource)

def worker(thread_id):
    """Munkás szál."""
    print(f"Szál {thread_id} elindult")
    time.sleep(0.1 * thread_id)  # Kis késleltetés

    # Erőforrás használata
    resource = shared_loader()
    print(f"Szál {thread_id} használja az erőforrást: {resource}")

# Több szál indítása
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,), name=f"Worker-{i}")
    threads.append(t)
    t.start()

# Várakozás a szálak befejezésére
for t in threads:
    t.join()

print("Minden szál befejezte a munkát")
print(f"Erőforrás végül betöltve: {shared_loader.is_loaded}")
```

## Teljesítmény optimalizációk

### 1. Memóriahatékonyság

A lazy loading optimalizálja a memóriahasználatot:

```python
from neural_ai.core.base.lazy_loading import LazyLoader

class MemoryIntensiveApp:
    def __init__(self):
        self._large_data_loader = LazyLoader(self._load_large_data)

    def _load_large_data(self):
        print("Nagy adathalmaz betöltése...")
        # Ez csak akkor fut le, ha tényleg szükség van rá
        return [i for i in range(10**7)]  # 10 millió elem

    def process_data(self):
        # Csak akkor töltődik be, ha meghívják ezt a metódust
        data = self._large_data_loader()
        return sum(data)

app = MemoryIntensiveApp()
print("Alkalmazás létrehozva, de a nagy adathalmaz még nincs a memóriában")

# Csak ha tényleg szükség van rá
if user_wants_processing:
    result = app.process_data()  # Most töltődik be
    print(f"Eredmény: {result}")
```

### 2. Gyors indítási idő

```python
from neural_ai.core.base.lazy_loading import LazyLoader
import time

def load_all_plugins():
    """Összes plugin betöltése."""
    print("Plugin-ek betöltése...")
    time.sleep(3)
    return ["plugin1", "plugin2", "plugin3"]

# Alkalmazás indítása
start_time = time.time()

# Lazy loader létrehozása
plugin_loader = LazyLoader(load_all_plugins)

end_time = time.time()
print(f"Alkalmazás indítási ideje: {end_time - start_time:.2f} másodperc")
print("Plugin-ek még nincsenek betöltve, de az alkalmazás már fut")

# Plugin-ek csak akkor töltődnek be, ha szükség van rájuk
if user_requests_plugins:
    plugins = plugin_loader()
    print(f"Plugin-ek betöltve: {plugins}")
```

## Hibakezelés

### Hibák lazy loading során

```python
from neural_ai.core.base.lazy_loading import LazyLoader

def load_config_with_errors():
    """Konfiguráció betöltése hibák esetén."""
    import random
    if random.random() < 0.3:
        raise ValueError("Konfigurációs fájl sérült")
    return {"setting": "value"}

loader = LazyLoader(load_config_with_errors)

try:
    config = loader()
    print("Konfiguráció sikeresen betöltve")
except ValueError as e:
    print(f"Hiba a betöltés során: {e}")
    # Reset és újrapróbálkozás
    loader.reset()
    try:
        config = loader()
        print("Konfiguráció sikeresen betöltve második próbálkozásra")
    except ValueError as e:
        print(f"Második hiba is történt: {e}")
        # Alapértelmezett konfiguráció
        config = {"setting": "default"}
```

## Kapcsolódó dokumentáció

- [API Áttekintés](overview.md)
- [CoreComponents API](core_components.md) - LazyLoader használata a CoreComponents-ben
- [CoreComponentFactory API](factory.md) - Lazy loading a Factory-ben
- [Architektúra áttekintés](../architecture/overview.md)
- [Teljesítmény optimalizációk](../../development/performance_optimization.md)

## Példák

- [Alap használati példák](../examples/basic_usage.md)
- [Haladó példák](../examples/advanced_usage.md)
- [Tesztelési példák](../examples/testing.md)

---

**Dokumentum verzió:** 1.0
**Utolsó frissítés:** 2025-12-19
**Osztály:** LazyLoader, lazy_property
