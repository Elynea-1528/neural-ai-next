# neural_ai/core/base/implementations/lazy_loader.py

Lustatöltés (lazy loading) segédeszközök.

Ez a modul a lustatöltés mechanizmust valósítja meg, amely lehetővé teszi,
hogy a drága erőforrások csak akkor töltődjenek be, amikor valóban szükség van rájuk.
Ez jelentősen javítja az alkalmazás indítási idejét és a memóriahasználatot.

## Importok

```python
import threading
from collections.abc import Callable
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import cast
from neural_ai.core.utils.decorators import trace
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
```

## Konstansok

- **`T`**
: `TypeVar('T')`


- **`__all__`**
: `['LazyLoader', 'lazy_property']`


- **`attr_name`**
: `f'_lazy_{func.__name__}'`


- **`value`**
: `func(instance)`


## Osztály: `LazyLoader`

Drága erőforrások lustatöltője.

Ez az osztály lehetővé teszi, hogy a drága erőforrások (pl. konfigurációk,
adatbázis kapcsolatok, nagy adathalmazok) csak akkor töltődjenek be,
amikor valóban szükség van rájuk.

A lustatöltés szálbiztos, így többszálú környezetben is biztonságosan
használható.

### Metódusok

#### `__init__()`

```python
def __init__(self, loader_func: Callable[[], T], logger: 'LoggerInterface | None' = None) -> None
```

Inicializálja a lustatöltőt.

**Paraméterek:**

- **`self`**
- **`loader_func`** (`Callable[[], T]`): A függvény, amely betölti az erőforrást. Ennek a függvénynek vissza kell térnie a betöltött erőforrással.
- **`logger`** (`'LoggerInterface | None'`) = `None`: Logger példány (opcionális - bootstrap során még nincs logger). Ha None, akkor minimális logolás (nincs log).

**Visszatérési érték:**

- Típus: `None`

#### `_load()`

```python
def _load(self) -> T
```

Betölti az erőforrást, ha még nincs betöltve.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `T`
- A betöltött erőforrás. Note: Ez egy belső metódus, általában nem kell közvetlenül használni. Ehelyett használd a __call__ metódust.

#### `__call__()`

```python
def __call__(self) -> T
```

Visszaadja a betöltött erőforrást. Ha az erőforrás még nincs betöltve, először meghívja a betöltő függvényt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `T`
- A betöltött erőforrás.

#### `is_loaded()`

```python
def is_loaded(self) -> bool
```

Ellenőrzi, hogy az erőforrás betöltve van-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- True, ha az erőforrás betöltve van, egyébként False.

#### `reset()`

```python
def reset(self) -> None
```

Visszaállítja a betöltőt az alaphelyzetbe. Ez kiüríti a betöltött erőforrást, lehetővé téve az újratöltést. Hasznos lehet tesztelés során vagy ha újra szeretnénk tölteni az erőforrást.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

### `lazy_property()`

```python
def lazy_property(func: Callable[..., T]) -> property
```

Dekorátor lustatöltésű property-k létrehozásához. Ez a dekorátor egy olyan property-t hoz létre, amelynek értéke csak az első hozzáféréskor számolódik ki, majd gyorsítótárba kerül. A későbbi hozzáférések már a gyorsítótárazott értéket adják vissza.

**Paraméterek:**

- **`func`** (`Callable[..., T]`): A függvény, amely kiszámolja a property értékét.

**Visszatérési érték:**

- Típus: `property`
- Egy property objektum lustatöltéssel. Példa: >>> class DataProcessor: ...     def __init__(self, data): ...         self._data = data ...     @lazy_property ...     def processed_data(self): ...         # Ez a kód csak egyszer fut le ...         return [x * 2 for x in self._data] >>> processor = DataProcessor([1, 2, 3]) >>> # A processed_data még nincs kiszámolva >>> result = processor.processed_data  # Most fut le először >>> result2 = processor.processed_data  # Már gyorsítótárból jön

### `wrapper()`

```python
def wrapper(instance: object) -> T
```

**Paraméterek:**

- **`instance`** (`object`)

**Visszatérési érték:**

- Típus: `T`

---

**Forrásfájl:** [`neural_ai/core/base/implementations/lazy_loader.py`](../../neural_ai/core/base/implementations/lazy_loader.py)
