# tests/neural_ai/core/config/test___init__.py

Unit tesztek a neural_ai.core.config __init__ modulhoz.

Ez a modul teszteli a config modul publikus API-ját és exportált interfészeit.

## Importok

```python
import pytest
from neural_ai.core.config import ConfigError
from neural_ai.core.config import ConfigKeyError
from neural_ai.core.config import ConfigLoadError
from neural_ai.core.config import ConfigSaveError
from neural_ai.core.config import ConfigTypeError
from neural_ai.core.config import ConfigValidationError
from neural_ai.core.config import ConfigManagerFactory
from neural_ai.core.config import ConfigManagerFactoryInterface
from neural_ai.core.config import ConfigManagerInterface
# ... és még 13 import
```

## Osztály: `TestConfigModuleExports`

Tesztek a config modul exportálásához.

### Metódusok

#### `test_config_module_imports_exceptions()`

```python
def test_config_module_imports_exceptions(self) -> None
```

Ellenőrzi, hogy a config modul exportálja a kivétel osztályokat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_module_imports_factory()`

```python
def test_config_module_imports_factory(self) -> None
```

Ellenőrzi, hogy a config modul exportálja a factory osztályt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_module_imports_interfaces()`

```python
def test_config_module_imports_interfaces(self) -> None
```

Ellenőrzi, hogy a config modul exportálja az interfészeket.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_module_imports_yaml_manager()`

```python
def test_config_module_imports_yaml_manager(self) -> None
```

Ellenőrzi, hogy a config modul exportálja a YAML managert.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_module_all_exports()`

```python
def test_config_module_all_exports(self) -> None
```

Ellenőrzi, hogy a __all__ lista tartalmazza az összes exportált elemet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestConfigFactoryIntegration`

Integrációs tesztek a config factory használatához.

### Metódusok

#### `test_factory_creates_yaml_manager()`

```python
def test_factory_creates_yaml_manager(self, tmp_path) -> None
```

Ellenőrzi, hogy a factory létrehoz egy YAML config manager példányt.

**Paraméterek:**

- **`self`**
- **`tmp_path`**

**Visszatérési érték:**

- Típus: `None`

#### `test_factory_get_manager_method_exists()`

```python
def test_factory_get_manager_method_exists(self) -> None
```

Ellenőrzi, hogy a factory get_manager metódusa elérhető.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_factory_create_manager_method_exists()`

```python
def test_factory_create_manager_method_exists(self) -> None
```

Ellenőrzi, hogy a factory create_manager metódusa elérhető.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestConfigExceptionHierarchy`

Tesztek a config kivétel hierarchiához.

### Metódusok

#### `test_config_error_is_base_exception()`

```python
def test_config_error_is_base_exception(self) -> None
```

Ellenőrzi, hogy a ConfigError az Exception leszármazottja.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_specific_errors_inherit_from_config_error()`

```python
def test_specific_errors_inherit_from_config_error(self) -> None
```

Ellenőrzi, hogy a specifikus hibák a ConfigError leszármazottai.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_errors_can_be_raised()`

```python
def test_config_errors_can_be_raised(self) -> None
```

Ellenőrzi, hogy a config hibák dobhatók.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/config/test___init__.py`](../../tests/neural_ai/core/config/test___init__.py)
