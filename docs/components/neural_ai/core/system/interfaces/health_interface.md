# neural_ai/core/system/interfaces/health_interface.py

Rendszer egészségügyi monitorozás interfészei.

Ez a modul a rendszer egészségügyi állapotának monitorozásához szükséges
interfészeket definiálja, beleértve a komponens állapotokat, erőforrás-használatot
és rendszer metrikákat.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
```

## Osztály: `ComponentStatus(Enum)`

Komponens állapot enum.

A rendszer komponenseinek állapotát definiálja.

## Osztály: `HealthStatus(Enum)`

Rendszer egészségügyi állapot enum.

A teljes rendszer egészségügyi állapotát definiálja.

## Osztály: `ComponentHealth`

Komponens egészségügyi információi.

Egy adott komponens egészségügyi állapotát és metrikáit tartalmazza.

Attributes:
    name: A komponens neve
    status: A komponens állapota (ComponentStatus enum)
    message: Részletes üzenet vagy hiba
    timestamp: Az állapot ellenőrzésének időpontja
    metrics: Opcionális metrikák (pl. response time, error rate)

## Osztály: `SystemHealth`

Rendszer egészségügyi információi.

A teljes rendszer egészségügyi állapotát és komponenseinek állapotát tartalmazza.

Attributes:
    overall_status: A rendszer általános állapota (HealthStatus enum)
    message: Részletes üzenet
    timestamp: Az ellenőrzés időpontja
    components: A komponensek egészségügyi információi
    system_metrics: Rendszer szintű metrikák (CPU, memória, stb.)

## Osztály: `HealthMonitorInterface(ABC)`

Rendszer egészségügyi monitorozás interfész.

Ez az interfész definiálja a rendszer egészségügyi állapotának
monitorozásához szükséges metódusokat.

### Metódusok

#### `check_health()`

```python
async def check_health(self) -> SystemHealth
```

Ellenőrzi a teljes rendszer egészségügyi állapotát. A metódus összegyűjti az összes komponens és a rendszer egészségügyi információit, majd összesíti azokat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `SystemHealth`
- SystemHealth: A rendszer teljes egészségügyi állapota

#### `check_component()`

```python
async def check_component(self, component_name: str) -> ComponentHealth
```

Ellenőrzi egy adott komponens egészségügyi állapotát.

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`): A komponens neve

**Visszatérési érték:**

- Típus: `ComponentHealth`
- ComponentHealth: A komponens egészségügyi információi

**Kivételek:**

- **`ValueError`**: Ha a komponens nem létezik

#### `get_registered_components()`

```python
def get_registered_components(self) -> list[str]
```

Visszaadja a monitorozott komponensek listáját.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[str]`
- list[str]: A monitorozott komponensek nevei

#### `register_component()`

```python
def register_component(self, component_name: str, health_check: Optional['HealthCheckInterface'] = None) -> None
```

Regisztrál egy új komponenst a monitorozásra.

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`): A komponens neve
- **`health_check`** (`Optional['HealthCheckInterface']`) = `None`: Az egészségügyi ellenőrzés interfésze (opcionális)

**Visszatérési érték:**

- Típus: `None`

#### `unregister_component()`

```python
def unregister_component(self, component_name: str) -> None
```

Eltávolít egy komponenst a monitorozás alól.

**Paraméterek:**

- **`self`**
- **`component_name`** (`str`): A komponens neve

**Visszatérési érték:**

- Típus: `None`

## Osztály: `HealthCheckInterface(ABC)`

Egyedi egészségügyi ellenőrzés interfész.

Ez az interfész egy specifikus egészségügyi ellenőrzést definiál,
amelyet a HealthMonitorInterface implementációk használhatnak.

### Metódusok

#### `check()`

```python
async def check(self) -> ComponentHealth
```

Végrehajtja az egészségügyi ellenőrzést.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `ComponentHealth`
- ComponentHealth: Az ellenőrzés eredménye

#### `get_name()`

```python
def get_name(self) -> str
```

Visszaadja az ellenőrzés nevét.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `str`
- str: Az ellenőrzés neve

---

**Forrásfájl:** [`neural_ai/core/system/interfaces/health_interface.py`](../../neural_ai/core/system/interfaces/health_interface.py)
