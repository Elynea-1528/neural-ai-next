# Neural AI Next - Core Komponensek Fejlesztési Kontextus

## 1. Rendszerszintű Dokumentáció
- [Rendszer Architektúra](../../docs/architecture/overview.md)
- [Hierarchikus Rendszer](../../docs/architecture/hierarchical_system/overview.md)
- [Modell Struktúra](../../docs/models/hierarchical/structure.md)
- [Dimenzió Processzorok](../../docs/processors/dimensions/overview.md)

## 2. Core Komponensek

### 2.1 Base Komponens
[... korábbi tartalom változatlan ...]

### 2.2 Config Komponens
[... korábbi tartalom változatlan ...]

### 2.3 Logger Komponens
[... korábbi tartalom változatlan ...]

### 2.4 Storage Komponens
[... korábbi tartalom változatlan ...]

### 2.5 MT5 Collector
A MetaTrader 5 platform integrációs komponens architektúrája:

#### 1. Expert Advisor (MQL5)
- Minimális WebSocket szerver funkcionalitás
- OHLCV és tick adatok streamelése
- Order végrehajtás fogadása
- Biztonságos kommunikáció
- Platform független működés
- Titkosított adatátvitel

#### 2. Neural-AI Collector
- EA-val való kommunikáció
- Nyers adatok fogadása és validálása
- Perzisztens tárolás (Storage komponens)
- Adat továbbítás a Dimension Processor felé
- Hibakezelés és újracsatlakozás
- Titkosítási kulcsok kezelése

#### 3. Dimension Processor
- Piaci elemzés és feature engineering
- Multi-timeframe és multi-instrument támogatás
- D1-D15 dimenziók számítása
- Market state detektálás
- Intelligens cache kezelés

#### 4. Neural Core
- Model training és optimalizáció
- Stratégia menedzsment
- Trading signal generálás
- Order és kockázat kezelés
- Teljesítmény monitoring

## 3. Fejlesztési Útmutatók
[... korábbi tartalom változatlan ...]

## 4. Template és Példák ✓
[... korábbi tartalom változatlan ...]

## 5. Aktuális Feladatok

### 5.1 Dokumentációs Standardizálás ✓
[... korábbi tartalom változatlan ...]

### 5.2 Template Kód Fejlesztés ✓
[... korábbi tartalom változatlan ...]

### 5.3 MT5 Collector Fejlesztés 🚧
- [ ] Expert Advisor implementáció
- [ ] Collector komponens fejlesztés
- [ ] Dimension Processor integráció
- [ ] Tesztelés és optimalizáció

## 6. Könyvtár Struktúra

```
neural_ai/
├── core/                     # Core komponensek
│   ├── base/                # Alap infrastruktúra
│   ├── config/              # Konfigurációkezelés
│   ├── logger/              # Naplózás
│   └── storage/             # Adattárolás
├── collectors/              # Adatgyűjtők
│   └── mt5/                # MT5 Collector
│       ├── collector.py    # Fő collector osztály
│       ├── connection.py   # EA kommunikáció
│       └── validator.py    # Adat validáció
├── processors/              # Adatfeldolgozók
├── models/                  # Modell definíciók
└── utils/                   # Segédeszközök

tests/                       # Tesztek
└── core/                    # Core tesztek

docs/                        # Dokumentáció
├── architecture/           # Rendszerarchitektúra
├── components/            # Komponens dokumentáció
├── development/          # Fejlesztői útmutatók
└── templates/            # Kód sablonok
```

## 7. Következő lépések

1. MT5 Collector Fejlesztés:
   - Expert Advisor implementáció (MQL5)
   - Neural-AI Collector komponens
   - Dimension Processor integráció
   - Tesztelés és dokumentáció

2. CI/CD pipeline bővítés:
   - Továbbfejlesztett típusellenőrzés
   - Biztonsági scan
   - Teljes körű tesztelés

3. Dokumentáció bővítés:
   - Példakód gyűjtemény
   - Telepítési útmutató
   - Hibaelhárítási útmutató
