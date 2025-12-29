# core/logger/implementations/default_logger.py

Alapértelmezett logger implementáció.

Ez a modul a standard logging könyvtár alapú logger implementációt tartalmazza,
amely a Python beépített logging rendszerét használja.

## Osztályok

### `DefaultLogger`

Alapértelmezett logger implementáció a Python logging moduljával.

    Ez az osztály a Python standard library logging rendszerét használja,
    és implementálja a LoggerInterface-t. Konfigurálható log szinttel,
    formátummal és stream handlerrel.

    Attributes:
        logger: A belső Python logger objektum


## Függvények

### `__init__`

Logger inicializálása.

        A konstruktor létrehoz egy Python logger objektumot a megadott névvel,
        eltávolítja a korábbi handlereket (ha voltak), és beállítja a log szintet,
        formátumot és stream handlert a kapott paraméterek alapján.

        Args:
            name: A logger egyedi neve. Ez a név jelenik meg a log üzenetekben.
            **kwargs: Opcionális kulcsszó argumentumok:
                - level (int): Log szint (pl. logging.DEBUG, logging.INFO).
                  Alapértelmezett: logging.INFO.
                - format (str): Log formátum string. Alapértelmezett:
                  "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                - stream: Kimeneti stream. Alapértelmezett: sys.stderr.

        Példa:
            >>> logger = DefaultLogger("my_app")
            >>> logger = DefaultLogger("my_app", level=logging.DEBUG)
            >>> logger = DefaultLogger("my_app",
            ...                       format="%(levelname)s: %(message)s")

### `debug`

Debug szintű üzenet logolása.

        Args:
            message: A log üzenet szövege.
            **kwargs: További paraméterek, amelyek az extra kulcs alatt
                kerülnek átadásra a loggernek.

        Példa:
            >>> logger.debug("Hibakeresési üzenet", user_id=123)

### `info`

Info szintű üzenet logolása.

        Args:
            message: A log üzenet szövege.
            **kwargs: További paraméterek, amelyek az extra kulcs alatt
                kerülnek átadásra a loggernek.

        Példa:
            >>> logger.info("Sikeres művelet", duration=0.5)

### `warning`

Warning szintű üzenet logolása.

        Args:
            message: A log üzenet szövege.
            **kwargs: További paraméterek, amelyek az extra kulcs alatt
                kerülnek átadásra a loggernek.

        Példa:
            >>> logger.warning("Elavult API hívás", version="1.0")

### `error`

Error szintű üzenet logolása.

        Args:
            message: A log üzenet szövege.
            **kwargs: További paraméterek, amelyek az extra kulcs alatt
                kerülnek átadásra a loggernek.

        Példa:
            >>> logger.error("Adatbázis kapcsolat hiba", db="main")

### `critical`

Critical szintű üzenet logolása.

        Args:
            message: A log üzenet szövege.
            **kwargs: További paraméterek, amelyek az extra kulcs alatt
                kerülnek átadásra a loggernek.

        Példa:
            >>> logger.critical("Kritikus rendszerhiba", component="auth")

### `set_level`

Logger log szintjének beállítása.

        A metódus beállítja a logger és a hozzá tartozó handler minimális
        log szintjét. Ez határozza meg, hogy melyik szintű üzenetek kerüljenek
        naplózásra.

        Args:
            level: Az új log szint (pl. logging.DEBUG, logging.INFO,
                logging.WARNING, logging.ERROR, logging.CRITICAL).

        Példa:
            >>> logger.set_level(logging.DEBUG)

### `get_level`

Aktuális log szint lekérése.

        Returns:
            int: Az aktuális log szint numerikus értéke. A visszaadott érték
                a logging modul konstansainak egyike (pl. logging.INFO -> 20).

        Példa:
            >>> level = logger.get_level()
            >>> print(f"Aktuális log szint: {level}")


---

**Forrásfájl:** [`core/logger/implementations/default_logger.py`](../../../neural_ai/core/logger/implementations/default_logger.py)
