# Adatgyűjtési Stratégia Átfogó - Teljes Dokumentáció

**Projekt:** Neural AI Next - MT5 Collector Fejlesztés
**Dátum:** 2025-12-16
**Verzió:** 1.0.0
**Állapot:** ✅ Kész implementációra

---

## Fordítás állapota

✅ **Teljes dokumentum lefordítva**
✅ **Minden szakasz magyar nyelven**
✅ **Markdown formázás megtartva**
✅ **Linkek a magyar fájlokra frissítve**
⚠️ **Implementáció állapota: Tervezési fázis**

---

## 📚 Dokumentáció áttekintés

Ez a könyvtár tartalmazza az MT5 Collector adatgyűjtési stratégia átfogó architektúra és implementációs tervét.

### 📄 Fő dokumentumok

1. **[`adatgyujtesi_strategia_atfogo.md`](adatgyujtesi_strategia_atfogo.md)** - Teljes architektúra terv
   - Vezetői összefoglaló
   - Jelenlegi állapot elemzése
   - Javasolt architektúra
   - Adatfolyam diagramok
   - Adatraktár szerkezet
   - API specifikációk
   - Adatminőségi keretrendszer
   - Képzési adathalmaz szervezés
   - Implementációs terv (10 hét)
   - Kockázatértékelés

2. **[`implementacio_gyors_kezdes.md`](implementacio_gyors_kezdes.md)** - Gyorsindítási útmutató
   - Fázisról fázisra implementáció
   - Hétről hétre feladatok
   - API referenciák
   - Siker kritériumok
   - Gyorsindítás ellenőrzőlista

3. **[`rendszer_architektura_diagramok.md`](rendszer_architektura_diagramok.md)** - Vizuális diagramok
   - 15 Mermaid diagram
   - Rendszer architektúra
   - Adatfolyamok
   - API végpontok
   - Tároló szerkezet
   - Monitorozás és riasztás

4. **[`mql5_ea_historikus_bovites_spec.md`](mql5_ea_historikus_bovites_spec.md)** - MQL5 EA specifikáció
   - Részletes funkció specifikációk
   - Kód példák
   - Hibakezelés
   - Teljesítmény optimalizálás
   - Tesztelési stratégia
   - Telepítési ellenőrzőlista

---

## 🎯 Amit építünk

### Öt kulcsképesség

1. **✅ Történelmi adatgyűjtés (25 év)**
   - Gyűjts 25 év történelmi adatot modellképzéshez
   - Támogasd mind a 4 instrumentum × 6 időkeret = 24 kombinációt
   - Köteg alapú gyűjtés folyamat követéssel
   - Hiba helyreállítás és folytatási képesség

2. **✅ Növekményes frissítések (3-12 hónap)**
   - Automatikus napi frissítések adatfrissességért
   - Hézag detektálás és automatikus kitöltés
   - Ütemezett karbantartás (2 AM napi)
   - Értesítési rendszer problémákra

3. **✅ Bővített valós idejű gyűjtés**
   - Jelenlegi funkcionalitás változatlanul folytatódik
   - Javított hibakezelés
   - Jobb naplózás és monitorozás
   - Teljesítmény optimalizálások

4. **✅ Adatminőségi keretrendszer**
   - 3 szintű validáció (Alap, Statisztikai, Konzisztencia)
   - Automatikus minőség pontozás (0-100%)
   - Valós idejű monitorozó vezérlőpult
   - Riasztó rendszer minőségi problémákra

5. **✅ Képzési adathalmaz szervezés**
   - 4 szegregált adathalmaz típus:
     - **Újraképzés** (1 év, heti frissítések)
     - **Közepes** (5 év, havi frissítések)
     - **Mély tanulás** (25 év, éves frissítések)
     - **Validáció** (6 hónap, soha nincs a képzésben)
   - Automatikus adathalmaz generálás
   - Minőségi szűrés és jellemző mérnökség
   - Verziózás és metaadat menedzsment

---

## 🏗️ Architektúra kiemelések

### Rendszer komponensek

