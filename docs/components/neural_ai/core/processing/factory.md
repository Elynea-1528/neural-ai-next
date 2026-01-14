# ProcessingFactory

## Áttekintés

A `ProcessingFactory` modul biztosítja a feldolgozási komponensek (TimeAlignmentService, DimensionProcessor-ek) létrehozását dinamikus factory loadinggal, Dependency Injection nélkül. Az architektúra elkerüli a konkrét osztályok statikus importálását, kizárólag interface-eket használva.

## Architektúra

Ez a modul a `neural_ai.core.processing` része, és biztosítja a központi factory függvényeket minden feldolgozási komponens számára.

## Funkcionalitás

### create_time_alignment_service Függvény

```python
def create_time_alignment_service() -> ITimeAlignmentService:
```

Létrehoz egy új `TimeAlignmentService` példányt dinamikus importlib használatával.

#### Visszatérési érték

`ITimeAlignmentService` - Az időszinkronizációs szolgáltatás példánya

### create_dimension_processor Függvény

```python
def create_dimension_processor(
    dimension_id: int, config: ConfigManagerInterface, logger: LoggerInterface
) -> IDimensionProcessor:
```

Létrehoz egy megfelelő dimenzió processzor példányt dinamikus factory loadinggal.

#### Paraméterek

- `dimension_id`: A dimenzió azonosítója (1-15)
- `config`: Konfigurációs menedzser interfész
- `logger`: Logger interfész

#### Visszatérési érték

`IDimensionProcessor` - A megfelelő dimenzió processor példány

#### Kivételek

- `ValueError`: Ha ismeretlen dimenzió ID-t adnak meg

## Dinamikus Loading Mechanizmus

A factory `importlib` használatával dinamikusan tölti be a dimenzió factory modulokat és osztályokat, elkerülve a statikus importokat. Ez biztosítja a loose couplingot és a könnyebb bővíthetőséget.

- **TimeAlignmentService**: Közvetlen dinamikus import az implementation osztályra
- **DimensionProcessor-ek**: Dinamikus import a megfelelő factory modulra és osztályra

## Konfiguráció

A támogatott dimenziók konfigurációja:

- `1`: price (D01PriceFactory)
- `2`: support (D02SupportFactory)

## Függőségek

- `ConfigManagerInterface` - Konfiguráció kezelése
- `LoggerInterface` - Logolás
- `IDimensionProcessor` - Dimenzió processzor interfész
- `ITimeAlignmentService` - Időszinkronizációs szolgáltatás interfész

## Big Data Támogatás

A factory által létrehozott komponensek támogatják a big data feldolgozást chunkolással, aszinkronitással és Parquet formátummal.