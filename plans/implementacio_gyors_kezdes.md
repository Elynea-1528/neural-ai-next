# Adatgyűjtési Stratégia - Implementációs Gyorsindítás

**Dátum:** 2025-12-16
**Verzió:** 1.0.0

---

## Fordítás állapota

✅ **Teljes dokumentum lefordítva**
✅ **Minden szakasz magyar nyelven**
✅ **Markdown formázás megtartva**
✅ **Kódpéldák angolul maradtak**
⚠️ **Implementáció állapota: Tervezési fázis**

---

## 🎯 Gyors áttekintés

Ez a dokumentum gyorsindítási útmutatót nyújt az új adatgyűjtési stratégia implementálásához. A teljes architektúra tervért lásd: [`adatgyujtesi_strategia_atfogo.md`](adatgyujtesi_strategia_atfogo.md).

---

## 📋 Implementációs összefoglaló

### Amit építünk

1. **Történelmi adatgyűjtés** (25 év) - Modellképzéshez
2. **Növekményes frissítések** (3-12 hónap) - Adatok friss tartása
3. **Bővített valós idejű gyűjtés** - Jelenlegi rendszer tovább működik
4. **Adatminőségi keretrendszer** - Automatizált validáció
5. **Képzési adathalmazok** - 4 kategória: Újraképzés, Közepes, Mély tanulás, Validáció

### Kulcs technológiák

- **MQL5 Expert Advisor** - Történelmi adatképességekkel bővítve
- **FastAPI (Python)** - Új végpontok történelmi gyűjtéshez
- **Parquet formátum** - Hatékony tárolás nagy adathalmazokhoz
- **Automatizált ütemező** - Növekményes frissítésekhez

---

## 🚀 Fázisról fázisra implementáció

### 1. fázis: Történelmi adatgyűjtés (4 hét)

**Cél:** 25 év történelmi adat gyűjtése minden instrumentumra és időkeretre

#### 1. hét: MQL5 EA bővítmények

**Feladatok:**
1. Történelmi adatkérés kezelő hozzáadása az EAhöz
2. Kötegelt adatlekérés implementálása (1 év darabokban)
3. Folyamat követés hozzáadása
4. Tesztelés 1 hónap adattal

**Módosítandó kulcs fájlok:**
- [`neural_ai/experts/mt5/src/Neural_AI_Next_Multi.mq5`](neural_ai/experts/mt5/src/Neural_AI_Next_Multi.mq5:1)

**Új EA funkciók:**
```mql
// Add these functions to the EA
bool HandleHistoricalRequest(string json_request);
void SendHistoricalDataBatch(int batch_number, string symbol, int timeframe, datetime start, datetime end);
void ReportProgress(int job_id, int progress_percentage);
```

#### 2. hét: FastAPI szerver bővítmények

**Feladatok:**
1. Történelmi adatkérés végpont implementálása
2. Job menedzsment rendszer hozzáadása
3. Történelmi adatgyűjtési végpont létrehozása
4. Folyamat követési API hozzáadása

**Új API végpontok:**
```
POST   /api/v1/historical/request     # Történelmi adatkérés
GET    /api/v1/historical/status/{job_id}  # Job állapot ellenőrzése
POST   /api/v1/historical/collect    # EA küld történelmi adatot
```

**Létrehozandó/módosítandó kulcs fájlok:**
- [`neural_ai/collectors/mt5/implementations/mt5_collector.py`](neural_ai/collectors/mt5/implementations/mt5_collector.py:1) - Új végpontok hozzáadása
- `neural_ai/collectors/mt5/implementations/historical_manager.py` - ÚJ FÁJL
- `neural_ai/collectors/mt5/implementations/job_manager.py` - ÚJ FÁJL

#### 3. hét: Tárolás és validáció

**Feladatok:**
1. Tároló réteg kiterjesztése történelmi adatokhoz
2. Köteg validáció implementálása
3. Hézag detektálás hozzáadása
4. Adatraktár szerkezet létrehozása

