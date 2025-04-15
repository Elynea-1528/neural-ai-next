# Fejlesztői Útmutató - Konfiguráció Kezelő

Ez az útmutató a konfiguráció kezelő komponens fejlesztéséhez és bővítéséhez nyújt segítséget.

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
import os
from typing import Dict, Any

import yaml

from neural_ai.core.config.interfaces import ConfigManagerInterface
```

### Docstring Formátum

```python
def method(self, param: str) -> bool:
    """Rövid leírás.

    Részletes leírás, ha szükséges.

    Args:
        param: A paraméter leírása

    Returns:
        bool: A visszatérési érték leírása

    Raises:
        ValueError: Kivétel dobásának körülményei
    """
    pass
```

## Új Konfiguráció Kezelő Implementálása

1. Interfész implementálása:
```python
from neural_ai.core.config.interfaces import ConfigManagerInterface

class MyConfigManager(ConfigManagerInterface):
    def __init__(self, filename: Optional[str] = None) -> None:
        self._config: Dict[str, Any] = {}
        if filename:
            self.load(filename)

    def get(self, *keys: str, default: Any = None) -> Any:
        # Implementáció...
        pass

    # További metódusok implementálása...
```

2. Factory-nál regisztrálás:
```python
from neural_ai.core.config.implementations import ConfigManagerFactory

ConfigManagerFactory.register_manager(".mycfg", MyConfigManager)
```

3. Tesztek írása:
```python
class TestMyConfigManager:
    @pytest.fixture
    def config_manager(self) -> MyConfigManager:
        return MyConfigManager()

    def test_load_config(self, config_manager: MyConfigManager) -> None:
        # Teszt implementáció...
        pass
```

## Séma Validáció Bővítése

### Új Validációs Szabály Hozzáadása

```python
class CustomValidator:
    def __init__(self, param: Any) -> None:
        self.param = param

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        # Validációs logika...
        return True, None

# Használat a sémában
schema = {
    "field": {
        "validator": CustomValidator(param)
    }
}
```

### Validátor Regisztrálása

```python
from neural_ai.core.config.validation import register_validator

@register_validator("custom")
def custom_validator(value: Any, **kwargs: Any) -> bool:
    # Validációs logika...
    return True
```

## Tesztelés

### Unit Tesztek Futtatása

```bash
# Összes teszt
pytest tests/core/config/

# Konkrét teszt fájl
pytest tests/core/config/test_my_config.py

# Lefedettség ellenőrzése
pytest --cov=neural_ai/core/config tests/core/config/
```

### Tesztelési Irányelvek

1. Minden publikus metódushoz teszt
2. Edge case-ek tesztelése
3. Kivételek tesztelése
4. Mock objektumok használata I/O műveleteknél

## Dokumentáció

### Dokumentáció Frissítése

1. API dokumentáció generálása:
```bash
pdoc --html neural_ai/core/config/
```

2. README.md frissítése új funkciókkal
3. Változási napló aktualizálása
4. Technikai specifikáció kiegészítése

### Példakódok

1. Példakódok a docs/examples mappába
2. Doctest-ek a dokumentációban
3. Jupyter notebook tutorialok

## Teljesítmény Optimalizálás

### Profilozás

```python
import cProfile
import pstats

with cProfile.Profile() as pr:
    # Kód amit profilozni szeretnénk
    pass

stats = pstats.Stats(pr)
stats.sort_stats('cumulative')
stats.print_stats()
```

### Memória Használat

```python
from memory_profiler import profile

@profile
def memory_intensive_operation():
    # Művelet
    pass
```

## Hibaelhárítás

### Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Config state: %s", self._config)
```

### Common Issues

1. YAML parsing hibák
2. Fájl hozzáférési problémák
3. Validációs hibák

## Code Review

### Pull Request Checklist

- [ ] Kód megfelel a konvencióknak
- [ ] Tesztek lefutnak és átmennek
- [ ] Dokumentáció frissítve
- [ ] Változási napló aktualizálva
- [ ] Példakódok tesztelve
- [ ] Teljesítmény ellenőrizve

## Kapcsolat

- Issue tracker: GitHub Issues
- Code review: Pull Requests
- Kérdések: Discussions fórum