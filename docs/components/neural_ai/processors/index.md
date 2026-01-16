# neural_ai/processors - Processor modul

## Áttekintés

A processors modul a Neural AI rendszer adatfeldolgozó komponenseit tartalmazza. Ez magában foglalja a dimenzió processzorokat, időszinkronizációs szolgáltatásokat és resampler funkciókat.

## Architektúra

A modul Interface/Implementation/Factory szerkezetet követ:

- **interfaces/**: Absztrakt interfészek
- **implementations/**: Konkrét implementációk
- **factory.py**: Belépési pont és példányosítás

## Fő komponensek

### Dimenzió processzorok (dimensions/)

- **d01_price/**: Alap adatok processzora (log return, Z-score, shadows)
- **d02_support/**: Support/Resistance szintek detektálása swing pontok alapján

### Időszinkronizációs szolgáltatás (implementations/time_alignment_service.py)

- Tökéletes időskála biztosítása különböző timeframe-ekhez
- Lyukak kezelése (gap filling)
- Piaci nyitvatartási idő szűrés

### Resampler szolgáltatás (resampler_service/)

- Tick adatokból OHLCV gyertyák létrehozása
- Pandas/Polars visszatérési típusok támogatása
- Kiterjesztett metrikák (Bid/Ask OHLC, Spread, Volume)

## Interfaces

### IDimensionProcessor

Absztrakt interfész minden dimenzió processzor számára.

### ITimeAlignmentService

Időszinkronizációs szolgáltatás interfész.

### ITensorConverter

Tensor konverter interfész (jövőbeli használat).

### IResamplerInterface

Resampler szolgáltatás interfész.

## Factory függvények

- `create_dimension_processor(dimension_id, config, logger)`: Dimenzió processzor létrehozása ID alapján
- `create_time_alignment_service()`: Időszinkronizációs szolgáltatás létrehozása

## Kapcsolódó dokumentáció

- [D01 Price Processor](dimensions/d01_price/processor.md)
- [D02 Support Processor](dimensions/d02_support/processor.md)
- [Time Alignment Service](implementations/time_alignment_service.md)
- [Resampler Service](resampler_service/implementations/resampler_service.md)