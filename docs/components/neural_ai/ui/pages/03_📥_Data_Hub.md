# neural_ai/ui/pages/03_📥_Data_Hub.py

Data Hub Page - Adatkezelő központ.

## Importok

```python
import asyncio
from datetime import UTC
from datetime import datetime
from datetime import time
from typing import TYPE_CHECKING
from typing import Any
import streamlit
from neural_ai.ui.interfaces.page_interface import PageInterface
from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
from neural_ai.ui.interfaces.data_service_interface import DataServiceInterface
# ... és még 2 import
```

## Konstansok

- **`bridge`**
: `CoreBridge()`


- **`page`**
: `DataHubPage(bridge)`


## Osztály: `DataHubPage(PageInterface)`

Data Hub oldal.

Ez az oldal felelős az adatok kezeléséért, letöltéséért és megjelenítéséért
a DataService segítségével, amely a UIServiceFactory-n keresztül érhető el.

### Metódusok

#### `__init__()`

```python
def __init__(self, bridge: 'CoreBridgeInterface') -> None
```

A Data Hub oldal inicializálása.

**Paraméterek:**

- **`self`**
- **`bridge`** (`'CoreBridgeInterface'`): A CoreBridge példány, amelyen keresztül elérjük a backendet **kwargs: További opcionális argumentumok

**Visszatérési érték:**

- Típus: `None`

#### `render()`

```python
def render(self) -> None
```

Az oldal megjelenítése Streamlit segítségével.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_render_data_listing()`

```python
def _render_data_listing(self) -> None
```

Elérhető adatok listázásának megjelenítése. A metódus lekéri a konfigurált szimbólumokat a DataService segítségével, és legördülő menüben felajánlja azokat szűréshez. Ezután a kiválasztott szűrővel listázza az elérhető adatokat. A metódus a következőket jeleníti meg: - Szimbólum szűrő legördülő menü - Adatok frissítése gomb - Az elérhető adatok DataFrame táblázatban - Összesítő metrikák (összes rekord, méret, adatforrások)

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_render_download_history()`

```python
def _render_download_history(self) -> None
```

Történelmi adatok letöltésének megjelenítése. A metódus lekéri a konfigurált szimbólumokat a DataService segítségével, és legördülő menüben felajánlja azokat a felhasználónak. Ezután dátum tartományt kér be, és indítja el a történelmi adatok letöltését. A metódus a következőket jeleníti meg: - Szimbólum választó legördülő menü (az "ALL" opcióval) - Kezdő és záró dátum választók (alapértelmezett értékekkel a configból) - Letöltés indítása gomb - Letöltési eredmények és statisztikák

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_render_data_export()`

```python
def _render_data_export(self) -> None
```

Adatok exportálásának megjelenítése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `on_navigate_to()`

```python
def on_navigate_to(self, params: dict[str, Any] | None = None) -> None
```

Az oldalra navigáláskor meghívott metódus.

**Paraméterek:**

- **`self`**
- **`params`** (`dict[str, Any] | None`) = `None`: Opcionális navigációs paraméterek

**Visszatérési érték:**

- Típus: `None`

#### `on_navigate_from()`

```python
def on_navigate_from(self) -> None
```

Az oldalról navigáláskor meghívott metódus.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `title()`

```python
def title(self) -> str
```

Az oldal címe.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `str`
- str: Az oldal címe

#### `is_loaded()`

```python
def is_loaded(self) -> bool
```

Az oldal betöltöttségi állapota.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha az oldal betöltődött, egyébként False

---

**Forrásfájl:** [`neural_ai/ui/pages/03_📥_Data_Hub.py`](../../neural_ai/ui/pages/03_📥_Data_Hub.py)
