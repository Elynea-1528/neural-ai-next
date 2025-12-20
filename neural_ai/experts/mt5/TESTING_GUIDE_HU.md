# Történelmi Adatgyűjtés Tesztelési Útmutató

**Dátum:** 2025-12-16
**Cél:** A történelmi adatgyűjtés funkció tesztelése

---

## Előkészületek

### 1. FastAPI Szerver Indítása

Győződj meg róla, hogy a FastAPI szerver fut:

```bash
cd /home/elynea/Dokumentumok/neural-ai-next
python -m neural_ai
```

Vagy alternatívaként:

```bash
uvicorn neural_ai:app --host 0.0.0.0 --port 8000
```

### 2. MT5 Indítása

Indítsd el az MT5-öt Wine-on keresztül:

```bash
wine /home/elynea/.mt5/drive_c/Program\ Files/MetaTrader\ 5/terminal64.exe
```

### 3. EA Telepítése

1. Nyisd meg az MT5-öt
2. Menj a Navigator panelre
3. Keress rá: **Neural_AI_Next_Multi**
4. Húzd az EA-t egy chartra (pl. EURUSD H1)

---

## Konfiguráció

### EA Beállítások

Állítsd be a következő paramétereket:

```
FastAPI Server: http://localhost:8000
Update Interval: 60
Enable HTTP Logs: true
Enable Historical Collection: true
Max Historical Batch Days: 365
Historical Request Timeout: 300
Log Historical Requests: true
```

---

## Tesztesetek

### 1. Alapvető Kapcsolódás Teszt

**Cél:** Ellenőrizni, hogy az EA csatlakozik-e a szerverhez

**Lépések:**
1. Indítsd el az EA-t
2. Nyisd meg az Experts logot (Ctrl+M)
3. Ellenőrizd a következő üzeneteket:

```
✓ Csatlakozva a FastAPI szerverhez: http://localhost:8000
✓ Figyelés 4 instrumentum
✓ Figyelés 6 időkeret
✓ Történelmi adatgyűjtés: ENGEDÉLYEZVE
✓ Max kötegméret: 365 nap
```

**Elvárt eredmény:** Minden ✓ jelzés megjelenik

---

### 2. Történelmi Adatkérés Küldése

**Cél:** Tesztelni a történelmi adatkérés fogadását

**Lépések:**

1. **Küldj egy HTTP POST kérést a szervernek:**

```bash
curl -X POST "http://localhost:8000/api/v1/historical/request" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "test_job_001",
    "symbol": "EURUSD",
    "timeframe": "M1",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "batch_size_days": 30
  }'
```

2. **Várj 10 percet** (az EA 10 percenként ellenőrzi az új kéréseket)

3. **Ellenőrizd az Experts logot:**

```
Történelmi adatkérés fogadva: {...}
Történelmi kérés validálva:
  Job ID: test_job_001
  Szimbólum: EURUSD
  Időkeret: M1
  Dátumtartomány: 2024.01.01 00:00 to 2024.01.31 00:00
  Kötegméret: 30 nap
  Összes köteg: 1
Új történelmi adat job indult: test_job_001
```

**Elvárt eredmény:** A kérés sikeresen feldolgozásra kerül

---

### 3. Adatgyűjtés Folyamat Követése

**Cél:** Ellenőrizni az adatgyűjtés folyamatát

**Lépések:**

1. Várj 1-2 percet a kérés elküldése után
2. Ellenőrizd az Experts logot:

```
Lekérve 43200 bar az 1. kötethez (2024.01.01 00:00 to 2024.01.31 23:59)
Köteg 1 sikeresen elküldve: 43200 bar
Folyamat jelentve: 100% (1/1)
Történelmi adatgyűjtés befejezve jobhoz: test_job_001
```

**Elvárt eredmény:** Az adatok sikeresen lekérdezve és elküldve

---

### 4. Hosszú Távú Adatgyűjtés Teszt

**Cél:** Tesztelni a hosszú távú adatgyűjtést több köteggel

**Lépések:**

1. **Küldj egy nagyobb dátumtartományú kérést:**

```bash
curl -X POST "http://localhost:8000/api/v1/historical/request" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "test_job_002",
    "symbol": "EURUSD",
    "timeframe": "H1",
    "start_date": "2023-01-01",
    "end_date": "2024-12-31",
    "batch_size_days": 90
  }'
```

2. **Figyeld a folyamatot:**

```
Folyamat jelentve: 0% (0/8)
Folyamat jelentve: 12% (1/8)
Folyamat jelentve: 25% (2/8)
...
Folyamat jelentve: 100% (8/8)
Történelmi adatgyűjtés befejezve jobhoz: test_job_002
```

**Elvárt eredmény:** Minden köteg sikeresen feldolgozásra kerül

---

### 5. Hibakezelés Teszt

**Cél:** Ellenőrizni a hibakezelést

**Lépések:**

1. **Küldj egy érvénytelen kérést:**

