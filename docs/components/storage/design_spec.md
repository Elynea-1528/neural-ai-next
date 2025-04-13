<!-- filepath: /home/elynea/Dokumentumok/neural-ai-next/docs/components/storage/README.md -->
# Storage Komponens

## Áttekintés

A Storage komponens a Neural-AI-Next rendszer adattárolási rétegét biztosítja. Felelős a nyers és feldolgozott adatok, modellek és metaadatok hatékony tárolásáért és kezeléséért. A komponens egy egységes interfészt biztosít különböző tárolási megoldásokhoz, támogatva a fájlrendszer, adatbázisok és felhőtárolók használatát.

## Fő funkciók

- Nyers és feldolgozott adatok tárolása és lekérdezése
- Modellek és metaadatok kezelése
- Idősoralapú adatok hatékony szűrése és lekérdezése
- Több formátum támogatása (Parquet, HDF5, CSV)
- Adatok particionálása és indexelése

## Architektúra

A Storage komponens az alábbi részekből áll:

1. **StorageInterface**: Egységes interfész az adattároláshoz
2. **StorageFactory**: Factory osztály a megfelelő implementáció létrehozásához
3. **Implementációk**:
   - FileSystemStorage: Helyi fájlrendszer alapú tárolás
   - DatabaseStorage: Adatbázis alapú tárolás
   - S3Storage: Amazon S3 alapú tárolás

## Adattípusok

A komponens a következő adattípusokat kezeli:

1. **Nyers adatok**: MT5 és egyéb forrásokból származó OHLCV adatok
2. **Feldolgozott adatok**: Processzorok által előállított feature-ök
3. **Modellek**: Betanított modellek és állapotok
4. **Metaadatok**: Adatkészletek és modellek metaadatai

## Adatstruktúra

A Storage komponens az alábbi adatstruktúrát használja:

```markdown
/data
├── raw/                   # Nyers adatok
│   ├── forex/             # Forex adatok
│   │   ├── EURUSD/        # Szimbólum szerinti csoportosítás
│   │   │   ├── M1/        # Időkeret szerinti csoportosítás
│   │   │   ├── M5/
│   │   │   └── ...
│   │   └── ...
│   └── crypto/            # Kripto adatok
├── processed/             # Feldolgozott adatok
│   ├── d1_price_action/   # Processzor szerinti csoportosítás
│   ├── d2_sr_levels/
│   └── ...
└── models/                # Modellek
    ├── trend_predictor/   # Modell név szerinti csoportosítás
    │   ├── 1.0.0/         # Verzió szerinti csoportosítás
    │   └── 1.1.0/
    └── volatility_model/
```

## Használati példák

### Nyers adatok mentése és betöltése

```python
# Storage inicializálása
storage = StorageFactory.get_storage("file")

# Adatok mentése
storage.save_raw_data(price_data, symbol="EURUSD", timeframe="M1")

# Adatok betöltése
data = storage.load_raw_data(
    symbol="EURUSD",
    timeframe="M1",
    start_date="2023-01-01",
    end_date="2023-01-31"
)

# Ellenőrzés, hogy létezik-e adat
has_data = storage.has_data("EURUSD", "M1")
```

### Feldolgozott adatok mentése és betöltése

```python
# Feldolgozott adatok mentése
storage.save_processed_data(
    processed_features,
    symbol="EURUSD",
    timeframe="M1",
    processor="d1_price_action"
)

# Feldolgozott adatok betöltése
features = storage.load_processed_data(
    symbol="EURUSD",
    timeframe="M1",
    processor="d1_price_action"
)
```

### Modellek mentése és betöltése

```python
# Modell mentése
storage.save_model(model, "trend_predictor", version="1.0.0")

# Modell betöltése
model = storage.load_model("trend_predictor", version="1.0.0")

# Modell metaadatok lekérése
metadata = storage.get_model_metadata("trend_predictor", version="1.0.0")

# Elérhető modellek listázása
models = storage.list_models()
```
## Teljesítmény optimalizáció
A Storage komponens a következő optimalizációkat alkalmazza:

1. Particionálás: Adatok particionálása szimbólum és időkeret szerint
2. Indexelés: Idősorok indexelése a gyors lekérdezéshez
3. Tömörítés: Adatok tömörítése a tárhely optimalizálásához
4. Gyorsítótárazás: Gyakran használt adatok memóriában tartása

## Fejlesztési útmutató
Új storage implementáció létrehozásához:

1. Implementálja a StorageInterface interfészt
2. Regisztrálja az új implementációt a StorageFactory osztályban
3. Készítsen unit teszteket az új implementációhoz
````

# Storage Komponens Tervezési Specifikáció

## Áttekintés

A Storage komponens a Neural-AI-Next rendszer adattárolási rétegét biztosítja. Felelős a nyers és feldolgozott adatok, modellek és metaadatok hatékony tárolásáért és kezeléséért. A komponens egy egységes interfészt biztosít különböző tárolási megoldásokhoz, támogatva a fájlrendszer, adatbázisok és felhőtárolók használatát.

