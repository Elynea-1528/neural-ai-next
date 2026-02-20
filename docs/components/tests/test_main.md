# tests/test_main.py

Unit tesztek a main.py modulhoz.

Ez a modul teszteli a CLI belépési pont összes funkcióját:
- Live mód indítása
- Download mód (történeti adatok)
- Dashboard mód (Streamlit)
- Argumentum parsing
- Dátum parsing
- Hibakezelés

## Importok

```python
import sys
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
import pytest
import main
# ... és még 1 import
```

## Osztály: `TestParseDateFunction`

Tesztek a parse_date() függvényhez.

### Metódusok

#### `test_parse_date_valid_format()`

```python
def test_parse_date_valid_format(self) -> None
```

Helyes dátum formátum parse-olása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_parse_date_invalid_format()`

```python
def test_parse_date_invalid_format(self) -> None
```

Érvénytelen dátum formátum ValueError-t dob.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_parse_date_wrong_separator()`

```python
def test_parse_date_wrong_separator(self) -> None
```

Rossz elválasztó karakter ValueError-t dob.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestParseArgumentsFunction`

Tesztek a parse_arguments() függvényhez.

### Metódusok

#### `test_parse_arguments_live_mode()`

```python
def test_parse_arguments_live_mode(self) -> None
```

Live mód argumentum parsing.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_parse_arguments_download_mode()`

```python
def test_parse_arguments_download_mode(self) -> None
```

Download mód argumentum parsing.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_parse_arguments_dashboard_mode_defaults()`

```python
def test_parse_arguments_dashboard_mode_defaults(self) -> None
```

Dashboard mód alapértelmezett értékekkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_parse_arguments_dashboard_mode_custom()`

```python
def test_parse_arguments_dashboard_mode_custom(self) -> None
```

Dashboard mód egyedi értékekkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestRunLiveMode`

Tesztek a run_live_mode() függvényhez.

### Metódusok

#### `test_run_live_mode_success()`

```python
async def test_run_live_mode_success(self) -> None
```

Live mód sikeres indítása és leállítása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_run_live_mode_none_components()`

```python
async def test_run_live_mode_none_components(self) -> None
```

Live mód None komponensekkel (graceful degradation).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestRunDownloadMode`

Tesztek a run_download_mode() függvényhez.

### Metódusok

#### `test_run_download_mode_success()`

```python
async def test_run_download_mode_success(self) -> None
```

Download mód sikeres futása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestRunDashboardMode`

Tesztek a run_dashboard_mode() függvényhez.

### Metódusok

#### `test_run_dashboard_mode_success()`

```python
def test_run_dashboard_mode_success(self) -> None
```

Dashboard mód sikeres indítása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_run_dashboard_mode_headless()`

```python
def test_run_dashboard_mode_headless(self) -> None
```

Dashboard mód headless flag-gel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_run_dashboard_mode_subprocess_error()`

```python
def test_run_dashboard_mode_subprocess_error(self) -> None
```

Dashboard mód subprocess hiba kezelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_run_dashboard_mode_keyboard_interrupt()`

```python
def test_run_dashboard_mode_keyboard_interrupt(self) -> None
```

Dashboard mód KeyboardInterrupt kezelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestMainFunction`

Tesztek a main() függvényhez.

### Metódusok

#### `test_main_live_mode()`

```python
def test_main_live_mode(self) -> None
```

Main függvény live móddal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_main_live_mode_keyboard_interrupt()`

```python
def test_main_live_mode_keyboard_interrupt(self) -> None
```

Main függvény live mód KeyboardInterrupt kezelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_main_live_mode_exception()`

```python
def test_main_live_mode_exception(self) -> None
```

Main függvény live mód exception kezelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_main_download_mode_success()`

```python
def test_main_download_mode_success(self) -> None
```

Main függvény download móddal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_main_download_mode_invalid_date_format()`

```python
def test_main_download_mode_invalid_date_format(self) -> None
```

Main függvény download mód érvénytelen dátum formátummal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_main_download_mode_start_after_end()`

```python
def test_main_download_mode_start_after_end(self) -> None
```

Main függvény download mód kezdő dátum > záró dátum.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_main_download_mode_future_date()`

```python
def test_main_download_mode_future_date(self) -> None
```

Main függvény download mód jövőbeli dátummal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_main_download_mode_keyboard_interrupt()`

```python
def test_main_download_mode_keyboard_interrupt(self) -> None
```

Main függvény download mód KeyboardInterrupt kezelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_main_download_mode_exception()`

```python
def test_main_download_mode_exception(self) -> None
```

Main függvény download mód exception kezelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_main_dashboard_mode()`

```python
def test_main_dashboard_mode(self) -> None
```

Main függvény dashboard móddal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_main_dashboard_mode_keyboard_interrupt()`

```python
def test_main_dashboard_mode_keyboard_interrupt(self) -> None
```

Main függvény dashboard mód KeyboardInterrupt kezelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_main_dashboard_mode_exception()`

```python
def test_main_dashboard_mode_exception(self) -> None
```

Main függvény dashboard mód exception kezelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_main_invalid_command()`

```python
def test_main_invalid_command(self) -> None
```

Main függvény érvénytelen paranccsal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_main_no_command()`

```python
def test_main_no_command(self) -> None
```

Main függvény parancs nélkül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_main_logger_assertion()`

```python
def test_main_logger_assertion(self) -> None
```

Main függvény logger None esetén assertion error.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/test_main.py`](../../tests/test_main.py)
