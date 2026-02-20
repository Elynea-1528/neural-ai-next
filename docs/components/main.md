# main.py

Neural AI Next - Unified CLI Entry Point.

Ez a modul a rendszer központi belépési pontja, amely egyesíti a live módot,
a történelmi adatok letöltését és a dashboard-t egy egységes CLI felületen keresztül.

Használat:
    python main.py live                    # Live mód indítása
    python main.py download --symbol EURUSD --start 2024-03-20 --end 2024-03-20
    python main.py dashboard               # Dashboard indítása
    python main.py dashboard --host 0.0.0.0 --port 8501 --server.headless True

## Importok

```python
import argparse
import asyncio
import sys
from contextlib import suppress
from datetime import UTC
from datetime import datetime
from typing import TYPE_CHECKING
from neural_ai.core import get_core_components
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed
# ... és még 7 import
```

## Konstansok

- **`streamlit_cmd`**
: `['/home/elynea/miniconda3/envs/neural-ai-next/bin/streamlit', 'run', 'neural_ai/ui/streamlit_app.py', '--server.address', host, '--server.port', str(port)]`


- **`parser`**
: `argparse.ArgumentParser(description='Neural AI Next - Unified CLI', formatter_class=argparse.RawDescriptionHelpFormatter, epilog='\nPéldák:\n  %(prog)s live\n  %(prog)s download --symbol EURUSD --start 2024-03-20 --end 2024-03-20\n  %(prog)s dashboard\n  %(prog)s dashboard --host 0.0.0.0 --port 8501 --headless\n        ')`


- **`subparsers`**
: `parser.add_subparsers(dest='command', help='Parancsok')`


- **`download_parser`**
: `subparsers.add_parser('download', help='Történelmi adatok letöltése')`


- **`dashboard_parser`**
: `subparsers.add_parser('dashboard', help='Dashboard indítása')`


- **`components`**
: `get_core_components()`


- **`logger`**
: `components.logger`


- **`args`**
: `parse_arguments()`


- **`start_date`**
: `parse_date(args.start)`


- **`end_date`**
: `parse_date(args.end).replace(hour=23, minute=59, second=59)`


### `run_live_mode()`

```python
async def run_live_mode() -> None
```

Live mód indítása - az eredeti main logika. Ez a függvény felelős az alkalmazás teljes életciklusáért: 1. Core komponensek inicializálása 2. Szolgáltatások indítása (event bus, adatbázis) 3. Örök futás biztosítása, amíg le nem állítják 4. Hiba kezelése és naplózása

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`SystemExit`**: Ha kritikus hiba történik az alkalmazás indítása során.

### `run_download_mode()`

```python
async def run_download_mode(logger: LoggerInterface, symbol: str, start_date: datetime, end_date: datetime) -> None
```

Történelmi adatok letöltése a megadott tartományban.

**Paraméterek:**

- **`logger`** (`LoggerInterface`): Logger példány a naplózáshoz
- **`symbol`** (`str`): A pénzpár szimbóluma (pl. 'EURUSD')
- **`start_date`** (`datetime`): A letöltés kezdő dátuma
- **`end_date`** (`datetime`): A letöltés záró dátuma

**Visszatérési érték:**

- Típus: `None`

### `run_dashboard_mode()`

```python
def run_dashboard_mode(logger: LoggerInterface, host: str, port: int, headless: bool) -> None
```

Dashboard indítása Streamlit-en keresztül.

**Paraméterek:**

- **`logger`** (`LoggerInterface`): Logger példány a naplózáshoz
- **`host`** (`str`): A szerver hosztja (pl. 'localhost' vagy '0.0.0.0')
- **`port`** (`int`): A szerver portja (pl. 8501)
- **`headless`** (`bool`): Ha True, headless módban fut (nincs browser automatikus megnyitása)

**Visszatérési érték:**

- Típus: `None`

### `parse_arguments()`

```python
def parse_arguments() -> argparse.Namespace
```

Argumentumok feldolgozása.

**Visszatérési érték:**

- Típus: `argparse.Namespace`
- A feldolgozott argumentumok

### `parse_date()`

```python
def parse_date(date_str: str) -> datetime
```

Dátum string parse-olása.

**Paraméterek:**

- **`date_str`** (`str`): Dátum string (YYYY-MM-DD formátumban)

**Visszatérési érték:**

- Típus: `datetime`
- A parse-olt dátum UTC időzónával

### `main()`

```python
def main() -> None
```

Főprogram.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`main.py`](../../main.py)
