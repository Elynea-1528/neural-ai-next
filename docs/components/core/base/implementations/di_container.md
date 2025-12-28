# DIContainer és LazyComponent

## Áttekintés

A `DIContainer` egy egyszerű dependency injection konténer, amely kezeli a komponensek közötti függőségeket és biztosítja azok megfelelő inicializálását. A `LazyComponent` egy wrapper osztály, amely lusta (lazy) betöltést valósít meg.

## LazyComponent

### Leírás

A `LazyComponent[T]` egy generikus osztály, amely lusta betöltést biztosít. Ez azt jelenti, hogy a komponens csak akkor jön létre, amikor először használják.

### Metódusok

- `__init__(factory_func: Callable[[], T]) -> None`: Inicializálja a lusta komponenst a megadott factory függvénnyel.
- `get() -> T`: Lekéri a komponens példányt (lusta betöltéssel). Ha még nincs betöltve, meghívja a factory függvényt.
- `is_loaded: bool`: Property, amely ellenőrzi, hogy a komponens betöltődött-e már.

### Példa

```python
from neural_ai.core.base.implementations.di_container import LazyComponent
from unittest.mock import MagicMock

# Factory függvény létrehozása
def create_expensive_service() -> MagicMock:
    print("Creating expensive service...")
    return MagicMock()

# Lazy component létrehozása
lazy_service = LazyComponent(create_expensive_service)

# Még nem hívódott meg a factory
print(lazy_service.is_loaded)  # False

# Első hozzáférés - most hívódik meg a factory
service = lazy_service.get()
print(lazy_service.is_loaded)  # True

# További hozzáférés - már nem hívódik meg a factory
service2 = lazy_service.get()
assert service is service2  # Ugyanaz a példány
```

## DIContainer

### Leírás

A `DIContainer` egy dependency injection konténer, amely támogatja a példányok, factory-k és lusta komponensek regisztrációját és feloldását.

### Metódusok

#### Regisztráció

- `register_instance(interface: InterfaceT, instance: InterfaceT) -> None`: Példány regisztrálása a konténerben.
- `register_factory(interface: InterfaceT, factory: Callable[[], InterfaceT]) -> None`: Factory függvény regisztrálása.
- `register_lazy(component_name: str, factory_func: Callable[[], T]) -> None`: Lusta betöltésű komponens regisztrálása.
- `register(component_name: str, instance: object) -> None`: Komponens példány regisztrálása névvel.

#### Feloldás

- `resolve(interface: InterfaceT) -> InterfaceT | None`: Függőség feloldása interfész alapján.
- `get(component_name: str) -> object`: Komponens példány lekérése név alapján (lusta betöltés támogatással).

#### Egyéb

- `get_lazy_components() -> dict[str, bool]`: Lekéri az összes lusta komponens státuszát.
- `preload_components(component_names: list[str]) -> None`: Előtölti a megadott komponenseket.
- `clear() -> None`: Kiüríti a konténert.
- `get_memory_usage() -> dict[str, int | dict[str, int]]`: Lekéri a memóriahasználat statisztikáit.

### Példa

```python
from neural_ai.core.base.implementations.di_container import DIContainer
from unittest.mock import MagicMock

# Konténer létrehozása
container = DIContainer()

# Példány regisztrálása
logger = MagicMock()
container.register_instance(type(logger), logger)

# Factory regisztrálása
def create_config() -> MagicMock:
    return MagicMock()

container.register_factory(MagicMock, create_config)

# Lusta komponens regisztrálása
def create_expensive_service() -> MagicMock:
    print("Creating expensive service...")
    return MagicMock()

container.register_lazy("expensive_service", create_expensive_service)

# Feloldás
resolved_logger = container.resolve(type(logger))
resolved_config = container.resolve(MagicMock)
resolved_service = container.get("expensive_service")  # Most jön létre

# Memóriahasználat lekérdezése
stats = container.get_memory_usage()
print(f"Total instances: {stats['total_instances']}")
```

## Szálbiztonság

A `LazyComponent` szálbiztos, RLock-ot használ a kritikus szakaszok védelmére. Ez biztosítja, hogy többszálú környezetben is csak egyszer hívódjon meg a factory függvény.

## DI Kompatibilitás

A konténer ellenőrzi a singleton mintát a `_verify_singleton` metódussal:

1. **`_initialized` flag**: Minden példánynak rendelkeznie kell ezzel a flag-gel, és True értéket kell tartalmaznia.
2. **`_instance` class variable**: A singleton osztályoknak rendelkezniük kell ezzel a class változóval.

Ha ezek a feltételek nem teljesülnek, a konténer figyelmeztetést ad ki.

## Hibakezelés

- `ValueError`: Érvénytelen komponensnév vagy factory függvény esetén.
- `ComponentNotFoundError`: Nem létező komponens lekérésekor.
- `SingletonViolationError`: Singleton minta megsértése esetén.

## Tesztelés

A modul tesztelése a `tests/core/base/implementations/test_di_container.py` fájlban található. A tesztek 100% statement coverage-t érnek el.