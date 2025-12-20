# MT5 Collector Változások Naplója

A dokumentum az MT5 Collector komponens verzióinak változásait tartalmazza.

## [1.0.0] - 2025-12-16

### Hozzáadva
- **Alapvető Collector struktúra** - Teljes átalakítás a projekt szabványainak megfelelően
- **Interfaces** - `CollectorInterface` és `DataValidatorInterface` implementáció
- **Factory Pattern** - `CollectorFactory` a collectorok létrehozásához
- **Exceptions** - Szabványos kivétel osztályok a hibakezeléshez
- **Mappa struktúra** - Új mappaszerkezet a Logger/Config mintájára
  - `neural_ai/collectors/mt5/interfaces/` - Interfészek
  - `neural_ai/collectors/mt5/implementations/` - Implementációk
  - `neural_ai/collectors/mt5/exceptions.py` - Kivételek
- **Data mappa átszervezés** - Data mappa áthelyezése a főkönyvtárba
  - `data/collectors/mt5/` - Collector specifikus adatok
  - `data/warehouse/` - Data warehouse struktúra
- **Log struktúra** - Strukturált log mappa létrehozása
  - `logs/collectors/mt5/` - Fő log fájlok
  - `logs/collectors/mt5/errors/` - Hiba logok
  - `logs/collectors/mt5/debug/` - Debug logok
- **Experts mappa átszervezés** - Experts mappa újraszervezése
  - `neural_ai/experts/mt5/src/` - Forráskódok
  - `neural_ai/experts/mt5/compiled/` - Lefordított fájlok
  - `neural_ai/experts/mt5/config/` - Konfigurációk
  - `neural_ai/experts/mt5/docs/` - Dokumentáció
- **Dokumentáció** - Teljes dokumentációs struktúra a projekt szabványainak megfelelően
  - `README.md` - Fő áttekintés
  - `api.md` - API dokumentáció
  - `architecture.md` - Architektúra leírás
  - `design_spec.md` - Tervezési specifikáció
  - `development_checklist.md` - Fejlesztési checklist
  - `examples.md` - Használati példák
  - `CHANGELOG.md` - Változások naplója

### Megváltozott
- **Fájlnevek** - Összes fájlnév egységesítése a projekt konvencióinak megfelelően
  - `collector.py` → `mt5_collector.py`
  - `error_handler.py` → `exceptions.py`
- **Importok** - Import utak frissítése az új struktúrához
- **Konfiguráció** - Konfigurációs fájlok frissítése az új elérési utakhoz

### Eltávolítva
- **Régi struktúra** - A régi nem szabványos mappa struktúra
- **Hibás fájlnevek** - Nem konvencionális fájlnevek

### Rögzített
- **Type hints** - Type annotation problémák javítása
- **Import hibák** - Import körkörös függőségek eltávolítása

## [0.9.0] - 2025-12-15

### Hozzáadva
- **DataValidator** - Komprehenzív adatvalidációs rendszer
- **ErrorHandler** - Robusztus hibakezelés és helyreállítás
- **CollectorStorage** - Többformátumú tárolás (JSONL, CSV)
- **Multi-instrument támogatás** - Több instrumentum egyidejű gyűjtése
- **Multi-timeframe támogatás** - Több időkeret támogatása
- **Data Warehouse integráció** - Automatikus adatszervezés

### Megváltozott
- **Adattárolás** - CSV formátum használata OHLCV adatokhoz
- **Logolás** - Dupla logolás (console + file)

## [0.8.0] - 2025-12-14

### Hozzáadva
- **FastAPI szerver** - HTTP alapú kommunikáció
- **Expert Advisor** - MQL5 kód a MetaTrader 5-höz
- **Alapvető adatgyűjtés** - Tick és OHLCV adatok fogadása

## [Unreleased]

### Tervezett
- **További validátorok** - Speciális validátorok különböző adattípusokhoz
- **Adatbázis támogatás** - SQL adatbázisokhoz való csatlakozás
- **Monitorozás** - Web alapú dashboard a collector állapotához
- **Alert rendszer** - Email/SMS értesítések hibák esetén

## Verziószámozás

A projekt [Semantic Versioning](https://semver.org/) szabványt követi:

- **Major (X.0.0):** Visszamenőlegesen nem kompatibilis változtatások
- **Minor (0.X.0):** Új funkciók, visszamenőlegesen kompatibilis változtatások
- **Patch (0.0.X):** Hibajavítások, visszamenőlegesen kompatibilis változtatások

## Kapcsolódó dokumentáció

- [MT5 Collector README](README.md)
- [API Dokumentáció](api.md)
- [Architektúra leírás](architecture.md)
- [Tervezési specifikáció](design_spec.md)
