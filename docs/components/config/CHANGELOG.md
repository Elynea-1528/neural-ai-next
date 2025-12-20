# Config Komponens Changelog

Minden jelentős változás ebben a fájlban kerül dokumentálásra.

A formátum a [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) alapján készült,
és a projekt a [Semantic Versioning](https://semver.org/spec/v2.0.0.html) elveit követi.

## [0.2.1] - 2025-12-20

### Javítva
- Kritikus logikai hiba a `get_manager` metódusban (61. sor)
  - A `Path.suffix` metódus dupla hívása és hibás értékadás javítva
  - A kiterjesztés helyes kisbetűsítése biztosítva
- Dokumentáció frissítve a `get_manager` metódus aktuális szignatúrájához

### Tesztelés
- Minden teszt sikeresen lefut (8/8)
- 100% tesztlefedettség biztosítva
- Ruff és MyPy ellenőrzések sikeresek

## [0.2.0] - 2025-04-18

### Változások
- ConfigManagerFactory refaktorálás az új base architektúrához
- Egységes interfész implementálás
- Konstruktor paraméterek javítása
- Típusozás és típusellenőrzés javítása

### Hozzáadva
- ConfigManagerInterface absztrakt __init__ metódus
- Típusellenőrzött paraméter átadás
- Egységes tesztelési infrastruktúra

### Javítva
- Típusozási problémák a factory-ban
- Hiányzó interfész definíciók
- Nem megfelelő paraméter átadások

### Kapcsolódó változások
- Base komponens integrációja
- Dependency injection támogatás
- Factory rendszer egységesítése

### Függőségek
- typing-extensions>=4.0.0
- pyyaml>=6.0.0
- pytest>=7.0.0 (csak fejlesztéshez)

## [0.1.0] - 2025-04-15

### Hozzáadva
- Alap YAML konfiguráció kezelés
- Konfigurációs fájl betöltés és mentés
- Hierarchikus konfiguráció kezelés
- Validációs rendszer
- Dokumentáció
