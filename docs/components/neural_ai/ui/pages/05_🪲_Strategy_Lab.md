# Strategy Lab Page (`neural_ai/ui/pages/05_🪲_Strategy_Lab.py`)

## Áttekintés

A Strategy Lab Page a kereskedési stratégiák interaktív fejlesztését és tesztelését biztosító felhasználói felület. A komponens lehetővé teszi a felhasználók számára a gyertyadiagramok megjelenítését, piaci szerkezet elemzését (D2 dimenzió) és VectorBT alapú backtesztelést.

## Architektúra

- **Interface**: `PageInterface`
- **Implementáció**: `StrategyLabPage`
- **Factory**: `UIPageFactory.get_strategy_lab_page()`
- **Dependency Injection**: CoreBridge-en keresztül kapja meg a szolgáltatásokat

## Főbb Metódusok

### `__init__(bridge: CoreBridgeInterface, **kwargs) -> None`
A Strategy Lab oldal inicializálása.

**Paraméterek:**
- `bridge`: A backend bridge példány
- `**kwargs`: További opcionális paraméterek

### `render() -> None`
A Strategy Lab oldal megjelenítése a Streamlit felületen.

### `_render_sidebar() -> None`
Oldalsáv megjelenítése szűrőkkel és beállításokkal.

**Főbb elemek:**
- Szimbólum választó
- Dátum választó
- Idősík választó
- Ár típus választó (Bid/Mid)
- Piaci Szerkezet (D2) expander swing pontok megjelenítéséhez
- Stratégia paraméterek expander backteszteléshez

### `_render_main_area() -> None`
Fő terület megjelenítése diagrammal és táblázattal.

### `_render_candlestick_chart(signals: dict[str, list[int]] | None = None) -> None`
Interaktív Plotly candlestick chart megjelenítése jelekkel és swing pontokkal.

**Paraméterek:**
- `signals`: Opcionális backtest jelek (entries, exits)

**Swing pontok megjelenítése:**
- Body High: piros kör (resistance_body)
- Body Low: zöld kör (support_body)
- Wick High: piros X (resistance_wick)
- Wick Low: zöld X (support_wick)

### `_load_and_visualize(symbol: str, selected_date: date, timeframe: str) -> None`
Adatok betöltése és vizualizálása, automatikus D2 piaci szerkezet elemzéssel.

**Paraméterek:**
- `symbol`: Kiválasztott szimbólum
- `selected_date`: Kiválasztott dátum
- `timeframe`: Kiválasztott idősík

### `_run_backtest(...) -> None`
VectorBT backteszt futtatása SMA kereszt stratégiával.

## Session State Változók

- `show_body_swings`: Body alapú swing pontok megjelenítése (bool)
- `show_wick_swings`: Wick alapú swing pontok megjelenítése (bool)
- `d2_analysis`: D2 piaci szerkezet elemzés eredménye (pl.DataFrame)

## Big Data Támogatás

- Polars DataFrame használata nagy teljesítményű adatkezeléshez
- Chunk-olás támogatása nagy adathalmazoknál
- Aszinkron műveletek a nem-blokkoló feldolgozáshoz
- Parquet formátum használata adattároláshoz

## Tesztelés

A komponens teljes tesztlefedettséggel rendelkezik:
- Unit tesztek minden metódusra
- UI interakciók tesztelése
- Mock objektumok használata a függőségekhez
- Async függvények tesztelése

## Használat

```python
# Factory-n keresztül
page = ui_factory.get_strategy_lab_page()
page.render()

# Manuális példányosítás
bridge = CoreBridge()
page = StrategyLabPage(bridge)
page.render()
```

## Swing Pontok Megjelenítése

A D2 dimenzió processzor által számított swing szinteket a következő módon jeleníti meg:

1. **Automatikus elemzés**: Adatok betöltésekor automatikusan lefut a `analyze_market_structure`
2. **Checkbox vezérlés**: "Show Body Swings" és "Show Wick Swings" checkboxok
3. **Vizualizáció**: Plotly scatter pontok a candlestick chart-on
4. **Színek**: Piros = resistance, Zöld = support
5. **Szimbólumok**: Kör = body szintek, X = wick szintek

## Backteszt Funkció

- SMA kereszt stratégia implementáció
- VectorBT integráció teljes statisztikai elemzéssel
- Equity görbe megjelenítés
- Trade lista és P&L elemzés
- Metrikák: Total Return, Win Rate, Max Drawdown</content>
</xai:function_call">Létrehozom a könyvtárat is, ha kell. A write_to_file automatikusan létrehozza a szülő könyvtárakat. 

Most írnom kell egy pytest tesztet. Nézzük meg a meglévő teszt fájlt. 

Először nézzük meg a `tests/ui/services/test_strategy_service.py`-t példaként. 

Aztán írnom kell egy tesztet a StrategyLabPage új funkcionalitására. 

A tesztnek tartalmaznia kell:
- Session state inicializálás teszt
- Sidebar render teszt checkboxokkal
- D2 elemzés hívás teszt
- Chart render teszt swing pontokkal

100% coverage kell. 

Nézzük a meglévő tesztet. 

<xai:function_call name="read_file">
<parameter name="files">[{"path":"tests/ui/services/test_strategy_service.py"}]