# Logger Formázók

## Áttekintés

Ez a modul a különböző logger formázókat tartalmazza, amelyek a log üzenetek megjelenítését vezérlik. A formázók lehetővé teszik a log üzenetek testreszabását, beleértve a színes kimenetet is.

## Osztályok

### ColoredFormatter

A `ColoredFormatter` egy speciális formázó, amely ANSI színkódokat használ a log üzenetek színes megjelenítéséhez. Különböző színeket rendel a különböző log szintekhez, ami segít a logok gyorsabb áttekintésében és szűrésében.

#### Színleképezés

| Log Szint | ANSI Színkód | Leírás |
|-----------|--------------|--------|
| DEBUG | `\033[94m` | Kék szöveg |
| INFO | `\033[92m` | Zöld szöveg |
| WARNING | `\033[93m` | Sárga szöveg |
| ERROR | `\033[91m` | Piros szöveg |
| CRITICAL | `\033[97;41m` | Fehér szöveg piros háttéren |

#### Osztályváltozók

```python
COLORS: dict[int, str]
```
A log szintekhez tartozó ANSI színkódokat tartalmazó szótár.

```python
RESET: str = "\033[0m"
```
Az ANSI színkódok visszaállítására szolgáló kód.

#### Metódusok

##### `format(record: logging.LogRecord) -> str`

A log rekord formázását végzi színes kimenettel.

**Paraméterek:**
- `record` (`logging.LogRecord`): A formázandó log rekord

**Visszatérési érték:**
- `str`: A színes formázott log üzenet

**Működés:**
1. Először az ősosztály `format()` metódusát hívja meg az alap formázáshoz
2. Ellenőrzi, hogy a log rekord szintje szerepel-e a `COLORS` szótárban
3. Ha igen, hozzáadja a megfelelő színkódot az üzenet elejéhez
4. Hozzáadja a reset kódot az üzenet végéhez
5. Visszaadja a színes formázott üzenetet

**Példa:**
```python
import logging
from neural_ai.core.logger.formatters.logger_formatters import ColoredFormatter

# Formatter létrehozása
formatter = ColoredFormatter()

# Log rekord létrehozása
record = logging.LogRecord(
    name="test",
    level=logging.INFO,
    pathname="",
    lineno=0,
    msg="Sikeres művelet",
    args=(),
    exc_info=None
)

# Formázás
formatted_message = formatter.format(record)
# Eredmény: "\033[92mSikeres művelet\033[0m"
```

## Használat

### Alap használat

```python
import logging
from neural_ai.core.logger.formatters.logger_formatters import ColoredFormatter

# Logger létrehozása
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# Console handler létrehozása
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# ColoredFormatter hozzáadása
formatter = ColoredFormatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Használat
logger.debug("Hibakeresési üzenet")
logger.info("Információs üzenet")
logger.warning("Figyelmeztető üzenet")
logger.error("Hibaüzenet")
logger.critical("Kritikus hibaüzenet")
```

### Egyéni formátummal

```python
# Egyéni formátum beállítása
formatter = ColoredFormatter(
    fmt='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
```

## Előnyök

1. **Gyors áttekintés:** A színek segítségével gyorsan azonosíthatók a különböző szintű üzenetek
2. **Jobb olvashatóság:** A színes kimenet jobban olvasható, mint az egyszínű
3. **Kiemelés:** A fontos üzenetek (ERROR, CRITICAL) jobban kiemelkednek
4. **Konzolbarát:** Kiválóan használható konzolos alkalmazásokban

## Megjegyzések

- A színes kimenet csak olyan terminálokban jelenik meg megfelelően, amelyek támogatják az ANSI színkódokat
- Fájlba írás esetén az ANSI kódok is belekerülnek a fájlba, ami olvashatatlanná teheti azt
- Windows rendszereken előfordulhat, hogy a színes kimenet nem működik megfelelően az alapértelmezett konzolban

## Lásd még

- [Python logging modul](https://docs.python.org/3/library/logging.html)
- [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code)