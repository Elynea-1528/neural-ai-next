# Rendszer Architektúra Diagramok

**Dátum:** 2025-12-16
**Verzió:** 1.0.0

---

## Fordítás állapota

✅ **Teljes dokumentum lefordítva**
✅ **Minden szakasz magyar nyelven**
✅ **Markdown formázás megtartva**
✅ **Mermaid diagramok változatlanok**
⚠️ **Implementáció állapota: Tervezési fázis**

---

Ez a dokumentum az adatgyűjtési rendszer architektúrájának vizuális diagramjait tartalmazza.

---

## 1. Magas szintű rendszer architektúra

```mermaid
graph TB
    subgraph "MT5 Platform"
        EA[MQL5 Expert Advisor]
    end

    subgraph "Python Backend"
        API[FastAPI Szerver]
        VALID[Adat Validátor]
        STORAGE[Tároló Menedzser]
        JOBS[Job Menedzser]
        SCHED[Ütemező]
    end

    subgraph "Adattárolás"
        RAW[Nyers adatok]
        VALIDATED[Validált adatok]
        HIST[Történelmi adatok]
        TRAIN[Képzési adathalmazok]
    end

    subgraph "Monitorozás"
        DASH[Vezérlőpult]
        ALERTS[Riasztások]
        LOGS[Naplók]
    end

    EA -->|HTTP POST| API
    API --> VALID
    VALID --> STORAGE
    STORAGE --> RAW
    STORAGE --> VALIDATED
    STORAGE --> HIST
    STORAGE --> TRAIN

    JOBS --> API
    SCHED --> JOBS

    API --> DASH
    VALID --> DASH
    STORAGE --> DASH
    DASH --> ALERTS
    DASH --> LOGS
```

---

## 2. Adatgyűjtési módok

```mermaid
graph LR
    subgraph "Gyűjtési módok"
        RT[Valós idejű<br/>Tick & OHLCV<br/>Eseményvezérelt]
        HIST[Történelmi<br/>Kötegelt kérések<br/>25 év]
        INC[Növekményes<br/>Napi frissítések<br/>3-12 hónap]
    end

    RT --> STORE[Tárolás]
    HIST --> STORE
    INC --> STORE

    STORE --> TRAIN[Képzési<br/>Adathalmazok]
    STORE --> VALID[Validáció]
```

---

## 3. Valós idejű adatfolyam

```mermaid
sequenceDiagram
    participant EA as MQL5 EA
    participant API as FastAPI
    participant VAL as Validátor
    participant STORE as Tároló
    participant WARE as Raktár

    EA->>API: Tick adatok
    API->>VAL: Validálás
    VAL-->>API: OK/Hiba

    alt Valid
        API->>STORE: Nyers tárolás
        API->>WARE: Validált tárolás
        API-->>EA: Sikeres
    else Invalid
        API->>STORE: Érvénytelen tárolás
        API-->>EA: Figyelmeztetés
    end

    Note over EA,API: Minden Tick Esemény

    EA->>API: OHLCV adatok (60s)
    API->>VAL: Barok validálása
    VAL-->>API: Eredmények

    alt Mind Valid
        API->>STORE: Nyers tárolás
        API->>WARE: Validált tárolás
        API-->>EA: Sikeres
    else Néhány Invalid
        API->>STORE: Valid tárolás
        API->>STORE: Érvénytelen tárolás
        API-->>EA: Részleges siker
    end
```

---

## 4. Történelmi adatgyűjtési folyam

```mermaid
flowchart TD
    A[Történelmi<br/>gyűjtés indítása] --> B[Python: Job létrehozása]
    B --> C[Python: Kérés küldése EAhöz]
    C --> D[EA: Adatlekérés MT5ből]
    D --> E{Adat elérhető?}

    E -->|Igen| F[EA: Köteg küldése]
    E -->|Nem| G[EA: Hiba jelentése]
    G --> H[Python: Hiba naplózása]

    F --> I[Python: Köteg validálása]
    I --> J{Valid?}

    J -->|Igen| K[Python: Köteg tárolása]
    J -->|Nem| L[Python: Érvénytelen tárolása]

    K --> M{További adat?}
    L --> M

    M -->|Igen| D
    M -->|Nem| N[Python: Job befejezése]
    N --> O[Metaadatok frissítése]
    O --> P[Kész]

    H --> P
```

