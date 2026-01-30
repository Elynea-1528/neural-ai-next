# Debug Mód Szabályai (Csak Nem-Nyilvánvaló Tudás)

## Teszt Végrehajtás

**Abszolút útvonal szükséges:** `/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest` - `conda activate` nem működik nem-interaktív shell-ekben.

**Egyetlen teszt fájl:** `/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/path/to/test_file.py -v`

## Gyakori Hiba Minták

**TypedDict hiányzik factory-kban:** Ha `config.get()` típus hibát okoz, ellenőrizd a factory metódusokat - KÖTELEZŐ TypedDict-re castolni:
```python
# Keresd ezt a mintát factory-kban (pl. neural_ai/core/base/factory.py:220-235)
from typing import cast, TypedDict
class MyConfig(TypedDict, total=False):
    key: str
typed = cast(MyConfig, config.get("section") or {})
```

**Körkörös import hibák:** Adj hozzá `if TYPE_CHECKING:` blokkot + string típus hinteket:
```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from neural_ai.module.interfaces import MyInterface
def method(self, param: "MyInterface"):  # String annotáció
    pass
```

**Import az implementations/-ból sikertelen:** Konkrét osztályokat CSAK factory-k lazy load metódusaiban vagy factory metódusokban szabad importálni - soha nem normál kódban.

## Réteg Szabálysértés Debugging

**Import hierarchia:** Ha import sikertelen, ellenőrizd a réteg sorrendet (lásd `docs/development/architecture_standards.md:28-41`):
- `neural_ai/ui` → importálhat processors, data, core-ból
- `neural_ai/processors` → importálhat data, core-ból (NEM ui)
- `neural_ai/data` → importálhat csak core-ból (NEM processors, ui)
- `neural_ai/collectors` → importálhat csak core-ból
- `neural_ai/core` → önálló (nincs függősége)

**Bootstrap sorrend számít:** Komponens init hibák gyakran rossz sorrend miatt. Helyes: HardwareInfo → ConfigManager → Logger → EventBus → Storage → Database → SystemMonitor (lásd `neural_ai/core/base/factory.py:120-147`).

## Adatfeldolgozási Hibák

**Polars vs Pandas összekeverés:** Ha `AttributeError` DataFrame-en, ellenőrizd hogy a kód Pandas szintaxist használ-e Polars DF-en. Polars csak `processors/` és `data/`-ban, Pandas csak `ui/`-ban.

**Sor iteráció teljesítmény:** Ha tesztek timeout-olnak, ellenőrizd `for row in df` használatát - ez TILOS. Használj vektorizált `pl.Expr` műveleteket.

## Logolási Hibák

**Strukturált logolás validálás:** Ha `TypeError` logger hívásnál, ellenőrizd f-stringeket az üzenetben:
```python
# ROSSZ: logger.info(f"Érték: {val}")
# JÓ: logger.info("Üzenet", extra={"value": val})
```

## Storage/Perzisztencia Problémák

**JForex formátum kikényszerítés:** Ha collector sikertelen, ellenőrizd hogy `.bi5` bináris formátumot használ, nem CSV-t (lásd `neural_ai/collectors/jforex/implementations/bi5_downloader.py`).

**Storage formátum ellenőrzés:** Ha storage sikertelen, biztosítsd hogy Parquet formátumot használ (nem CSV/JSON) `neural_ai/data/storage/implementations/`-ban.