**Módosítandó kulcs fájlok:**
- [`neural_ai/collectors/mt5/implementations/storage/collector_storage.py`](neural_ai/collectors/mt5/implementations/storage/collector_storage.py:1)
- [`neural_ai/collectors/mt5/data_validator.py`](neural_ai/collectors/mt5/data_validator.py:1)

**Hozzáadandó új metódusok:**
```python
def store_historical_data(self, symbol: str, timeframe: str,
                         data: pd.DataFrame, date_range: Tuple[datetime, datetime]):
    """Történelmi adatok tárolása raktár szerkezetben."""

def detect_gaps(self, symbol: str, timeframe: str,
               start_date: datetime, end_date: datetime) -> List[Dict]:
    """Hézagok detektálása történelmi adatokban."""
```

#### 4. hét: Integráció és tesztelés

**Feladatok:**
1. End-to-end tesztelés
2. Teljesítmény optimalizálás
3. Hibakezelés
4. Dokumentáció

**Teszt forgatókönyvek:**
- 1 év EURUSD M1 adat
- 5 év több instrumentum
- Hiba helyreállítás (kapcsolat vesztés)
- Nagy köteg feldolgozás

### 2. fázis: Növekményes frissítések (2 hét)

**Cél:** 3-12 hónapos adatfrissesség automatikus karbantartása

#### 5. hét: Ütemező és automatizálás

**Feladatok:**
1. Napi ütemező implementálása
2. Növekményes frissítési logika hozzáadása
3. Hézag detektálás automatizálás létrehozása
4. Értesítési rendszer építése

**Létrehozandó kulcs fájlok:**
- `scripts/incremental_updater.py` - ÚJ FÁJL
- `scripts/gap_detector.py` - ÚJ FÁJL
- `scripts/scheduler.py` - ÚJ FÁJL

**Ütemező logika:**
```python
# Daily at 2 AM
schedule.every().day.at("02:00").do(run_incremental_update)

def run_incremental_update():
    # 1. Utolsó frissítés dátumának ellenőrzése
    # 2. Hiányzó adatok azonosítása
    # 3. Kérés az EAtól
    # 4. Validálás és tárolás
    # 5. Metaadatok frissítése
```

#### 6. hét: Monitorozás

**Feladatok:**
1. Monitorozó vezérlőpult építése
2. Health check implementálása
3. Naplózás és riasztás hozzáadása
4. Karbantartási szkriptek létrehozása

**Monitorozási metrikák:**
- Adatfrissesség (órák az utolsó frissítés óta)
- Gyűjtési siker arány
- Adatminőség pontszámok
- Tároló kihasználtság

### 3. fázis: Képzési adathalmaz generálás (2 hét)

**Cél:** Különböző modelltípusokhoz szegregált képzési adathalmazok létrehozása

#### 7. hét: Adathalmaz generátor

**Feladatok:**
1. Adathalmaz kiválasztási logika implementálása
2. Minőségi szűrés hozzáadása
3. Jellemző mérnökség folyamat létrehozása
4. Adathalmaz felosztás építése

**Létrehozandó kulcs fájlok:**
- `scripts/training_dataset_generator.py` - ÚJ FÁJL
- `scripts/data_quality_filter.py` - ÚJ FÁJL

**Adathalmaz típusok:**
```python
DATASET_CONFIGS = {
    "retraining": {
        "years": 1,
        "update_frequency": "weekly",
        "quality_threshold": 0.95
    },
    "medium": {
        "years": 5,
        "update_frequency": "monthly",
        "quality_threshold": 0.95
    },
    "deep_learning": {
        "years": 25,
        "update_frequency": "yearly",
        "quality_threshold": 0.90
    },
    "validation": {
        "months": 6,
        "update_frequency": "weekly",
        "quality_threshold": 0.98,
        "never_in_training": True
    }
}
```

#### 8. hét: Adathalmaz menedzsment

**Feladatok:**
1. Adathalmaz verziózás implementálása
2. Metaadat menedzsment hozzáadása
3. Validációs eszközök létrehozása
4. Export funkcionalitás építése

