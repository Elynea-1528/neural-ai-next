# scripts/audit_data.py

Adatintegritási audit script.

Összehasonlítja a nyers .bi5 fájlokban lévő adatokat a feldolgozott Parquet
fájlokkal óránkénti bontásban, hogy feltérképezze a hiányzó adatokat.

## Importok

```python
import lzma
import struct
from collections import defaultdict
from datetime import UTC
from datetime import datetime
from pathlib import Path
import polars
```

## Konstansok

- **`data`**
: `f.read()`


- **`filename`**
: `file_path.stem`


- **`parts`**
: `filename.split('_')`


- **`year`**
: `int(parts[1])`


- **`month`**
: `int(parts[2])`


- **`day`**
: `int(parts[3])`


- **`hour`**
: `int(parts[4].replace('h', ''))`


- **`base_timestamp`**
: `int(datetime(year, month, day, hour, 0, 0, tzinfo=UTC).timestamp()) * 1000`


- **`record_size`**
: `12`


- **`record_size`**
: `20`


- **`num_records`**
: `len(data) // record_size`


- **`offset`**
: `i * record_size`


- **`timestamp_delta`**
: `struct.unpack('>I', data[offset:offset + 4])[0]`


- **`timestamp_ms`**
: `base_timestamp + timestamp_delta`


- **`timestamp`**
: `datetime.fromtimestamp(timestamp_ms / 1000, tz=UTC)`


- **`bi5_files`**
: `sorted(raw_dir.glob('*.bi5'))`


- **`timestamps`**
: `parse_bi5_file(bi5_file)`


- **`hour`**
: `ts.strftime('%H')`


- **`parquet_files`**
: `sorted(tick_dir.glob('**/*.parquet'))`


- **`hour`**
: `str(row[0]).zfill(2)`


- **`count`**
: `row[1]`


- **`all_hours`**
: `sorted(set(list(raw_counts.keys()) + list(sys_counts.keys())))`


- **`total_raw`**
: `0`


- **`total_sys`**
: `0`


- **`raw_count`**
: `raw_counts.get(hour, 0)`


- **`sys_count`**
: `sys_counts.get(hour, 0)`


- **`status`**
: `'ÜRES'`


- **`status`**
: `'❌ HIÁNYZIK'`


- **`status`**
: `'✅ OK'`


- **`diff`**
: `raw_count - sys_count`


- **`status`**
: `f'⚠️  -{diff}'`


- **`project_root`**
: `Path(__file__).parent.parent`


- **`raw_dir`**
: `project_root / 'data' / 'debug_raw'`


- **`tick_dir`**
: `project_root / 'data' / 'tick'`


- **`raw_counts`**
: `analyze_raw_data(raw_dir)`


- **`sys_counts`**
: `analyze_system_data(tick_dir)`


### `parse_bi5_file()`

```python
def parse_bi5_file(file_path: Path) -> list[datetime]
```

Kicsomagolja és feldolgozza a .bi5 fájlt, visszaadja az összes tick timestamp-et. A .bi5 fájl LZMA tömörített bináris adatot tartalmaz, ahol minden rekord 12 bájt (timestamp_delta: 4 bájt, ask: 4 bájt, bid: 4 bájt) vagy 20 bájt lehet. A timestamp_delta az óra elejétől mért ezredmásodpercben.

**Paraméterek:**

- **`file_path`** (`Path`)

**Visszatérési érték:**

- Típus: `list[datetime]`

### `analyze_raw_data()`

```python
def analyze_raw_data(raw_dir: Path) -> dict[str, int]
```

Analizálja a nyers .bi5 fájlokat és visszaadja óránkénti darabszámot.

**Paraméterek:**

- **`raw_dir`** (`Path`): A data/debug_raw mappa útvonala

**Visszatérési érték:**

- Típus: `dict[str, int]`
- Dict ahol a kulcs az óra (pl. "00", "01", ..., "23"), az érték a darabszám

### `analyze_system_data()`

```python
def analyze_system_data(tick_dir: Path) -> dict[str, int]
```

Analizálja a feldolgozott Parquet fájlokat és visszaadja óránkénti darabszámot.

**Paraméterek:**

- **`tick_dir`** (`Path`): A data/tick mappa útvonala

**Visszatérési érték:**

- Típus: `dict[str, int]`
- Dict ahol a kulcs az óra (pl. "00", "01", ..., "23"), az érték a darabszám

### `compare_data()`

```python
def compare_data(raw_counts: dict[str, int], sys_counts: dict[str, int]) -> None
```

Összehasonlítja a nyers és rendszer adatokat, kiírja a táblázatot.

**Paraméterek:**

- **`raw_counts`** (`dict[str, int]`): Nyers adatok óránkénti darabszáma
- **`sys_counts`** (`dict[str, int]`): Rendszer adatok óránkénti darabszáma

**Visszatérési érték:**

- Típus: `None`

### `main()`

```python
def main() -> None
```

Fő végrehajtási függvény.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`scripts/audit_data.py`](../../scripts/audit_data.py)
