# neural_ai/core/base/interfaces/container_interface.py

Dependency injection konténer interfészek.

Ez a modul tartalmazza a DI konténerhez és lusta betöltéshez kapcsolódó interfészeket.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from collections.abc import Callable
from typing import TypeVar
```

## Konstansok

- **`T`**
: `TypeVar('T')`


- **`InterfaceT`**
: `TypeVar('InterfaceT')`


## Osztály: `DIContainerInterface(ABC)`

Dependency injection konténer interfész.

Ez az interfész definiálja a dependency injection konténer alapvető
funkcionalitását, amely a komponensek közötti függőségek kezelését biztosítja.

### Metódusok

#### `register_instance()`

```python
def register_instance(self, interface: InterfaceT, instance: InterfaceT) -> None
```

Komponens példány regisztrálása a konténerben.

**Paraméterek:**

- **`self`**
- **`interface`** (`InterfaceT`): Az interfész típusa, amihez a példányt regisztráljuk
- **`instance`** (`InterfaceT`): A regisztrálandó példány

**Visszatérési érték:**

- Típus: `None`

#### `register_factory()`

```python
def register_factory(self, interface: InterfaceT, factory: Callable[[], InterfaceT]) -> None
```

Factory függvény regisztrálása a konténerben.

**Paraméterek:**

- **`self`**
- **`interface`** (`InterfaceT`): Az interfész típusa, amihez a factory-t regisztráljuk
- **`factory`** (`Callable[[], InterfaceT]`): A factory függvény, ami létrehozza az implementációt

**Visszatérési érték:**

- Típus: `None`

#### `resolve()`

```python
def resolve(self, interface: InterfaceT) -> InterfaceT | None
```

Függőség feloldása a konténerből.

**Paraméterek:**

- **`self`**
- **`interface`** (`InterfaceT`): Az interfész típusa, amit fel szeretnénk oldani

**Visszatérési érték:**

- Típus: `InterfaceT | None`
- A regisztrált példány vagy None ha nem található

#### `register_lazy()`

```python
def register_lazy(self, component_name: str, factory_func: Callable[[], T]) -> None
```

Lusta betöltésű komponens regisztrálása.

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`): A komponens neve
- **`factory_func`** (`Callable[[], T]`): A komponens létrehozásához használt factory függvény

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha a komponens név érvénytelen vagy a factory függvény nem hívható

#### `get()`

```python
def get(self, component_name: str) -> object
```

Komponens példány lekérése (lusta betöltéssel).

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`): A lekérendő komponens neve

**Visszatérési érték:**

- Típus: `object`
- A komponens példánya

**Kivételek:**

- **`ComponentNotFoundError`**: Ha a komponens nem található

#### `clear()`

```python
def clear(self) -> None
```

Konténer ürítése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `LazyComponentInterface(ABC)`

Lusta betöltésű komponens interfész.

Ez az interfész definiálja a lusta (lazy) betöltésű komponensek
alapvető funkcionalitását.

### Metódusok

#### `get()`

```python
def get(self) -> object
```

Komponens példány lekérése (lusta betöltéssel).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `object`
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

---

**Forrásfájl:** [`neural_ai/core/base/interfaces/container_interface.py`](../../neural_ai/core/base/interfaces/container_interface.py)
