# CoreComponents API

## Áttekintés

A `CoreComponents` osztály a Neural AI Next projekt core komponenseinek egységes kezeléséért felelős. Ez az osztály biztosítja a logger, config és storage komponensek egységes elérését lazy loadinggel.

## Osztály: CoreComponents

```python
class CoreComponents:
    """Core components with lazy loading support."""
```

### Konstruktor

```python
def __init__(self, container: Optional[DIContainer] = None):
    """Initialize core components."""
```

**Leírás:** Létrehoz egy új CoreComponents példányt a megadott konténerrel vagy egy új konténerrel.

**Paraméterek:**
- `container`: Egy opcionális DIContainer példány. Ha nincs megadva, létrehoz egy újat.

**Példa:**
```python
from neural_ai.core.base import CoreComponents, DIContainer

# 1. Új konténerrel
components = CoreComponents()

# 2. Meglévő konténerrel
container = DIContainer()
components = CoreComponents(container=container)
```

## Tulajdonságok

### config

```python
@property
def config(self) -> Optional[ConfigManagerInterface]:
    """Get config manager (lazy-loaded)."""
```

**Leírás:** Visszaadja a konfiguráció kezelő komponenst. A komponens lazy-loaded, azaz csak akkor töltődik be, amikor először használják.

**Visszatérési érték:**
- A konfiguráció kezelő példánya, ha elérhető
- `None`, ha a komponens nem elérhető

**Példa:**
```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path='configs/app_config.yaml'
)

# Konfiguráció használata (csak most töltődik be)
if components.has_config():
    app_settings = components.config.get_section('app')
    print(f"App name: {app_settings.get('name')}")
```

### logger

```python
@property
def logger(self) -> Optional[LoggerInterface]:
    """Get logger (lazy-loaded)."""
```

**Leírás:** Visszaadja a naplózó komponenst. A komponens lazy-loaded, azaz csak akkor töltődik be, amikor először használják.

**Visszatérési érték:**
- A naplózó példánya, ha elérhető
- `None`, ha a komponens nem elérhető

**Példa:**
```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    log_path='logs/app.log'
)

# Naplózás (csak most töltődik be a logger)
if components.has_logger():
    components.logger.info("Alkalmazás elindult")
    components.logger.debug("Részletes hibakeresési információ")
```

### storage

```python
@property
def storage(self) -> Optional[StorageInterface]:
    """Get storage (lazy-loaded)."""
```

**Leírás:** Visszaadja a tároló komponenst. A komponens lazy-loaded, azaz csak akkor töltődik be, amikor először használják.

**Visszatérési érték:**
- A tároló példánya, ha elérhető
- `None`, ha a komponens nem elérhető

**Példa:**
```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    storage_path='./data'
)

# Adatok mentése (csak most töltődik be a storage)
if components.has_storage():
    data = {"key": "value", "number": 42}
    components.storage.save_object(data, "test_data.json")

    # Adatok betöltése
    loaded_data = components.storage.load_object("test_data.json")
    print(loaded_data)  # {'key': 'value', 'number': 42}
```

## Metódusok

### preload_all

```python
def preload_all(self) -> None:
    """Preload all components."""
```

**Leírás:** Előzetesen betölti az összes komponenst, még mielőtt szükség lenne rájuk. Ez hasznos lehet, ha szeretnénk elkerülni a késleltetést az első használatkor.

**Példa:**
```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path='config.yaml',
    log_path='app.log',
    storage_path='./data'
)

# Összes komponens előtöltése
components.preload_all()

# Most minden komponens azonnal elérhető
components.logger.info("Minden komponens betöltve")
settings = components.config.get_section('app')
components.storage.save_object({}, "init.json")
```

### has_config

```python
def has_config(self) -> bool:
    """Ellenőrzi, hogy van-e config komponens.

    Returns:
        bool: True ha van config komponens, False ha nincs
    """
```

