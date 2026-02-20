# neural_ai/processors/dimensions/d02_support/exceptions/support_error.py

Kivételek a D02 Support/Resistance processzor modulhoz.

Ez a modul definiálja a support/resistance szintek számítása során
fellépő összes kivételt.

## Osztály: `SupportError(Exception)`

Alap kivétel a support/resistance processzor hibákhoz.

Ez az osztály szolgál közös alapként az összes support/resistance
számítással kapcsolatos kivételnek a rendszerben.

Attributes:
    message: A hibaüzenet részletes leírása.
    error_code: Opcionális hibakód a hibák kategorizálásához.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, error_code: str | None = None) -> None
```

Inicializálja a SupportError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet részletes leírása.
- **`error_code`** (`str | None`) = `None`: Opcionális hibakód a hibák kategorizálásához.

**Visszatérési érték:**

- Típus: `None`

## Osztály: `SwingPointCalculationError(SupportError)`

Swing pont számítási hiba.

Akkor dobódik, ha a swing high vagy swing low pontok számítása
sikertelen. Ez tartalmazhatja a rolling window műveletek hibáit
vagy érvénytelen adatokat.

Attributes:
    window_size: A használt rolling window mérete.
    column_name: Az érintett oszlop neve.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, window_size: int | None = None, column_name: str | None = None) -> None
```

Inicializálja a SwingPointCalculationError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet részletes leírása.
- **`window_size`** (`int | None`) = `None`: A használt rolling window mérete.
- **`column_name`** (`str | None`) = `None`: Az érintett oszlop neve.

**Visszatérési érték:**

- Típus: `None`

## Osztály: `SupportResistanceLevelError(SupportError)`

Support/Resistance szint számítási hiba.

Akkor dobódik, ha a support vagy resistance szintek aggregálása
sikertelen. Ez tartalmazhatja az átlagolási műveletek hibáit
vagy érvénytelen swing pont adatokat.

Attributes:
    level_type: A szint típusa ("support" vagy "resistance").
    aggregation_method: A használt aggregációs módszer.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, level_type: str | None = None, aggregation_method: str | None = None) -> None
```

Inicializálja a SupportResistanceLevelError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet részletes leírása.
- **`level_type`** (`str | None`) = `None`: A szint típusa ("support" vagy "resistance").
- **`aggregation_method`** (`str | None`) = `None`: A használt aggregációs módszer.

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TimeframeConfigurationError(SupportError)`

Timeframe konfigurációs hiba.

Akkor dobódik, ha a timeframe-specifikus konfiguráció érvénytelen
vagy hiányzik. Ez tartalmazhatja a swing_window vagy min_distance
paraméterek hibás értékeit.

Attributes:
    timeframe: Az érintett timeframe.
    config_key: A hiányzó vagy érvénytelen konfigurációs kulcs.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, timeframe: str | None = None, config_key: str | None = None) -> None
```

Inicializálja a TimeframeConfigurationError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet részletes leírása.
- **`timeframe`** (`str | None`) = `None`: Az érintett timeframe.
- **`config_key`** (`str | None`) = `None`: A hiányzó vagy érvénytelen konfigurációs kulcs.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/processors/dimensions/d02_support/exceptions/support_error.py`](../../neural_ai/processors/dimensions/d02_support/exceptions/support_error.py)
