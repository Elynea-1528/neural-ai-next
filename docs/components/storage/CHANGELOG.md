# Storage Komponens Changelog

Minden jelentős változás ebben a fájlban kerül dokumentálásra.

A formátum a [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) alapján készült,
és a projekt a [Semantic Versioning](https://semver.org/spec/v2.0.0.html) elveit követi.

## [0.1.0] - 2025-04-18

### Hozzáadva
- Alap StorageInterface definiálása
- FileStorage implementáció
  - DataFrame műveletek (CSV, JSON, Excel formátumok)
  - Python objektum szerializáció (JSON formátum)
  - Fájlrendszer műveletek (létezés, metaadatok, törlés, listázás)
- Kivételek hierarchiája
  - StorageError alap kivétel
  - StorageFormatError formátum hibákhoz
  - StorageNotFoundError nem létező erőforrásokhoz
  - StorageSerializationError szerializációs hibákhoz
  - StorageIOError I/O művelet hibákhoz
- Unit tesztek 79%+ kódlefedettséggel
- Részletes dokumentáció
  - API referencia
  - Architektúra leírás
  - Tervezési specifikáció
  - Fejlesztői checklist
  - Használati példák

### Változtatva
- A DataFrame műveletek alapértelmezett formátuma CSV
- Az objektum műveletek alapértelmezett formátuma JSON

### Javítva
- CSV DataFrame mentés/betöltés index kezelése
- Útvonal normalizálás Windows rendszereken
- Kivételek hierarchiája és üzenetei

### Biztonsági javítások
- Útvonal manipuláció elleni védelem
- Jogosultságok ellenőrzése műveletek előtt

### Függőségek
- pandas>=1.5.0
- typing-extensions>=4.0.0