**Leírás:** Ellenőrzi, hogy a konfiguráció kezelő komponens elérhető-e.

**Visszatérési érték:**
- `True`, ha a konfiguráció kezelő elérhető
- `False`, ha nem elérhető

**Példa:**
```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása konfiguráció nélkül
components = CoreComponentFactory.create_minimal()

# Konfiguráció ellenőrzése
if components.has_config():
    print("Konfiguráció elérhető")
else:
    print("Konfiguráció nem elérhető")
```

### has_logger

```python
def has_logger(self) -> bool:
    """Ellenőrzi, hogy van-e logger komponens.

    Returns:
        bool: True ha van logger komponens, False ha nincs
    """
```

**Leírás:** Ellenőrzi, hogy a naplózó komponens elérhető-e.

**Visszatérési érték:**
- `True`, ha a naplózó elérhető
- `False`, ha nem elérhető

**Példa:**
```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(log_path='app.log')

# Logger ellenőrzése
if components.has_logger():
    components.logger.info("Logger elérhető")
else:
    print("Logger nem elérhető, használj konzol kiírást")
```

### has_storage

```python
def has_storage(self) -> bool:
    """Ellenőrzi, hogy van-e storage komponens.

    Returns:
        bool: True ha van storage komponens, False ha nincs
    """
```

**Leírás:** Ellenőrzi, hogy a tároló komponens elérhető-e.

**Visszatérési érték:**
- `True`, ha a tároló elérhető
- `False`, ha nem elérhető

**Példa:**
```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(storage_path='./data')

# Storage ellenőrzése
if components.has_storage():
    components.storage.save_object({"test": "data"}, "test.json")
else:
    print("Storage nem elérhető, adatok nem menthetők")
```

### validate

```python
def validate(self) -> bool:
    """Ellenőrzi, hogy minden szükséges komponens megvan-e.

    Returns:
        bool: True ha minden komponens megvan, False ha valamelyik hiányzik
    """
```

**Leírás:** Ellenőrzi, hogy az összes alapvető komponens (config, logger, storage) elérhető-e.

**Visszatérési érték:**
- `True`, ha minden komponens elérhető
- `False`, ha legalább egy komponens hiányzik

**Példa:**
```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path='config.yaml',
    log_path='app.log',
    storage_path='./data'
)

# Komponensek validálása
if components.validate():
    print("Minden komponens elérhető, az alkalmazás készen áll")
else:
    print("Figyelmeztetés: néhány komponens hiányzik")
    if not components.has_config():
        print("  - Konfiguráció hiányzik")
    if not components.has_logger():
        print("  - Logger hiányzik")
    if not components.has_storage():
        print("  - Storage hiányzik")
```

## Belső metódusok

### _register_lazy_components

```python
def _register_lazy_components(self) -> None:
    """Register all core components as lazy-loaded."""
```

**Leírás:** Regisztrálja az összes core komponenst lazy-loaded módon a konténerben. Ez a metódus automatikusan meghívódik a konstruktorban.

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
- `loader_func`: A függvény, amely betölti az erőforrást

**Példa:**
```python
from neural_ai.core.base.lazy_loading import LazyLoader

def load_expensive_config():
    print("Drága konfiguráció betöltése...")
    time.sleep(2)  # Szimulált drága művelet
    return {"setting": "value"}

# Lazy loader létrehozása
config_loader = LazyLoader(load_expensive_config)
```

### _load

```python
def _load(self) -> T:
    """Load the resource if not already loaded."""
```

**Leírás:** Betölti az erőforrást, ha még nincs betöltve. Szálbiztos művelet.

**Visszatérési érték:**
- A betöltött erőforrás

### __call__

```python
def __call__(self) -> T:
    """Get the loaded resource."""
```

**Leírás:** Visszaadja a betöltött erőforrást. Ha még nincs betöltve, először betölti.

**Visszatérési érték:**
- A betöltött erőforrás

