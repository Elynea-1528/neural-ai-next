# neural_ai/ui/streamlit_app.py

Streamlit Dashboard Application.

Ez a modul implementálja a Neural AI Next Streamlit dashboardját,
ami a rendszer állapotát és teljesítményét jeleníti meg.

## Importok

```python
import sys
from pathlib import Path
from typing import TYPE_CHECKING
import streamlit
from neural_ai.ui.app import UIApplication
```

## Konstansok

- **`factory`**
: `app.get_factory()`


- **`dashboard_service`**
: `factory.get_dashboard_service()`


- **`health_status`**
: `dashboard_service.get_health_status()`


- **`core_status`**
: `health_status.get('core', 'UNKNOWN')`


- **`core_icon`**
: `'✅' if core_status == 'OK' else '⚠️' if core_status == 'WARNING' else '❌'`


- **`db_status`**
: `health_status.get('database', 'UNKNOWN')`


- **`db_icon`**
: `'✅' if db_status == 'OK' else '⚠️' if db_status == 'WARNING' else '❌'`


- **`event_status`**
: `health_status.get('event_bus', 'UNKNOWN')`


- **`event_icon`**
: `'✅' if event_status == 'OK' else '⚠️' if event_status == 'WARNING' else '❌'`


- **`collector_status`**
: `health_status.get('collectors', 'UNKNOWN')`


- **`collector_icon`**
: `'✅' if collector_status == 'OK' else '⚠️' if collector_status == 'WARNING' else '❌'`


- **`factory`**
: `app.get_factory()`


- **`dashboard_service`**
: `factory.get_dashboard_service()`


- **`health_status`**
: `dashboard_service.get_health_status()`


- **`factory`**
: `app.get_factory()`


- **`dashboard_service`**
: `factory.get_dashboard_service()`


- **`metrics`**
: `dashboard_service.get_performance_metrics()`


- **`cpu_usage`**
: `metrics.get('cpu_usage', 0.0)`


- **`memory_usage`**
: `metrics.get('memory_usage', 0.0)`


- **`disk_usage`**
: `metrics.get('disk_usage', 0.0)`


- **`response_time`**
: `metrics.get('response_time', 0.0)`


- **`factory`**
: `app.get_factory()`


- **`dashboard_service`**
: `factory.get_dashboard_service()`


- **`activities`**
: `dashboard_service.get_recent_activities()`


- **`timestamp`**
: `activity.get('timestamp', '')`


- **`activity_type`**
: `activity.get('type', 'INFO')`


- **`message`**
: `activity.get('message', '')`


- **`component`**
: `activity.get('component', '')`


- **`icon`**
: `{'INFO': 'ℹ️', 'SUCCESS': '✅', 'WARNING': '⚠️', 'ERROR': '❌'}.get(activity_type, 'ℹ️')`


- **`factory`**
: `app.get_factory()`


- **`dashboard_service`**
: `factory.get_dashboard_service()`


- **`app`**
: `UIApplication()`


### `setup_page_config()`

```python
def setup_page_config() -> None
```

Oldal konfiguráció beállítása.

**Visszatérési érték:**

- Típus: `None`

### `render_header()`

```python
def render_header() -> None
```

Fejléc renderelése.

**Visszatérési érték:**

- Típus: `None`

### `render_system_overview()`

```python
def render_system_overview(app: UIApplication) -> None
```

Rendszer áttekintő megjelenítése. A valós rendszerállapotot jeleníti meg a DashboardService.get_health_status() metódusból lekért adatok alapján.

**Paraméterek:**

- **`app`** (`UIApplication`): A UI alkalmazás példány

**Visszatérési érték:**

- Típus: `None`

### `render_health_status()`

```python
def render_health_status(app: UIApplication) -> None
```

Egészségügyi állapot megjelenítése.

**Paraméterek:**

- **`app`** (`UIApplication`): A UI alkalmazás példány

**Visszatérési érték:**

- Típus: `None`

### `render_performance_metrics()`

```python
def render_performance_metrics(app: UIApplication) -> None
```

Teljesítmény metrikák megjelenítése.

**Paraméterek:**

- **`app`** (`UIApplication`): A UI alkalmazás példány

**Visszatérési érték:**

- Típus: `None`

### `render_recent_activities()`

```python
def render_recent_activities(app: UIApplication) -> None
```

Legutóbbi tevékenységek megjelenítése.

**Paraméterek:**

- **`app`** (`UIApplication`): A UI alkalmazás példány

**Visszatérési érték:**

- Típus: `None`

### `render_sidebar()`

```python
def render_sidebar(app: UIApplication) -> None
```

Oldalsáv renderelése.

**Paraméterek:**

- **`app`** (`UIApplication`): A UI alkalmazás példány

**Visszatérési érték:**

- Típus: `None`

### `main()`

```python
def main() -> None
```

Fő alkalmazás.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/ui/streamlit_app.py`](../../neural_ai/ui/streamlit_app.py)
