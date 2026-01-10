# Strategy Lab Page (`05_🪲_Strategy_Lab.py`)

## Áttekintés

Ez a dokumentum a `neural_ai/ui/pages/05_🪲_Strategy_Lab.py` modult dokumentálja, amely a Neural AI Next rendszer Strategy Lab oldalát implementálja.

## Modul leírása

A **Strategy Lab Page** egy interaktív Streamlit oldal, amely lehetővé teszi a felhasználók számára a kereskedési gyertyadiagramok vizualizálását és a stratégiák tesztelését.

## Architektúra

### Függőségek

```python
from datetime import date
from typing import TYPE_CHECKING, Any, Coroutine, Union
import streamlit as st
```

### Import struktúra

- **`CoreBridgeInterface`**: Backend kommunikáció interfésze
- **`PageInterface`**: Alap oldal interfész
- **`StrategyServiceInterface`**: Stratégia szolgáltatás interfész

## Osztály: `StrategyLabPage`

### Ősosztály

```python
class StrategyLabPage(PageInterface)
```

A `PageInterface` osztályból származik, amely az oldalak alapvető szerződését definiálja.

### Konstruktor

```python
def __init__(self, bridge: "CoreBridgeInterface", **kwargs: Any) -> None
```

**Paraméterek:**
- `bridge`: A backend bridge példány
- `**kwargs`: További opcionális paraméterek

### Attribútumok

| Attribútum | Típus | Leírás |
|------------|-------|--------|
| `_bridge` | `CoreBridgeInterface` | Backend kapcsolat |
| `_loaded` | `bool` | Oldal betöltött állapota |
| `_title` | `str` | Az oldal címe |
| `_candles` | `DataFrame \| None` | Betöltött gyertya adatok |

### Fő metódusok

#### `render()` - Oldal megjelenítése

```python
def render(self) -> None
```

A teljes oldal megjelenítése, beleértve:
- Oldalsáv (sidebar) szűrőkkel
- Fő terület diagrammal és táblázattal

#### `_render_sidebar()` - Oldalsáv megjelenítése

```python
def _render_sidebar(self) -> None
```

Az oldalsáv tartalma:
- **Szimbólum választó**: Konfigurációból betöltött devizapárok
- **Dátum választó**: Napi bontású dátumválasztó
- **Idősík választó**: `1m`, `5m`, `15m`, `1h` opciókkal
- **Price Type választó**: Radio button `Bid` vagy `Mid` ár típus kiválasztására
- **Load & Visualize gomb**: Adatok betöltése és megjelenítése

#### `_render_main_area()` - Fő terület megjelenítése

```python
def _render_main_area(self) -> None
```

A fő terület tartalma:
- Ha vannak adatok: Candlestick chart és adat táblázat
- Ha nincs adat: Információs üzenet

#### `_render_candlestick_chart()` - Interaktív Plotly chart

```python
def _render_candlestick_chart(self) -> None
```

Plotly alapú candlestick chart létrehozása:
- Dinamikus OHLC adatok megjelenítése (`Bid` vagy `Mid` típus alapján)
- `Bid` típus: `bid_open`, `bid_high`, `bid_low`, `bid_close` oszlopok használata
- `Mid` típus: `mid_open`, `mid_high`, `mid_low`, `mid_close` oszlopok használata
- Zöld/piros színezés a növekedés/csökkenés szerint
- Zoomolható és interaktív

#### `_render_data_table()` - Adat táblázat

```python
def _render_data_table(self) -> None
```

Az első 10 sor megjelenítése `st.dataframe` segítségével:
- Dinamikus OHLC oszlopok megjelenítése (Price Type alapján)
- `Spread` oszlop megjelenítése (ask - bid átlag)
- `Z-Score` (rolling_z_score) oszlop megjelenítése
- Volume oszlopok (`real_volume`, `tick_volume`) megjelenítése

#### `_get_symbols()` - Szimbólumok lekérése

```python
def _get_symbols(self) -> list[str]
```

**Visszatérési érték:**
- Elérhető szimbólumok listája a konfigurációból
- Alapértelmezett érték: `["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]`

#### `_load_and_visualize()` - Adatok betöltése

```python
def _load_and_visualize(self, symbol: str, selected_date: date, timeframe: str) -> None
```

**Paraméterek:**
- `symbol`: Kereskedési szimbólum (pl. `EURUSD`)
- `selected_date`: Kiválasztott dátum
- `timeframe`: Idősík (`1m`, `5m`, `15m`, `1h`)

#### `_get_strategy_service()` - Strategy Service lekérése

```python
def _get_strategy_service(self) -> "StrategyServiceInterface | None"
```

**Visszatérési érték:**
- `StrategyServiceInterface`: A stratégia szolgáltatás példánya
- `None`: Ha a szolgáltatás nem elérhető

#### Navigációs metódusok

```python
def on_navigate_to(self, params: dict[str, Any] | None = None) -> None
def on_navigate_from(self) -> None
```

### Property-k

| Property | Típus | Leírás |
|----------|-------|--------|
| `title` | `str` | Az oldal címe |
| `is_loaded` | `bool` | Oldal betöltött állapota |

## Használat

### Alapvető inicializálás

```python
from neural_ai.ui.pages.Strategy_Lab import StrategyLabPage
from neural_ai.ui.core_bridge import CoreBridge

bridge = CoreBridge()
page = StrategyLabPage(bridge)
page.render()
```

### Szimbólumok a konfigurációból

A szimbólumok a `config.get("symbols")` metóduson keresztül érhetők el.

### Adatok betöltése

```python
import asyncio

strategy_service = page._get_strategy_service()
if strategy_service:
    candles = asyncio.run(
        strategy_service.get_candles("EURUSD", "2024-03-20", "1m")
    )
```

## Tesztelés

A modul teszteléséhez használandó:

```bash
pytest tests/ui/pages/test_strategy_lab_page.py -v
```

## Kapcsolódó modulok

- [`StrategyServiceInterface`](../../interfaces/strategy_service_interface.md)
- [`CoreBridgeInterface`](../../interfaces/core_bridge_interface.md)
- [`PageInterface`](../../interfaces/page_interface.md)
- [`StrategyService`](../../../services/strategy_service.md)

---

*Generálva: 2026-01-09*