**Példa:**
```python
from neural_ai.core.base.lazy_loading import LazyLoader

def load_config():
    return {"setting": "value"}

loader = LazyLoader(load_config)

# Erőforrás használata (csak most töltődik be)
config = loader()
print(config)  # {'setting': 'value'}
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

loader = LazyLoader(lambda: "erőforrás")

print(f"Betöltve: {loader.is_loaded}")  # False

# Erőforrás használata
resource = loader()

print(f"Betöltve: {loader.is_loaded}")  # True
```

### reset

```python
def reset(self) -> None:
    """Reset the loader to unload the resource."""
```

**Leírás:** Visszaállítja a betöltőt az alaphelyzetbe, kitéve a betöltött erőforrást. Ez hasznos lehet tesztelés során.

**Példa:**
```python
from neural_ai.core.base.lazy_loading import LazyLoader

loader = LazyLoader(lambda: "erőforrás")

# Használat
resource1 = loader()
print(f"Betöltve: {loader.is_loaded}")  # True

# Reset
loader.reset()
print(f"Betöltve: {loader.is_loaded}")  # False

# Újra használat
resource2 = loader()
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

class ExpensiveObject:
    def __init__(self):
        self._data = list(range(1000000))

    @lazy_property
    def processed_data(self):
        print("Adatok feldolgozása...")
        # Drága művelet szimulálása
        time.sleep(2)
        return [x * 2 for x in self._data]

obj = ExpensiveObject()

# Első hozzáférés - most számolódik ki
print("Első hozzáférés:")
data1 = obj.processed_data  # Kiírja: "Adatok feldolgozása..."

# Második hozzáférés - már gyorsítótárból jön
print("Második hozzáférés:")
data2 = obj.processed_data  # Nem ír ki semmit, gyors

print(f"Azonos adatok: {data1 is data2}")  # True
```

## Használati példák

### 1. Alapvető használat

```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path='configs/app_config.yaml',
    log_path='logs/app.log',
    storage_path='./data'
)

# Komponensek használata
components.logger.info("Alkalmazás elindult")

app_config = components.config.get_section('app')
print(f"App name: {app_config.get('name')}")

components.storage.save_object(
    {"status": "running"},
    "app_status.json"
)
```

### 2. Komponensek ellenőrzése

```python
from neural_ai.core.base import CoreComponentFactory

# Komponensek létrehozása
components = CoreComponentFactory.create_minimal()

# Komponensek ellenőrzése
print(f"Config elérhető: {components.has_config()}")
print(f"Logger elérhető: {components.has_logger()}")
print(f"Storage elérhető: {components.has_storage()}")

# Teljes validáció
if components.validate():
    print("Minden komponens elérhető")
else:
    print("Néhány komponens hiányzik")
```

### 3. Lazy loading demonstráció

```python
from neural_ai.core.base import CoreComponentFactory
import time

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path='config.yaml',
    log_path='app.log',
    storage_path='./data'
)

print("Komponensek létrehozva, de még nincsenek betöltve")

# Lazy loading demonstráció
print("\n1. Logger használata (első alkalommal töltődik be):")
start_time = time.time()
components.logger.info("Első naplóbejegyzés")
end_time = time.time()
print(f"Betöltési idő: {end_time - start_time:.2f} másodperc")

print("\n2. Config használata (első alkalommal töltődik be):")
start_time = time.time()
settings = components.config.get_section('app')
end_time = time.time()
print(f"Betöltési idő: {end_time - start_time:.2f} másodperc")

print("\n3. Második használat (már betöltve van):")
start_time = time.time()
components.logger.info("Második naplóbejegyzés")
end_time = time.time()
print(f"Hozzáférési idő: {end_time - start_time:.4f} másodperc")
```

### 4. Preload használata

