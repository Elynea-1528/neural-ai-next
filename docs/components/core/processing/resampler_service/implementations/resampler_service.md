# ResamplerService - Tick adatokból OHLCV gyertyák létrehozása

## Áttekintés

A `ResamplerService` osztály implementálja a `ResamplerInterface`-t, amely tick adatokból hoz létre OHLCV gyertyákat különböző időkeretekben. A szolgáltatás Polars-t használ a hatékonyság érdekében, és támogatja a Pandas és Polars DataFrame visszaadást.

## Architektúra

### Osztály hierarchia
```
ResamplerInterface (ABC)
└── ResamplerService
```

### Dependenciák
- **StorageInterface**: Tick adatok betöltése
- **LoggerInterface**: Naplózás (LoggerFactory-ból)

### Főbb komponensek
- **Tick adat betöltés**: Aszinkron adatbetöltés a tárolóból
- **OHLCV konverzió**: Kiterjesztett gyertyák (Mid/Bid OHLC, Spread, Real/Tick/Bid/Ask Volume)
- **Időkeret validálás**: Támogatott időkeretek ellenőrzése
- **Return type handling**: Pandas vagy Polars DataFrame visszaadás

## API Referencia

### Inicializáció

```python
service = ResamplerService(storage=storage_interface)
```

### Tick adatok resample-olása

```python
await service.resample(
    symbol="EURUSD",
    start=datetime(2023, 12, 1),
    end=datetime(2023, 12, 31),
    timeframe="1m",
    return_type="pandas"
)
```

### Paraméterek
- `symbol`: Kereskedési szimbólum (str)
- `start`: Kezdő időpont (datetime)
- `end`: Záró időpont (datetime)
- `timeframe`: Időkeret ('1m', '5m', '15m', '30m', '1h', '4h', '1D', '1W', '1M')
- `return_type`: Visszaadott típus ('pandas' vagy 'polars')

## Konfiguráció

### Támogatott időkeretek
- '1m', '5m', '15m', '30m', '1h', '4h', '1D', '1W', '1M'

### Szükséges tick adat oszlopok
- `timestamp`: Időbélyeg
- `bid`: Bid ár
- `ask`: Ask ár
- `bid_volume`: Bid volume (opcionális)
- `ask_volume`: Ask volume (opcionális)

## Adatmodell

### OHLCV gyertya struktúra
```python
{
    "timestamp": datetime,
    "mid_open": float,
    "mid_high": float,
    "mid_low": float,
    "mid_close": float,
    "bid_open": float,
    "bid_high": float,
    "bid_low": float,
    "bid_close": float,
    "spread": float,
    "real_volume": float,
    "tick_volume": int,
    "bid_volume": float,  # Ha elérhető
    "ask_volume": float   # Ha elérhető
}
```

### Aggregációs logika
- **Mid OHLC**: (bid + ask) / 2 átlag alapján
- **Bid/Ask OHLC**: Bid és ask árak alapján
- **Spread**: Átlagos spread (ask - bid)
- **Real Volume**: bid_volume + ask_volume összeg
- **Tick Volume**: Tick szám az időkeretben

## Teljesítmény jellemzők

### Polars használat
- Hatékony group_by_dynamic aggregáció
- Zero-copy DataFrame műveletek
- AVX2 optimalizáció támogatása

### Aszinkron feldolgozás
- Aszinkron tick adat betöltés
- Párhuzamos feldolgozás támogatása

### Memória kezelés
- Chunk-olás nagy adathalmazokhoz
- Polars lazy evaluation ahol lehetséges

## Hibakezelés

### Kivételek
- `InvalidTimeframeError`: Érvénytelen időkeret
- `DataLoadError`: Adatbetöltési hiba
- `ResamplingError`: Átalakítási hiba
- `ValueError`: Hiányzó szükséges oszlopok

### Naplózás
- Strukturált naplózás LoggerInterface-en keresztül
- Debug, info, warning szintek
- Teljesítmény metrikák

## Tesztelés

### Egységtesztek
A szolgáltatás teljes lefedettséget biztosító pytest teszteket tartalmaz:

```bash
pytest tests/core/processing/resampler_service/implementations/test_resampler_service.py
```

### Lefedett funkciók
- Inicializáció különböző konfigurációkkal
- Tick adatok resample-olása
- Időkeret validálás
- Hibakezelés
- Return type konverziók

## Kapcsolódó komponensek

### Resampler modul
- `ResamplerInterface`: Absztrakt interfész
- `ResamplerFactory`: Factory implementáció
- `ResamplerError`: Egyedi kivételek

### Egyéb modulok
- `StorageInterface`: Adattárolás
- `LoggerInterface`: Naplózás
- `ConfigInterface`: Konfiguráció kezelés

## Fejlesztési megjegyzések

### Refaktorálás dátuma
2026-01-11 - Volume oszlop kezelés módosítása, LoggerFactory használat

### Jövőbeli fejlesztések
- Big data chunking implementáció
- Elosztott feldolgozás támogatása
- Automatikus optimalizáció időkeretekhez
