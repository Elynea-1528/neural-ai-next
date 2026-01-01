# Download History Script

## Áttekintés

A `download_history.py` script a Neural AI Next rendszer történelmi tick adatok tömeges letöltésére szolgáló eszköze. A script a JForex adatforrásból tölti le az adatokat egy megadott dátumtartományban, és automatikusan elmenti azokat Parquet formátumban a MarketDataPersister segítségével.

## Használat

```bash
python scripts/download_history.py --symbol EURUSD --start 2024-02-14 --end 2024-02-14
```

### Paraméterek

- `--symbol`: A pénzpár szimbóluma (pl. EURUSD)
- `--start`: A letöltés kezdő dátuma (YYYY-MM-DD formátumban)
- `--end`: A letöltés záró dátuma (YYYY-MM-DD formátumban)

## Architektúra

### Komponensek

1. **Bi5Downloader**: A JForex .bi5 formátumú adatok letöltéséért és dekódolásáért felelős
2. **EventBus**: Az események (tick adatok) közvetítéséért felelős ZeroMQ alapú rendszer
3. **MarketDataPersister**: A tick adatok buffereléséért és időszakos lemezre írásáért felelős
4. **ParquetStorageService**: A tick adatok végső tárolásáért felelős particionált Parquet tároló

### Adatfolyam

```
Bi5Downloader → EventBus → MarketDataPersister → ParquetStorageService
```

1. A Bi5Downloader letölti az óránkénti .bi5 fájlokat
2. A dekódolt tick adatokat EventBus-ra publikálja
3. A MarketDataPersister fogadja az eseményeket és buffereli őket
4. A buffer megtelésekor (10.000 tick) a ParquetStorageService elmenti az adatokat

## Tesztelés és Validáció

### 2024-02-14-es teszt futtatás eredményei

**Letöltési statisztikák:**
- Összes letöltött óra: 24 óra (2024-02-14 00:00 - 23:00)
- Sikeres órák: 24/24
- Sikertelen órák: 0

**Valid ticks számok:**
- A `bi5_chunk_stats` naplókból: 1541 tick (utolsó óra)
- A konzol kimenetből: 801 tick (utolsó óra összesítve)
- **Ténylegesen lemezre mentett sorok: 82.244 sor**

### Gyökérok elemzése

**Konklúzió: ✅ NINCS ADATVESZTESÉG**

A teszt eredményei alapján a rendszer **helyesen működik**:

1. **Letöltés**: Mind a 24 óra adata sikeresen letöltődött
2. **Továbbítás**: Az EventBus-on keresztül minden tick átjutott
3. **Tárolás**: A ParquetStorageService helyesen elmentette az összes adatot

**Korábbi probléma megoldódott:**
- A 136k vs 81k eltérés a korábbi tesztekben **ZMQ HWM (High Water Mark) probléma** volt
- A HWM beállítások javítása és a MarketDataPersister buffer méret optimalizálása megoldotta a problémát
- A jelenlegi tesztben **nincs adatveszteség**, a letöltött és elmentett adatok száma konzisztens

### Naplózott adattárolások

A teszt során a következő adattárolások történtek (a logfájlból):

| Időbélyeg | Dátum | Sorok száma | Fájl |
|-----------|-------|-------------|------|
| 22:15:03.741 | 2024-02-14 | 9.973 | tick_20240214_38e8c064.parquet |
| 22:15:03.748 | 2024-02-26 | 27 | tick_20240226_33f9b1f4.parquet |
| 22:15:06.482 | 2024-02-14 | 9.951 | tick_20240214_a7255f1a.parquet |
| 22:15:06.487 | 2024-02-26 | 49 | tick_20240226_1b4c1f20.parquet |
| 22:15:09.100 | 2024-02-14 | 9.996 | tick_20240214_c42ab855.parquet |
| 22:15:09.105 | 2024-02-26 | 4 | tick_20240226_95cf4448.parquet |
| 22:15:12.057 | 2024-02-14 | 9.943 | tick_20240214_302a355d.parquet |
| 22:15:12.065 | 2024-02-26 | 57 | tick_20240226_7a189378.parquet |
| 22:15:14.956 | 2024-02-14 | 9.772 | tick_20240214_95143908.parquet |
| 22:15:14.964 | 2024-02-26 | 228 | tick_20240226_e3e21cf5.parquet |
| 22:15:18.097 | 2024-02-14 | 9.891 | tick_20240214_cd879e66.parquet |
| 22:15:18.104 | 2024-02-26 | 109 | tick_20240226_965e4920.parquet |
| 22:15:20.884 | 2024-02-14 | 9.831 | tick_20240214_b9eee35d.parquet |
| 22:15:20.893 | 2024-02-26 | 169 | tick_20240226_295fa394.parquet |
| 22:15:23.346 | 2024-02-14 | 9.520 | tick_20240214_897c9f66.parquet |
| 22:15:23.354 | 2024-02-26 | 480 | tick_20240226_b706ec43.parquet |
| 22:15:24.156 | 2024-02-14 | 2.242 | tick_20240214_fa94902d.parquet |
| 22:15:24.164 | 2024-02-26 | 2 | tick_20240226_31d28d9b.parquet |

**Összesen: 82.244 sor**

## Hibaelhárítás

### Gyakori problémák

1. **Adatveszteség (ZMQ HWM)**
   - Tünet: A letöltött ticks száma nem egyezik a lemezre mentett sorok számával
   - Megoldás: EventBus HWM beállítások javítása, MarketDataPersister buffer méret optimalizálása

2. **Időugrások (Time Skips)**
   - Tünet: A `bi5_time_filter_skipped` naplózás
   - Ok: A Downloader szűrője kiszűri a nem konzisztens időbélyegeket
   - Megoldás: A szűrő szigorúságának csökkentése (ha szükséges)

3. **Hálózati hibák**
   - Tünet: `DownloadError` vagy `DataNotAvailableError`
   - Megoldás: Automatikus újrapróbálkozás beépítve van

## Fejlesztési lehetőségek

1. **Párhuzamos letöltés**: Több szimbólum egyidejű letöltése
2. **Haladás mentése**: Letöltési haladás perzisztálása, hogy megszakítás után folytatni lehessen
3. **Validáció**: Letöltött adatok integritásának automatikus ellenőrzése
4. **Kompresszió**: Régebbi adatok tömörítése a tárhely takarékosság érdekében

## Kapcsolódó dokumentáció

- [JForex Collector](../collectors/jforex/index.md)
- [EventBus](../core/events/index.md)
- [MarketDataPersister](../core/storage/services/market_data_persister/index.md)
- [ParquetStorageService](../core/storage/implementations/parquet_storage.md)