# core/logger/implementations/colored_logger.py

Színes konzol logger implementáció.

Ez a modul a ColoredLogger osztályt tartalmazza, amely színes konzol kimenetet
biztosít a log üzenetekhez a Python standard logging könyvtárát felhasználva.

## Osztályok

### `ColoredLogger`

Színes konzol kimenettel rendelkező logger implementáció.

    Ez az osztály a LoggerInterface-t implementálja, és színes formázást alkalmaz
    a log üzenetekhez a konzolon. A színek a log szinttől függenek, ami segít
    a gyorsabb hibakeresésben és a logok könnyebb olvashatóságában.

    Attributes:
        logger: A belső Python logger objektum


## Függvények

### `__init__`

Logger inicializálása színes konzol kimenettel.

        Args:
            name: A logger egyedi neve. Ez a név jelenik meg a log üzenetekben.
            level: A log szint (pl. logging.DEBUG, logging.INFO). Alapértelmezett
                értéke a logging.INFO.
            format_str: A log üzenetek formátuma. Alapértelmezett formátum:
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            stream: A kimeneti stream, ahova a logok íródnak. Alapértelmezett
                értéke a sys.stdout.
            **kwargs: További opcionális paraméterek, amelyeket a jövőbeli
                bővíthetőség érdekében elfogad az osztály.

        Példa:
            >>> logger = ColoredLogger("my_app", level=logging.DEBUG)
            >>> logger.info("Alkalmazás elindult")

### `debug`

Debug szintű üzenet logolása.

        Ez a metódus részletes hibakeresési információkat logol, amelyek általában
        csak fejlesztés közben hasznosak.

        Args:
            message: A logolandó debug üzenet.
            **kwargs: További paraméterek, amelyek az extra adatokhoz adhatók
                a log rekordban.

        Példa:
            >>> logger.debug("Adatfeldolgozás elkezdődött", file="data.txt")

### `info`

Info szintű üzenet logolása.

        Ez a metódus általános információkat logol az alkalmazás működéséről.

        Args:
            message: A logolandó info üzenet.
            **kwargs: További paraméterek az extra adatokhoz.

        Példa:
            >>> logger.info("Sikeres bejelentkezés", user="admin")

### `warning`

Warning szintű üzenet logolása.

        Ez a metódus figyelmeztető üzeneteket logol, amelyek nem kritikusak,
        de érdemes rájuk figyelni.

        Args:
            message: A logolandó warning üzenet.
            **kwargs: További paraméterek az extra adatokhoz.

        Példa:
            >>> logger.warning("A cache majdnem tele van", usage=85)

### `error`

Error szintű üzenet logolása.

        Ez a metódus hibákat logol, amelyek befolyásolják az alkalmazás
        működését, de nem okoznak leállást.

        Args:
            message: A logolandó error üzenet.
            **kwargs: További paraméterek az extra adatokhoz.

        Példa:
            >>> logger.error("Adatbázis kapcsolódási hiba", error=str(e))

### `critical`

Critical szintű üzenet logolása.

        Ez a metódus kritikus hibákat logol, amelyek az alkalmazás leállását
        okozhatják vagy jelentős problémát jeleznek.

        Args:
            message: A logolandó critical üzenet.
            **kwargs: További paraméterek az extra adatokhoz.

        Példa:
            >>> logger.critical("A rendszer leállt", reason="Nincs elég memória")

### `set_level`

Logger log szintjének beállítása.

        Ez a metódus lehetővé teszi a log szint dinamikus módosítását futás közben.

        Args:
            level: Az új log szint (pl. logging.DEBUG, logging.INFO,
                logging.WARNING, logging.ERROR, logging.CRITICAL).

        Példa:
            >>> logger.set_level(logging.DEBUG)

### `get_level`

Aktuális log szint lekérése.

        Returns:
            int: Az aktuális log szint numerikus értéke.

        Példa:
            >>> current_level = logger.get_level()
            >>> print(f"Aktuális log szint: {current_level}")


---

**Forrásfájl:** [`core/logger/implementations/colored_logger.py`](../../../neural_ai/core/logger/implementations/colored_logger.py)
