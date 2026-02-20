# tests/neural_ai/core/config/exceptions/test_config_error.py

Átfogó tesztek a konfigurációs kivételekhez.

Ez a modul tartalmazza a ConfigError és leszármazott osztályok
részletes tesztelését, beleértve az attribútumok ellenőrzését.

## Importok

```python
from neural_ai.core.config.exceptions.config_error import ConfigError
from neural_ai.core.config.exceptions.config_error import ConfigKeyError
from neural_ai.core.config.exceptions.config_error import ConfigLoadError
from neural_ai.core.config.exceptions.config_error import ConfigSaveError
from neural_ai.core.config.exceptions.config_error import ConfigTypeError
from neural_ai.core.config.exceptions.config_error import ConfigValidationError
```

## Osztály: `TestConfigError`

ConfigError alaposztály tesztjei.

### Metódusok

#### `test_base_error_creation()`

```python
def test_base_error_creation(self) -> None
```

Teszteli az alap ConfigError létrehozását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_base_error_with_code()`

```python
def test_base_error_with_code(self) -> None
```

Teszteli a ConfigError létrehozását hibakóddal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestConfigLoadError`

ConfigLoadError tesztjei.

### Metódusok

#### `test_load_error_creation()`

```python
def test_load_error_creation(self) -> None
```

Teszteli a ConfigLoadError létrehozását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_load_error_without_optional_params()`

```python
def test_load_error_without_optional_params(self) -> None
```

Teszteli a ConfigLoadError létrehozását opcionális paraméterek nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestConfigSaveError`

ConfigSaveError tesztjei.

### Metódusok

#### `test_save_error_creation()`

```python
def test_save_error_creation(self) -> None
```

Teszteli a ConfigSaveError létrehozását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_save_error_without_optional_params()`

```python
def test_save_error_without_optional_params(self) -> None
```

Teszteli a ConfigSaveError létrehozását opcionális paraméterek nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestConfigValidationError`

ConfigValidationError tesztjei.

### Metódusok

#### `test_validation_error_creation()`

```python
def test_validation_error_creation(self) -> None
```

Teszteli a ConfigValidationError létrehozását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_validation_error_without_optional_params()`

```python
def test_validation_error_without_optional_params(self) -> None
```

Teszteli a ConfigValidationError létrehozását opcionális paraméterek nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestConfigTypeError`

ConfigTypeError tesztjei.

### Metódusok

#### `test_type_error_creation()`

```python
def test_type_error_creation(self) -> None
```

Teszteli a ConfigTypeError létrehozását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_type_error_without_optional_params()`

```python
def test_type_error_without_optional_params(self) -> None
```

Teszteli a ConfigTypeError létrehozását opcionális paraméterek nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestConfigKeyError`

ConfigKeyError tesztjei.

### Metódusok

#### `test_key_error_creation()`

```python
def test_key_error_creation(self) -> None
```

Teszteli a ConfigKeyError létrehozását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_key_error_without_optional_params()`

```python
def test_key_error_without_optional_params(self) -> None
```

Teszteli a ConfigKeyError létrehozását opcionális paraméterek nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_key_error_with_none_available_keys()`

```python
def test_key_error_with_none_available_keys(self) -> None
```

Teszteli a ConfigKeyError létrehozását None available_keys paraméterrel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestExceptionHierarchy`

Kivétel hierarchia tesztjei.

### Metódusok

#### `test_exception_inheritance()`

```python
def test_exception_inheritance(self) -> None
```

Teszteli, hogy a kivételek helyesen öröklődnek.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_exception_is_exception()`

```python
def test_exception_is_exception(self) -> None
```

Teszteli, hogy minden kivétel az Exception leszármazottja.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/config/exceptions/test_config_error.py`](../../tests/neural_ai/core/config/exceptions/test_config_error.py)
