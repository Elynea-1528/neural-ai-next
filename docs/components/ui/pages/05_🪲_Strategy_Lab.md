# Strategy Lab Page (`neural_ai/ui/pages/05_🪲_Strategy_Lab.py`)

## Áttekintés

A Strategy Lab oldal interaktív kereskedési stratégia fejlesztő és tesztelő felület. Lehetővé teszi a felhasználók számára a gyertyadiagramok megjelenítését, stratégiák paraméterezését és VectorBT alapú backtesztelését.

## Architektúra

- **Interface**: `PageInterface`
- **Implementáció**: `StrategyLabPage`
- **Dependency Injection**: CoreBridge-en keresztül kapja meg a szolgáltatásokat
- **UI Framework**: Streamlit

## Főbb Komponensek

### Sidebar (Oldalsáv)
- **Szimbólum választó**: Konfigurációból származó devizapárok
- **Dátum választó**: Nap szintű időválasztás
- **Időkeret választó**: 1m, 5m, 15m, 1h opciók
- **Ár típus választó**: Bid/Mid árak
- **Load & Visualize**: Adatok betöltése és megjelenítése
- **Stratégia Paraméterek**: SMA kereszt stratégia beállításai
- **Futtatás (VectorBT)**: Backteszt indítása

### Main Area (Fő terület)
- **Gyertya Diagram**: Plotly alapú interaktív candlestick chart
- **Adatok Tábla**: OHLCV, spread, z-score adatok megjelenítése
- **Backteszt Eredmények**: Metrikák, equity görbe, kereskedések listája

## Big Data Támogatás

- Polars DataFrame használata nagy teljesítményű adatkezeléshez
- Pandas konverzió megjelenítéshez (Streamlit kompatibilitás)
- Aszinkron adatbetöltés nem-blokkoló UI-hoz

## Workflow

1. **Adatbetöltés**: Szimbólum, dátum, időkeret kiválasztása
2. **Vizualizáció**: Gyertyadiagram és adattábla megjelenítése
3. **Paraméterezés**: SMA periódusok és tőke beállítása
4. **Backteszt**: VectorBT futtatás eredményekkel
5. **Elemzés**: Metrikák és kereskedések vizsgálata

## Integrációk

### Strategy Service
```python
strategy_service = bridge.get_component("strategy_service")
candles = await strategy_service.get_candles(symbol, date, timeframe)
result = await strategy_service.run_sma_backtest(...)
```

### Streamlit Session State
- `candles`: Betöltött adatok tárolása
- `backtest_result`: Backteszt eredmények tárolása
- `price_type`: Ár típus (Bid/Mid) tárolása

## UI/UX Funkciók

- **Responsive Design**: Konténer szélességű megjelenítés
- **Interaktív Chart**: Zoom, pan navigáció
- **Dinamikus Jelek**: Belépési/kilépési pontok a charton
- **Valós idejű Frissítés**: Session state alapú újrarajzolás

## Tesztelés

A page teljes tesztlefedettséggel rendelkezik:
- UI komponensek tesztelése
- Adatfolyam tesztelése
- Backteszt integráció tesztelése
- Hibakezelés tesztelése

## Használat

```python
# Page példányosítása
page = StrategyLabPage(bridge)

# Oldal renderelése
page.render()

# Navigációs események
page.on_navigate_to(params)
page.on_navigate_from()
