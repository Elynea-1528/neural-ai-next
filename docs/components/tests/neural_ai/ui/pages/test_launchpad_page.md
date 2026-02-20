# tests/neural_ai/ui/pages/test_launchpad_page.py

Tesztelési modul a Launchpad oldalhoz.

Ez a modul tartalmazza a LaunchpadPage osztály egységtesztjeit,
amelyek ellenőrzik az oldal alapvető funkcionalitását.

## Importok

```python
import importlib.util
import sys
from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
```

## Konstansok

- **`spec`**
: `importlib.util.spec_from_file_location('launchpad_page', 'neural_ai/ui/pages/01_🚀_Launchpad.py')`


- **`launchpad_module`**
: `importlib.util.module_from_spec(spec)`


- **`LaunchpadPage`**
: `launchpad_module.LaunchpadPage`


## Osztály: `TestLaunchpadPage`

LaunchpadPage osztály tesztjei.

Ezek a tesztek ellenőrzik az oldal inicializálását, renderelését
és navigációs metódusait.

### Metódusok

#### `mock_bridge()`

```python
def mock_bridge(self) -> MagicMock
```

Mock CoreBridgeInterface létrehozása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MagicMock`
- MagicMock: A mockolt bridge példány.

#### `mock_logger()`

```python
def mock_logger(self) -> MagicMock
```

Mock LoggerInterface létrehozása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `MagicMock`
- MagicMock: A mockolt logger példány.

#### `launchpad_page()`

```python
def launchpad_page(self, mock_bridge: MagicMock, mock_logger: MagicMock) -> LaunchpadPage
```

LaunchpadPage példány létrehozása teszteléshez.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.
- **`mock_logger`** (`MagicMock`): A mockolt logger példány.

**Visszatérési érték:**

- Típus: `LaunchpadPage`
- LaunchpadPage: A tesztelendő oldal példány.

#### `test_init()`

```python
def test_init(self, mock_bridge: MagicMock, mock_logger: MagicMock) -> None
```

Teszteli az osztály inicializálását.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.
- **`mock_logger`** (`MagicMock`): A mockolt logger példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_init_with_kwargs()`

```python
def test_init_with_kwargs(self, mock_bridge: MagicMock, mock_logger: MagicMock) -> None
```

Teszteli az inicializálást további paraméterekkel.

**Paraméterek:**

- **`self`**
- **`mock_bridge`** (`MagicMock`): A mockolt bridge példány.
- **`mock_logger`** (`MagicMock`): A mockolt logger példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_title_property()`

```python
def test_title_property(self, launchpad_page: LaunchpadPage) -> None
```

Teszteli a title property-t.

**Paraméterek:**

- **`self`**
- **`launchpad_page`** (`LaunchpadPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_is_loaded_property_initial()`

```python
def test_is_loaded_property_initial(self, launchpad_page: LaunchpadPage) -> None
```

Teszteli az is_loaded property kezdeti állapotát.

**Paraméterek:**

- **`self`**
- **`launchpad_page`** (`LaunchpadPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_is_loaded_property_after_navigation()`

```python
def test_is_loaded_property_after_navigation(self, launchpad_page: LaunchpadPage) -> None
```

Teszteli az is_loaded property-t navigáció után.

**Paraméterek:**

- **`self`**
- **`launchpad_page`** (`LaunchpadPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_on_navigate_to_with_params()`

```python
def test_on_navigate_to_with_params(self, launchpad_page: LaunchpadPage) -> None
```

Teszteli a navigációt paraméterekkel.

**Paraméterek:**

- **`self`**
- **`launchpad_page`** (`LaunchpadPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_on_navigate_to_without_params()`

```python
def test_on_navigate_to_without_params(self, launchpad_page: LaunchpadPage) -> None
```

Teszteli a navigációt paraméterek nélkül.

**Paraméterek:**

- **`self`**
- **`launchpad_page`** (`LaunchpadPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_on_navigate_from()`

```python
def test_on_navigate_from(self, launchpad_page: LaunchpadPage) -> None
```

Teszteli az oldal elhagyásakor történő akciót.

**Paraméterek:**

- **`self`**
- **`launchpad_page`** (`LaunchpadPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_render()`

```python
def test_render(self, mock_divider: MagicMock, mock_page_link: MagicMock, mock_write: MagicMock, mock_subheader: MagicMock, mock_container: MagicMock, mock_columns: MagicMock, mock_markdown: MagicMock, mock_title: MagicMock, launchpad_page: LaunchpadPage) -> None
```

Teszteli az oldal renderelését.

**Paraméterek:**

- **`self`**
- **`mock_divider`** (`MagicMock`): Mockolt divider.
- **`mock_page_link`** (`MagicMock`): Mockolt page_link.
- **`mock_write`** (`MagicMock`): Mockolt write.
- **`mock_subheader`** (`MagicMock`): Mockolt subheader.
- **`mock_container`** (`MagicMock`): Mockolt container.
- **`mock_columns`** (`MagicMock`): Mockolt columns.
- **`mock_markdown`** (`MagicMock`): Mockolt markdown.
- **`mock_title`** (`MagicMock`): Mockolt title.
- **`launchpad_page`** (`LaunchpadPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

#### `test_render_without_errors()`

```python
def test_render_without_errors(self, launchpad_page: LaunchpadPage) -> None
```

Teszteli, hogy a render metódus hiba nélkül lefut.

**Paraméterek:**

- **`self`**
- **`launchpad_page`** (`LaunchpadPage`): A tesztelendő oldal példány.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/ui/pages/test_launchpad_page.py`](../../tests/neural_ai/ui/pages/test_launchpad_page.py)
