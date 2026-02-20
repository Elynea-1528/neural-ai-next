# tests/neural_ai/core/logger/test_logger_factory.py

Logger Factory tesztek - Mirror Test a factory.py-hoz.

Ez a teszt suite kiegészíti a test_logger_factory.py-t
valós config betöltéssel és edge case teszteléssel.

## Importok

```python
import logging
from pathlib import Path
from typing import Any
import pytest
import yaml
from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager
from neural_ai.core.logger.factory import LoggerFactory
```

## Osztály: `TestLoggerFactoryRealConfig`

Valós YAML config tesztelése.

### Metódusok

#### `test_configure_with_real_yaml_parsing()`

```python
def test_configure_with_real_yaml_parsing(self, tmp_path: Path) -> None
```

Valós YAML fájl betöltése és config alkalmazása.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_configure_fallback_with_missing_handlers()`

```python
def test_configure_fallback_with_missing_handlers(self, caplog: pytest.LogCaptureFixture) -> None
```

Hiányos config esetén fallback console handler + warning.

**Paraméterek:**

- **`self`**
- **`caplog`** (`pytest.LogCaptureFixture`)

**Visszatérési érték:**

- Típus: `None`

#### `test_configure_fallback_warning_is_structured()`

```python
def test_configure_fallback_warning_is_structured(self, caplog: pytest.LogCaptureFixture) -> None
```

A fallback warning strukturált logolással történik.

**Paraméterek:**

- **`self`**
- **`caplog`** (`pytest.LogCaptureFixture`)

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestLoggerFactoryCoverage`

100%-os lefedettség biztosítása.

### Metódusok

#### `test_all_branches_in_get_logger()`

```python
def test_all_branches_in_get_logger(self) -> None
```

get_logger() minden ága le van fedve.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_configure_file_handler_creation()`

```python
def test_configure_file_handler_creation(self, tmp_path: Path) -> None
```

configure() file handler létrehozásának tesztelése.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_configure_rotating_file_handler()`

```python
def test_configure_rotating_file_handler(self, tmp_path: Path) -> None
```

Rotating file handler létrehozásának tesztelése.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_configure_trace_file_handler()`

```python
def test_configure_trace_file_handler(self, tmp_path: Path) -> None
```

Trace file handler létrehozásának tesztelése.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_configure_trace_file_handler_non_rotating()`

```python
def test_configure_trace_file_handler_non_rotating(self, tmp_path: Path) -> None
```

Trace file handler nem-rotating változatának tesztelése.

**Paraméterek:**

- **`self`**
- **`tmp_path`** (`Path`)

**Visszatérési érték:**

- Típus: `None`

#### `test_schema_version_methods()`

```python
def test_schema_version_methods(self) -> None
```

Schema version getter/setter tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_clear_instances()`

```python
def test_clear_instances(self) -> None
```

clear_instances() metódus tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_registered_types()`

```python
def test_get_registered_types(self) -> None
```

get_registered_types() metódus tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_is_logger_registered()`

```python
def test_is_logger_registered(self) -> None
```

is_logger_registered() metódus tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/logger/test_logger_factory.py`](../../tests/neural_ai/core/logger/test_logger_factory.py)
