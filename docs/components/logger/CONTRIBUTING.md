# Fejlesztői Útmutató

Ez az útmutató a logger komponens fejlesztéséhez és bővítéséhez nyújt segítséget.

## Fejlesztési Környezet Beállítása

1. Python környezet létrehozása:
```bash
conda env create -f environment.yml
conda activate neural-ai-next
```

2. Függőségek telepítése:
```bash
pip install -e ".[dev]"
```

3. Pre-commit hooks beállítása:
```bash
pre-commit install
```

## Kódolási Konvenciók

### Általános Irányelvek

- PEP 8 követése
- Típus annotációk használata
- Docstringek minden publikus elemhez
- SOLID elvek betartása
- Tiszta kód elvek alkalmazása

### Importálási Sorrend

1. Standard library
2. Külső függőségek
3. Belső modulok

```python
import logging
from typing import Optional

from external_lib import something

from neural_ai.core.logger import interfaces
```

### Formázás

- Black formázó használata
- 100 karakteres sorhossz
- Következetes idézőjel használat (dupla)

## Új Logger Implementáció Készítése

1. Interfész implementálása:
```python
from neural_ai.core.logger.interfaces import LoggerInterface

class MyLogger(LoggerInterface):
    def __init__(self, name: str) -> None:
        self._logger = logging.getLogger(name)

    def debug(self, message: str, **kwargs: Any) -> None:
        self._logger.debug(message, extra=kwargs)

    # ... további metódusok implementálása
```

2. Tesztek írása:
```python
class TestMyLogger:
    def test_initialization(self) -> None:
        logger = MyLogger("test")
        assert isinstance(logger, LoggerInterface)
```

## Tesztelés

### Unit Tesztek Futtatása

```bash
pytest tests/core/logger/
```

### Lefedettség Ellenőrzése

```bash
pytest --cov=neural_ai/core/logger tests/core/logger/
```

### Lint Ellenőrzések

```bash
flake8 neural_ai/core/logger/
pylint neural_ai/core/logger/
mypy neural_ai/core/logger/
```

## Pull Request Folyamat

1. Feature branch létrehozása:
```bash
git checkout -b feature/my-logger-implementation
```

2. Commit konvenciók:
```
feat(logger): add új logger implementáció
fix(logger): hibajavítás
docs(logger): dokumentáció frissítése
```

3. PR készítése
   - Leírás a változtatásokról
   - Tesztek sikerességének igazolása
   - Dokumentáció frissítése
   - Code review kérése

## Dokumentáció

### Dokumentáció Frissítése

1. API dokumentáció:
   - Új típusok dokumentálása
   - Példák hozzáadása
   - Paraméterek leírása

2. Technikai specifikáció:
   - Architekturális döntések
   - Teljesítmény megfontolások
   - Biztonsági szempontok

3. README:
   - Használati példák
   - Konfigurációs opciók
   - Hibaelhárítási tippek

## Tippek és Trükkök

### Debugging

1. Debug logolás engedélyezése:
```python
logging.getLogger().setLevel(logging.DEBUG)
```

2. Handler vizsgálata:
```python
logger = logging.getLogger("my_logger")
print(logger.handlers)  # Aktív handlerek listázása
```

### Gyakori Problémák

1. Duplikált logok:
   ```python
   logger.propagate = False  # Propagáció kikapcsolása
   ```

2. Handler tisztítás:
   ```python
   logger.handlers.clear()  # Minden handler eltávolítása
   ```

## Teljesítmény Optimalizálás

1. Lazy értékelés használata:
```python
if logger.isEnabledFor(logging.DEBUG):
    logger.debug(expensive_operation())
```

2. Batch műveletek:
```python
with open(log_file, "a") as f:
    for record in records:
        f.write(format_record(record))
```

## Biztonsági Megfontolások

1. Fájl jogosultságok:
```python
os.chmod(log_file, 0o600)  # Csak tulajdonos olvasás/írás
```

2. Szenzitív adatok kezelése:
```python
def mask_sensitive_data(data: str) -> str:
    return re.sub(r"password=\w+", "password=***", data)
```

## Kapcsolat

- Issue tracker: GitHub Issues
- Code review: Pull Requests
- Kérdések: Discussions fórum