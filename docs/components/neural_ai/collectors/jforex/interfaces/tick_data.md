# neural_ai/collectors/jforex/interfaces/tick_data.py

Tick Data Model for JForex Collector.

## Importok

```python
from dataclasses import dataclass
from datetime import datetime
```

## Osztály: `TickData`

Tick adat modell JForex piaci adatokhoz.

Egyetlen tick-et reprezentál (bid/ask ár pár) a Dukascopy-tól.

Attributes:
    timestamp: Tick UTC időbélyege
    symbol: Kereskedelmi szimbólum (pl. 'EURUSD')
    bid: Bid ár (5 tizedesjeggyel forexhez)
    ask: Ask ár (5 tizedesjeggyel forexhez)
    ask_volume: Ask volume (opcionális, 20-bájtos formátumhoz)
    bid_volume: Bid volume (opcionális, 20-bájtos formátumhoz)
    source: Adatforrás azonosító (alapértelmezett: 'jforex')

### Metódusok

#### `spread()`

```python
def spread(self) -> float
```

Spread kiszámítása pip-ben.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `float`
- Spread pip-ben (1 pip = 0.0001 a legtöbb forex párnál)

#### `mid_price()`

```python
def mid_price(self) -> float
```

Mid ár kiszámítása (bid és ask átlaga).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `float`
- Mid ár, 5 tizedesjegyre kerekítve

---

**Forrásfájl:** [`neural_ai/collectors/jforex/interfaces/tick_data.py`](../../neural_ai/collectors/jforex/interfaces/tick_data.py)
