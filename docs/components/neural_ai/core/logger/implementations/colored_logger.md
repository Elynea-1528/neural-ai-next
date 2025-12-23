# ColoredLogger

## Áttekintés

A `ColoredLogger` egy színes konzol kimenetet biztosító logger implementáció, amely a Python standard `logging` könyvtárát használja, és színes formázást alkalmaz a log üzenetekhez.

## Osztály

```python
class ColoredLogger(LoggerInterface)
```

## Jellemzők

- **Színes kimenet**: A log üzenetek színesek a konzolon a log szinttől függően
- **Testre szabható**: Egyéni log szint, formátum és stream használata
- **Handler kezelés**: Automatikusan eltávolítja a meglévő handlereket
- **Nincs propagáció**: A log üzenetek nem propagálódnak a szülő logger-ekhez

## Inicializálás

### Alapértelmezett inicializálás

```python
logger = ColoredLogger("my_logger")
```

### Egyéni beállításokkal

```python
logger = ColoredLogger(
    name="my_logger",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
```

## Paraméterek

| Paraméter | Típus | Leírás | Alapértelmezett |
|-----------|-------|--------|-----------------|
| `name` | `str` | A logger neve | Kötelező |
| `level` | `int` | Log szint (DEBUG, INFO, WARNING, ERROR, CRITICAL) | `logging.INFO` |
| `format` | `str` | Log formátum string | `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"` |
| `stream` | `IO[str]` | Kimeneti stream | `sys.stdout` |

## Metódusok

### debug(message, **kwargs)

Debug szintű üzenet logolása.

**Paraméterek:**
- `message` (`str`): A log üzenet
- `**kwargs`: További paraméterek az extra adatokhoz

**Példa:**
```python
logger.debug("Ez egy debug üzenet", user_id=123)
```

### info(message, **kwargs)

Info szintű üzenet logolása.

**Paraméterek:**
- `message` (`str`): A log üzenet
- `**kwargs`: További paraméterek az extra adatokhoz

**Példa:**
```python
logger.info("Sikeres kapcsolódás", host="localhost")
```

### warning(message, **kwargs)

Warning szintű üzenet logolása.

**Paraméterek:**
- `message` (`str`): A log üzenet
- `**kwargs`: További paraméterek az extra adatokhoz

**Példa:**
```python
logger.warning("A cache majdnem tele van", usage=85)
```

### error(message, **kwargs)

Error szintű üzenet logolása.

**Paraméterek:**
- `message` (`str`): A log üzenet
- `**kwargs`: További paraméterek az extra adatokhoz

**Példa:**
```python
logger.error("Adatbázis kapcsolódási hiba", error=str(e))
```

### critical(message, **kwargs)

Critical szintű üzenet logolása.

**Paraméterek:**
- `message` (`str`): A log üzenet
- `**kwargs`: További paraméterek az extra adatokhoz

**Példa:**
```python
logger.critical("A rendszer leállt", reason="Nincs elég memória")
```

### set_level(level)

Logger log szintjének beállítása.

**Paraméterek:**
- `level` (`int`): Az új log szint

**Példa:**
```python
logger.set_level(logging.DEBUG)
```

### get_level()

Aktuális log szint lekérése.

**Visszatérési érték:**
- `int`: Az aktuális log szint

**Példa:**
```python
current_level = logger.get_level()
```

## Használati példák

### Egyszerű használat

```python
from neural_ai.core.logger.implementations.colored_logger import ColoredLogger
import logging

# Logger létrehozása
logger = ColoredLogger("my_application")

# Különböző szintű üzenetek logolása
logger.debug("Részletes debug információ")
logger.info("Alkalmazás elindult")
logger.warning("Figyelmeztetés: a beállítás nem található")
logger.error("Hiba történt a feldolgozás során")
logger.critical("Kritikus hiba: a rendszer leáll")
```

### Egyéni streammel

```python
from io import StringIO

# StringIO stream használata
stream = StringIO()
logger = ColoredLogger("test_logger", stream=stream)

logger.info("Teszt üzenet")
print(stream.getvalue())  # Kiírja a logot
```

### Fájlba logolás

```python
# Fájl stream használata
with open("app.log", "w") as f:
    logger = ColoredLogger("file_logger", stream=f)
    logger.info("Ez a fájlba kerül")
```

### Log szint módosítása

```python
# Alapértelmezett INFO szint
logger = ColoredLogger("app")

# DEBUG szintre állítás
logger.set_level(logging.DEBUG)

# Szint lekérdezése
level = logger.get_level()
print(f"Aktuális log szint: {level}")
```

## Függőségek

- `logging`: Python standard logging könyvtár
- `sys`: Rendszer-specifikus paraméterek és függvények
- `ColoredFormatter`: Színes formázó a log üzenetekhez
- `LoggerInterface`: Logger interfész definíció

## Megjegyzések

- A logger automatikusan eltávolítja a meglévő handlereket inicializáláskor
- A log üzenetek nem propagálódnak a szülő logger-ekhez
- A ColoredFormatter automatikusan alkalmazza a megfelelő színeket a log szint alapján
- Ha DEBUG szint van beállítva, a root logger szintje is DEBUG-ra állíródik

## Hibakezelés

A `ColoredLogger` robusztus hibakezeléssel rendelkezik:
- Érvénytelen log szint esetén a logger továbbra is működik
- Ha a stream nem érhető el, a logger kivételt dob
- Extra paraméterek hiánya esetén a logger normálisan működik

## Lásd még

- [`LoggerInterface`](../interfaces/logger_interface.md): Logger interfész
- [`ColoredFormatter`](../formatters/logger_formatters.md): Színes formázó
- [`DefaultLogger`](default_logger.md): Alapértelmezett logger implementáció
- [`RotatingFileLogger`](rotating_file_logger.md): Forgatófájl logger