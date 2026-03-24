# neural_ai/core/base/implementations/di_container.py

Dependency injection konténer implementáció.

## Importok

```python
import sys
import threading
from collections.abc import Callable
from typing import TypeVar
from typing import cast
from neural_ai.core.base.exceptions import ComponentNotFoundError
from neural_ai.core.base.exceptions import SingletonViolationError
from neural_ai.core.base.implementations.singleton import SingletonMeta
from neural_ai.core.base.interfaces import DIContainerInterface
from neural_ai.core.base.interfaces import LazyComponentInterface
# ... és még 2 import
```

## Konstansok

- **`T`**
: `TypeVar('T')`


- **`InterfaceT`**
: `TypeVar('InterfaceT')`


## Osztály: `LazyComponent(LazyComponentInterface)`

Lusta betöltésű komponensek wrapper osztálya.

Ez az osztály biztosítja a komponensek lusta (lazy) betöltését,
ami azt jelenti, hogy a komponens csak akkor jön létre, amikor
először használják.

### Metódusok

#### `__init__()`

```python
def __init__(self, factory_func: Callable[[], T]) -> None
```

Inicializálja a lusta komponenst.

**Paraméterek:**

- **`self`**
- **`factory_func`** (`Callable[[], T]`): A komponens létrehozásához használt factory függvény

**Visszatérési érték:**

- Típus: `None`

#### `get()`

```python
def get(self) -> T
```

Lekéri a komponens példányt (lusta betöltéssel).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `T`
- A komponens példánya

#### `is_loaded()`

```python
def is_loaded(self) -> bool
```

Ellenőrzi, hogy a komponens betöltődött-e már.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- True, ha a komponens már betöltődött, egyébként False

## Osztály: `DIContainer(DIContainerInterface)`

Egyszerű dependency injection konténer (Singleton).

A konténer kezeli a komponensek közötti függőségeket és biztosítja
azok megfelelő inicializálását. Singleton pattern biztosítja, hogy
az alkalmazásban egyetlen konténer példány létezzen.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

Konténer inicializálása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `register_instance()`

```python
def register_instance(self, interface: InterfaceT, instance: InterfaceT) -> None
```

Példány regisztrálása a konténerben.

**Paraméterek:**

- **`self`**
- **`interface`** (`InterfaceT`): Az interfész típusa
- **`instance`** (`InterfaceT`): Az interfészt megvalósító példány

**Visszatérési érték:**

- Típus: `None`

#### `register_factory()`

```python
def register_factory(self, interface: InterfaceT, factory: Callable[[], InterfaceT]) -> None
```

Factory függvény regisztrálása a konténerben.

**Paraméterek:**

- **`self`**
- **`interface`** (`InterfaceT`): Az interfész típusa
- **`factory`** (`Callable[[], InterfaceT]`): Az interfész implementációját létrehozó factory függvény

**Visszatérési érték:**

- Típus: `None`

#### `resolve()`

```python
def resolve(self, interface: InterfaceT) -> InterfaceT | None
```

Függőség feloldása.

**Paraméterek:**

- **`self`**
- **`interface`** (`InterfaceT`): Az interfész típusa

**Visszatérési érték:**

- Típus: `InterfaceT | None`
- Az interfészhez tartozó példány vagy None

#### `register_lazy()`

```python
def register_lazy(self, component_name: str, factory_func: Callable[[], T]) -> None
```

Lusta betöltésű komponens regisztrálása.

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`): A komponens neve
- **`factory_func`** (`Callable[[], T]`): A komponenst létrehozó függvény

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha a komponens név érvénytelen vagy a factory

#### `get()`

```python
def get(self, component_name: str) -> object
```

Komponens példány lekérése (lusta betöltés támogatással).

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`): A lekérendő komponens neve

**Visszatérési érték:**

- Típus: `object`
- A komponens példánya

**Kivételek:**

- **`ComponentNotFoundError`**: Ha a komponens nem található

#### `get_lazy_components()`

```python
def get_lazy_components(self) -> dict[str, bool]
```

Get status of all lazy components.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, bool]`
- A dictionary where keys are component names and values indicate whether the component has been loaded

#### `preload_components()`

```python
def preload_components(self, component_names: list[str]) -> None
```

Preload specific components.

**Paraméterek:**

- **`self`**
- **`component_names`** (`list[str]`): List of component names to preload

**Visszatérési érték:**

- Típus: `None`

#### `clear()`

```python
def clear(self) -> None
```

Clear the container.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_verify_singleton()`

```python
def _verify_singleton(self, instance: object, component_name: str) -> None
```

Ellenőrzi, hogy az instance követi-e a singleton mintát.

**Paraméterek:**

- **`self`**
- **`instance`** (`object`): Az ellenőrizendő példány
- **`component_name`** (`str`): A komponens neve

**Visszatérési érték:**

- Típus: `None`

#### `_enforce_singleton()`

```python
def _enforce_singleton(self, component_name: str, instance: object) -> None
```

Enforce singleton pattern by preventing duplicate registration.

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`): The name of the component
- **`instance`** (`object`): The instance being registered

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`SingletonViolationError`**: If singleton pattern is violated

#### `register()`

```python
def register(self, component_name: str, instance: object) -> None
```

Komponens példány regisztrálása.

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`): A komponens neve
- **`instance`** (`object`): A regisztrálandó példány

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha a component_name érvénytelen vagy az instance None
- **`SingletonViolationError`**: Ha a singleton minta megsértésre kerül

#### `get_memory_usage()`

```python
def get_memory_usage(self) -> dict[str, int | dict[str, int]]
```

Get memory usage statistics.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, int | dict[str, int]]`

---

**Forrásfájl:** [`neural_ai/core/base/implementations/di_container.py`](../../neural_ai/core/base/implementations/di_container.py)