**Adathalmaz szerkezet:**
```
data/training/
├── retraining/          # 1 év, heti frissítések
├── medium/              # 5 év, havi frissítések
├── deep_learning/       # 25 év, éves frissítések
└── validation/          # 6 hónap, soha nincs a képzésben
```

### 4. fázis: Adatminőségi keretrendszer (2 hét)

**Cél:** Átfogó adatminőség validáció és monitorozás

#### 9. hét: Fejlett validáció

**Feladatok:**
1. Statisztikai validáció implementálása
2. Konzisztencia ellenőrzések hozzáadása
3. Kiugró érték detektálás építése
4. Anomália detektálás létrehozása

**Validációs szintek:**
- **1. szint:** Alap (valós idejű) - Adattípusok, tartományok, kapcsolatok
- **2. szint:** Statisztikai (köteg) - Kiugró értékek, hézagok, duplikátumok
- **3. szint:** Konzisztencia (történelmi) - Keresztvalidáció, korrelációk

#### 10. hét: Minőség monitorozás

**Feladatok:**
1. Minőségi vezérlőpult építése
2. Minőség pontozás implementálása
3. Automatikus jelentéskészítés hozzáadása
4. Minőségi riasztások létrehozása

**Minőség pontszám formula:**
```
Minőségi pontszám = (
    Teljesség * 0.3 +
    Pontosság * 0.3 +
    Konzisztencia * 0.2 +
    Időbenesség * 0.2
)
```

---

## 📊 Adatraktár szerkezet

```
data/
├── collectors/mt5/          # Nyers adatok (30-90 nap megőrzés)
├── warehouse/
│   ├── historical/          # 25 év (állandó)
│   ├── update/              # 3-12 hónap (évente egyesítés)
│   ├── realtime/            # Jelenlegi (30 nap)
│   └── validated/           # Minőség-ellenőrzött
└── training/                # Képzési adathalmazok
    ├── retraining/          # 1 év
    ├── medium/              # 5 év
    ├── deep_learning/       # 25 év
    └── validation/          # 6 hónap
```

---

## 🔧 API végpontok referenciája

### Történelmi adatgyűjtés

**Történelmi adatkérés:**
```bash
POST /api/v1/historical/request
{
  "symbol": "EURUSD",
  "timeframe": "M1",
  "start_date": "2000-01-01",
  "end_date": "2025-12-31",
  "batch_size": 365,
  "priority": "low"
}
```

**Job állapot ellenőrzése:**
```bash
GET /api/v1/historical/status/job_12345
```

**EA adatokat küld:**
```bash
POST /api/v1/historical/collect
{
  "job_id": "job_12345",
  "batch_number": 1,
  "symbol": "EURUSD",
  "timeframe": "M1",
  "date_range": {"start": "2000-01-01", "end": "2000-12-31"},
  "bars": [...]
}
```

### Hézag detektálás és kitöltés

**Hézagok azonosítása:**
```bash
GET /api/v1/data/gaps?symbol=EURUSD&timeframe=M1
```

**Hézagok kitöltése:**
```bash
POST /api/v1/data/fill-gaps
{
  "gaps": [{"symbol": "EURUSD", "timeframe": "M1", ...}],
  "priority": "high"
}
```

### Képzési adathalmaz generálás

**Adathalmaz generálása:**
```bash
POST /api/v1/training/generate
{
  "dataset_type": "retraining",
  "symbols": ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"],
  "timeframes": ["M1", "M5", "M15", "H1", "H4", "D1"],
  "date_range": {"start": "2024-01-01", "end": "2025-12-16"},
  "quality_threshold": 0.95
}
```

---

## 🎯 Siker kritériumok

### Technikai metrikák
- ✅ 100% adatlefedettség a kért dátumtartományokra
- ✅ >95% adatminőség pontszám
- ✅ <24 óra 25 év gyűjtése (instrumentum/időkeretenként)
- ✅ <1GB tároló évente instrumentum/időkeretenként

### Operációs metrikák
- ✅ 99.9% collector uptime
- ✅ <1 másodperc valós idejű adat késés
- ✅ <0.1% hibaráta
- ✅ <5 perc job helyreállítási idő

