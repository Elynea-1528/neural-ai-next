# neural_ai/ui/app.py

UI Main Application - A felhasználói felület fő alkalmazása.

Ez a modul implementálja a UI alkalmazás fő belépési pontját,
amely összekapcsolja az összes UI komponenst.

## Importok

```python
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional
from neural_ai.core.config.interfaces.types import UIConfig
from neural_ai.ui.core_bridge import CoreBridge
from neural_ai.ui.factory import UIServiceFactory
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.ui.interfaces.navigation_service_interface import NavigationServiceInterface
from neural_ai.core.logger.factory import LoggerFactory
```

## Osztály: `UIApplication`

UI Application - A felhasználói felület fő alkalmazása.

Ez az osztály felelős a teljes UI rendszer inicializálásáért és
működtetéséért, összekapcsolva az összes komponenst.

### Metódusok

#### `__init__()`

```python
def __init__(self, config: dict[str, Any] | None = None, logger: Optional['LoggerInterface'] = None) -> None
```

A UI alkalmazás inicializálása.

**Paraméterek:**

- **`self`**
- **`config`** (`dict[str, Any] | None`) = `None`: Konfigurációs beállítások
- **`logger`** (`Optional['LoggerInterface']`) = `None`: Logger példány

**Visszatérési érték:**

- Típus: `None`

#### `initialize()`

```python
def initialize(self) -> bool
```

Az alkalmazás inicializálása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha sikeres az inicializálás

#### `run()`

```python
def run(self) -> None
```

Az alkalmazás indítása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `stop()`

```python
def stop(self) -> None
```

Az alkalmazás leállítása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `get_navigation_service()`

```python
def get_navigation_service(self) -> 'NavigationServiceInterface'
```

Navigation Service lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `'NavigationServiceInterface'`
- NavigationServiceInterface: A Navigation Service példány

#### `get_factory()`

```python
def get_factory(self) -> UIServiceFactory
```

UI Service Factory lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `UIServiceFactory`
- UIServiceInterface: Az UI Service Factory példány

#### `is_running()`

```python
def is_running(self) -> bool
```

Az alkalmazás futási állapotát ellenőrző property.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha az alkalmazás fut, egyébként False

#### `is_running()`

```python
def is_running(self, value: bool) -> None
```

Az alkalmazás futási állapotának beállítása.

**Paraméterek:**

- **`self`**
- **`value`** (`bool`): Az új futási állapot

**Visszatérési érték:**

- Típus: `None`

#### `is_initialized()`

```python
def is_initialized(self) -> bool
```

Az alkalmazás inicializáltságát ellenőrző property.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha az alkalmazás inicializálva van, egyébként False

#### `init_error()`

```python
def init_error(self) -> Exception | None
```

Az inicializálási hiba lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Exception | None`
- Exception | None: A hiba, ha volt, egyébként None

#### `config()`

```python
def config(self) -> dict[str, Any]
```

Konfigurációs beállítások lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- dict[str, Any]: A konfigurációs szótár

#### `config()`

```python
def config(self, value: dict[str, Any]) -> None
```

Konfigurációs beállítások beállítása.

**Paraméterek:**

- **`self`**
- **`value`** (`dict[str, Any]`): Az új konfigurációs szótár

**Visszatérési érték:**

- Típus: `None`

#### `logger()`

```python
def logger(self) -> Optional['LoggerInterface']
```

Logger példány lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Optional['LoggerInterface']`
- LoggerInterface | None: A logger példány, vagy None

#### `logger()`

```python
def logger(self, value: Optional['LoggerInterface']) -> None
```

Logger példány beállítása.

**Paraméterek:**

- **`self`**
- **`value`** (`Optional['LoggerInterface']`): Az új logger példány

**Visszatérési érték:**

- Típus: `None`

#### `bridge()`

```python
def bridge(self) -> CoreBridge | None
```

Core Bridge példány lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `CoreBridge | None`
- CoreBridge | None: A bridge példány, vagy None

#### `bridge()`

```python
def bridge(self, value: CoreBridge | None) -> None
```

Core Bridge példány beállítása.

**Paraméterek:**

- **`self`**
- **`value`** (`CoreBridge | None`): Az új bridge példány

**Visszatérési érték:**

- Típus: `None`

#### `factory()`

```python
def factory(self) -> UIServiceFactory | None
```

UI Service Factory példány lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `UIServiceFactory | None`
- UIServiceFactory | None: A factory példány, vagy None

#### `factory()`

```python
def factory(self, value: UIServiceFactory | None) -> None
```

UI Service Factory példány beállítása.

**Paraméterek:**

- **`self`**
- **`value`** (`UIServiceFactory | None`): Az új factory példány

**Visszatérési érték:**

- Típus: `None`

#### `navigation()`

```python
def navigation(self) -> Optional['NavigationServiceInterface']
```

Navigation Service példány lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Optional['NavigationServiceInterface']`
- NavigationServiceInterface | None: A navigation példány, vagy None

#### `navigation()`

```python
def navigation(self, value: Optional['NavigationServiceInterface']) -> None
```

Navigation Service példány beállítása.

**Paraméterek:**

- **`self`**
- **`value`** (`Optional['NavigationServiceInterface']`): Az új navigation példány

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/ui/app.py`](../../neural_ai/ui/app.py)