```python
from neural_ai.core.base import CoreComponentFactory
import time

# Komponensek létrehozása
components = CoreComponentFactory.create_components(
    config_path='config.yaml',
    log_path='app.log',
    storage_path='./data'
)

print("Komponensek előtöltése...")
start_time = time.time()
components.preload_all()
end_time = time.time()
print(f"Előtöltési idő: {end_time - start_time:.2f} másodperc")

print("\nKomponensek használata (azonnal elérhetők):")
start_time = time.time()
components.logger.info("Azonnali hozzáférés")
settings = components.config.get_section('app')
components.storage.save_object({}, "test.json")
end_time = time.time()
print(f"Használati idő: {end_time - start_time:.4f} másodperc")
```

### 5. LazyLoader egyedi használata

```python
from neural_ai.core.base.lazy_loading import LazyLoader
import time

def load_expensive_resource():
    """Drága erőforrás betöltése."""
    print("Erőforrás betöltése...")
    time.sleep(3)
    return {"data": [1, 2, 3, 4, 5]}

# Lazy loader létrehozása
resource_loader = LazyLoader(load_expensive_resource)

print("Lazy loader létrehozva")
print(f"Betöltve: {resource_loader.is_loaded}")

# Erőforrás használata
print("\nErőforrás első használata:")
start_time = time.time()
resource = resource_loader()
end_time = time.time()
print(f"Betöltési idő: {end_time - start_time:.2f} másodperc")
print(f"Betöltve: {resource_loader.is_loaded}")
print(f"Adatok: {resource}")

# Második használat (már betöltve van)
print("\nErőforrás második használata:")
start_time = time.time()
resource2 = resource_loader()
end_time = time.time()
print(f"Hozzáférési idő: {end_time - start_time:.4f} másodperc")
print(f"Azonos objektum: {resource is resource2}")
```

## Hibakezelés

### ComponentNotFoundError

Akkor dobódik, ha egy komponens nem található.

```python
from neural_ai.core.base import CoreComponents, DIContainer
from neural_ai.core.base.exceptions import ComponentNotFoundError

# Üres konténerrel hozzuk létre a komponenseket
container = DIContainer()
components = CoreComponents(container=container)

# Komponens használata (kivételt dob)
try:
    config = components.config
    if config:
        print("Konfiguráció elérhető")
    else:
        print("Konfiguráció nem elérhető")
except ComponentNotFoundError:
    print("Hiba: A konfiguráció komponens nem található a konténerben")
```

## Teljesítmény optimalizációk

### 1. Lazy Loading

A lazy loading optimalizálja a memóriahasználatot és a betöltési időt:

```python
# A komponensek csak akkor töltődnek be, amikor először használják őket
components.logger  # Most töltődik be a logger
components.config  # Most töltődik be a config
components.storage  # Most töltődik be a storage
```

### 2. Preload

Előzetes betöltés használata, ha tudjuk, hogy szükség lesz az összes komponensre:

```python
# Összes komponens előtöltése
components.preload_all()

# Most minden komponens azonnal elérhető
components.logger.info("Minden komponens betöltve")
```

### 3. Thread Safety

A CoreComponents szálbiztos, így több szál is biztonságosan használhatja:

```python
import threading

def worker(components, thread_id):
    components.logger.info(f"Szál {thread_id} elindult")
    # Biztonságos műveletek

# Több szál használhatja ugyanazt a komponenset
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(components, i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

## Kapcsolódó dokumentáció

- [API Áttekintés](overview.md)
- [DIContainer API](container.md)
- [CoreComponentFactory API](factory.md)
- [Lazy Loading API](lazy_loading.md)
- [Architektúra áttekintés](../architecture/overview.md)
- [Komponens életciklus](../architecture/lifecycle.md)

## Példák

- [Alap használati példák](../examples/basic_usage.md)
- [Haladó példák](../examples/advanced_usage.md)
- [Tesztelési példák](../examples/testing.md)

---

**Dokumentum verzió:** 1.0
**Utolsó frissítés:** 2025-12-19
**Osztály:** CoreComponents
