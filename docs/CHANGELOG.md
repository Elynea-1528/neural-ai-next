# Changelog

## [1.1.0] - 2025-12-19

### Added
- Broker választási opciók bővítése csoportos telepítéssel
  - Összes MT5 bróker (MetaQuotes, XM, Dukascopy)
  - Összes JForex bróker (JForex4)
  - Minden bróker telepítése
- Telepítési dokumentáció áthelyezése a `scripts/install/docs/` mappába
- Részletesebb GPU ellenőrzés (memória, CUDA core-ok, compute capability)
- CUDA core becslő funkció a check_installation.py-ban

### Changed
- PyTorch telepítési parancsok javítása a dokumentációban
- Relatív linkek frissítése a scripts/install/docs/INSTALLATION_GUIDE.md-ban
- Telepítő scriptek útvonalainak egységesítése

### Documentation
- Dokumentáció linkek frissítése a scripts/install/ mappából
- Telepítési útmutató bővítése a csoportos broker telepítéssel
- GPU specifikációk hozzáadása az ellenőrző script kimenetéhez

## [1.0.0] - 2025-12-17

### Added
- MT5 Collector komponens teljes implementációja
- Historical Data Manager a 25 éves historikus adatgyűjtéshez
- Data Quality Framework 3-szintű validálással
- Data Warehouse Manager hierarchikus adattároláshoz
- Training Dataset Generator 4 típusú adathalmaz létrehozásához
- MQL5 Expert Advisor bővítése historikus adatgyűjtéssel
- 194 teszteset a komponensekhez
- Modularizált konfigurációs rendszer

### Changed
- Collector config átstrukturálása modularizált formára
- Pre-commit hookok optimalizálása
- Kódminőség javítása (flake8, black, isort)

### Fixed
- Körkörös import problémák
- Típusannotációs hibák
- Kódformázási problémák

### Documentation
- Dokumentáció magyarra fordítása
- PROJECT_STATUS_REPORT.md frissítése valós adatokkal
- DEVELOPMENT_STATUS.md frissítése
- Hiányzó API dokumentációk hozzáadása
