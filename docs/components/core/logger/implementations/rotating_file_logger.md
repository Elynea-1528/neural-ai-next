# core/logger/implementations/rotating_file_logger.py

Rotáló fájl logger implementáció.

## Osztályok

### `RotatingFileLogger`

File alapú logger, ami automatikusan rotálja a log fájlokat.

    A logger támogatja a méret alapú és idő alapú rotációt is. A méret alapú
    rotáció esetén a fájl elér egy bizonyos méretet, az idő alapú rotáció
    esetén pedig egy adott időközönként történik a rotáció.

    Attributes:
        logger: A Python logging logger példány


## Függvények

### `__init__`

Logger inicializálása.

        Args:
            name: A logger egyedi neve.
            log_file: A log fájl teljes útvonala.
            level: A log szint (alapértelmezett: INFO).
            max_bytes: Maximum fájlméret bájtban rotálás előtt (méret alapú rotációhoz).
            backup_count: Megtartott backup fájlok száma.
            format_str: A log üzenetek formátuma.
            rotation_type: A rotáció típusa ('size' vagy 'time').
            when: Időegység időalapú rotáció esetén ('S', 'M', 'H', 'D', stb.).
            **kwargs: További paraméterek (az interfész kompatibilitás miatt).

        Raises:
            ValueError: Ha a log_file nincs megadva vagy érvénytelen a rotation_type.

### `debug`

Debug szintű üzenet logolása.

        Args:
            message: A logolandó üzenet.
            **kwargs: További paraméterek (pl. extra adatok a loghoz).

### `info`

Info szintű üzenet logolása.

        Args:
            message: A logolandó üzenet.
            **kwargs: További paraméterek (pl. extra adatok a loghoz).

### `warning`

Warning szintű üzenet logolása.

        Args:
            message: A logolandó üzenet.
            **kwargs: További paraméterek (pl. extra adatok a loghoz).

### `error`

Error szintű üzenet logolása.

        Args:
            message: A logolandó üzenet.
            **kwargs: További paraméterek (pl. extra adatok a loghoz).

### `critical`

Critical szintű üzenet logolása.

        Args:
            message: A logolandó üzenet.
            **kwargs: További paraméterek (pl. extra adatok a loghoz).

### `set_level`

Logger log szintjének beállítása.

        Args:
            level: Az új log szint (pl. logging.DEBUG, logging.INFO).

### `get_level`

Aktuális log szint lekérése.

        Returns:
            Az aktuális log szint értéke.

### `clean_old_logs`

Régi log fájlok eltávolítása.

        Figyelmeztetés: Ez a metódus véglegesen törli a log könyvtárat
        és annak teljes tartalmát!

        Args:
            log_dir: A log könyvtár útvonala.


---

**Forrásfájl:** [`core/logger/implementations/rotating_file_logger.py`](../../../neural_ai/core/logger/implementations/rotating_file_logger.py)
