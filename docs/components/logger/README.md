# Neural AI - Logger Komponens

## Áttekintés

A Logger komponens a Neural AI Next rendszer központi naplózó rendszere. Biztosítja a különböző szintű és formátumú naplózást, támogatja a fájl és konzol alapú naplózást, valamint a naplófájlok automatikus kezelését.

## Főbb funkciók

- Többszintű naplózás (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Színes konzol kimenet a jobb olvashatóságért
- Fájl alapú naplózás rotációs támogatással
- Méret és idő alapú log rotáció
- Automatikus log tömörítés
- Strukturált naplózás
- Testreszabható formátumok
- Többszintű konfiguráció

## Telepítés és függőségek

A komponens a Neural AI keretrendszer részeként települ.

### Függőségek
- colorama: Színes konzol kimenet Windows rendszereken (opcionális)
- gzip: Log fájl tömörítés (beépített)

## Használat

### 1. Alap használat

```python
from neural_ai.core.logger.implementations import LoggerFactory

# Alapértelmezett logger
logger = LoggerFactory.get_logger(__name__)

# Naplózás különböző szinteken
logger.debug("Részletes diagnosztikai információ")
logger.info("Általános információs üzenet")
logger.warning("Figyelmeztetés - nem kritikus hiba")
logger.error("Hiba - művelet sikertelen")
logger.critical("Kritikus hiba - alkalmazás leállhat")
```

### 2. Színes konzol logger

```python
# Színes kimenettel
logger = LoggerFactory.get_logger(
    __name__,
    logger_type="colored",
    colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white"
    }
)
```

### 3. Rotáló fájl logger

```python
# Méret alapú rotációval
logger = LoggerFactory.get_logger(
    __name__,
    logger_type="rotating_file",
    filename="logs/app.log",
    max_bytes=1024*1024,  # 1MB
    backup_count=5,
    compress=True
)
```

## Architektúra

A komponens felépítése:

```
neural_ai/core/logger/
├── interfaces/
│   ├── logger_interface.py    # Alap logger interfész
│   └── factory_interface.py   # Logger factory interfész
├── implementations/
│   ├── default_logger.py      # Alapértelmezett logger
│   ├── colored_logger.py      # Színes konzol logger
│   ├── rotating_logger.py     # Rotáló fájl logger
│   └── logger_factory.py      # Logger gyártó osztály
├── formatters/
│   └── logger_formatters.py   # Formázó osztályok
└── exceptions.py              # Logger kivételek
```

### Főbb osztályok

1. **LoggerInterface**
   - Alap naplózási műveletek
   - Konzisztens API minden implementációhoz

2. **DefaultLogger, ColoredLogger, RotatingFileLogger**
   - Specifikus naplózási implementációk
   - Különböző output formátumok és célok

3. **LoggerFactory**
   - Logger példányok létrehozása
   - Konfiguráció kezelés
   - Singleton példányok cache-elése

## API gyorsreferencia

```python
# Logger létrehozása
logger = LoggerFactory.get_logger(__name__)

# Naplózási szintek
logger.debug(message, **kwargs)
logger.info(message, **kwargs)
logger.warning(message, **kwargs)
logger.error(message, **kwargs)
logger.critical(message, **kwargs)

# Kivétel naplózása
try:
    raise ValueError("Hiba")
except Exception as e:
    logger.exception("Kivétel történt")
```

## Fejlesztői információk

### Új logger implementálása

1. Implementálja a `LoggerInterface`-t
2. Regisztrálja a logger típust a factory-ban:

```python
LoggerFactory.register_logger("custom", MyCustomLogger)
```

### Színkódok testreszabása

```python
COLORS = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red,bg_white"
}
```

## Tesztelés

```bash
# Unit tesztek futtatása
pytest tests/core/logger/

# Lefedettség ellenőrzése
pytest --cov=neural_ai.core.logger tests/core/logger/
```

## Közreműködés

1. Fork létrehozása
2. Feature branch létrehozása (`git checkout -b feature/új_logger`)
3. Változtatások commit-olása (`git commit -am 'Új logger: xyz'`)
4. Branch feltöltése (`git push origin feature/új_logger`)
5. Pull Request nyitása

## Licensz

MIT License - lásd a LICENSE fájlt a részletekért.

## További dokumentáció

- [API Dokumentáció](api.md)
- [Architektúra leírás](architecture.md)
- [Tervezési specifikáció](design_spec.md)
- [Példák](examples.md)
- [Fejlesztési checklist](development_checklist.md)
