# neural_ai/core/base/implementations/singleton.py

Singleton metaclass megvalósítása a singleton tervezési minta biztosításához.

Ez a modul egy metaclass-t biztosít, amely garantálja, hogy minden osztályból,
ami ezt a metaclass-t használja, csak egyetlen példány létezzen az alkalmazás
életciklusa során.

## Importok

```python
from abc import ABCMeta
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import cast
from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.core.utils.decorators import trace
from neural_ai.core.logger.interfaces import LoggerInterface
```

## Konstansok

- **`T`**
: `TypeVar('T')`


## Osztály: `SingletonMeta(ABCMeta)`

Singleton minta megvalósítására szolgáló metaclass.

Ez a metaclass biztosítja, hogy egy osztályból csak egy példány létezzen.
A létrehozott példányokat egy osztályszintű szótárban tárolja, és minden
következő példányosításnál ezt adja vissza.

Attribútumok:
    _instances: Osztályszintű szótár, amely tárolja a singleton példányokat.
        A kulcs az osztály, az érték pedig a létrehozott példány.

Példa:
    >>> class MyClass(metaclass=SingletonMeta):
    ...     def __init__(self, value: int):
    ...         self.value = value
    ...
    >>> obj1 = MyClass(42)
    >>> obj2 = MyClass(100)
    >>> obj1 is obj2
    True
    >>> obj1.value
    42

### Metódusok

#### `__call__()`

```python
def __call__(cls: type[T]) -> T
```

Singleton példány létrehozása vagy visszaadása. Ha az osztály még nem szerepel a _instances szótárban, létrehoz egy új példányt és eltárolja. Ellenkező esetben a meglévő példányt adja vissza. DI Container kompatibilitás érdekében beállítja az _initialized és _instance attribútumokat.

**Paraméterek:**

- **`cls`** (`type[T]`): Az osztály, amelyből példányt szeretnénk létrehozni. *args: Pozicionális argumentumok az osztály konstruktorához. **kwargs: Kulcsszavas argumentumok az osztály konstruktorához.

**Visszatérési érték:**

- Típus: `T`
- A létrehozott vagy meglévő singleton példány. Példa: >>> class Database(metaclass=SingletonMeta): ...     def __init__(self, connection_string: str): ...         self.connection_string = connection_string ... >>> db1 = Database("sqlite:///mydb.db") >>> db2 = Database("postgresql://localhost/mydb") >>> obj1 is obj2 True >>> db1.connection_string 'sqlite:///mydb.db'

#### `reset_singleton()`

```python
def reset_singleton(cls, target_cls: type) -> None
```

Singleton példány resetelése tesztelés céljából.

**Paraméterek:**

- **`cls`**
- **`target_cls`** (`type`): Az osztály, amelynek singleton példányát resetelni kell.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/core/base/implementations/singleton.py`](../../neural_ai/core/base/implementations/singleton.py)
