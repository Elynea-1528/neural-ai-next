# 📥 Data Hub Oldal

## Áttekintés

A Data Hub oldal a Neural AI Next rendszer adatkezelő központja. Ez az oldal felelős az adatok listázásáért, történelmi adatok letöltéséért és az adatok exportálásáért a DataService segítségével.

## Architektúra

### Osztály: `DataHubPage`

```python
class DataHubPage(PageInterface):
    """Data Hub oldal.

    Ez az oldal felelős az adatok kezeléséért, letöltéséért és megjelenítéséért
    a DataService segítségével, amely a UIServiceFactory-n keresztül érhető el.
    """
```

### Főbb jellemzők

- **Cím**: "📥 Data Hub"
- **Interfész**: `PageInterface`
- **Szolgáltatás**: `DataServiceInterface`

## Metódusok

### `__init__(bridge: CoreBridgeInterface, **kwargs: Any) -> None`

A Data Hub oldal inicializálása.

**Paraméterek:**
- `bridge`: A CoreBridge példány, amelyen keresztül elérjük a backendet
- `**kwargs`: További opcionális argumentumok

**Inicializálás:**
- `_bridge`: A CoreBridge példány
- `_loaded`: Az oldal betöltöttségi állapota (kezdetben False)
- `_title`: Az oldal címe ("📥 Data Hub")
- `_data_service`: A DataService példány (kezdetben None)

### `render() -> None`

Az oldal megjelenítése Streamlit segítségével.

**Funkciók:**
1. Oldalcím megjelenítése
2. UIServiceFactory inicializálás ellenőrzése
3. DataService lekérése a factory-ből
4. Oldalsáv menü megjelenítése:
   - Adatok listázása
   - Történelmi adatok letöltése
   - Adatok exportálása
5. Kiválasztott menüpont megjelenítése

**Hibakezelés:**
- Ha a factory nincs inicializálva, hibaüzenet jelenik meg
- Váratlan hibák esetén hibaüzenet és kivétel részletei

### `_render_data_listing() -> None`

Elérhető adatok listázásának megjelenítése.

**Funkciók:**
1. Szimbólumok lekérése a DataService `get_configured_symbols()` metódusával
2. Szimbólum szűrő legördülő menü megjelenítése
3. "Adatok frissítése" gomb
4. Adatok betöltése a DataService `list_available_data()` metódusával
5. Eredmények megjelenítése DataFrame táblázatban
6. Összesítő metrikák:
   - Összes rekord
   - Összes méret (GB)
   - Adatforrások száma

**Hibakezelés:**
- Ha a DataService nem érhető el, hibaüzenet jelenik meg
- Ha a szimbólumok lekérdezése sikertelen, fallback értékkel működik tovább
- Ha nincsenek elérhető adatok, figyelmeztető üzenet jelenik meg

### `_render_download_history() -> None`

Történelmi adatok letöltésének megjelenítése.

**Funkciók:**
1. Szimbólumok lekérése a DataService `get_configured_symbols()` metódusával
2. Szimbólum választó legördülő menü
3. Kezdő és záró dátum választók
4. "Letöltés indítása" gomb
5. Aszinkron letöltés indítása a DataService `download_history()` metódusával
6. Eredmények megjelenítése:
   - Letöltött rekordok száma
   - Letöltött adatok mérete (MB)
   - Letöltési státusz
   - Részletes információk (expanderekben)

**Hibakezelés:**
- Dátumtartomány ellenőrzése (kezdő dátum nem lehet későbbi, mint a záró dátum)
- Ha a DataService nem érhető el, hibaüzenet jelenik meg
- Részleges letöltés esetén figyelmeztető üzenet a sikertelen napokkal
- Sikertelen letöltés esetén hibaüzenet

### `_render_data_export() -> None`

Adatok exportálásának megjelenítése.

**Funkciók:**
1. Export formátum választása (parquet, csv, json)
2. Adatforrás választása (tick_data, ohlc_data, market_data)
3. Cél útvonal megadása
4. "Exportálás indítása" gomb
5. Adatok betöltése chunkokban a DataService `load_data()` metódusával
6. Exportálás a DataService `export_data()` metódusával
7. Eredmények megjelenítése

