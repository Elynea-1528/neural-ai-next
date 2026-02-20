# tests/neural_ai/core/config/test_processors_config.py

Processors konfigurációs teszt.

A processors.yaml konfigurációs fájl betöltésének és használatának tesztjei.

## Importok

```python
from typing import TYPE_CHECKING
import pytest
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager
```

## Osztály: `TestProcessorsConfig`

Processors konfigurációs osztály tesztjei.

### Metódusok

#### `config_manager()`

```python
def config_manager(self) -> 'ConfigManagerInterface'
```

Konfiguráció kezelő példány létrehozása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `'ConfigManagerInterface'`

#### `test_processors_config_loaded()`

```python
def test_processors_config_loaded(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli, hogy a processors konfiguráció sikeresen betöltődött.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_d01_processor_config_exists()`

```python
def test_d01_processor_config_exists(self, config_manager)
```

Teszteli, hogy a d01 processor konfigurációja létezik.

**Paraméterek:**

- **`self`**
- **`config_manager`**

#### `test_required_timeframes_config()`

```python
def test_required_timeframes_config(self, config_manager)
```

Teszteli a required_timeframes konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`**

#### `test_timeframe_configs_structure()`

```python
def test_timeframe_configs_structure(self, config_manager)
```

Teszteli a timeframe_configs struktúrát.

**Paraméterek:**

- **`self`**
- **`config_manager`**

#### `test_tick_timeframe_config()`

```python
def test_tick_timeframe_config(self, config_manager)
```

Teszteli a tick timeframe konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`**

#### `test_1m_timeframe_config()`

```python
def test_1m_timeframe_config(self, config_manager)
```

Teszteli az 1m timeframe konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`**

#### `test_general_z_score_window_config()`

```python
def test_general_z_score_window_config(self, config_manager)
```

Teszteli az általános z_score_window konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`**

#### `test_calc_shadows_config()`

```python
def test_calc_shadows_config(self, config_manager)
```

Teszteli a calc_shadows konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`**

#### `test_timeframe_configs_keys_exist()`

```python
def test_timeframe_configs_keys_exist(self, config_manager)
```

Teszteli, hogy a timeframe_configs-ban a megfelelő kulcsok léteznek.

**Paraméterek:**

- **`self`**
- **`config_manager`**

#### `test_timeframe_configs_z_score_window_type()`

```python
def test_timeframe_configs_z_score_window_type(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli, hogy a timeframe-specifikus z_score_window értékek helyes típusúak.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_config_section_accessible_via_get_section()`

```python
def test_config_section_accessible_via_get_section(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli a konfigurációs szekció lekérését get_section metódussal.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_d02_processor_config_exists()`

```python
def test_d02_processor_config_exists(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli, hogy a d02 processor konfigurációja létezik.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_d02_swing_window_config()`

```python
def test_d02_swing_window_config(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli a d02 swing_window konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_d02_min_distance_config()`

```python
def test_d02_min_distance_config(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli a d02 min_distance konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_d02_use_close_open_config()`

```python
def test_d02_use_close_open_config(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli a d02 use_close_open konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_d02_use_high_low_config()`

```python
def test_d02_use_high_low_config(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli a d02 use_high_low konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_d02_primary_weight_config()`

```python
def test_d02_primary_weight_config(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli a d02 primary_weight konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_d02_secondary_weight_config()`

```python
def test_d02_secondary_weight_config(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli a d02 secondary_weight konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_d02_level_merge_config()`

```python
def test_d02_level_merge_config(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli a d02 level_merge konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_d02_min_touches_config()`

```python
def test_d02_min_touches_config(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli a d02 min_touches konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_d02_volume_confirmation_config()`

```python
def test_d02_volume_confirmation_config(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli a d02 volume_confirmation konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_d02_strength_window_config()`

```python
def test_d02_strength_window_config(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli a d02 strength_window konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_d02_timeframe_configs_structure()`

```python
def test_d02_timeframe_configs_structure(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli a d02 timeframe_configs struktúrát.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_d02_m1_timeframe_config()`

```python
def test_d02_m1_timeframe_config(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli a d02 M1 timeframe konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_d02_h1_timeframe_config()`

```python
def test_d02_h1_timeframe_config(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli a d02 H1 timeframe konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

#### `test_d02_d1_timeframe_config()`

```python
def test_d02_d1_timeframe_config(self, config_manager: 'ConfigManagerInterface') -> None
```

Teszteli a d02 D1 timeframe konfigurációt.

**Paraméterek:**

- **`self`**
- **`config_manager`** (`'ConfigManagerInterface'`)

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/config/test_processors_config.py`](../../tests/neural_ai/core/config/test_processors_config.py)
