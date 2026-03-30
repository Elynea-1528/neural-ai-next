# neural_ai/ui/pages/__init__.py

UI oldalak csomagja.

Ez a csomag tartalmazza a különböző főoldalakat (Launchpad, Dev Center,
Data Hub, AI Lab, Strategy Lab, Live Ops), amelyek a felhasználói
felület különböző szekcióit reprezentálják.

## Importok

```python
from typing import TYPE_CHECKING
from typing import cast
from neural_ai.ui.core_bridge import CoreBridge
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.ui.interfaces.page_interface import PageInterface
import importlib.util
from neural_ai.ui.interfaces.page_interface import PageInterface
```

## Konstansok

- **`bridge`**
: `CoreBridge()`


- **`spec`**
: `importlib.util.spec_from_file_location('launchpad_module', 'neural_ai/ui/pages/01_🚀_Launchpad.py')`


- **`launchpad_module`**
: `importlib.util.module_from_spec(spec)`


- **`LaunchpadPage`**
: `launchpad_module.LaunchpadPage`


- **`__all__`**
: `['create_launchpad_page']`


### `create_launchpad_page()`

```python
def create_launchpad_page(logger: 'LoggerInterface', config: 'ConfigManagerInterface') -> 'PageInterface'
```

Launchpad oldal példány létrehozása Dependency Injection segítségével. Ez a factory függvény a LaunchpadPage példányt hozza létre a szükséges függőségekkel. A függőségeket interfészeken keresztül kapja meg, biztosítva a loose coupling-ot.

**Paraméterek:**

- **`logger`** (`'LoggerInterface'`): Logger interfész a logoláshoz.
- **`config`** (`'ConfigManagerInterface'`): Konfigurációkezelő interfész.

**Visszatérési érték:**

- Típus: `'PageInterface'`
- PageInterface: A létrehozott Launchpad oldal példány. Note: A függvény belsőleg létrehozza és inicializálja a CoreBridge-et, amely biztosítja a backend kapcsolatot.

---

**Forrásfájl:** [`neural_ai/ui/pages/__init__.py`](../../neural_ai/ui/pages/__init__.py)
