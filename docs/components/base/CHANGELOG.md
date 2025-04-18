# Base Komponens Changelog

Minden jelentős változás ebben a fájlban kerül dokumentálásra.

A formátum a [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) alapján készült,
és a projekt a [Semantic Versioning](https://semver.org/spec/v2.0.0.html) elveit követi.

## [0.1.0] - 2025-04-18

### Hozzáadva
- Dependency Injection konténer implementáció
- Core komponensek gyűjtemény
- CoreComponentFactory a komponensek létrehozásához
- Teljes körű dokumentáció
  - README.md az áttekintéshez
  - API referencia
  - Architektúra dokumentáció
- Unit tesztek 100% kódlefedettséggel

### Jellemzők
- Komponensek közötti függőségek automatikus kezelése
- Egységes komponens inicializálás
- Típusbiztos interfészek
- Factory mintán alapuló komponens létrehozás
- Automatikus komponens validáció

### Tervezett jövőbeli fejlesztések
- Lifecycle management
- Dependency injection container plugin rendszer
- Scope kezelés
- Lazy loading támogatás
- Metrika gyűjtés és monitorozás

### Függőségek
- typing-extensions>=4.0.0
- pytest>=7.0.0 (csak fejlesztéshez)
- pytest-cov>=3.0.0 (csak fejlesztéshez)

### Kapcsolódó változások
- Core komponensek (Logger, Config, Storage) átalakítása az új architektúra használatához
- Központi függőség kezelés bevezetése
- Egységes inicializálási folyamat bevezetése
