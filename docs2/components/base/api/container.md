# DIContainer API

## Áttekintés

A `DIContainer` (Dependency Injection Container) osztály a Neural AI Next projekt dependency injection megvalósításáért felelős. Ez az osztály kezeli a komponensek közötti függőségeket, biztosítja azok megfelelő inicializálását és életciklusát.

## Osztály: DIContainer

```python
class DIContainer:
    """Egyszerű dependency injection konténer.

    A konténer kezeli a komponensek közötti függőségeket és biztosítja
    azok megfelelő inicializálását.
    """
```

### Konstruktor

```python
def __init__(self) -> None:
    """Konténer inicializálása."""
```

**Leírás:** Létrehoz egy új DIContainer példányt üres komponens listával.

**Példa:**
```python
from neural_ai.core.base import DIContainer

# Konténer létrehozása
container = DIContainer()
```

## Metódusok

### register_instance

```python
def register_instance(self, interface: Any, instance: Any) -> None:
    """Példány regisztrálása a konténerben.

    Args:
        interface: Az interfész típusa
        instance: A példány, ami implementálja az interfészt
    """
```

**Leírás:** Regisztrál egy már létrehozott példányt a konténerben egy adott interfészhez társítva.

**Paraméterek:**
- `interface`: Az interfész típusa (általában egy osztály vagy interfész)
- `instance`: A példány, ami implementálja az interfészt

**Példa:**
```python
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.logger.implementations.default_logger import DefaultLogger

# Logger példány létrehozása és regisztrálása
logger = DefaultLogger(name="my_logger")
container.register_instance(LoggerInterface, logger)
```

### register_factory

```python
def register_factory(self, interface: Any, factory: Any) -> None:
    """Factory függvény regisztrálása a konténerben.

    Args:
        interface: Az interfész típusa
        factory: A factory függvény az interfész implementáció létrehozásához
    """
```

**Leírás:** Regisztrál egy factory függvényt, amely akkor hívódik meg, amikor az interfészre szükség van.

**Paraméterek:**
- `interface`: Az interfész típusa
- `factory`: A factory függvény, ami létrehozza az implementációt

**Példa:**
```python
# Factory függvény definiálása
def create_logger():
    return DefaultLogger(name="factory_logger")

# Factory regisztrálása
container.register_factory(LoggerInterface, create_logger)
```

### resolve

```python
def resolve(self, interface: Any) -> Optional[Any]:
    """Függőség feloldása.

    Args:
        interface: Az interfész típusa

    Returns:
        Az interfészhez tartozó példány vagy None
    """
```

**Leírás:** Megpróbálja feloldani egy interfész függőségét a konténerben. Először a regisztrált példányokat, majd a factory-kat próbálja meg használni.

**Paraméterek:**
- `interface`: Az interfész típusa

**Visszatérési érték:**
- Az interfészhez tartozó példány, ha megtalálható
- `None`, ha az interfész nincs regisztrálva

**Példa:**
```python
# Függőség feloldása
logger = container.resolve(LoggerInterface)
if logger:
    logger.info("Függőség feloldva")
```

### register_lazy

```python
def register_lazy(
    self,
    component_name: str,
    factory_func: Callable[[], Any]
) -> None:
    """Register a lazy-loaded component.

    Args:
        component_name: Name of the component
        factory_func: Function to create the component
    """
```

**Leírás:** Regisztrál egy lazy-loaded komponenst, amely csak akkor töltődik be, amikor először használják.

**Paraméterek:**
- `component_name`: A komponens egyedi neve (nem üres string)
- `factory_func`: A factory függvény, ami létrehozza a komponenst

**Kivételek:**
- `ValueError`: Ha a `component_name` nem string vagy üres
- `ValueError`: Ha a `factory_func` nem hívható

**Példa:**
```python
# Lazy komponens regisztrálása
container.register_lazy(
    'expensive_service',
    lambda: ExpensiveService(config)
)

# Komponens használata (csak most töltődik be)
service = container.get('expensive_service')
```

### get

```python
def get(self, component_name: str) -> Any:
    """Get a component instance (with lazy loading support)."""
```

**Leírás:** Lekér egy komponens példányt a neve alapján. Támogatja a lazy loadinget is.

**Paraméterek:**
- `component_name`: A komponens neve

**Visszatérési érték:**
- A komponens példánya

**Kivételek:**
- `ComponentNotFoundError`: Ha a komponens nem található

**Példa:**
```python
# Komponens lekérése
try:
    logger = container.get('logger')
    logger.info("Komponens sikeresen lekérve")
except ComponentNotFoundError as e:
    print(f"Hiba: {e}")
```

### get_lazy_components

```python
def get_lazy_components(self) -> Dict[str, bool]:
    """Get status of all lazy components."""
```

