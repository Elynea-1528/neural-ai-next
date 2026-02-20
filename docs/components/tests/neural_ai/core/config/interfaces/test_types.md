# tests/neural_ai/core/config/interfaces/test_types.py

Unit tesztek a neural_ai.core.config.interfaces.types modulhoz.

Ez a modul teszteli a Pydantic config típusokat és validációt.

## Importok

```python
import pytest
from pydantic import ValidationError
from neural_ai.core.config.interfaces.types import SystemConfig
from neural_ai.core.config.interfaces.types import StorageConfig
from neural_ai.core.config.interfaces.types import ProcessorsConfig
from neural_ai.core.config.interfaces.types import LoggingConfig
from neural_ai.core.config.interfaces.types import DatabaseConfig
from neural_ai.core.config.interfaces.types import EventsConfig
from neural_ai.core.config.interfaces.types import CollectorsConfig
from neural_ai.core.config.interfaces.types import ConfigSchema
# ... és még 28 import
```

## Osztály: `TestPydanticConfigTypesExist`

Tesztek a Pydantic config típusok létezéséhez.

### Metódusok

#### `test_system_config_exists()`

```python
def test_system_config_exists(self) -> None
```

Ellenőrzi, hogy a SystemConfig létezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_storage_config_exists()`

```python
def test_storage_config_exists(self) -> None
```

Ellenőrzi, hogy a StorageConfig létezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_processors_config_exists()`

```python
def test_processors_config_exists(self) -> None
```

Ellenőrzi, hogy a ProcessorsConfig létezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logging_config_exists()`

```python
def test_logging_config_exists(self) -> None
```

Ellenőrzi, hogy a LoggingConfig létezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_config_exists()`

```python
def test_database_config_exists(self) -> None
```

Ellenőrzi, hogy a DatabaseConfig létezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_events_config_exists()`

```python
def test_events_config_exists(self) -> None
```

Ellenőrzi, hogy az EventsConfig létezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_collectors_config_exists()`

```python
def test_collectors_config_exists(self) -> None
```

Ellenőrzi, hogy a CollectorsConfig létezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_schema_exists()`

```python
def test_config_schema_exists(self) -> None
```

Ellenőrzi, hogy a ConfigSchema létezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestPydanticBaseModelInheritance`

Tesztek a Pydantic BaseModel örökléshez.

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

## Osztály: `TestPydanticValidation`

Tesztek a Pydantic validációhoz.

### Metódusok

#### `test_handler_config_validates_level_pattern()`

```python
def test_handler_config_validates_level_pattern(self) -> None
```

Ellenőrzi, hogy a HandlerConfig validálja a level pattern-t.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_paths_config_validates_min_length()`

```python
def test_paths_config_validates_min_length(self) -> None
```

Ellenőrzi, hogy a PathsConfig validálja a min_length-et.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_handler_config_validates_max_bytes_positive()`

```python
def test_handler_config_validates_max_bytes_positive(self) -> None
```

Ellenőrzi, hogy a HandlerConfig validálja a max_bytes pozitív értékét.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_handler_config_validates_backup_count_non_negative()`

```python
def test_handler_config_validates_backup_count_non_negative(self) -> None
```

Ellenőrzi, hogy a HandlerConfig validálja a backup_count nem-negatív értékét.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestPydanticModelConfig`

Tesztek a Pydantic model config-hoz.

### Metódusok

#### `test_system_config_forbids_extra_fields()`

```python
def test_system_config_forbids_extra_fields(self) -> None
```

Ellenőrzi, hogy a SystemConfig tiltja az extra mezőket.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_storage_config_forbids_extra_fields()`

```python
def test_storage_config_forbids_extra_fields(self) -> None
```

Ellenőrzi, hogy a StorageConfig tiltja az extra mezőket.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_config_schema_forbids_extra_fields()`

```python
def test_config_schema_forbids_extra_fields(self) -> None
```

Ellenőrzi, hogy a ConfigSchema tiltja az extra mezőket.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestAdditionalConfigTypes`

Tesztek további config típusokhoz.

### Metódusok

#### `test_paths_config_exists()`

```python
def test_paths_config_exists(self) -> None
```

Ellenőrzi, hogy a PathsConfig létezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_handler_config_exists()`

```python
def test_handler_config_exists(self) -> None
```

Ellenőrzi, hogy a HandlerConfig létezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_logger_config_exists()`

```python
def test_logger_config_exists(self) -> None
```

Ellenőrzi, hogy a LoggerConfig létezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_ingestion_config_exists()`

```python
def test_ingestion_config_exists(self) -> None
```

Ellenőrzi, hogy az IngestionConfig létezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_ui_config_exists()`

```python
def test_ui_config_exists(self) -> None
```

Ellenőrzi, hogy a UIConfig létezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/config/interfaces/test_types.py`](../../tests/neural_ai/core/config/interfaces/test_types.py)