**Hibakezelés:**
- Ha a DataService nem érhető el, hibaüzenet jelenik meg
- Ha nincsenek exportálandó adatok, figyelmeztető üzenet jelenik meg
- Sikertelen exportálás esetén hibaüzenet

### `on_navigate_to(params: dict[str, Any] | None = None) -> None`

Az oldalra navigáláskor meghívott metódus.

**Paraméterek:**
- `params`: Opcionális navigációs paraméterek

**Funkció:**
- Beállítja az oldal betöltöttségi állapotát True-ra

### `on_navigate_from() -> None`

Az oldalról navigáláskor meghívott metódus.

**Funkció:**
- Jelenleg üres metódus

### `title: str` (property)

Az oldal címe.

**Visszatérési érték:**
- `str`: Az oldal címe

### `is_loaded: bool` (property)

Az oldal betöltöttségi állapota.

**Visszatérési érték:**
- `bool`: True, ha az oldal betöltődött, egyébként False

## Refaktorálási változások

### 2026-01-07

A Data Hub oldalt refaktoráltuk, hogy a beégetett szimbólumlistákat lecserélje dinamikus, konfigurációból lekérdezett szimbólumokra.

#### Változások:

1. **`_render_data_listing()` metódus:**
   - **Régi:** Beégetett szimbólumlista: `["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]`
   - **Új:** Dinamikus szimbólumlista a `data_service.get_configured_symbols()` hívással
   - **Előny:** A szimbólumok mostantól a konfigurációból jönnek, rugalmasabb és konfigurálhatóbb

2. **`_render_download_history()` metódus:**
   - **Régi:** Beégetett szimbólumlista: `["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]`
   - **Új:** Dinamikus szimbólumlista a `data_service.get_configured_symbols()` hívással
   - **Előny:** A letöltési opciók mostantól a ténylegesen konfigurált szimbólumokat tartalmazzák

3. **Dokumentáció fejlesztés:**
   - Magyar Google Style docstring-ek hozzáadása minden metódushoz
   - Részletes leírás a metódusok funkcióiról és hibakezeléséről

4. **Típusbiztonság:**
   - A `_data_service` típusa mostantól `DataServiceInterface | None`
   - A `DataServiceInterface`-hez hozzáadva a `get_configured_symbols()` metódus
   - `TYPE_CHECKING` blokk használata a körkörös importok elkerülésére

5. **Hibakezelés:**
   - Fallback mechanizmus: ha a szimbólumok lekérdezése sikertelen, a rendszer `["EURUSD"]` értékkel folytatja
   - Felhasználóbarát hibaüzenetek megjelenítése

## Használati példa

```python
from neural_ai.ui.core_bridge import CoreBridge
from neural_ai.ui.pages.data_hub_page import DataHubPage

# CoreBridge létrehozása
bridge = CoreBridge()

# DataHubPage létrehozása
page = DataHubPage(bridge)

# Oldal megjelenítése
page.render()
```

## Függőségek

- `neural_ai.ui.interfaces.page_interface.PageInterface`
- `neural_ai.ui.interfaces.data_service_interface.DataServiceInterface`
- `neural_ai.ui.interfaces.core_bridge_interface.CoreBridgeInterface`
- `neural_ai.ui.factory.UIServiceFactory`
- `streamlit`

## Tesztelés

A Data Hub oldal tesztelése a következőképpen történik:

```bash
# Ruff linter ellenőrzés
ruff check neural_ai/ui/pages/03_📥_Data_Hub.py

# Pytest teszt futtatása
pytest tests/ui/pages/test_data_hub_page.py -v

# Coverage ellenőrzés
pytest tests/ui/pages/test_data_hub_page.py --cov=neural_ai.ui.pages.data_hub_page --cov-report=term-missing
```

## Jövőbeli fejlesztések

- [ ] Több adatforrás támogatása
- [ ] Speciális szűrők implementálása
- [ ] Valós idejű adatfrissítés
- [ ] Grafikonok és vizualizációk hozzáadása
- [ ] Tömeges műveletek támogatása