---

## 🚨 Kockázat enyhítés

### Fő kockázatok és megoldások

**Kockázat 1: MT5 API korlátozások**
- ✅ Megoldás: Nagy kérések darabolása, rátelimítés
- ✅ Tesztelés kis tartományokkal először

**Kockázat 2: Tároló kapacitás**
- ✅ Megoldás: Igények becslése, tömörítés használata
- ✅ Cloud tárolás fontolóra vétele történelmi adatokhoz

**Kockázat 3: Adatminőségi problémák**
- ✅ Megoldás: Átfogó validáció, tisztító folyamat
- ✅ Kézi ellenőrzés gyanús adatokra

**Kockázat 4: Teljesítmény szűk keresztmetszetek**
- ✅ Megoldás: Párhuzamos feldolgozás, gyorsítótár, optimalizálás

---

## 📝 Gyorsindítás ellenőrzőlista

### Implementáció előtt
- [ ] Teljes architektúra terv áttekintése
- [ ] Tároló igények becslése
- [ ] Fejlesztői környezet beállítása
- [ ] MQL5 EA kód áttekintése

### 1. hét
- [ ] MQL5 EA bővítése történelmi funkciókkal
- [ ] Tesztelés 1 hónap adattal
- [ ] Új EA funkcionalitás dokumentálása

### 2. hét
- [ ] Történelmi adat API végpontok implementálása
- [ ] Job menedzsment rendszer hozzáadása
- [ ] API integráció tesztelése

### 3. hét
- [ ] Tároló réteg kiterjesztése
- [ ] Köteg validáció implementálása
- [ ] Hézag detektálás hozzáadása

### 4. hét
- [ ] End-to-end tesztelés
- [ ] Teljesítmény optimalizálás
- [ ] Dokumentáció

### 5-6. hét
- [ ] Ütemező implementálása
- [ ] Növekményes frissítések hozzáadása
- [ ] Monitorozás építése

### 7-8. hét
- [ ] Adathalmaz generátor létrehozása
- [ ] Minőségi szűrés implementálása
- [ ] Adathalmaz menedzsment hozzáadása

### 9-10. hét
- [ ] Fejlett validáció
- [ ] Minőség monitorozás
- [ ] Végső tesztelés és dokumentáció

---

## 📚 Kapcsolódó dokumentumok

- **Teljes architektúra:** [`adatgyujtesi_strategia_atfogo.md`](adatgyujtesi_strategia_atfogo.md)
- **MT5 EA forrás:** [`neural_ai/experts/mt5/src/Neural_AI_Next_Multi.mq5`](neural_ai/experts/mt5/src/Neural_AI_Next_Multi.mq5:1)
- **Collector implementáció:** [`neural_ai/collectors/mt5/implementations/mt5_collector.py`](neural_ai/collectors/mt5/implementations/mt5_collector.py:1)
- **Tároló implementáció:** [`neural_ai/collectors/mt5/implementations/storage/collector_storage.py`](neural_ai/collectors/mt5/implementations/storage/collector_storage.py:1)

---

## 💡 Tippek a sikerhez

1. **Kezdd kicsiben:** Tesztelj 1 hónap adattal mielőtt 25 évre skálázod
2. **Figyelj közeli:** Nézd a teljesítmény problémákat és állíts
3. **Dokumentálj mindent:** Tarts részletes naplókat az adatgyűjtési jobokról
4. **Validálj korán:** Ellenőrizd az adatminőséget gyakran a gyűjtés alatt
5. **Tervezz hibákra:** Implementálj robusztus hibakezelést és helyreállítást
6. **Kommunikálj:** Tartsd a résztvevőket tájékoztatva a folyamatról

---

**Kész vagy kezdeni? Kezd az 1. hét feladatokkal!**

**Kérdések?** Tekintsd át a teljes architektúra tervet vagy lépj kapcsolatba a fejlesztő csapattal.

---

**Dokumentum verzió:** 1.0.0
**Utolsó frissítés:** 2025-12-16
**Szerző:** Roo (AI Architect)
