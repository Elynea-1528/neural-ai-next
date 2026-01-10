# DataServiceInterface

## Áttekintés

A `DataServiceInterface` egy Protocol alapú interfész, amely definiálja az adatkezelési szolgáltatás szerződését a Neural AI Next rendszerben. Ez az interfész felelős az adatok betöltéséért, szűréséért, kezeléséért és exportálásáért, Big Data támogatással.

## Elhelyezkedés

- **Forráskód:** [`neural_ai/ui/interfaces/data_service_interface.py`](../../../neural_ai/ui/interfaces/data_service_interface.py)
- **Dokumentáció:** `docs/components/ui/interfaces/data_service_interface.md`

## Metódusok

### `load_data`

```python
def load_data(
    self,
    source: str,
    filters: dict[str, Any] | None = None,
    chunk_size: int = 10000
) -> Generator[list[dict[str, Any]], None, None]
```

Adatok aszinkron betöltése chunkokban.

**Paraméterek:**
- `source` (str): Az adatforrás azonosítója
- `filters` (dict[str, Any] | None): Szűrőfeltételek
- `chunk_size` (int): A chunkok mérete (alapértelmezett: 10000)

**Visszatérési érték:**
- `Generator[list[dict[str, Any]], None, None]`: Adat chunkok generátora

---

### `get_data_sources`

```python
def get_data_sources(self) -> list[dict[str, str]]
```

Elérhető adatforrások lekérdezése.

**Visszatérési érték:**
- `list[dict[str, str]]`: Az adatforrások listája

---

### `get_data_info`

```python
def get_data_info(self, source: str) -> dict[str, Any]
```

Adatforrás információk lekérdezése.

**Paraméterek:**
- `source` (str): Az adatforrás azonosítója

**Visszatérési érték:**
- `dict[str, Any]`: Az adatforrás metaadatai

---

### `apply_filters`

```python
def apply_filters(
    self,
    data: list[dict[str, Any]],
    filters: dict[str, Any]
) -> list[dict[str, Any]]
```

Szűrők alkalmazása adatokra.

**Paraméterek:**
- `data` (list[dict[str, Any]]): A szűrendő adatok
- `filters` (dict[str, Any]): Az alkalmazandó szűrők

**Visszatérési érték:**
- `list[dict[str, Any]]`: A szűrt adatok

---

### `export_data`

```python
def export_data(
    self,
    data: list[dict[str, Any]],
    format: str,
    destination: str
) -> bool
```

Adatok exportálása különböző formátumokba.

**Paraméterek:**
- `data` (list[dict[str, Any]]): Az exportálandó adatok
- `format` (str): A célformátum (parquet, csv, json)
- `destination` (str): A cél útvonal

**Visszatérési érték:**
- `bool`: True, ha sikeres az exportálás

---

### `download_history` ⭐ ÚJ

```python
async def download_history(
    self,
    symbol: str,
    start: datetime,
    end: datetime
) -> dict[str, Any]
```

Történelmi adatok letöltése aszinkron módon a Data Hub-ból.

**Paraméterek:**
- `symbol` (str): A szimbólum (pl. 'EURUSD')
- `start` (datetime): A kezdő dátum
- `end` (datetime): A záró dátum

**Visszatérési érték:**
- `dict[str, Any]`: A letöltés eredménye és metaadatok

---

### `list_available_data` ⭐ ÚJ

```python
def list_available_data(
    self,
    symbol: str | None = None
) -> pd.DataFrame
```

Elérhető adatok listázása a Data Hub-ban.

**Paraméterek:**
- `symbol` (str | None): Opcionális szimbólum szűréshez

**Visszatérési érték:**
- `pd.DataFrame`: Az elérhető adatok táblázata

---

### `get_storage_path` ⭐ ÚJ

```python
def get_storage_path(self) -> Path
```

A Data Hub tárhelyének elérési útjának lekérdezése.

**Visszatérési érték:**
- `Path`: A tárhely elérési útja

---

## Implementációk

Az interfész implementációit a `neural_ai/ui/services/` mappában találhatók.

## Használat

```python
from neural_ai.ui.interfaces.data_service_interface import DataServiceInterface
from neural_ai.ui.factory import UIFactory

# Factory-n keresztül példányosítás
data_service = UIFactory.get_instance().get_service("data")

# Adatok betöltése
for chunk in data_service.load_data("EURUSD", chunk_size=5000):
    process_data(chunk)

# Történelmi adatok letöltése (aszinkron)
result = await data_service.download_history(
    symbol="EURUSD",
    start=datetime(2024, 1, 1),
    end=datetime(2024, 12, 31)
)

# Elérhető adatok listázása
available_data = data_service.list_available_data(symbol="EURUSD")

# Tárhely elérési út lekérdezése
storage_path = data_service.get_storage_path()
```

## Jellemzők

- **Big Data támogatás:** Chunk-based adatbetöltés generátorokkal
- **Aszinkron műveletek:** Történelmi adatok letöltése aszinkron módon
- **Típusos megjelölések:** Szigorú típusellenőrzés a teljes interfészen
- **Data Hub integráció:** Új metódusok a Data Hub-hoz való integrációhoz
- **Parquet támogatás:** Exportálás Parquet formátumba

## Kapcsolódó dokumentáció

- [UI Architektúra](../architecture.md)
- [Streamlit App](../streamlit_app.md)
- [Data Service implementáció](../../../neural_ai/ui/services/data_service.py)