# tests/neural_ai/core/config/interfaces/test_config_interfaces_init.py

Unit tesztek a neural_ai.core.config.interfaces __init__ modulhoz.

Ez a modul teszteli a config interfaces modul publikus API-ját és exportált interfészeit.

## Importok

```python
from neural_ai.core.config.interfaces import ConfigManagerInterface
from neural_ai.core.config.interfaces import ConfigManagerFactoryInterface
from neural_ai.core.config.interfaces import CollectorsConfig
from neural_ai.core.config.interfaces import ConfigSchema
from neural_ai.core.config.interfaces import DatabaseConfig
from neural_ai.core.config.interfaces import EventsConfig
from neural_ai.core.config.interfaces import LoggingConfig
from neural_ai.core.config.interfaces import ProcessorsConfig
from neural_ai.core.config.interfaces import StorageConfig
from neural_ai.core.config.interfaces import SystemConfig
# ... és még 21 import
```

## Osztály: `TestConfigInterfacesModuleExports`

Tesztek a config interfaces modul exportálásához.

### Metódusok

#### `test_interfaces_module_exports_config_manager_interface()`

```python
def test_interfaces_module_exports_config_manager_interface(self) -> None
```

Ellenőrzi, hogy az interfaces modul exportálja a ConfigManagerInterface-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interfaces_module_exports_factory_interface()`

```python
def test_interfaces_module_exports_factory_interface(self) -> None
```

Ellenőrzi, hogy az interfaces modul exportálja a ConfigManagerFactoryInterface-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interfaces_module_exports_pydantic_types()`

```python
def test_interfaces_module_exports_pydantic_types(self) -> None
```

Ellenőrzi, hogy az interfaces modul exportálja a Pydantic típusokat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interfaces_module_all_exports()`

```python
def test_interfaces_module_all_exports(self) -> None
```

Ellenőrzi, hogy a __all__ lista tartalmazza az összes exportált elemet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestConfigManagerInterfaceMethods`

Tesztek a ConfigManagerInterface metódusaihoz.

### Metódusok

#### `test_config_manager_interface_has_get_method()`

```python
def test_config_manager_interface_has_get_method(self) -> None
```

Ellenőrzi, hogy a ConfigManagerInterface tartalmazza a get metódust.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_manager_interface_has_get_section_method()`

```python
def test_config_manager_interface_has_get_section_method(self) -> None
```

Ellenőrzi, hogy a ConfigManagerInterface tartalmazza a get_section metódust.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_manager_interface_has_validate_method()`

```python
def test_config_manager_interface_has_validate_method(self) -> None
```

Ellenőrzi, hogy a ConfigManagerInterface tartalmazza a validate metódust.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestConfigManagerFactoryInterfaceMethods`

Tesztek a ConfigManagerFactoryInterface metódusaihoz.

### Metódusok

#### `test_factory_interface_has_create_manager_method()`

```python
def test_factory_interface_has_create_manager_method(self) -> None
```

Ellenőrzi, hogy a ConfigManagerFactoryInterface tartalmazza a create_manager metódust.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestPydanticConfigModels`

Tesztek a Pydantic config modellekhez.

### Metódusok

#### `test_system_config_is_pydantic_model()`

```python
def test_system_config_is_pydantic_model(self) -> None
```

Ellenőrzi, hogy a SystemConfig Pydantic BaseModel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_storage_config_is_pydantic_model()`

```python
def test_storage_config_is_pydantic_model(self) -> None
```

Ellenőrzi, hogy a StorageConfig Pydantic BaseModel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_processors_config_is_pydantic_model()`

```python
def test_processors_config_is_pydantic_model(self) -> None
```

Ellenőrzi, hogy a ProcessorsConfig Pydantic BaseModel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logging_config_is_pydantic_model()`

```python
def test_logging_config_is_pydantic_model(self) -> None
```

Ellenőrzi, hogy a LoggingConfig Pydantic BaseModel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_config_is_pydantic_model()`

```python
def test_database_config_is_pydantic_model(self) -> None
```

Ellenőrzi, hogy a DatabaseConfig Pydantic BaseModel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_events_config_is_pydantic_model()`

```python
def test_events_config_is_pydantic_model(self) -> None
```

Ellenőrzi, hogy az EventsConfig Pydantic BaseModel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_collectors_config_is_pydantic_model()`

```python
def test_collectors_config_is_pydantic_model(self) -> None
```

Ellenőrzi, hogy a CollectorsConfig Pydantic BaseModel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_schema_is_pydantic_model()`

```python
def test_config_schema_is_pydantic_model(self) -> None
```

Ellenőrzi, hogy a ConfigSchema Pydantic BaseModel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/config/interfaces/test_config_interfaces_init.py`](../../tests/neural_ai/core/config/interfaces/test_config_interfaces_init.py)