---

## 5. Növekményes frissítési folyam

```mermaid
flowchart TD
    A[Napi ütemező<br/>2:00 AM] --> B[Utolsó frissítés ellenőrzése]
    B --> C{Frissítés szükséges?}

    C -->|Nem| D[Kihagyás]
    C -->|Igen| E[Dátumtartomány kiszámítása]

    E --> F[Kérés EAtól]
    F --> G[Adat gyűjtése]
    G --> H[Validálás]

    H --> I{Valid?}
    I -->|Nem| J[Hiba naplózása]
    I -->|Igen| K[Raktárban tárolás]

    K --> L[Metaadatok frissítése]
    L --> M[Hézagok ellenőrzése]

    M --> N{Hézagok találva?}
    N -->|Nem| O[Befejezve]
    N -->|Igen| P[Hézag kitöltés indítása]

    P --> Q[Hézagok kitöltése]
    Q --> O

    J --> O
    D --> O
```

---

## 6. Képzési adathalmaz generálási folyam

```mermaid
flowchart TD
    A[Adathalmaz generátor] --> B[Adathalmaz típus kiválasztása]

    B --> C1[Újraképzés<br/>1 Év]
    B --> C2[Közepes<br/>5 Év]
    B --> C3[Mély tanulás<br/>25 Év]
    B --> C4[Validáció<br/>6 Hónap]

    C1 --> D[Raktárból betöltés]
    C2 --> D
    C3 --> D
    C4 --> D

    D --> E[Minőségi szűrők alkalmazása]
    E --> F{Minőség OK?}

    F -->|Nem| G[Figyelmeztetés naplózása]
    F -->|Igen| H[Jellemzők mérnöksége]

    H --> I[Adatok felosztása]
    I --> J[Adathalmaz tárolása]

    J --> K[Metaadatok generálása]
    K --> L[Katalógus frissítése]

    G --> L
```

---

## 7. Adatraktár szerkezet

```mermaid
graph TD
    ROOT[data/] --> COLL[collectors/mt5/]
    ROOT --> WARE[warehouse/]
    ROOT --> TRAIN[training/]
    ROOT --> META[metadata/]

    COLL --> RAW[raw/]
    COLL --> INVALID[invalid/]

    RAW --> RTICKS[ticks/]
    RAW --> ROHLCV[ohlcv/]

    RTICKS --> RT_EUR[EURUSD/]
    RTICKS --> RT_GBP[GBPUSD/]
    RTICKS --> RT_JPY[USDJPY/]
    RTICKS --> RT_XAU[XAUUSD/]

    ROHLCV --> RO_EUR[EURUSD/]
    ROHLCV --> RO_GBP[GBPUSD/]
    ROHLCV --> RO_JPY[USDJPY/]
    ROHLCV --> RO_XAU[XAUUSD/]

    WARE --> WHIST[historical/]
    WARE --> WUPDATE[update/]
    WARE --> WREAL[realtime/]
    WARE --> WVALID[validated/]

    WHIST --> WH_EUR[EURUSD 25év]
    WHIST --> WH_GBP[GBPUSD 25év]
    WHIST --> WH_JPY[USDJPY 25év]
    WHIST --> WH_XAU[XAUUSD 25év]

    TRAIN --> TRET[retraining/]
    TRAIN --> TMED[medium/]
    TRAIN --> TDEEP[deep_learning/]
    TRAIN --> TVAL[validation/]

    TRET --> TR_EUR[EURUSD 1év]
    TMED --> TM_EUR[EURUSD 5év]
    TDEEP --> TD_EUR[EURUSD 25év]
    TVAL --> TV_EUR[EURUSD 6hó]

    META --> MI[instruments.json]
    META --> MT[timeframes.json]
    META --> MQ[data_quality.json]
    META --> MJ[collection_jobs.json]
```

