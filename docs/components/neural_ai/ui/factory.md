# neural_ai/ui/factory.py

UI Service Factory - A UI szolgáltatások gyártója.

Ez a modul implementálja a UI szolgáltatások létrehozását és kezelését
Dependency Injection minta szerint.

## Importok

```python
from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Any
from neural_ai.core.base.implementations.singleton import SingletonMeta
from neural_ai.core.config.interfaces.types import AIServiceConfig
from neural_ai.core.config.interfaces.types import DashboardConfig
from neural_ai.core.config.interfaces.types import DataServiceConfig
from neural_ai.core.config.interfaces.types import LiveOpsConfig
from neural_ai.core.config.interfaces.types import NavigationConfig
from neural_ai.core.config.interfaces.types import StrategyConfig
# ... és még 15 import
```

## Osztály: `UIServiceFactory`

UI Service Factory - A UI szolgáltatások gyártója.

Ez az osztály felelős a UI szolgáltatások létrehozásáért és
kezeléséért Singleton minta szerint, Dependency Injectionnel.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

A UI Service Factory inicializálása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `initialize()`

```python
def initialize(self, bridge: CoreBridgeInterface, config: dict[str, Any] | UIConfig, logger: Any, core_components: Any) -> None
```

A factory inicializálása a függőségekkel.

**Paraméterek:**

- **`self`**
- **`bridge`** (`CoreBridgeInterface`): A backend bridge példány
- **`config`** (`dict[str, Any] | UIConfig`): A UI factory konfiguráció (dict vagy UIConfig)
- **`logger`** (`Any`): A logger példány
- **`core_components`** (`Any`): A core komponensek

**Visszatérési érték:**

- Típus: `None`

#### `get_navigation_service()`

```python
def get_navigation_service(self, config: UIConfig | None = None, logger: Any | None = None, core_components: Any | None = None) -> NavigationServiceInterface
```

Navigation Service példány lekérdezése.

**Paraméterek:**

- **`self`**
- **`config`** (`UIConfig | None`) = `None`: A UI factory konfiguráció (opcionális, fallback: self._config)
- **`logger`** (`Any | None`) = `None`: A logger példány (opcionális, fallback: self._logger)
- **`core_components`** (`Any | None`) = `None`: A core komponensek (opcionális, fallback: self._core_components)

**Visszatérési érték:**

- Típus: `NavigationServiceInterface`
- NavigationServiceInterface: A Navigation Service példány

#### `get_dashboard_service()`

```python
def get_dashboard_service(self, config: UIConfig | None = None, logger: Any | None = None, core_components: Any | None = None) -> DashboardServiceInterface
```

Dashboard Service példány lekérdezése.

**Paraméterek:**

- **`self`**
- **`config`** (`UIConfig | None`) = `None`: A UI factory konfiguráció (opcionális, fallback: self._config)
- **`logger`** (`Any | None`) = `None`: A logger példány (opcionális, fallback: self._logger)
- **`core_components`** (`Any | None`) = `None`: A core komponensek (opcionális, fallback: self._core_components)

**Visszatérési érték:**

- Típus: `DashboardServiceInterface`
- DashboardServiceInterface: A Dashboard Service példány

#### `get_data_service()`

```python
def get_data_service(self, config: UIConfig | None = None, logger: Any | None = None, core_components: Any | None = None) -> DataServiceInterface
```

Data Service példány lekérdezése.

**Paraméterek:**

- **`self`**
- **`config`** (`UIConfig | None`) = `None`: A UI factory konfiguráció (opcionális, fallback: self._config)
- **`logger`** (`Any | None`) = `None`: A logger példány (opcionális, fallback: self._logger)
- **`core_components`** (`Any | None`) = `None`: A core komponensek (opcionális, fallback: self._core_components)

**Visszatérési érték:**

- Típus: `DataServiceInterface`
- DataServiceInterface: A Data Service példány

#### `get_ai_service()`

```python
def get_ai_service(self, config: UIConfig | None = None, logger: Any | None = None, core_components: Any | None = None) -> AIServiceInterface
```

AI Service példány lekérdezése.

**Paraméterek:**

- **`self`**
- **`config`** (`UIConfig | None`) = `None`: A UI factory konfiguráció (opcionális, fallback: self._config)
- **`logger`** (`Any | None`) = `None`: A logger példány (opcionális, fallback: self._logger)
- **`core_components`** (`Any | None`) = `None`: A core komponensek (opcionális, fallback: self._core_components)

**Visszatérési érték:**

- Típus: `AIServiceInterface`
- AIServiceInterface: Az AI Service példány

#### `get_strategy_service()`

```python
def get_strategy_service(self, config: UIConfig | None = None, logger: Any | None = None, core_components: Any | None = None) -> StrategyServiceInterface
```

Strategy Service példány lekérdezése.

**Paraméterek:**

- **`self`**
- **`config`** (`UIConfig | None`) = `None`: A UI factory konfiguráció (opcionális, fallback: self._config)
- **`logger`** (`Any | None`) = `None`: A logger példány (opcionális, fallback: self._logger)
- **`core_components`** (`Any | None`) = `None`: A core komponensek (opcionális, fallback: self._core_components)

**Visszatérési érték:**

- Típus: `StrategyServiceInterface`
- StrategyServiceInterface: A Strategy Service példány

#### `get_live_ops_service()`

```python
def get_live_ops_service(self, config: UIConfig | None = None, logger: Any | None = None, core_components: Any | None = None) -> LiveOpsServiceInterface
```

Live Ops Service példány lekérdezése.

**Paraméterek:**

- **`self`**
- **`config`** (`UIConfig | None`) = `None`: A UI factory konfiguráció (opcionális, fallback: self._config)
- **`logger`** (`Any | None`) = `None`: A logger példány (opcionális, fallback: self._logger)
- **`core_components`** (`Any | None`) = `None`: A core komponensek (opcionális, fallback: self._core_components)

**Visszatérési érték:**

- Típus: `LiveOpsServiceInterface`
- LiveOpsServiceInterface: A Live Ops Service példány

#### `get_all_services()`

```python
def get_all_services(self, config: UIConfig | None = None, logger: Any | None = None, core_components: Any | None = None) -> dict[str, Any]
```

Az összes szolgáltatás lekérdezése.

**Paraméterek:**

- **`self`**
- **`config`** (`UIConfig | None`) = `None`: A UI factory konfiguráció (opcionális, fallback: self._config)
- **`logger`** (`Any | None`) = `None`: A logger példány (opcionális, fallback: self._logger)
- **`core_components`** (`Any | None`) = `None`: A core komponensek (opcionális, fallback: self._core_components)

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: Az összes szolgáltatás példány

#### `is_initialized()`

```python
def is_initialized(self) -> bool
```

A factory inicializáltságát ellenőrző property.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha a factory inicializálva van, egyébként False

#### `reset()`

```python
def reset(self) -> None
```

A factory visszaállítása alapállapotba.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/ui/factory.py`](../../neural_ai/ui/factory.py)
