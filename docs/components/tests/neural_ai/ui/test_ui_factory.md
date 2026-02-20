# tests/neural_ai/ui/test_ui_factory.py

Tesztek a UI Service Factory számára.

## Importok

```python
from unittest.mock import Mock
import pytest
from pydantic import ValidationError
from neural_ai.core.config.interfaces.types import UIConfig
from neural_ai.ui.factory import UIServiceFactory
from neural_ai.ui.interfaces.ai_service_interface import AIServiceInterface
from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
from neural_ai.ui.interfaces.dashboard_service_interface import DashboardServiceInterface
from neural_ai.ui.interfaces.data_service_interface import DataServiceInterface
from neural_ai.ui.interfaces.live_ops_service_interface import LiveOpsServiceInterface
# ... és még 4 import
```

## Osztály: `TestUIServiceFactory`

A UIServiceFactory tesztosztálya.

### Metódusok

#### `setup_method()`

```python
def setup_method(self) -> None
```

Tesztelés előtti beállítások.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `teardown_method()`

```python
def teardown_method(self) -> None
```

Tesztelés utáni takarítás.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_factory_initialization()`

```python
def test_factory_initialization(self) -> None
```

A factory inicializálásának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_initialize_with_bridge()`

```python
def test_initialize_with_bridge(self) -> None
```

A factory inicializálásának tesztelése bridge-el.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_navigation_service_before_initialization()`

```python
def test_get_navigation_service_before_initialization(self) -> None
```

Navigation service lekérdezése inicializálás előtt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_navigation_service_after_initialization()`

```python
def test_get_navigation_service_after_initialization(self) -> None
```

Navigation service lekérdezése inicializálás után.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_dashboard_service_before_initialization()`

```python
def test_get_dashboard_service_before_initialization(self) -> None
```

Dashboard service lekérdezése inicializálás előtt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_dashboard_service_after_initialization()`

```python
def test_get_dashboard_service_after_initialization(self) -> None
```

Dashboard service lekérdezése inicializálás után.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_data_service_before_initialization()`

```python
def test_get_data_service_before_initialization(self) -> None
```

Data service lekérdezése inicializálás előtt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_data_service_after_initialization()`

```python
def test_get_data_service_after_initialization(self) -> None
```

Data service lekérdezése inicializálás után.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_ai_service_before_initialization()`

```python
def test_get_ai_service_before_initialization(self) -> None
```

AI service lekérdezése inicializálás előtt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_ai_service_after_initialization()`

```python
def test_get_ai_service_after_initialization(self) -> None
```

AI service lekérdezése inicializálás után.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_strategy_service_before_initialization()`

```python
def test_get_strategy_service_before_initialization(self) -> None
```

Strategy service lekérdezése inicializálás előtt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_strategy_service_after_initialization()`

```python
def test_get_strategy_service_after_initialization(self) -> None
```

Strategy service lekérdezése inicializálás után.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_live_ops_service_before_initialization()`

```python
def test_get_live_ops_service_before_initialization(self) -> None
```

Live Ops service lekérdezése inicializálás előtt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_live_ops_service_after_initialization()`

```python
def test_get_live_ops_service_after_initialization(self) -> None
```

Live Ops service lekérdezése inicializálás után.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_all_services()`

```python
def test_get_all_services(self) -> None
```

Az összes szolgáltatás lekérdezésének tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_all_services_before_initialization()`

```python
def test_get_all_services_before_initialization(self) -> None
```

Összes szolgáltatás lekérdezése inicializálás előtt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_is_initialized_property()`

```python
def test_is_initialized_property(self) -> None
```

Az is_initialized property tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_reset_method()`

```python
def test_reset_method(self) -> None
```

A reset metódus tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_singleton_pattern()`

```python
def test_singleton_pattern(self) -> None
```

A Singleton minta tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_data_service_compatibility()`

```python
def test_data_service_compatibility(self) -> None
```

DataService kompatibilitás ellenőrzése a factory-val.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_service_caching()`

```python
def test_service_caching(self) -> None
```

Szolgáltatások gyorsítótárazásának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestUIConfigValidation`

UIConfig Pydantic validáció tesztek.

### Metódusok

#### `test_valid_ui_config()`

```python
def test_valid_ui_config(self) -> None
```

Érvényes UI konfiguráció tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_invalid_theme_raises_error()`

```python
def test_invalid_theme_raises_error(self) -> None
```

Érvénytelen téma ValidationError-t dob.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_negative_refresh_rate_raises_error()`

```python
def test_negative_refresh_rate_raises_error(self) -> None
```

Negatív refresh_rate ValidationError-t dob.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_zero_refresh_rate_raises_error()`

```python
def test_zero_refresh_rate_raises_error(self) -> None
```

Nulla refresh_rate ValidationError-t dob.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_factory_validates_config()`

```python
def test_factory_validates_config(self) -> None
```

Factory Pydantic validációt végez.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_default_values()`

```python
def test_default_values(self) -> None
```

Alapértelmezett értékek tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_nested_config_validation()`

```python
def test_nested_config_validation(self) -> None
```

Beágyazott konfiguráció validálása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/ui/test_ui_factory.py`](../../tests/neural_ai/ui/test_ui_factory.py)
