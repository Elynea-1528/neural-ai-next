# scripts/test_tick_pipeline.py

## Áttekintés

A `test_tick_pipeline.py` szkript a tick adatok feldolgozási útvonalának teljes validációját végzi el. Ez magában foglalja a Resampler és D1 Dimension Processor komponensek együttműködését "tick" timeframe-mal.

## Architektúra

A szkript követi a projekt DI (Dependency Injection) elveit:
- Factory-k használata komponensek létrehozására
- Interface-eken keresztül történő függőség injektálás
- TYPE_CHECKING használata körkörös importok elkerülésére

## Főbb Komponensek

### Mock Komponensek
- **Config**: Mock konfigurációs objektum D1 processor beállításokkal
- **Logger**: Mock logger objektum naplózáshoz
- **Storage**: Mock storage objektum tick adatok betöltéséhez

### Validációs Lépések

1. **Adat Generálás**: Mock tick adatok létrehozása (timestamp, bid, ask, bid_volume, ask_volume)
2. **Resample Validáció**:
   - Sorok számának egyezősége bemenet és kimenet között
   - Új oszlopok megléte (mid_close, spread, tick_volume)
   - Tick volume értékek ellenőrzése (minden sorban 1)
3. **D1 Processor Validáció**:
   - Log return oszlop megléte
   - Shadow oszlopok None értékei tick timeframe esetén

## Használat

```bash
python scripts/test_tick_pipeline.py
```

## Kimenet

A szkript részletes kimenetet ad a validációs lépésekről:
- ✅ Sikeres validációk esetén zöld pipa és részletek
- ❌ Hibák esetén piros X és hibalista
- 🎉 Végső sikeresség üzenet

## Függőségek

- `neural_ai.core.processing.resampler_service.factory.ResamplerServiceFactory`
- `neural_ai.core.processing.factory.create_dimension_processor`
- `polars`, `pandas` adatkezeléshez
- `asyncio` aszinkron műveletekhez

## Validációs Kritériumok

### Resample Eredmény
- Sorok száma változatlan (bypass aggregáció)
- `mid_close` oszlop jelenléte: `(bid + ask) / 2`
- `spread` oszlop jelenléte: `ask - bid`
- `tick_volume` minden sorban 1

### D1 Processor Eredmény
- `log_return` oszlop jelenléte: `ln(mid_close / mid_close.shift(1))`
- `upper_shadow` és `lower_shadow` None értékek tick timeframe esetén
- Eredeti tick oszlopok megőrzése