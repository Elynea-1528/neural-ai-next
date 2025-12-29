# core/logger/formatters/logger_formatters.py

Logger formázók.

Ez a modul tartalmazza a különböző logger formázókat, amelyek
a log üzenetek megjelenítését vezérlik (pl. színes kimenet).

## Osztályok

### `ColoredFormatter`

Színes megjelenítést biztosító formatter.

    Különböző színekkel jelöli a különböző log szinteket:
    - DEBUG: Kék
    - INFO: Zöld
    - WARNING: Sárga
    - ERROR: Piros
    - CRITICAL: Piros (háttér)


## Függvények

### `format`

Log rekord formázása színes kimenettel.

        Args:
            record: A formázandó log rekord

        Returns:
            str: A színes formázott log üzenet


---

**Forrásfájl:** [`core/logger/formatters/logger_formatters.py`](../../../neural_ai/core/logger/formatters/logger_formatters.py)
