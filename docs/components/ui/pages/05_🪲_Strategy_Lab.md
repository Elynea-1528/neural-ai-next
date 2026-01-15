# 🪲 Strategy Lab Oldal

## Áttekintés

A Strategy Lab oldal interaktív stratégiafejlesztő környezet, ahol a felhasználók vizuálisan vizsgálhatják a gyertyadiagramokat, alkalmazhatják a piaci szerkezet elemzést (D2 processzor), és tesztelhetik a kereskedési stratégiákat VectorBT backteszteléssel.

## Szerkezet

### Fájl elérési út
- **Forráskód**: [`neural_ai/ui/pages/05_🪲_Strategy_Lab.py`](../../../neural_ai/ui/pages/05_🪲_Strategy_Lab.py)
- **Tesztfájl**: [`tests/ui/pages/test_strategy_lab_page.py`](../../../tests/ui/pages/test_strategy_lab_page.py)

### Osztályok

#### `StrategyLabPage`

A Strategy Lab fő osztálya, amely implementálja a `PageInterface` interfészt és biztosítja az interaktív stratégiafejlesztési funkciókat.

##### Attribútumok

- `_bridge: CoreBridgeInterface` - A backend bridge példány
- `_loaded: bool` - Az oldal betöltöttségi állapota
- `_title: str` - Az oldal címe ("🪲 Strategy Lab")
- `_candles: pl.DataFrame | None` - Az aktuális gyertyák adatai

##### Metódusok

###### `__init__(bridge: CoreBridgeInterface, **kwargs: Any) -> None`

Az osztály konstruktora, amely beállítja a session state változókat.

**Paraméterek:**
- `bridge`: A backend bridge példány
- `**kwargs`: Opcionális kulcsszó argumentumok

**Session State változók:**
- `backtest_result`: Backteszt eredmények tárolása
- `candles`: Betöltött gyertyák adatai
- `price_type`: Ár típus ('Bid' vagy 'Mid')
- `show_body_swings`: Body alapú swing pontok megjelenítése
- `show_wick_swings`: Wick alapú swing pontok megjelenítése
- `d2_analysis`: D2 piaci szerkezet elemzés eredménye

###### `render() -> None`

Az oldal fő renderelési metódusa, amely megjeleníti a sidebar-t és a fő területet.

**Funkcionalitás:**
- Oldalsáv: Szűrők, beállítások
- Fő terület: Diagram és adatok megjelenítése

###### `_render_sidebar() -> None`

Az oldalsáv megjelenítése szűrőkkel és beállításokkal.

**Komponensek:**
- Szimbólum választó (konfigurációból)
- Dátum választó
- Idősík választó (1m, 5m, 15m, 1h)
- Ár típus választó (Bid/Mid)
- "Load & Visualize" gomb
- Piaci szerkezet expander (D2 swing pontok)
- Stratégia paraméterek expander (SMA kereszteződés)

###### `_render_main_area() -> None`

A fő terület megjelenítése diagrammal és táblázattal.

**Komponensek:**
- Gyertya diagram (Plotly)
- Adatok táblázata
- Backteszt eredmények (ha vannak)

###### `_render_candlestick_chart(signals: dict[str, list[int]] | None = None) -> None`

Interaktív candlestick chart megjelenítése jelekkel és D2 elemekkel.

**Funkcionalitás:**
- OHLC gyertyák megjelenítése
- Belépési/kilépési jelek (backtest eredmények)
- Swing pontok megjelenítése (ha aktív)
- Nearest resistance/support szintek horizontális vonalaként (strength alapú opacity-val)
- Debug expander D2 adatokkal

**D2 vizualizáció:**
- Swing pontok: triangle-up/down markerek
- Nearest szintek: horizontális vonalak rgba színnel (opacity = strength * 0.8 + 0.2)

###### `_render_data_table() -> None`

Az adatok táblázatos megjelenítése a kiválasztott oszlopokkal.

**Megjelenített oszlopok:**
- OHLC oszlopok (price_type alapján)
- spread (ha elérhető)
- rolling_z_score (ha elérhető)
- volume oszlopok (ha elérhetők)
- D2 oszlopok: nearest_resistance, nearest_support, resistance_strength, support_strength (ha elérhetők)

###### `_render_backtest_results() -> None`

Backteszt eredmények megjelenítése metrikákkal, equity görbével és trades listával.

**Komponensek:**
- Metrikák: Total Return, Win Rate, Max Drawdown, Total Trades
- Equity görbe (line chart)
- Trades táblázat: P&L, Duration

###### `_prepare_data_for_view(df: pl.DataFrame, price_type: str) -> pl.DataFrame`

Adatok előkészítése megjelenítéshez oszlopátnevezéssel.

**Funkcionalitás:**
- Bid/Mid prefix alapján OHLC oszlopok átnevezése általános névre

###### `_get_symbols() -> list[str]`

Szimbólumok lekérése a konfigurációból, alapértelmezett értékekkel.

###### `_load_and_visualize(symbol: str, selected_date: date, timeframe: str) -> None`

