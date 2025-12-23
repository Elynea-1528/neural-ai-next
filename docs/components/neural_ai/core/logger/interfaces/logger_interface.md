# LoggerInterface

## Áttekintés

A `LoggerInterface` egy absztrakt alaposztály, amely definiálja a naplózási rendszer alapvető műveleteit. Ez az interfész biztosítja a konzisztens naplózási viselkedést az összes logger implementációban.

## Cél

Az interfész célja, hogy:
- Egységes naplózási API-t biztosítson a teljes rendszer számára
- Lehetővé tegye a különböző logger implementációk egyszerű cserélhetőségét
- Támogassa a konfiguráció alapú inicializálást
- Biztosítsa a típusbiztonságot a naplózási műveletekhez

## Osztály Struktúra

```python
class LoggerInterface(ABC):
    """Logger interfész a naplózási műveletek absztrakt definíciójához."""
```

## Metódusok

### `__init__`

```python
def __init__(
    self,
    name: str,
    config: Optional['ConfigManagerInterface'] = None,
    **kwargs: Mapping[str, AnyStr]
) -> None
```

**Paraméterek:**
- `name` (str): A logger egyedi azonosítója
- `config` (Optional[ConfigManagerInterface]): Opcionális konfigurációs interfész
- `**kwargs` (Mapping[str, AnyStr]): További opcionális paraméterek

**Leírás:**
Inicializálja a logger példányt. A konfigurációs interfész lehetővé teszi a logger beállításainak dinamikus kezelését.

---

### `debug`

```python
def debug(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None
```

**Paraméterek:**
- `message` (str): A naplózandó üzenet szövege
- `**kwargs` (Mapping[str, AnyStr]): További kontextusparaméterek

**Leírás:**
Debug szintű üzenet naplózása. Részletes hibakeresési információk naplózására szolgál, amelyek általában csak fejlesztés közben relevánsak.

---

### `info`

```python
def info(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None
```

**Paraméterek:**
- `message` (str): A naplózandó üzenet szövege
- `**kwargs` (Mapping[str, AnyStr]): További kontextusparaméterek

**Leírás:**
Információs szintű üzenet naplózása. Általános információk naplózására szolgál, amelyek a rendszer normál működéséről adnak tájékoztatást.

---

### `warning`

```python
def warning(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None
```

**Paraméterek:**
- `message` (str): A naplózandó üzenet szövege
- `**kwargs` (Mapping[str, AnyStr]): További kontextusparaméterek

**Leírás:**
Figyelmeztető szintű üzenet naplózása. Olyan helyzetek naplózására szolgál, amelyek nem kritikusak, de figyelmet igényelnek.

---

### `error`

```python
def error(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None
```

**Paraméterek:**
- `message` (str): A naplózandó üzenet szövege
- `**kwargs` (Mapping[str, AnyStr]): További kontextusparaméterek

**Leírás:**
Hiba szintű üzenet naplózása. Hibák naplózására szolgál, amelyek befolyásolják a rendszer működését, de nem okoznak alkalmazásleállást.

---

### `critical`

```python
def critical(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None
```

**Paraméterek:**
- `message` (str): A naplózandó üzenet szövege
- `**kwargs` (Mapping[str, AnyStr]): További kontextusparaméterek

**Leírás:**
Kritikus szintű üzenet naplózása. Súlyos hibák naplózására szolgál, amelyek alkalmazásleállást okozhatnak.

---

### `set_level`

```python
def set_level(self, level: int) -> None
```

**Paraméterek:**
- `level` (int): Az új naplózási szint (0-50 közötti egész szám)

**Leírás:**
Beállítja a minimális naplózási szintet. A szintnél alacsonyabb prioritású üzenetek nem lesznek naplózva.

---

### `get_level`

```python
def get_level(self) -> int
```

**Visszatérési érték:**
- `int`: A jelenleg beállított naplózási szint értéke

**Leírás:**
Aktuális naplózási szint lekérdezése.

## Használati Példák

### Alap inicializálás

```python
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

class MyLogger(LoggerInterface):
    def __init__(self, name: str, config=None, **kwargs):
        super().__init__(name, config, **kwargs)
        # Implementáció
    
    # További metódusok implementációja...
```

### Konfigurációval történő inicializálás

```python
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface

class ConfigurableLogger(LoggerInterface):
    def __init__(self, name: str, config: ConfigManagerInterface, **kwargs):
        super().__init__(name, config, **kwargs)
        level = config.get("log_level", default="INFO")
        # Logger konfigurálása
```

### Naplózási műveletek

```python
logger = MyLogger(name="my_app")

# Különböző szinteken történő naplózás
logger.debug("Részletes hibakeresési információ")
logger.info("Alkalmazás elindult")
logger.warning("Figyelmeztetés: erőforrás szűkös")
logger.error("Adatbázis kapcsolati hiba")
logger.critical("Kritikus hiba: alkalmazás leáll")

# Szint beállítása
logger.set_level(20)
current_level = logger.get_level()
```

## Implementációs Javaslatok

1. **Konfiguráció kezelés:** Használd a `config` paramétert a logger beállításainak kezelésére
2. **Típusbiztonság:** Minden metódusnak típusozott paramétereket kell fogadnia
3. **Hibakezelés:** Implementáld a hibák megfelelő kezelését a naplózási műveletek során
4. **Teljesítmény:** A naplózási műveleteknek hatékonyaknak kell lenniük

## Kapcsolódó Komponensek

- [`ConfigManagerInterface`](../config/interfaces/config_interface.md): Konfiguráció kezelés
- [`LoggerFactory`](../implementations/logger_factory.md): Logger példányok létrehozása
- [`DefaultLogger`](../implementations/default_logger.md): Alapértelmezett logger implementáció

## Verzió Történet

- **1.0.0**: Kezdeti verzió - alap naplózási interfész definíció