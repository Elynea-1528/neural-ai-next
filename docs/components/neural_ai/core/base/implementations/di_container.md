# DI Container Implementáció

## Áttekintés

Dependency injection konténer implementáció.

## Osztályok

### `LazyComponent[T]`

Lusta betöltésű komponensek wrapper osztálya.

Ez az osztály biztosítja a komponensek lusta (lazy) betöltését, ami azt jelenti, hogy a komponens csak akkor jön létre, amikor először használják.

#### Metódusok

##### `__init__(factory_func)`

Inicializálja a lusta komponenst.

**Paraméterek:**
- `factory_func`: A komponens létrehozásához használt factory függvény

##### `get()`

Lekéri a komponens példányt (lusta betöltéssel).

**Visszatérési érték:**
- `T`: A komponens példánya

##### `is_loaded` property

Ellenőrzi, hogy a komponens betöltődött-e már.

**Visszatérési érték:**
- `bool`: True, ha a komponens már betöltődött, egyébként False

### `DIContainer`

Egyszerű dependency injection konténer.

A konténer kezeli a komponensek közötti függőségeket és biztosítja azok megfelelő inicializálását.

#### Metódusok

##### `__init__()`

Konténer inicializálása.

##### `register_instance(interface, instance)`

Példány regisztrálása a konténerben.

**Paraméterek:**
- `interface`: Az interfész típusa
- `instance`: Az interfészt megvalósító példány

##### `register_factory(interface, factory)`

Factory függvény regisztrálása a konténerben.

**Paraméterek:**
- `interface`: Az interfész típusa
- `factory`: Az interfész implementációját létrehozó factory függvény

##### `resolve(interface)`

Függőség feloldása.

**Paraméterek:**
- `interface`: Az interfész típusa

**Visszatérési érték:**
- `InterfaceT | None`: Az interfészhez tartozó példány vagy None

##### `register_lazy(component_name, factory_func)`

Lusta betöltésű komponens regisztrálása.

**Paraméterek:**
- `component_name`: A komponens neve
- `factory_func`: A komponenst létrehozó függvény

**Kivételek:**
- `ValueError`: Ha a komponens név érvénytelen vagy a factory függvény nem hívható

##### `get(component_name)`

Komponens példány lekérése (lusta betöltés támogatással).

**Paraméterek:**
- `component_name`: A lekérendő komponens neve

**Visszatérési érték:**
- `object`: A komponens példánya

**Kivételek:**
- `ComponentNotFoundError`: Ha a komponens nem található

##### `get_lazy_components()`

Get status of all lazy components.

**Visszatérési érték:**
- `dict[str, bool]`: A dictionary where keys are component names and values indicate whether the component has been loaded

##### `preload_components(component_names)`

Preload specific components.

**Paraméterek:**
- `component_names`: List of component names to preload

##### `clear()`

Clear the container.

##### `register(component_name, instance)`

Komponens példány regisztrálása.

**Paraméterek:**
- `component_name`: A komponens neve
- `instance`: A regisztrálandó példány

**Kivételek:**
- `ValueError`: Ha a component_name érvénytelen vagy az instance None
- `SingletonViolationError`: Ha a singleton minta megsértésre kerül

##### `get_memory_usage()`

Get memory usage statistics.

**Visszatérési érték:**
- `dict[str, int | dict[str, int]]`: Memory usage statistics

## Használati Példák

### Alap konténer használat

```python
from neural_ai.core.base.implementations.di_container import DIContainer
from neural_ai.core.logger.interfaces import LoggerInterface
from neural_ai.core.logger.implementations import DefaultLogger

# Konténer létrehozása
container = DIContainer()

# Példány regisztrálása
logger = DefaultLogger(name="my_app")
container.register_instance(LoggerInterface, logger)

# Példány lekérése
retrieved_logger = container.resolve(LoggerInterface)
```

### Factory regisztrálása

```python
from neural_ai.core.config.interfaces import ConfigManagerInterface
from neural_ai.core.config.implementations import YamlConfigManager

def create_config_manager():
    return YamlConfigManager("config.yml")

container.register_factory(ConfigManagerInterface, create_config_manager)

# A factory csak most hozza létre a példányt
config_manager = container.resolve(ConfigManagerInterface)
```

### Lusta betöltés használata

```python
def create_expensive_component():
    print("Drága komponens létrehozása...")
    # Szimulált drága művelet
    import time
    time.sleep(2)
    return ExpensiveComponent()

# Lusta komponens regisztrálása
container.register_lazy("expensive", create_expensive_component)

# A komponens még nincs létrehozva
print("Komponens regisztrálva")

# Most jön létre a komponens
component = container.get("expensive")
print("Komponens létrejött")
```

### Singleton ellenőrzés

```python
# Singleton osztály definiálása
class DatabaseManager(metaclass=SingletonMeta):
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self._initialized = True

# Regisztrálás
db1 = DatabaseManager("sqlite:///mydb.db")
container.register_instance(DatabaseManager, db1)

# Lekérés - ugyanazt a példányt kapjuk vissza
db2 = container.resolve(DatabaseManager)
assert db1 is db2  # True
```

## Kapcsolódó Dokumentáció

- [Component Bundle](component_bundle.md)
- [Lazy Loader](lazy_loader.md)
- [Singleton](singleton.md)
- [Container Interface](../interfaces/container_interface.md)
- [Base Modul](../__init__.md)