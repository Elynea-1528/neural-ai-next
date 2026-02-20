# neural_ai/core/logger/formatters/logger_formatters.py

Logger formázók.

Ez a modul tartalmazza a különböző logger formázókat, amelyek
a log üzenetek megjelenítését vezérlik (pl. színes kimenet).

## Importok

```python
import logging
```

## Osztály: `ColoredFormatter(logging.Formatter)`

Színes megjelenítést biztosító formatter.

Különböző színekkel jelöli a különböző log szinteket:
- DEBUG: Kék
- INFO: Zöld
- WARNING: Sárga
- ERROR: Piros
- CRITICAL: Piros (háttér)

### Metódusok

#### `format()`

```python
def format(self, record: logging.LogRecord) -> str
```

Log rekord formázása színes kimenettel.

**Paraméterek:**

- **`self`**
- **`record`** (`logging.LogRecord`): A formázandó log rekord

**Visszatérési érték:**

- Típus: `str`
- str: A színes formázott log üzenet

---

**Forrásfájl:** [`neural_ai/core/logger/formatters/logger_formatters.py`](../../neural_ai/core/logger/formatters/logger_formatters.py)
