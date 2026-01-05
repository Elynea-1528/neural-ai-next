# Data Hub Page - Adatkezelő központ

## Áttekintés

A Data Hub Page a Neural AI Next rendszer adatkezelő felületét biztosítja. Ez az oldal felelős az adatok listázásáért, történelmi adatok letöltéséért és adatok exportálásáért a DataService segítségével, amely a UIServiceFactory-n keresztül érhető el.

## Architektúra

### Osztálystruktúra

```python
class DataHubPage(PageInterface):
    """Data Hub oldal.

    Ez az oldal felelős az adatok kezeléséért, letöltéséért és megjelenítéséért
    a DataService segítségével, amely a UIServiceFactory-n keresztül érhető el.
    """
```

### Függőségek

- **PageInterface**: Az oldal alapinterfésze
- **DataServiceInterface**: Az adatszolgáltatás interfésze
- **CoreBridgeInterface**: A backend bridge interfésze
- **UIServiceFactory**: A UI szolgáltatások gyártója

## Metódusok

### `__init__(bridge: CoreBridgeInterface, **kwargs: Any) -> None`

A Data Hub oldal inicializálása.

**Paraméterek:**
- `bridge`: A CoreBridge példány, amelyen keresztül elérjük a backendet
- `**kwargs`: További opcionális argumentumok

### `render() -> None`

Az oldal megjelenítése Streamlit segítségével.

Ez a metódus felelős a felhasználói felület létrehozásáért, amely három fő szekciót tartalmaz:
1. Adatok listázása
2. Történelmi adatok letöltése
3. Adatok exportálása

### `_render_data_listing() -> None`

Elérhető adatok listázásának megjelenítése.

Ez a metódus a következőket végzi:
- Szimbólum szűrést biztosít a felhasználónak
- A DataService `list_available_data()` metódusát használja az adatok lekérdezéséhez
- DataFrame formátumban jeleníti meg az adatokat
- Összesítő információkat szolgáltat (összes rekord, méret, adatforrások)

### `_render_download_history() -> None`

Történelmi adatok letöltésének megjelenítése.

Ez a metódus a következőket végzi:
- Bemeneti mezőket jelenít meg (szimbólum, dátumtartomány)
- A DataService `download_history()` metódusát használja az adatok letöltéséhez
- Aszinkron módon végzi a letöltést
- Eredményeket jelenít meg (sikeres/ sikertelen letöltések, méretek)

### `_render_data_export() -> None`

Adatok exportálásának megjelenítése.

Ez a metódus a következőket végzi:
- Exportálási beállításokat jelenít meg (formátum, forrás, cél)
- A DataService `load_data()` és `export_data()` metódusait használja
- Chunkolással tölti be az adatokat a memóriahatékony működés érdekében

### `on_navigate_to(params: Optional[dict[str, Any]] = None) -> None`

Az oldalra navigáláskor meghívott metódus.

**Paraméterek:**
- `params`: Opcionális navigációs paraméterek

### `on_navigate_from() -> None`

Az oldalról navigáláskor meghívott metódus.

### `title: str` (property)

Az oldal címe.

**Visszatérési érték:**
- `str`: Az oldal címe

### `is_loaded: bool` (property)

Az oldal betöltöttségi állapota.

**Visszatérési érték:**
- `bool`: True, ha az oldal betöltődött, egyébként False

## DataService integráció

A Data Hub Page a következő DataService metódusokat használja:

### `list_available_data(symbol: str | None = None) -> pd.DataFrame`

Elérhető adatok listázása DataFrame formátumban.

**Paraméterek:**
- `symbol`: Opcionális szimbólum szűréshez

**Visszatérési érték:**
- `pd.DataFrame`: Az elérhető adatok DataFrame-je

### `download_history(symbol: str, start: datetime, end: datetime) -> dict[str, Any]`

Történelmi adatok letöltése aszinkron módon.

**Paraméterek:**
- `symbol`: A szimbólum (pl. 'EURUSD')
- `start`: A kezdő dátum
- `end`: A záró dátum

**Visszatérési érték:**
- `dict[str, Any]`: A letöltés eredménye és metaadatok

### `load_data(source: str, filters: dict[str, Any] | None = None, chunk_size: int = 10000) -> Generator[list[dict[str, Any]], None, None]`

Adatok aszinkron betöltése chunkokban.

**Paraméterek:**
- `source`: Az adatforrás azonosítója
- `filters`: Szűrőfeltételek
- `chunk_size`: A chunkok mérete

**Visszatérési érték:**
- `Generator`: Adat chunkok generátora

### `export_data(data: list[dict[str, Any]], format: str, destination: str) -> bool`

Adatok exportálása különböző formátumokba.

**Paraméterek:**
- `data`: Az exportálandó adatok
- `format`: A célformátum (parquet, csv, json)
- `destination`: A cél útvonal

**Visszatérési érték:**
- `bool`: True, ha sikeres az exportálás

## Factory használata

A Data Hub Page a UIServiceFactory segítségével éri el a DataService-t:

```python
from neural_ai.ui.factory import UIServiceFactory

factory = UIServiceFactory()
if not factory.is_initialized:
    st.error("A UI Service Factory nincs inicializálva")
    return

self._data_service = factory.get_data_service()
```

Ez biztosítja a Dependency Injection elvét, és lehetővé teszi a lazyloadingot és a tesztelhetőséget.

## Big Data támogatás

A Data Hub Page Big Data támogatással rendelkezik:

- **Chunkolás**: Az adatok kis darabokban történő betöltése
- **Aszinkron működés**: A letöltések nem blokkolják a felhasználói felületet
- **Parquet formátum**: Hatékony bináris adattárolás
- **Streamelés**: Nagy adatmennyiségek feldolgozása memóriahatékonyan

## Hibakezelés

Az oldal szilárd hibakezeléssel rendelkezik:

- Factory inicializálás ellenőrzése
- Dátumtartomány validáció
- Hibaüzenetek megjelenítése a felhasználónak
- Kivételek elkapása és felhasználóbarát üzenetekkel való helyettesítése

## Példa használatra

```python
# Oldal létrehozása
page = DataHubPage(bridge=core_bridge)

# Oldal megjelenítése
page.render()
```

## Kapcsolódó dokumentáció

- [DataService](../services/data_service.md)
- [DataServiceInterface](../interfaces/data_service_interface.md)
- [UIServiceFactory](../factory.md)
- [PageInterface](../interfaces/page_interface.md)