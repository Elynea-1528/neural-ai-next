# core/logger/factory.py

Logger factory implementáció structlog használatával.

Ez a modul biztosítja a LoggerFactory osztályt, amely felelős a különböző
típusú loggerek létrehozásáért és kezeléséért. A factory mintát követve
lehetővé teszi a dinamikus logger típusok regisztrálását és példányosítását.

A factory kizárólag structlog renderereket használ:
- Console: structlog.dev.ConsoleRenderer(colors=True)
- File: structlog.processors.JSONRenderer()

## Osztályok

### `LoggerFactory`

Factory osztály loggerek létrehozásához structlog-gal.

    A factory mintát követve centralizálja a logger példányosítást és
    életciklus kezelést. Támogatja a különböző logger implementációk
    regisztrálását és lekérdezését.

    A configure metódus kizárólag structlog renderereket használ:
    - Console: structlog.dev.ConsoleRenderer(colors=True)
    - File: structlog.processors.JSONRenderer()

    Attributes:
        _logger_types: Regisztrált logger típusok és osztályaik.
        _instances: Létrehozott logger példányok gyorsítótárban.


## Függvények

### `register_logger`

Új logger típus regisztrálása.

        Args:
            logger_type: A logger típus neve.
            logger_class: A logger osztály.

        Raises:
            TypeError: Ha a logger_class nem implementálja a LoggerInterface-t.

### `get_logger`

Logger példány létrehozása vagy visszaadása.

        Args:
            name: A logger egyedi neve.
            logger_type: A kért logger típus ('default', 'colored', 'rotating').
            **kwargs: További paraméterek a loggernek (pl. log_file, level).

        Returns:
            LoggerInterface: Az inicializált logger példány.

        Raises:
            ValueError: Ha a 'rotating' típushoz nincs megadva 'log_file'.
            TypeError: Ha a létrehozott logger nem implementálja az interfészt.

        Példa:
            >>> logger = LoggerFactory.get_logger("my_app")
            >>> colored = LoggerFactory.get_logger("app", logger_type="colored")
            >>> file_logger = LoggerFactory.get_logger(
            ...     "file_app",
            ...     logger_type="rotating",
            ...     log_file="/var/log/app.log"
            ... )

### `configure`

Logger rendszer konfigurálása structlog-gal.

        A metódus kizárólag structlog renderereket használ:
        - Console: structlog.dev.ConsoleRenderer(colors=True)
        - File: structlog.processors.JSONRenderer()

        Args:
            config: Konfigurációs dict a következő struktúrával:
                {
                    'default_level': 'DEBUG',
                    'handlers': {
                        'console': {
                            'enabled': True,
                            'level': 'DEBUG',
                            'colored': True
                        },
                        'file': {
                            'enabled': True,
                            'filename': 'logs/neural_ai.log',
                            'level': 'DEBUG',
                            'json_format': True,
                            'rotating': True,
                            'max_bytes': 10485760,
                            'backup_count': 5
                        }
                    },
                    'loggers': {
                        'neural_ai': {'level': 'DEBUG', 'propagate': True},
                        'aiosqlite': {'level': 'WARNING'},
                        'asyncio': {'level': 'WARNING'}
                    }
                }

### `get_schema_version`

A logger factory sémaváltozatának lekérdezése.

        Returns:
            str: A sémaváltozat string formátumban (pl. '1.0.0').

### `set_schema_version`

A logger factory sémaváltozatának beállítása.

        Args:
            version: Az új sémaváltozat (pl. '1.1.0').

### `clear_instances`

Összes logger példány törlése a gyorsítótárból.

        Ez a metódus hasznos teszteléskor vagy amikor teljesen
        új logger példányokat szeretnénk létrehozni.

### `get_registered_types`

Regisztrált logger típusok listázása.

        Returns:
            list[str]: A regisztrált logger típusok neveinek listája.

### `is_logger_registered`

Ellenőrzi, hogy egy logger típus regisztrálva van-e.

        Args:
            logger_type: A logger típus neve.

        Returns:
            bool: True, ha a logger típus regisztrálva van, egyébként False.


---

**Forrásfájl:** [`core/logger/factory.py`](../../../neural_ai/core/logger/factory.py)