```bash
curl -X POST "http://localhost:8000/api/v1/historical/request" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "test_job_003",
    "symbol": "INVALID_SYMBOL",
    "timeframe": "M1",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  }'
```

2. **Ellenőrizd a hibanaplót:**

```
Hiba: Érvénytelen történelmi kérés paraméterek
```

**Elvárt eredmény:** Az EA észleli a hibát és nem indul el a job

---

## API Végpontok Tesztelése

### Health Check

```bash
curl "http://localhost:8000/api/v1/ping"
```

**Elvárt válasz:**
```json
{
  "status": "ok",
  "message": "MT5 Collector is running"
}
```

### Történelmi Kérés Poll

```bash
curl "http://localhost:8000/api/v1/historical/poll"
```

**Elvárt válasz:** Üres JSON vagy egy aktív kérés

---

## Hibaelhárítás

### 1. EA nem csatlakozik

**Probléma:** "⚠ Figyelmeztetés: Nem sikerült csatlakozni a FastAPI szerverhez"

**Megoldások:**
- Ellenőrizd, hogy a FastAPI szerver fut-e
- Ellenőrizd a `FastAPI_Server` beállítást
- Nyisd meg a böngészőben: `http://localhost:8000/api/v1/ping`

### 2. Nincs történelmi adat

**Probléma:** "Figyelmeztetés: Nem található adat"

**Megoldások:**
- Ellenőrizd az MT5 történelmi adatbázisát
- Nyisd meg: Tools → History Center
- Töltsd le a hiányzó adatokat

### 3. Timeout hiba

**Probléma:** "Hiba: HTTP -1" vagy timeout

**Megoldások:**
- Növeld a `Historical_Request_Timeout` értékét
- Csökkentsd a `Max_Historical_Batch_Days` értékét
- Ellenőrizd a hálózati kapcsolatot

### 4. Kompilációs hiba

**Probléma:** EA nem indul el

**Megoldások:**
- Fordítsd újra az EA-t: `bash scripts/compile_mql.sh neural_ai/experts/mt5/src/Neural_AI_Next_Multi.mq5`
- Ellenőrizd az MT5 logokat: View → Experts

---

## Teljesítmény Tesztelés

### Kis Adatmennyiség (Gyors teszt)

```bash
# 1 hónap M1 adat (kb. 30-40k bar)
curl -X POST "http://localhost:8000/api/v1/historical/request" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "perf_test_small",
    "symbol": "EURUSD",
    "timeframe": "M1",
    "start_date": "2024-12-01",
    "end_date": "2024-12-31",
    "batch_size_days": 30
  }'
```

**Várható idő:** 1-2 perc

### Nagy Adatmennyiség (Teljes teszt)

```bash
# 1 év H1 adat (kb. 8-9k bar)
curl -X POST "http://localhost:8000/api/v1/historical/request" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "perf_test_large",
    "symbol": "EURUSD",
    "timeframe": "H1",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "batch_size_days": 90
  }'
```

**Várható idő:** 5-10 perc

---

## Naplózás Engedélyezése

### Részletes Naplózás

Állítsd be az EA paramétereket:

```
Enable HTTP Logs: true
Log Historical Requests: true
```

### Naplók Megtekintése

1. **MT5 Experts log:**
   - View → Experts
   - Ctrl+M

2. **FastAPI log:**
   - A terminál, ahol a szerver fut

---

## Tesztelési Ellenőrzőlista

- [ ] FastAPI szerver fut
- [ ] MT5 fut és csatlakoztatva van
- [ ] EA telepítve van egy charton
- [ ] EA csatlakozik a szerverhez
- [ ] Történelmi adatgyűjtés engedélyezve van
- [ ] Kérés küldése sikeres
- [ ] Adatok lekérése sikeres
- [ ] Adatok küldése sikeres
- [ ] Progress jelentés működik
- [ ] Hibakezelés működik

---

## Gyors Teszt Parancsok

### Teljes teszt egy parancsban:

```bash
# 1. Ping
curl "http://localhost:8000/api/v1/ping"

# 2. Küldj egy kérést
curl -X POST "http://localhost:8000/api/v1/historical/request" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "quick_test",
    "symbol": "EURUSD",
    "timeframe": "M15",
    "start_date": "2024-12-01",
    "end_date": "2024-12-16",
    "batch_size_days": 15
  }'

# 3. Ellenőrizd a státuszt (10 perc múlva)
curl "http://localhost:8000/api/v1/historical/status/quick_test"
```

---

## Kapcsolódó Dokumentáció

- [Implementáció dokumentáció](HISTORICAL_EXTENSION_IMPLEMENTATION.md:1)
- [Tervezési specifikáció](../../plans/mql5_ea_historikus_bovites_spec.md:1)
- [API dokumentáció](../../docs/components/collectors/mt5/api.md:1)

---

**Készítette:** Roo (AI Architect)
**Dátum:** 2025-12-16
**Verzió:** 1.0.0
