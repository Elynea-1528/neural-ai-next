# neural_ai/processors/dimensions/d02_support/implementations/support_processor.py

D02SupportProcessor - Support/Resistance szintek processzora.

## Importok

```python
from typing import TYPE_CHECKING
from typing import Any
from typing import cast
import polars
from neural_ai.core.config.interfaces.types import ProcessorConfig
from neural_ai.processors.dimensions.base import BaseDimensionProcessor
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
```

## Osztály: `D02SupportProcessor(BaseDimensionProcessor)`

D2 - Support/Resistance szintek processzora.

Feladata a support és resistance szintek azonosítása és számítása
swing pontok alapján különböző timeframe-ekre.

### Metódusok

#### `__init__()`

```python
def __init__(self, config: 'ConfigManagerInterface', logger: 'LoggerInterface') -> None
```

Inicializálja a D2 processzort.

**Paraméterek:**

- **`self`**
- **`config`** (`'ConfigManagerInterface'`): Konfigurációs menedzser interfész
- **`logger`** (`'LoggerInterface'`): Logger interfész

**Visszatérési érték:**

- Típus: `None`

#### `_find_swing_points_close_open()`

```python
def _find_swing_points_close_open(self, df: pl.DataFrame) -> pl.DataFrame
```

Swing pontok keresése záró/nyitó árak alapján. Kiszámolja a gyertya testének top és bottom értékeit mid_open és mid_close alapján, majd swing pontokat keres rajtuk gördülő maximum szukcesszióval.

**Paraméterek:**

- **`self`**
- **`df`** (`pl.DataFrame`): Bemeneti Polars DataFrame

**Visszatérési érték:**

- Típus: `pl.DataFrame`
- pl.DataFrame: swing_high_body és swing_low_body oszlopokkal kiegészített DataFrame

#### `_find_swing_points_high_low()`

```python
def _find_swing_points_high_low(self, df: pl.DataFrame) -> pl.DataFrame
```

Swing pontok keresése high/low értékeken. Swing pontokat keres high és low értékeken gördülő maximum szukcesszióval.

**Paraméterek:**

- **`self`**
- **`df`** (`pl.DataFrame`): Bemeneti Polars DataFrame

**Visszatérési érték:**

- Típus: `pl.DataFrame`
- pl.DataFrame: swing_high_wick és swing_low_wick oszlopokkal kiegészített DataFrame

#### `_merge_levels()`

```python
def _merge_levels(self, df: pl.DataFrame) -> pl.DataFrame
```

Iteratív klaszterezés a swing szintek összevonására. Amíg vannak a merge_threshold-nél közelebbi szintpárok, addig ismétli a legkisebb távolságú pár megtalálását és összevonását súlyozott átlagolással.

**Paraméterek:**

- **`self`**
- **`df`** (`pl.DataFrame`): Polars DataFrame price, weight, type oszlopokkal

**Visszatérési érték:**

- Típus: `pl.DataFrame`
- pl.DataFrame: Klaszterezett szintek DataFrame

#### `_calculate_level_strength()`

```python
def _calculate_level_strength(self, levels: list[dict[str, float | int | str]]) -> list[dict[str, float | int | str]]
```

Szintek erősségének számítása. Minden szinthez kiszámolja a strength értéket az érintések, súly és volumen tényező alapján, majd normalizálja 0-1 közé.

**Paraméterek:**

- **`self`**
- **`levels`** (`list[dict[str, float | int | str]]`): Szintek listája dict-ekkel, amelyek tartalmazzák 'touches' és opcionálisan 'volume_factor'.

**Visszatérési érték:**

- Típus: `list[dict[str, float | int | str]]`
- list[dict[str, float | int | str]]: Frissített szintek listája 'strength' kulccsal.

#### `_categorize_zones()`

```python
def _categorize_zones(self, levels: list[dict[str, str | float | int]]) -> dict[str, dict[str, list[dict[str, str | float | int]]]]
```

Szintek kategorizálása strength és touches alapján. A szinteket erősíti support és resistance kategóriákba, majd minden kategóriában további alcsoportokba: strong, moderate, weak.

**Paraméterek:**

- **`self`**
- **`levels`** (`list[dict[str, str | float | int]]`): Szintek listája dict-ekkel, melyek tartalmazzák 'strength', 'touches', 'type' stb.

**Visszatérési érték:**

- Típus: `dict[str, dict[str, list[dict[str, str | float | int]]]]`
- dict: Kategorizált szintek struktúrája: { "support": {"strong": [...], "moderate": [...], "weak": [...]}, "resistance": {"strong": [...], "moderate": [...], "weak": [...]} }

#### `_confirm_with_volume()`

```python
def _confirm_with_volume(self, df: pl.DataFrame, swing_mask: pl.Expr) -> pl.Expr
```

Swing pontok megerősítése volumen alapján. Ellenőrzi, hogy a swing pontokon a real_volume nagyobb-e a mozgóátlagnál. Ha volume_confirmation false, mindig 1.0-s szorzót ad vissza.

**Paraméterek:**

- **`self`**
- **`df`** (`pl.DataFrame`): Bemeneti Polars DataFrame (nem használt, de konzisztenciáért)
- **`swing_mask`** (`pl.Expr`): Swing pontokat jelölő kifejezés

**Visszatérési érték:**

- Típus: `pl.Expr`
- pl.Expr: Szorzó kifejezés (1.2 ha megerősített, 1.0 ha nem)

#### `process()`

```python
def process(self, df: pl.DataFrame, timeframe: str = 'H1') -> pl.DataFrame
```

Support/Resistance szintek számítása swing pontok alapján. Detektálja a swingeket Body és Wick alapján, gyűjti őket listába VolumeFactor-ral, futtatja a szintek összevonását, erősség számítását és kategorizálását. Idősoros vetítés minden gyertyánál a legközelebbi support/resistance-hez.

**Paraméterek:**

- **`self`**
- **`df`** (`pl.DataFrame`): Bemeneti Polars DataFrame (time-aligned OHLCV adatok)
- **`timeframe`** (`str`) = `'H1'`: Időkeret ("H1", "H4", "D1"), default "H1"

**Visszatérési érték:**

- Típus: `pl.DataFrame`
- Polars DataFrame frissített oszlopokkal: swing_high_body, swing_low_body, swing_high_wick, swing_low_wick, nearest_resistance, nearest_support, resistance_strength, support_strength.

#### `find_nearest_support()`

```python
def find_nearest_support(mid_close: float) -> tuple[float | None, float | None]
```

**Paraméterek:**

- **`mid_close`** (`float`)

**Visszatérési érték:**

- Típus: `tuple[float | None, float | None]`

#### `find_nearest_resistance()`

```python
def find_nearest_resistance(mid_close: float) -> tuple[float | None, float | None]
```

**Paraméterek:**

- **`mid_close`** (`float`)

**Visszatérési érték:**

- Típus: `tuple[float | None, float | None]`

#### `dimension_id()`

```python
def dimension_id(self) -> int
```

Dimenzió azonosító (1-15).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `int`
- int: 2 (D2 dimenzió)

---

**Forrásfájl:** [`neural_ai/processors/dimensions/d02_support/implementations/support_processor.py`](../../neural_ai/processors/dimensions/d02_support/implementations/support_processor.py)