---

## 8. API végpont architektúra

```mermaid
graph TB
    API[FastAPI Szerver] --> RT[Valós idejű végpontok]
    API --> HIST[Történelmi végpontok]
    API --> GAP[Hézag végpontok]
    API --> TRAIN[Képzési végpontok]
    API --> MON[Monitorozó végpontok]

    RT --> RT1[POST /collect/tick]
    RT --> RT2[POST /collect/ohlcv]
    RT --> RT3[GET /validation/report]

    HIST --> H1[POST /historical/request]
    HIST --> H2[GET /historical/status/{id}]
    HIST --> H3[POST /historical/collect]

    GAP --> G1[GET /data/gaps]
    GAP --> G2[POST /data/fill-gaps]

    TRAIN --> T1[POST /training/generate]
    TRAIN --> T2[GET /training/status/{id}]

    MON --> M1[GET /storage/stats]
    MON --> M2[GET /errors/report]
```

---

## 9. Adatminőség validációs folyamat

```mermaid
flowchart LR
    A[Nyers adatok] --> B[1. szint: Alap]

    B --> C{Sikeres?}
    C -->|Nem| D[Érvénytelen tárolás]
    C -->|Igen| E[2. szint: Statisztikai]

    E --> F{Sikeres?}
    F -->|Nem| D
    F -->|Igen| G[3. szint: Konzisztencia]

    G --> H{Sikeres?}
    H -->|Nem| D
    H -->|Igen| I[Validált tárolás]

    D --> J[Hiba naplózása]
    I --> K[Minőség pontszám frissítése]

    J --> L[Minőségi jelentés]
    K --> L
```

**Validációs szintek:**

1. **1. szint - Alap:** Adattípusok, tartományok, kapcsolatok
2. **2. szint - Statisztikai:** Kiugró értékek, hézagok, duplikátumok
3. **3. szint - Konzisztencia:** Keresztvalidáció, korrelációk

---

## 10. Job menedzsment rendszer

```mermaid
graph TB
    REQ[Felhasználói kérés] --> JM[Job Menedzser]

    JM --> QUEUE[Job várólista]
    QUEUE --> J1[Job 1: Történelmi EURUSD M1]
    QUEUE --> J2[Job 2: Történelmi GBPUSD M1]
    QUEUE --> J3[Job 3: Hézag kitöltés]

    J1 --> STATUS[Állapot követés]
    J2 --> STATUS
    J3 --> STATUS

    STATUS --> PROG[Folyamat monitorozás]
    PROG --> LOG[Job naplók]

    STATUS --> COMPLETE{Kész?}
    COMPLETE -->|Igen| NOTIFY[Felhasználó értesítése]
    COMPLETE -->|Nem| WAIT[Folytatás]

    WAIT --> PROG

    NOTIFY --> EMAIL[Email/Slack]
    NOTIFY --> DASH[Vezérlőpult frissítés]
```

---

## 11. Monitorozás és riasztás

```mermaid
graph TB
    COLL[Adatgyűjtés] --> METRICS[Mérőszámok gyűjtése]

    METRICS --> M1[Adatminőség pontszám]
    METRICS --> M2[Gyűjtési ráta]
    METRICS --> M3[Hibaráta]
    METRICS --> M4[Tároló használat]

    M1 --> DASH[Vezérlőpult]
    M2 --> DASH
    M3 --> DASH
    M4 --> DASH

    DASH --> THRESH{Küszöbérték<br/>túllépve?}

    THRESH -->|Igen| ALERT[Riasztás küldése]
    THRESH -->|Nem| MONITOR[Monitorozás folytatása]

    ALERT --> SLACK[Slack értesítés]
    ALERT --> EMAIL[Email értesítés]
    ALERT --> LOG[Napló bejegyzés]

    MONITOR --> METRICS
```

---

## 12. Hibakezelési folyam

