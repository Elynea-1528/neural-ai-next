# scripts/download_history.py

## Áttekintés

Ez a script a Neural AI Next rendszer tömeges tick adat letöltő eszköze, amely lehetővé teszi a JForex adatforrásból történő tick adatok letöltését egy megadott dátumtartományban.

**Verzió:** 2.0.0 (Direct Storage Mode)

## Fő jellemzők

- **Direct Storage Mode:** A letöltött adatok közvetlenül a ParquetStorageService által kerülnek mentésre, kikerülve az EventBus-t a maximális sebesség érdekében.
- **Smart Resume:** Intelligens folytatási mechanizmus, amely ellenőrzi a már letöltött adatokat és kihagyja az ismételt letöltéseket.
- **Chunkolt feldolgozás:** Óránkénti adatletöltés a memória hatékony kezelése érdekében.
- **Parquet formátum:** Az adatok particionált Parquet formátumban kerülnek mentésre.

## Használat

```bash
python scripts/download_history.py --symbol EURUSD --start 2023-01-01 --end 2023-12-31
```

### Paraméterek

| Paraméter | Típus | Kötelező | Leírás |
|-----------|-------|----------|--------|
| `--symbol` | string | Igen | A pénzpár szimbóluma (pl. EURUSD) |
| `--start` | string | Igen | Kezdő dátum (YYYY-MM-DD formátumban) |
| `--end` | string | Igen | Záró dátum (YYYY-MM-DD formátumban) |

## Architektúra

### Fő komponensek

1. **Bootstrap Core:** A rendszer inicializálása a core komponensekkel (logger, storage, config)
2. **JForexFactory:** A Bi5Downloader példányosítása
3. **Direct Storage:** Közvetlen adatmentés a Polars és ParquetStorageService használatával

### Smart Resume logika

A Smart Resume mechanizmus ellenőrzi, hogy van-e már letöltött parquet fájl az adott óra mappában:

```python
hour_dir = Path(
    f"data/tick/{symbol.upper()}/tick/year={current_hour.year}/"
    f"month={current_hour.month:02d}/day={current_hour.day:02d}"
)

if hour_dir.exists() and any(hour_dir.glob("*.parquet")):
    # Skip, mert már létezik adat
```

Ez biztosítja, hogy ha a storage időbélyeges nevet generál, akkor is felismerje a meglévő fájlokat.

## Adat struktúra

A letöltött tick adatok a következő struktúrában kerülnek mentésre:

```python
{
    "timestamp": datetime,  # Tick időbélyege
    "bid": float,          # Bid ár
    "ask": float,          # Ask ár
    "ask_volume": float,   # Ask volumen
    "bid_volume": float,   # Bid volumen
    "volume": float,       # Összesített volumen
    "source": str,         # Adatforrás
}
```

## Tesztelés

A scripthez tartozó tesztek a `tests/scripts/` mappában találhatók.

```bash
pytest tests/scripts/test_download_history.py -v
```

## Függőségek

- `neural_ai.collectors.jforex` - JForex adatgyűjtő
- `neural_ai.core` - Core komponensek (logger, storage, config)
- `polars` - DataFrame kezelés
- `parquet` - Adatmentés
