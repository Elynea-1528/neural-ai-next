# Code Mód Szabályai (Csak Nem-Nyilvánvaló Tudás)

## Factory Pattern Követelmények

**TypedDict cast kötelező factory-kban:** A `config.get()` `Any`-t ad vissza, factory-knak KÖTELEZŐ TypedDict-re castolni:
```python
from typing import TypedDict, cast
class JForexConfig(TypedDict, total=False):
    base_url: str
    timeout: int
raw = config.get("jforex")
typed_cfg = cast(JForexConfig, raw if isinstance(raw, dict) else {})
```

**Lazy loading csak factory-ban:** Konkrét implementációk importálása CSAK factory `_lazy_load_implementations()` vagy factory metódusaiban. Soha nem `__init__.py`-ban vagy más modulokban.

**Factory DI-vel hoz létre:** Minden komponens konstruktor megkapja a függőségeket (logger, config, event_bus) - soha nem példányosítják magukat.

## Import Szabályok

**Körkörös import megoldás:** Használd az `if TYPE_CHECKING:` blokkot típus hintekhez, string annotációval runtime-ban:
```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from neural_ai.data.storage.interfaces import StorageInterface

def __init__(self, storage: "StorageInterface"):
    self.storage = storage
```

**Réteg szabálysértés detektálás:** `neural_ai/processors` NEM importálhat `neural_ai/ui`-ból. `neural_ai/data` NEM importálhat `neural_ai/processors` vagy `neural_ai/ui`-ból. Ellenőrizd `docs/development/architecture_standards.md:28-41` réteg hierarchiát.

## Adatkezelés

**Polars kötelező feldolgozáshoz:** Használj `pl.DataFrame`-et `neural_ai/processors/` és `neural_ai/data/`-ban. Pandas CSAK `neural_ai/ui/`-ban megjelenítéshez. `for row in df` iteráció TILOS - használj `pl.Expr` vektorizált műveleteket.

**JForex csak bináris:** TILOS CSV olvasása/írása `neural_ai/collectors/jforex/`-ban. Csak `.bi5` LZMA formátum `implementations/bi5_downloader.py`-on keresztül.

**Storage csak Parquet:** TILOS CSV/JSON használata `neural_ai/data/storage/`-ban. Csak particionált Parquet `fastparquet` backend-del.

## Logolás

**Strukturált logolás kikényszerítve:** SOHA ne használj f-stringeket log üzenetekben. Használd az `extra` dict-et:
```python
# ROSSZ: logger.info(f"Feldolgozva {count} sor {symbol}-hoz")
# JÓ: logger.info("Feldolgozás kész", extra={"rows": count, "symbol": symbol})
```

**Nincs print utasítás:** `print()` TILOS `neural_ai/`-ban (kivéve `if __name__ == "__main__"` CLI blokkokban).

## Modul Struktúra

**Mirror dokumentáció kötelező:** `neural_ai/X/Y/Z.py` létrehozása/módosítása igényli `docs/components/X/Y/Z.md` létrehozását/frissítését. Futtasd `python scripts/generate_docs.py` változtatások után.

**__init__.py csak Interface + Factory exportálása:** Implementációk SOHA nem exportáltak. Minta:
```python
# neural_ai/data/storage/__init__.py
from .factory import StorageFactory
from .interfaces import StorageInterface
__all__ = ['StorageFactory', 'StorageInterface']
```

## Tesztelés

**Abszolút útvonalak tesztekben:** Használd `/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest` - `conda activate` nem működik nem-interaktív shell-ekben.

**Mirror teszt struktúra:** `neural_ai/processors/dimensions/d01_price/processor.py` → `tests/processors/dimensions/d01_price/test_processor.py`
