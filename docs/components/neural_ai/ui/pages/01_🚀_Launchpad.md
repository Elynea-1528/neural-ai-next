# neural_ai/ui/pages/01_🚀_Launchpad.py

Launchpad Page - Az alkalmazás indítólapja.

Ez a modul implementálja a fő indítólapot, amely a rendszer
áttekintését és gyors elérést nyújt a különböző funkciókhoz.

## Importok

```python
from typing import TYPE_CHECKING
import streamlit
from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
from neural_ai.ui.interfaces.page_interface import PageInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.ui.core_bridge import CoreBridge
```

## Konstansok

- **`logger`**
: `LoggerFactory.get_logger(__name__)`


- **`bridge`**
: `CoreBridge()`


- **`page`**
: `LaunchpadPage(bridge, logger)`


## Osztály: `LaunchpadPage(PageInterface)`

Launchpad Page - Az alkalmazás indítólapja.

Ez az osztály implementálja a fő indítólapot, amely a rendszer
áttekintését és gyors elérést biztosít a különböző funkciókhoz
vizuális kártyák formájában.

### Metódusok

#### `__init__()`

```python
def __init__(self, bridge: CoreBridgeInterface, logger: 'LoggerInterface') -> None
```

A Launchpad oldal inicializálása.

**Paraméterek:**

- **`self`**
- **`bridge`** (`CoreBridgeInterface`): A backend bridge példány, amely biztosítja a kapcsolatot a core rendszerrel.
- **`logger`** (`'LoggerInterface'`): Logger interfész a logoláshoz. **kwargs: Opcionális kulcsszó argumentumok, amelyek további konfigurációt adhatnak meg.

**Visszatérési érték:**

- Típus: `None`

#### `render()`

```python
def render(self) -> None
```

Az oldal tartalmának renderelése. Létrehozza a vizuális kártyákat a különböző modulokhoz, amelyek kerettel ellátott container-ekben jelennek meg. Minden kártya tartalmaz egy rövid leírást és egy linket a megfelelő oldalra.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `on_navigate_to()`

```python
def on_navigate_to(self, params: dict[str, str] | None = None) -> None
```

Akció, amikor az oldalra navigálnak.

**Paraméterek:**

- **`self`**
- **`params`** (`dict[str, str] | None`) = `None`: Navigációs paraméterek dictionary formájában, vagy None ha nincsenek paraméterek.

**Visszatérési érték:**

- Típus: `None`

#### `on_navigate_from()`

```python
def on_navigate_from(self) -> None
```

Akció, amikor elnavigálnak az oldalról. Ezt a metódust akkor hívja a rendszer, amikor a felhasználó elhagyja ezt az oldalt és egy másikra navigál.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `title()`

```python
def title(self) -> str
```

Az oldal címét visszaadó property.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `str`
- str: Az oldal címe.

#### `is_loaded()`

```python
def is_loaded(self) -> bool
```

Az oldal betöltöttségi állapotát ellenőrző property.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha az oldal betöltött, egyébként False.

---

**Forrásfájl:** [`neural_ai/ui/pages/01_🚀_Launchpad.py`](../../neural_ai/ui/pages/01_🚀_Launchpad.py)