**Leírás:** Visszaadja az összes lazy komponens aktuális állapotát.

**Visszatérési érték:**
- Egy szótár, ahol a kulcsok a komponens nevek, az értékek pedig a betöltöttségi állapot (True/False)

**Példa:**
```python
# Lazy komponensek állapotának lekérdezése
lazy_status = container.get_lazy_components()
print(f"Betöltött komponensek: {lazy_status}")
# {'logger': True, 'config': False, 'storage': True}
```

### preload_components

```python
def preload_components(self, component_names: List[str]) -> None:
    """Preload specific components.

    Args:
        component_names: List of component names to preload
    """
```

**Leírás:** Előzetesen betölti a megadott komponenseket, még mielőtt szükség lenne rájuk.

**Paraméterek:**
- `component_names`: A betöltendő komponensek neveinek listája

**Példa:**
```python
# Komponensek előtöltése
container.preload_components(['logger', 'config', 'storage'])
```

### clear

```python
def clear(self) -> None:
    """Konténer ürítése."""
```

**Leírás:** Kiüríti a konténert, eltávolítva az összes regisztrált példányt, factory-t és lazy komponenst.

**Példa:**
```python
# Konténer ürítése
container.clear()
```

### register

```python
def register(self, component_name: str, instance: Any) -> None:
    """Register a component instance.

    Args:
        component_name: The name of the component
        instance: The instance to register

    Raises:
        ValueError: If component_name is invalid or instance is None
        SingletonViolationError: If singleton pattern is violated
    """
```

**Leírás:** Regisztrál egy komponens példányt a megadott névvel. Ellenőrzi a singleton mintát.

**Paraméterek:**
- `component_name`: A komponens neve (nem üres string)
- `instance`: A regisztrálandó példány (nem lehet None)

**Kivételek:**
- `ValueError`: Ha a `component_name` érvénytelen vagy az `instance` None
- `SingletonViolationError`: Ha a singleton minta megsérül

**Példa:**
```python
# Komponens regisztrálása
service = MyService()
container.register('my_service', service)
```

### get_memory_usage

```python
def get_memory_usage(self) -> Dict[str, Any]:
    """Get memory usage statistics."""
```

**Leírás:** Visszaadja a konténer memóriahasználati statisztikáit.

**Visszatérési érték:**
- Egy szótár a következő kulcsokkal:
  - `total_instances`: A regisztrált példányok száma
  - `lazy_components`: A lazy komponensek száma
  - `loaded_lazy_components`: A betöltött lazy komponensek száma
  - `instance_sizes`: Az egyes példányok mérete (bájtokban)

**Példa:**
```python
# Memóriahasználat lekérdezése
memory_stats = container.get_memory_usage()
print(f"Összes példány: {memory_stats['total_instances']}")
print(f"Példány méretek: {memory_stats['instance_sizes']}")
```

## Belső metódusok

### _verify_singleton

```python
def _verify_singleton(self, instance: Any, component_name: str) -> None:
    """Verify that the instance follows singleton pattern.

    Args:
        instance: The instance to verify
        component_name: The name of the component

    Raises:
        UserWarning: If singleton pattern is not properly implemented
    """
```

**Leírás:** Ellenőrzi, hogy a példány követi-e a singleton mintát. Figyelmeztetést ad, ha nem.

### _enforce_singleton

```python
def _enforce_singleton(self, component_name: str, instance: Any) -> None:
    """Enforce singleton pattern by preventing duplicate registration.

    Args:
        component_name: The name of the component
        instance: The instance being registered

    Raises:
        SingletonViolationError: If singleton pattern is violated
    """
```

**Leírás:** Kényszeríti a singleton mintát azáltal, hogy megakadályozza a duplikált regisztrációt.

## Osztály: LazyComponent

```python
class LazyComponent:
    """Wrapper for lazy-loaded components."""
```

### Konstruktor

```python
def __init__(self, factory_func: Callable[[], Any]):
    """Initialize lazy component.

    Args:
        factory_func: Function to create the component
    """
```

**Leírás:** Létrehoz egy új LazyComponent példányt a megadott factory függvénnyel.

### get

```python
def get(self) -> Any:
    """Get the component instance (lazy-loaded)."""
```

**Leírás:** Lekéri a komponens példányt. Ha még nincs betöltve, meghívja a factory függvényt.

**Visszatérési érték:**
- A komponens példánya

### is_loaded

```python
@property
def is_loaded(self) -> bool:
    """Check if the component is loaded."""
```

**Leírás:** Visszaadja, hogy a komponens betöltöttségi állapotát.

**Visszatérési érték:**
- `True`, ha a komponens betöltve van
- `False`, ha még nincs betöltve

## Használati példák