```mermaid
flowchart TD
    A[Művelet] --> B{Hiba?}

    B -->|Nem| C[Siker]
    B -->|Igen| D[Hiba osztályozása]

    D --> E1[Validációs hiba]
    D --> E2[Tároló hiba]
    D --> E3[Hálózati hiba]
    D --> E4[Rendszer hiba]

    E1 --> F1[Érvénytelen adatok tárolása]
    E2 --> F2[Lemezterület ellenőrzése]
    E3 --> F3[Kapcsolat újrapróbálása]
    E4 --> F4[Naplózás és riasztás]

    F1 --> G[Helyreállítási javaslat kérése]
    F2 --> G
    F3 --> G
    F4 --> G

    G --> H[Helyreállítás alkalmazása]
    H --> I{Helyreállítva?}

    I -->|Igen| C
    I -->|Nem| J[Eskaláció]

    J --> K[Kézi beavatkozás]
```

---

## 13. Tároló megőrzési politika

```mermaid
gantt
    title Adat megőrzési idővonal
    dateFormat YYYY-MM-DD
    section Nyers adatok
    Tickek 30nap           :active, ticks, 2025-11-16, 30d
    OHLCV 90nap           :active, ohlcv, 2025-09-17, 90d
    Érvénytelen 1év          :active, invalid, 2024-12-16, 365d

    section Raktár
    Történelmi Állandó :active, hist, 2000-01-01, 9500d
    Frissítés 1év           :active, update, 2024-12-16, 365d
    Valós idejű 30nap        :active, real, 2025-11-16, 30d

    section Képzés
    Újraképzés Állandó :active, retrain, 2024-01-01, 730d
    Közepes Állandó     :active, medium, 2020-01-01, 2190d
    Mély tanulás Áll   :active, deep, 2000-01-01, 9500d
    Validáció Állandó :active, valid, 2025-06-01, 180d
```

---

## 14. Teljes rendszer áttekintés

```mermaid
graph TB
    subgraph "Adatforrások"
        MT5[MT5 Platform]
    end

    subgraph "Gyűjtési réteg"
        EA[MQL5 Expert Advisor]
        API[FastAPI Szerver]
    end

    subgraph "Feldolgozási réteg"
        VAL[Adat Validátor]
        PROC[Adat Feldolgozó]
        JOBS[Job Menedzser]
    end

    subgraph "Tárolási réteg"
        STOR[Tároló Menedzser]
        WARE[Adatraktár]
        TRAIN[Képzési adathalmazok]
    end

    subgraph "Menedzsment réteg"
        SCHED[Ütemező]
        MON[Monitorozás]
        ALERT[Riasztás]
    end

    MT5 --> EA
    EA --> API
    API --> VAL
    API --> JOBS
    VAL --> PROC
    PROC --> STOR
    JOBS --> STOR
    STOR --> WARE
    STOR --> TRAIN

    SCHED --> JOBS
    STOR --> MON
    VAL --> MON
    JOBS --> MON
    MON --> ALERT
```

---

## 15. Telepítési architektúra

```mermaid
graph TB
    subgraph "Termelési környezet"
        SERVER[Linux Szerver]
        DOCKER[Docker Konténerek]
        DB[(PostgreSQL<br/>Metaadatok)]
        STORAGE[Tároló kötetek]
    end

    subgraph "MT5 környezet"
        MT5[MT5 Platform<br/>Windows/Wine]
        EA1[EA példány 1]
        EA2[EA példány 2]
    end

    subgraph "Monitorozás"
        PROM[Prometheus]
        GRAF[Grafana]
        ALERT[Riasztó Menedzser]
    end

    EA1 --> SERVER
    EA2 --> SERVER

    SERVER --> DOCKER
    DOCKER --> APP1[FastAPI App]
    DOCKER --> APP2[Ütemező]
    DOCKER --> APP3[Adathalmaz generátor]

    APP1 --> DB
    APP2 --> DB
    APP3 --> DB

    APP1 --> STORAGE
    APP2 --> STORAGE
    APP3 --> STORAGE

    SERVER --> PROM
    PROM --> GRAF
    GRAF --> ALERT
```

---

**Dokumentum verzió:** 1.0.0
**Utolsó frissítés:** 2025-12-16
**Szerző:** Roo (AI Architect)
