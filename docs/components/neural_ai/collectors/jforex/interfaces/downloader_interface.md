# neural_ai/collectors/jforex/interfaces/downloader_interface.py

JForex Downloader Interface Definition.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING
from neural_ai.collectors.jforex.interfaces.tick_data import TickData
```

## Osztály: `IJForexDownloader(ABC)`

JForex .bi5 adat letöltő interfész.

Ez az interfész definiálja a szerződést a Dukascopy natív .bi5 tick adat
formátum letöltéséhez és feldolgozásához.

### Metódusok

#### `download_tick_data()`

```python
async def download_tick_data(self, symbol: str, date: datetime) -> list['TickData']
```

Tick adatok letöltése és dekódolása adott szimbólumhoz és dátumhoz.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): Kereskedelmi szimbólum (pl. 'EURUSD', 'GBPUSD')
- **`date`** (`datetime`): Dátum, amelyhez az adatokat le kell tölteni

**Visszatérési érték:**

- Típus: `list['TickData']`
- TickData objektumok listája bid/ask árakkal

**Kivételek:**

- **`DownloadError`**: Ha a letöltés sikertelen (hálózati problémák, szerverhibák)
- **`DecodeError`**: Ha az adat dekódolása sikertelen (sérült fájl)
- **`DataNotAvailableError`**: Ha az adat nem elérhető (hétvége, ünnep)

#### `get_available_dates()`

```python
async def get_available_dates(self, symbol: str, start_date: datetime, end_date: datetime) -> list[datetime]
```

Szimbólum elérhető adatainak dátumlistája.

**Paraméterek:**

- **`self`**
- **`symbol`** (`str`): Kereskedelmi szimbólum
- **`start_date`** (`datetime`): Dátumtartomány kezdete
- **`end_date`** (`datetime`): Dátumtartomány vége

**Visszatérési érték:**

- Típus: `list[datetime]`
- Elérhető adatokkal rendelkező dátumok datetime objektumai

#### `validate_bi5_data()`

```python
def validate_bi5_data(self, data: bytes) -> bool
```

.bi5 adat integritásának ellenőrzése.

**Paraméterek:**

- **`self`**
- **`data`** (`bytes`): Nyers .bi5 adat bájtok

**Visszatérési érték:**

- Típus: `bool`
- True ha az adat érvényes, különben False

#### `close()`

```python
async def close(self) -> None
```

Letöltő bezárása és erőforrások felszabadítása. Ez a metódus biztosítja, hogy minden hálózati kapcsolat megfelelően bezáródjon és az erőforrások felszabaduljanak, amikor a letöltőre már nincs szükség.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/collectors/jforex/interfaces/downloader_interface.py`](../../neural_ai/collectors/jforex/interfaces/downloader_interface.py)
