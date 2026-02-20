# neural_ai/ui/core_bridge.py

Core Bridge implementáció - Backend kapcsolat a Neural AI Next rendszerhez.

Ez a modul implementálja a backend rendszerrel való kommunikációt biztosító
CoreBridge osztályt, amely a core komponensek elérését teszi lehetővé a UI számára.

## Importok

```python
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional
from neural_ai.core.base.implementations.singleton import SingletonMeta
from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader
from neural_ai.core.base.implementations.component_bundle import CoreComponents
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.data.storage.interfaces.storage_interface import StorageInterface
from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
# ... és még 5 import
```

## Osztály: `CoreBridge`

Core Bridge osztály - Backend kapcsolatért felelős Singleton.

Ez az osztály biztosítja a kommunikációt a backend rendszerrel,
inicializálja a core komponenseket, és lehetővé teszi a UI számára
a parquet_storage, bi5_downloader és strategy_service komponensek elérését.

### Metódusok

#### `__init__()`

```python
def __init__(self) -> None
```

A Core Bridge inicializálása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `get_instance()`

```python
def get_instance(self) -> 'CoreBridgeInterface'
```

A Singleton példányt visszaadó metódus.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `'CoreBridgeInterface'`
- CoreBridgeInterface: A Singleton példány

#### `initialize()`

```python
def initialize(self) -> None
```

A bridge inicializálása a backend core komponensekkel. Ez a metódus meghívja a bootstrap_core() függvényt, amely elindítja az összes alapvető rendszerkomponenst (logger, config, storage, stb.).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_initialize_strategy_service()`

```python
def _initialize_strategy_service(self) -> None
```

A Strategy Service inicializálása. Létrehozza és regisztrálja a Strategy Service-t, amely a kereskedési stratégiák kezeléséért felelős.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `get_component()`

```python
def get_component(self, component_type: str) -> object | None
```

Komponens lekérése a backend rendszerből.

**Paraméterek:**

- **`self`**
- **`component_type`** (`str`): A lekérdezni kívánt komponens típusa. Támogatott típusok: 'parquet_storage', 'bi5_downloader', 'strategy_service', 'config'

**Visszatérési érték:**

- Típus: `object | None`
- Optional[object]: A lekérdezett komponens vagy None, ha nem található vagy a bridge nincs inicializálva.

**Kivételek:**

- **`RuntimeError`**: Ha a bridge nincs inicializálva

#### `_get_parquet_storage()`

```python
def _get_parquet_storage(self) -> Optional['StorageInterface']
```

Parquet storage komponens lekérése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Optional['StorageInterface']`
- Optional[StorageInterface]: A parquet storage komponens vagy None

#### `_get_bi5_downloader()`

```python
def _get_bi5_downloader(self) -> Optional['IJForexDownloader']
```

BI5 downloader komponens létrehozása és visszaadása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Optional['IJForexDownloader']`
- Optional[IJForexDownloader]: A BI5 downloader komponens vagy None

#### `_get_strategy_service()`

```python
def _get_strategy_service(self) -> Optional['StrategyServiceInterface']
```

Strategy Service komponens lekérése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Optional['StrategyServiceInterface']`
- Optional[StrategyServiceInterface]: A Strategy Service komponens vagy None

#### `send_command()`

```python
def send_command(self, command: str, params: dict[str, Any]) -> dict[str, Any]
```

Parancs küldése a backend rendszernek.

**Paraméterek:**

- **`self`**
- **`command`** (`str`): A végrehajtandó parancs
- **`params`** (`dict[str, Any]`): A parancshoz tartozó paraméterek

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: A parancs válasza

#### `get_system_info()`

```python
def get_system_info(self) -> dict[str, Any]
```

Rendszerinformáció lekérése a backendről.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: A rendszer aktuális állapotinformációi

#### `is_connected()`

```python
def is_connected(self) -> bool
```

A backendkel való kapcsolat állapotát ellenőrző property.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha a kapcsolat aktív, egyébként False

#### `core()`

```python
def core(self) -> Optional['CoreComponents']
```

A core komponensek elérését biztosító property.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Optional['CoreComponents']`
- Optional[CoreComponents]: A core komponensek vagy None, ha nincs inicializálva

#### `core()`

```python
def core(self, value: Optional['CoreComponents']) -> None
```

A core komponensek beállítása (tesztelés céljából).

**Paraméterek:**

- **`self`**
- **`value`** (`Optional['CoreComponents']`)

**Visszatérési érték:**

- Típus: `None`

#### `connected()`

```python
def connected(self) -> bool
```

A backendkel való kapcsolat állapotát ellenőrző property.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha a kapcsolat aktív, egyébként False

#### `connected()`

```python
def connected(self, value: bool) -> None
```

A kapcsolat állapotának beállítása (tesztelés céljából).

**Paraméterek:**

- **`self`**
- **`value`** (`bool`)

**Visszatérési érték:**

- Típus: `None`

#### `strategy_service()`

```python
def strategy_service(self) -> Optional['StrategyServiceInterface']
```

A strategy service elérését biztosító property.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Optional['StrategyServiceInterface']`
- Optional[StrategyServiceInterface]: A strategy service vagy None

#### `strategy_service()`

```python
def strategy_service(self, value: Optional['StrategyServiceInterface']) -> None
```

A strategy service beállítása (tesztelés céljából).

**Paraméterek:**

- **`self`**
- **`value`** (`Optional['StrategyServiceInterface']`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/ui/core_bridge.py`](../../neural_ai/ui/core_bridge.py)