## Funkcionális követelmények

### Elsődleges követelmények

- Nyers idősor-adatok mentése és betöltése
- Feldolgozott adatok mentése és betöltése
- Modellek mentése és betöltése metaadatokkal
- Dinamikus adatszűrés (idő és oszlopok szerint)
- Egyszerű kereshetőség az adatforrások között
- Konzisztens hibakezelés

### Másodlagos követelmények

- Különböző adatformátumok támogatása (CSV, HDF5, Pickle)
- Tömörítés támogatása
- Teljesítmény-optimalizált tárolás és lekérés
- Adatminőség-ellenőrzés

## Architektúrális terv

### Komponens felépítés

1. **Interfész réteg**:
   - StorageInterface: A komponens publikus API-ja
   - StorageFactoryInterface: Példány létrehozás és konfiguráció

2. **Implementáció réteg**:
   - FileSystemStorage: Fájlrendszer alapú tárolás
   - (Tervezett) DatabaseStorage: Adatbázis alapú tárolás
   - (Tervezett) S3Storage: Amazon S3 alapú tárolás

3. **Kivétel réteg**:
   - Hierarchikus kivételkezelési struktúra

### Osztálydiagram

  +-----------------------+          +---------------------------+
  |                       |          |                           |
  | StorageInterface      |<---------+ StorageFactoryInterface   |
  | (Abstract)            |          | (Abstract)                |
  +-----------+-----------+          +-----------+---------------+
              ^                                  ^
              |                                  |
              |                                  |
  +-----------+-----------+          +-----------+---------------+
  |                       |          |                           |
  | FileSystemStorage     |          | StorageFactory            |
  |                       |          |                           |
  +-----------------------+          +---------------------------+

## Adattárolási stratégia

### Fájlrendszer tárolás

Könyvtárstruktúra terve:

/base_path
├── raw/                   # Nyers adatok
│   ├── {symbol}/          # Szimbólum szerinti csoportosítás
│   │   ├── {timeframe}/   # Időkeret szerinti csoportosítás
│   │   │   └── data.{format} # Adatok a konfigurált formátumban
├── processed/             # Feldolgozott adatok
│   ├── {processor}/       # Processzor szerinti csoportosítás
│   │   ├── {symbol}/      # Szimbólum szerinti csoportosítás
│   │   │   ├── {timeframe}/ # Időkeret szerinti csoportosítás
└── models/                # Modellek
    ├── {model_name}/      # Modell név szerinti csoportosítás
    │   ├── {version}/     # Verzió szerinti csoportosítás
    │   │   ├── model.pkl  # Modell fájl
    │   │   └── metadata.pkl # Metaadatok

### Adatformátum kezelés

- **CSV**: Emberi olvasható, általánosan kompatibilis formátum
  - Előnyök: Könnyű olvashatóság, széles körben támogatott
  - Hátrányok: Nagy fájlméret, lassabb feldolgozás

- **HDF5**: Nagy teljesítményű, hierarchikus adattároló formátum
  - Előnyök: Gyors elérés, indexelés, részleges lekérdezés
  - Hátrányok: Specifikus függőségek szükségesek

- **Pickle**: Python natív objektum szerializációs formátum
  - Előnyök: Közvetlen objektum mentés/betöltés
  - Hátrányok: Csak Python-nal használható, biztonsági kockázat

## Teljesítmény megfontolások

### Optimalizációs stratégiák

1. **Gyorsítótárazás**: Gyakran használt adatok memóriában tárolása
2. **Indexelés**: Dátum alapú indexek a gyors kereséshez
3. **Részleges adatbetöltés**: Csak a szükséges oszlopok és sorok betöltése
4. **Tömörítés**: Adatok tömörítése a tárhely optimalizálásához
5. **Párhuzamos feldolgozás**: Nagy adathalmazok többszálú feldolgozása

### Benchmark célok

- Nyers adatok mentése: <100 ms 10,000 sornál
- Adatok betöltése: <50 ms 10,000 sornál
- Modell mentés/betöltés: <200 ms 100MB-ig

## Hibakezelés és robosztusság

- Egységes kivételkezelési mechanizmus
- Automatikus helyreállítási lehetőségek
- Szigorú típusellenőrzés
- Részletes naplózás

## Bővíthetőség

Tervezett jövőbeli kiterjesztések:

- Elosztott tárolási rendszerek támogatása
- Time-series optimalizált adatbázis backenek
- Automatikus adatszinkronizáció
- Többverziós adattárolás (adatverzió-követés)
- Jogosultságkezelés

## Függőségek

- pandas: Adatmanipuláció
- numpy: Numerikus műveletek
- h5py/tables: HDF5 támogatás
- Logger komponens: Naplózás
- ConfigManager komponens: Konfiguráció kezelés

## Biztonsági megfontolások

- Adatok integritásának biztosítása
- Modell verziókövetés
- Pickle használati korlátok ismertetése
- Fájlrendszer jogosultságok kezelése
