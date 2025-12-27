# Dekorátorok - `neural_ai.core.utils.decorators`

## Áttekintés

Ez a modul a Neural AI Next rendszer funkcionális dekorátorait tartalmazza. A dekorátorok segítségével lehetőség van a függvények viselkedésének módosítására anélkül, hogy magát a függvényt módosítani kellene.

## Tartalom

### `@trace` Dekorátor

A `@trace` dekorátor automatikusan logolja a függvényhívásokat, beleértve a hívás azonosítóját, a függvény nevét, az argumentumokat és a futási időt.

#### Jellemzők

- **Logger**: `structlog.get_logger("neural_ai.trace")`
- **Log szint**: DEBUG
- **Logolt információk**:
  - `call_id`: Egyedi UUID4 azonosító
  - `function`: A hívott függvény neve
  - `args`: A pozicionális argumentumok biztonságos reprezentációja
  - `kwargs`: A kulcsszavas argumentumok biztonságos reprezentációja
  - `duration_ms`: Futási idő milliszekundumban

#### Biztonságos Argumentum Szerializálás

A dekorátor csak biztonságos típusokat logol közvetlenül:
- `str`: Szöveges adatok
- `int`: Egész számok
- `float`: Lebegőpontos számok
- `bool`: Logikai értékek
- `None`: Nincs érték

Minden egyéb típus esetén az argumentum értéke "UNSAFE_ARG" lesz, hogy elkerüljük a bizalmas adatok véletlen kiírását.

#### Használat

```python
from neural_ai.core.utils.decorators import trace

@trace
def add_numbers(a: int, b: int) -> int:
    """Két szám összeadása."""
    return a + b

@trace
def process_data(data: str, threshold: float = 0.5) -> bool:
    """Adatok feldolgozása."""
    return len(data) > int(threshold * 100)
```

#### Log Output

```
call_id=123e4567-e89b-12d3-a456-426614174000 
function=add_numbers 
args=['5', '3'] 
kwargs={} 
duration_ms=0.123
```

#### Hibakezelés

A dekorátor hibák esetén is logolja a hívás információit, és tartalmazza a hibaüzenetet is:

```
call_id=123e4567-e89b-12d3-a456-426614174000 
function=process_data 
args=['test_data'] 
kwargs={'threshold': '0.8'} 
duration_ms=1.456 
error="ValueError: Invalid threshold value"
```

## Implementáció

### `_serialize_arg(arg: Any) -> str`

Segédfüggvény egy argumentum biztonságos szöveges reprezentációjának létrehozásához.

**Paraméterek:**
- `arg`: A konvertálandó argumentum

**Visszatérési érték:**
- Az argumentum szöveges reprezentációja, vagy "UNSAFE_ARG"

### `trace(func: F) -> F`

Fő dekorátor függvény a funkcióhívások nyomon követéséhez.

**Paraméterek:**
- `func`: A dekorálandó függvény

**Visszatérési érték:**
- A dekorált függvény, amely automatikusan logolja a hívásokat

## Függőségek

- `time`: Futási idő méréséhez
- `uuid`: Egyedi hívásazonosítók generálásához
- `structlog`: Strukturált logoláshoz
- `functools.wraps`: A dekorált függvény metaadatok megőrzéséhez

## Teljesítmény

A dekorátor minimalizálja a teljesítménybeli hatást:
- Gyors argumentum ellenőrzés
- Hatékony időmérés `time.perf_counter()` használatával
- Aszinkron logolás a structlog segítségével

## Biztonság

- **Adatvédelem**: Csak biztonságos típusok logolása
- **Bizalmas adatok**: Objektumok és komplex adatszerkezetek nem kerülnek naplózásra
- **Hibabiztonság**: A dekorátor nem befolyásolja a függvény normál működését

## Kapcsolódó Dokumentáció

- [Logger Architektúra](../logger/factory.md)
- [Structlog Konfiguráció](../../../configs/logging.yaml)
- [Core Utils Áttekintés](../utils.md)