```
┌─────────────────────────────────────────────────────────────┐
│                    MQL5 Expert Advisor                      │
│  • Valós idejű tick & OHLCV gyűjtés                         │
│  • Történelmi adat kötegelt lekérés                         │
│  • Folyamat követés & hibakezelés                           │
└────────────────────────┬────────────────────────────────────┘
                          │ HTTP/JSON
                          │
┌────────────────────────▼────────────────────────────────────┐
│                  FastAPI Szerver (Python)                   │
│  • API végpontok (valós idejű, történelmi, képzési)         │
│  • Adat validáció & minőségellenőrzések                     │
│  • Job menedzsment & ütemezés                               │
│  • Hézag detektálás & kitöltés                              │
└────────────────────────┬────────────────────────────────────┘
                          │
          ┌───────────────┴───────────────┐
          │                               │
┌────────▼────────┐            ┌────────▼────────┐
│  Adatraktár     │            │  Képzési halmazok│
│  • Történelmi   │            │  • 4 kategória  │
│  • Frissítés    │            │  • Auto-gen     │
│  • Valós idejű  │            │  • Minőség      │
│  • Validált     │            │    szűrt        │
└─────────────────┘            └─────────────────┘
```

### Adatraktár szerkezet

```
data/
├── collectors/mt5/          # Nyers adatok (30-90 nap)
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

## 🚀 Implementációs idővonal

### 1. fázis: Történelmi adatgyűjtés (4 hét)
- **1. hét:** MQL5 EA bővítmények
- **2. hét:** FastAPI szerver bővítmények
- **3. hét:** Tárolás és validáció
- **4. hét:** Integráció és tesztelés

### 2. fázis: Növekményes frissítések (2 hét)
- **5. hét:** Ütemező és automatizálás
- **6. hét:** Monitorozás és karbantartás

### 3. fázis: Képzési adathalmaz generálás (2 hét)
- **7. hét:** Adathalmaz generátor
- **8. hét:** Adathalmaz menedzsment

### 4. fázis: Adatminőségi keretrendszer (2 hét)
- **9. hét:** Fejlett validáció
- **10. hét:** Minőség monitorozás

**Összesen: 10 hét**

---

## 📊 Kulcs metrikák

### Technikai siker kritériumok
- ✅ 100% adatlefedettség a kért dátumtartományokra
- ✅ >95% adatminőség pontszám
- ✅ <24 óra 25 év gyűjtése (instrumentum/időkeretenként)
- ✅ <1GB tároló évente instrumentum/időkeretenként

### Operációs siker kritériumok
- ✅ 99.9% collector uptime
- ✅ <1 másodperc valós idejű adat késés
- ✅ <0.1% hibaráta
- ✅ <5 perc job helyreállítási idő

---

## 🔧 Technológiai stack

### Backend
- **Python 3.x** FastAPI-val
- **Pandas** adatfeldolgozáshoz
- **FastParquet** hatékony tároláshoz
- **Pydantic** adatvalidációhoz
- **APScheduler** job ütemezéshez

### MQL5 Expert Advisor
- **Több instrumentum** támogatás (4 instrumentum)
- **Több időkeret** támogatás (6 időkeret)
- **HTTP kommunikáció** FastAPIval
- **Kötegelt feldolgozás** történelmi adatokhoz

### Tárolás
- **Parquet formátum** (elsődleges) - Tömörített, gyors lekérdezés
- **JSONL formátum** (másodlagos) - Csak hozzáfűzés, könnyű hibakeresés
- **CSV formátum** (harmadlagos) - Ember által olvasható exportok

---

## 🎯 API végpontok

### Történelmi adatgyűjtés
```
POST   /api/v1/historical/request      # Történelmi adatkérés
GET    /api/v1/historical/status/{id}  # Job állapot ellenőrzése
POST   /api/v1/historical/collect     # EA adatokat küld
POST   /api/v1/historical/progress    # Folyamat jelentése
POST   /api/v1/historical/error       # Hibák jelentése
```

### Hézag detektálás és kitöltés
```
GET    /api/v1/data/gaps              # Hézagok azonosítása
POST   /api/v1/data/fill-gaps         # Hézagok kitöltése
```

### Képzési adathalmaz generálás
```
POST   /api/v1/training/generate      # Adathalmaz generálása
GET    /api/v1/training/status/{id}   # Állapot ellenőrzése
```

### Monitorozás
```
GET    /api/v1/storage/stats          # Tároló statisztikák
GET    /api/v1/validation/report      # Minőségi jelentés
GET    /api/v1/errors/report          # Hiba jelentés
```

---

## 💡 Fő jellemzők

### 1. Intelligens kötegelt feldolgozás
- Konfigurálható kötegek (alapértelmezett: 365 nap)
- Automatikus optimalizálás időkeret alapján
- Folyamat követés és jelentés
- Folytatási képesség megszakított jobokhoz

### 2. Átfogó adatminőség
- 3 szintű validációs folyamat
- Valós idejű minőség pontozás
- Automatikus hézag detektálás
- Statisztikai anomália detektálás

### 3. Rugalmas képzési adathalmazok
- 4 adathalmaz típus különböző használati esetekre
- Automatikus generálás és frissítés
- Minőségi szűrés és jellemző mérnökség
- Verziózás és metaadat követés

### 4. Robusztus hibakezelés
- Automatikus újrapróbálkozás exponenciális backoffel
- Gracióz hiba helyreállítás
- Részletes hiba naplózás
- Helyreállítási javaslatok

### 5. Automatikus karbantartás
- Napi növekményes frissítések
- Heti képzési adathalmaz frissítés
- Havi minőségi auditok
- Automatikus hézag kitöltés

---

## 📈 Előnyök

### Modell képzéshez
- ✅ 25 év magas minőségű történelmi adat
- ✅ Szegregált adathalmazok különböző modelltípusokhoz
- ✅ Automatikus adathalmaz generálás
- ✅ Minőség szűrt adatok

### Műveletekhez
- ✅ Automatikus adatgyűjtés és frissítések
- ✅ Átfogó monitorozás és riasztás
- ✅ Robusztus hibakezelés és helyreállítás
- ✅ Hatékony tárolás tömörítéssel

### Fejlesztéshez
- ✅ Tiszta, moduláris architektúra
- ✅ Jól dokumentált API
- ✅ Átfogó tesztelési stratégia
- ✅ Könnyű bővíthető és karbantartható

---

## 🚨 Kockázat enyhítés

### Fő kockázatok és megoldások

1. **MT5 API korlátozások**
   - ✅ Megoldás: Nagy kérések darabolása, rátelimítés
   - ✅ Tesztelés kis tartományokkal először

2. **Tároló kapacitás**
   - ✅ Megoldás: Igények becslése, tömörítés használata
   - ✅ Cloud tárolás fontolóra vétele történelmi adatokhoz

3. **Adatminőségi problémák**
   - ✅ Megoldás: Átfogó 3 szintű validáció
   - ✅ Automatikus tisztító folyamat
   - ✅ Kézi ellenőrzés gyanús adatokra

4. **Teljesítmény szűk keresztmetszetek**
   - ✅ Megoldás: Párhuzamos feldolgozás, gyorsítótár, optimalizálás

---

## 📋 Implementációs ellenőrzőlista

### Implementáció előtt
- [ ] Összes dokumentáció áttekintése
- [ ] Tároló igények becslése
- [ ] Fejlesztői környezet beállítása
- [ ] MQL5 EA kód áttekintése

### 1. fázis (1-4. hét)
- [ ] MQL5 EA bővítése történelmi funkciókkal
- [ ] Történelmi adat API végpontok implementálása
- [ ] Tároló réteg kiterjesztése
- [ ] Köteg validáció implementálása
- [ ] End-to-end tesztelés

### 2. fázis (5-6. hét)
- [ ] Ütemező implementálása
- [ ] Növekményes frissítések hozzáadása
- [ ] Monitorozó vezérlőpult építése

### 3. fázis (7-8. hét)
- [ ] Adathalmaz generátor létrehozása
- [ ] Minőségi szűrés implementálása
- [ ] Adathalmaz menedzsment hozzáadása

### 4. fázis (9-10. hét)
- [ ] Fejlett validáció
- [ ] Minőség monitorozás
- [ ] Végső tesztelés és dokumentáció

---

## 🎓 Tanulási források

### MQL5 dokumentáció
- [MQL5 referencia](https://www.mql5.com/en/docs)
- [CopyRates funkció](https://www.mql5.com/en/docs/series/copyrates)
- [WebRequest funkció](https://www.mql5.com/en/docs/common/webrequest)

### Python FastAPI
- [FastAPI dokumentáció](https://fastapi.tiangolo.com/)
- [Pydantic validáció](https://docs.pydantic.dev/)
- [Pandas dokumentáció](https://pandas.pydata.org/docs/)

### Parquet formátum
- [Parquet specifikáció](https://parquet.apache.org/documentation/latest/)
- [FastParquet dokumentáció](https://fastparquet.readthedocs.io/)

---

## 🤝 Csapat együttműködés

### Szerepkörök és felelősségek

**Architekt (Roo)**
- ✅ Teljes architektúra tervezés
- ✅ Technikai specifikációk
- ✅ Implementációs tervezés

**MQL5 fejlesztő**
- EA bővítmények implementálása
- Történelmi adatlekérés tesztelése
- Kötegelt feldolgozás optimalizálása

**Python fejlesztő**
- FastAPI végpontok implementálása
- Adatfeldolgozó folyamat építése
- Monitorozó eszközök létrehozása

**Adatmérnök**
- Adatraktár szerkezet tervezése
- Tároló réteg implementálása
- Adatfeldolgozás optimalizálása

**QA mérnök**
- Összes funkcionalitás tesztelése
- Adatminőség validálása
- Teljesítmény tesztelés

---

## 📞 Támogatás és kérdések

Kérdésekre vagy pontosításokra ezzel az architektúrával kapcsolatban:

1. **Tekintsd át a dokumentációt** - A legtöbb kérdésre választ adnak a részletes dokumentumok
2. **Nézd meg a diagramokat** - A vizuális ábrázolások segítenek megérteni a folyamatokat
3. **Lásd a gyorsindítási útmutatót** - Lépésről lépésre implementációs útmutatás
4. **Nézd át az EA specifikációt** - Részletes MQL5 implementációs részletek

---

## 🎉 Következő lépések

1. **Ellenőrzés és jóváhagyás** - A résztvevők ellenőrzik a teljes architektúrát
2. **Implementáció indítása** - Kezdd az 1. fázis, 1. hét feladataival
3. **Iteráció** - Rendszeres ellenőrzések és beállítások visszajelzés alapján
4. **Telepítés** - Fokozatos bevezetés alapos teszteléssel

---

## 📝 Dokumentum történet

- **v1.0.0** (2025-12-16): Kezdeti teljes architektúra
  - Mind a 4 fő dokumentum létrehozva
  - 15 architektúra diagram
  - Teljes API specifikációk
  - 10 hetes implementációs terv
  - MQL5 EA részletes specifikáció

---

## ✅ Teljesítmények összefoglaló

### Dokumentáció (4 fájl)
- ✅ Teljes architektúra terv (1274 sor)
- ✅ Gyorsindítási útmutató (átfogó)
- ✅ Rendszer diagramok (15 Mermaid diagram)
- ✅ MQL5 EA specifikáció (részletes)

### Architektúra komponensek
- ✅ Történelmi adatgyűjtési rendszer
- ✅ Növekményes frissítés automatizálás
- ✅ Adatminőségi keretrendszer
- ✅ Képzési adathalmaz szervezés
- ✅ Monitorozás és riasztás

### Implementációs terv
- ✅ 10 hetes fázisos megközelítés
- ✅ Hétről hétre feladatok
- ✅ Kockázatértékelés
- ✅ Siker kritériumok

---

**Kész vagy implementálni? Kezd az [`implementacio_gyors_kezdes.md`](implementacio_gyors_kezdes.md)-el!**

**Kérdések? Tekintsd át a részletes architektúrát az [`adatgyujtesi_strategia_atfogo.md`](adatgyujtesi_strategia_atfogo.md)-ban.**

---

**Dokumentum verzió:** 1.0.0
**Utolsó frissítés:** 2025-12-16
**Szerző:** Roo (AI Architect)
**Állapot:** ✅ Kész és kész implementációra