Adatok betöltése és vizualizálása az adott paraméterekkel.

**Funkcionalitás:**
- Gyertyák betöltése StrategyService segítségével
- Automatikus D2 piaci szerkezet elemzés
- Session state frissítés
- Oldal újrarajzolása

###### `_run_backtest(symbol: str, date: str, timeframe: str, fast_period: int, slow_period: int, initial_capital: float) -> None`

SMA kereszteződés stratégia backtesztelése VectorBT-vel.

**Paraméterek:**
- Stratégia paraméterek: fast_period, slow_period
- Kezdeti tőke
- Adatok: symbol, date, timeframe

###### `_get_strategy_service() -> StrategyServiceInterface | None`

Strategy Service példány lekérése a bridge-ből.

##### Property-k

###### `title: str` (read-only)

Az oldal címe ("🪲 Strategy Lab").

###### `is_loaded: bool` (read-only)

Az oldal betöltöttségi állapota.

## Használat

### Alapvető használat

```python
from neural_ai.ui.pages import StrategyLabPage
from neural_ai.ui.core_bridge import CoreBridge

bridge = CoreBridge()
page = StrategyLabPage(bridge=bridge)
page.render()
```

### D2 Elemzés használata

```python
# Swing pontok megjelenítése
st.session_state.show_body_swings = True
st.session_state.show_wick_swings = True

# Adatok betöltése és D2 elemzés
page._load_and_visualize("EURUSD", date(2024, 3, 20), "1h")
```

### Backteszt futtatása

```python
# SMA stratégia backteszt
page._run_backtest(
    symbol="EURUSD",
    date="2024-03-20",
    timeframe="1h",
    fast_period=10,
    slow_period=50,
    initial_capital=10000.0
)
```

## Tesztelés

### Tesztesetek

1. **Inicializálás**: Konstruktor és session state beállítás
2. **Property-k**: title és is_loaded ellenőrzése
3. **Navigáció**: on_navigate_to/from metódusok
4. **Komponensek**: Strategy Service és szimbólumok lekérése
5. **Renderelés**: Hibamentes render metódus
6. **Session State**: Session state változók perzisztenciája
7. **Adattábla**: Price type alapú oszlop megjelenítés

### Tesztfuttatás

```bash
# Összes teszt futtatása
pytest tests/ui/pages/test_strategy_lab_page.py -v

# Coverage jelentés
pytest tests/ui/pages/test_strategy_lab_page.py --cov=neural_ai.ui.pages --cov-report=html
```

### Teszt eredmények

- **Tesztesetek száma**: 26
- **Sikeres tesztek**: 26/26 ✅
- **Coverage**: 100% (Statement és Branch)

## Fejlesztés

### Architektúra

A `StrategyLabPage` osztály követi a projekt szabványait:

- **Interface-elv**: `PageInterface` implementáció
- **Dependency Injection**: `CoreBridgeInterface` konstruktoron keresztül
- **D2 Integráció**: Automatikus piaci szerkezet elemzés
- **Session State**: Streamlit session state használata perzisztenciára
- **Típusos annotációk**: Szigorú típusok, `Any` tiltva

### Kódminőség

- **Linter**: Ruff (0 hiba)
- **Típusellenőrzés**: Pylance kompatibilis
- **Dokumentáció**: Magyar Google Style docstring-ek

### Legutóbbi refaktorálás (D2 bővítés)

**Változtatások:**

1. **Táblázat bővítés**: Hozzáadva `nearest_resistance`, `nearest_support`, `resistance_strength`, `support_strength` oszlopok
2. **Vizualizáció fejlesztés**: Nearest szintek horizontális vonalaként megjelenítése strength alapú opacity-val
3. **Logika javítás**: Feltételes megjelenítés csak akkor, ha az oszlopok elérhetők
4. **Kódminőség**: Ruff linting javítások, hosszú sorok tördelése

**D2 Specifikáció:**
- `nearest_resistance`: Legközelebbi ellenállás szint árértéke
- `nearest_support`: Legközelebbi támasz szint árértéke
- `resistance_strength`: Ellenállás erősség (0-1)
- `support_strength`: Támasz erősség (0-1)
- **Opacity képlet**: `strength * 0.8 + 0.2`

## Kapcsolódó dokumentáció

- [UI Architektúra](../architecture.md)
- [Page Interface](../../interfaces/page_interface.md)
- [Strategy Service](../../services/strategy_service.md)
- [D2 Support Processor](../../../../processors/dimensions/d02_support/processor.md)
- [Streamlit App](../../streamlit_app.md)

## Verziótörténet

- **v6.0.1** (2026-01-15): D2 bővítés - Nearest szintek vizualizációja és táblázat bővítés
- **v6.0.0** (2026-01-04): Refaktorálás - Architektúra szabványok alkalmazása
- **v5.x**: Előző verziók alap funkciókkal

## Szerző

- **Fejlesztő**: Neural AI Next Team
- **Utolsó módosítás**: 2026-01-15