### 1. Alapvető használat

```python
from neural_ai.core.base import DIContainer
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.logger.implementations.default_logger import DefaultLogger

# Konténer létrehozása
container = DIContainer()

# Példány regisztrálása
logger = DefaultLogger(name="app_logger")
container.register_instance(LoggerInterface, logger)

# Példány lekérése
retrieved_logger = container.resolve(LoggerInterface)
retrieved_logger.info("Sikeres regisztráció és lekérés")
```

### 2. Lazy loading használata

```python
from neural_ai.core.base import DIContainer

# Konténer létrehozása
container = DIContainer()

# Lazy komponens regisztrálása
def create_expensive_service():
    print("Drága szolgáltatás létrehozása...")
    return ExpensiveService()

container.register_lazy('expensive_service', create_expensive_service)

# Komponens használata (csak most jön létre)
print("Komponens lekérése...")
service = container.get('expensive_service')
service.do_something()
```

### 3. Komponens állapot nyomon követése

```python
from neural_ai.core.base import DIContainer

# Konténer létrehozása
container = DIContainer()

# Több lazy komponens regisztrálása
container.register_lazy('logger', lambda: create_logger())
container.register_lazy('config', lambda: create_config())
container.register_lazy('storage', lambda: create_storage())

# Lazy komponensek állapotának ellenőrzése
print("Kezdeti állapot:", container.get_lazy_components())
# {'logger': False, 'config': False, 'storage': False}

# Egy komponens használata
logger = container.get('logger')

# Állapot ellenőrzése újra
print("Logger használata után:", container.get_lazy_components())
# {'logger': True, 'config': False, 'storage': False}
```

### 4. Memóriahasználat monitorozása

```python
from neural_ai.core.base import DIContainer

# Konténer létrehozása és feltöltése
container = DIContainer()
container.register_lazy('service1', lambda: Service1())
container.register_lazy('service2', lambda: Service2())

# Memóriahasználat ellenőrzése
stats = container.get_memory_usage()
print(f"Összes példány: {stats['total_instances']}")
print(f"Lazy komponensek: {stats['lazy_components']}")

# Komponensek használata
service1 = container.get('service1')

# Memóriahasználat ellenőrzése újra
stats = container.get_memory_usage()
print(f"Betöltött lazy komponensek: {stats['loaded_lazy_components']}")
```

## Hibakezelés

### ComponentNotFoundError

Akkor dobódik, ha egy komponens nem található a konténerben.

```python
from neural_ai.core.base import DIContainer
from neural_ai.core.base.exceptions import ComponentNotFoundError

container = DIContainer()

try:
    component = container.get('non_existent_component')
except ComponentNotFoundError as e:
    print(f"Hiba: {e}")
    # Hiba: Component 'non_existent_component' not found
```

### SingletonViolationError

Akkor dobódik, ha a singleton minta megsérül.

```python
from neural_ai.core.base import DIContainer
from neural_ai.core.base.exceptions import SingletonViolationError

container = DIContainer()

# Első regisztráció
service1 = MyService()
container.register('my_service', service1)

# Második regisztráció ugyanazzal a névvel (kivételt dob)
try:
    service2 = MyService()
    container.register('my_service', service2)
except SingletonViolationError as e:
    print(f"Hiba: {e}")
```

## Teljesítmény optimalizációk

### 1. Lazy Loading

A lazy loading optimalizálja a memóriahasználatot és a betöltési időt:

```python
# A komponens csak akkor töltődik be, amikor először használják
container.register_lazy('expensive_component', create_expensive_component)
# A create_expensive_component() csak itt hívódik meg először:
component = container.get('expensive_component')
```

### 2. Preload

Előzetes betöltés használata, ha tudjuk, hogy szükség lesz a komponensekre:

```python
# Komponensek előtöltése
container.preload_components(['logger', 'config', 'storage'])
```

### 3. Thread Safety

A konténer szálbiztos, így több szál is biztonságosan használhatja:

```python
import threading

def worker():
    component = container.get('my_component')
    # Biztonságos műveletek

# Több szál használhatja ugyanazt a konténert
threads = [threading.Thread(target=worker) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

## Kapcsolódó dokumentáció

- [API Áttekintés](overview.md)
- [CoreComponents API](core_components.md)
- [CoreComponentFactory API](factory.md)
- [Architektúra áttekintés](../architecture/overview.md)
- [Komponens kölcsönhatások](../architecture/component_interactions.md)

## Példák

- [Alap használati példák](../examples/basic_usage.md)
- [Haladó példák](../examples/advanced_usage.md)
- [Tesztelési példák](../examples/testing.md)

---

**Dokumentum verzió:** 1.0
**Utolsó frissítés:** 2025-12-19
**Osztály:** DIContainer
