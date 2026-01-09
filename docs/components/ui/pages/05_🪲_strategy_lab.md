# Strategy Lab Page - Stratégia Fejlesztő Labor

## Áttekintés

Ez a dokumentum a `neural_ai/ui/pages/05_🪲_Strategy_Lab.py` modult dokumentálja, amely a Strategy Lab oldalt implementálja a Neural AI Next alkalmazásban.

## Architektúra

### Fájl struktúra

```
neural_ai/ui/pages/
└── 05_🪲_Strategy_Lab.py
```

### Kapcsolódó komponensek

- **Interface**: [`PageInterface`](neural_ai/ui/interfaces/page_interface:PageInterface)
- **Core Bridge**: [`CoreBridgeInterface`](neural_ai/ui/interfaces/core_bridge_interface:CoreBridgeInterface)
- **Strategy Service**: [`StrategyServiceInterface`](neural_ai/ui/interfaces/strategy_service_interface:StrategyServiceInterface)

## Session State Kezelés

### Inicializálás

Az oldal a következő session state változókat használja:

```python
# candles: DataFrame | None
# A betöltött gyertya adatok
if "candles" not in st.session_state:
    st.session_state.candles = None

# backtest_result: dict[str, Any] | None
# A backteszt eredményei
if "backtest_result" not in st.session_state:
    st.session_state.backtest_result = None
```

### Adat persistence

A session state használata biztosítja, hogy az adatok megmaradjanak a Streamlit gombnyomások között:

1. **`render()` metódus**: A render elején szinkronizálja a local `_candles` változót a `st.session_state.candles`-szel
2. **`_load_and_visualize()` metódus**: A betöltött adatokat közvetlenül a `st.session_state.candles`-be menti
3. **`on_navigate_to()` metódus**: Navigáláskor nullázza a `st.session_state.candles` értékét

## Funkciók

### Fő funkciók

1. **Adat betöltés és vizualizáció**: Gyertya adatok betöltése a Strategy Service-en keresztül
2. **Stratégia paraméterek**: SMA kereszt stratégia paramétereinek beállítása
3. **VectorBT backteszt**: VectorBT alapú backteszt futtatása
4. **Eredmények megjelenítése**: Chartok, metrikák és kereskedések listájának megjelenítése

### Oldalsáv funkciók

- Szimbólum választó (konfigurációból vagy alapértelmezett)
- Dátum választó
- Idősík választó (1m, 5m, 15m, 1h)
- "Load & Visualize" gomb
- Stratégia paraméterek (Fast/Slow SMA, kezdeti tőke)
- "Futtatás (VectorBT)" gomb

## Használat

```python
from neural_ai.ui.pages.05_🪲_Strategy_Lab import StrategyLabPage

# Oldal inicializálása
page = StrategyLabPage(bridge=bridge)

# Oldal megjelenítése
page.render()

# Navigálás az oldalra
page.on_navigate_to(params=None)
```

## Módosítások

### v1.0.1 - Session State Persistence

A legutóbbi módosítások a session state használatát implementálják:

- `__init__`: Session state inicializálása a `candles` változóhoz
- `render`: Szinkronizálás a session state-szel
- `_load_and_visualize`: Adatok közvetlenül a session state-be mentése
- `on_navigate_to`: Session state nullázása navigáláskor

Ez biztosítja, hogy a betöltött adatok megmaradjanak a felhasználói interakciók között.
