# Logger Komponens Changelog

Minden jelentős változás ebben a fájlban kerül dokumentálásra.

A formátum a [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) alapján készült,
és a projekt a [Semantic Versioning](https://semver.org/spec/v2.0.0.html) elveit követi.

## [0.2.0] - 2025-04-19

### Változások
- Logger factory és implementációk refaktorálása az új base architektúrához
- Egységes interfész implementáció
- Konstruktor paraméterek egységesítése
- Típusozás és típusellenőrzés javítása

### Hozzáadva
- LoggerInterface absztrakt __init__ metódus
- Típusellenőrzött paraméter átadás
- Egységes tesztelési infrastruktúra
- Debug szint megfelelő kezelése
- Handler-ek megfelelő inicializálása
- Fájl rotáció javított támogatása

### Javítva
- Színes logger debug üzenetek megjelenítése
- Handler és formatter inicializálás
- Mock objektumok kezelése tesztekben
- Fájl rotáció és backup kezelés
- Könyvtárkezelés és cleanup a tesztekben

### Kapcsolódó változások
- Base komponens integrációja
- Dependency injection támogatás
- Factory rendszer egységesítése

### Függőségek
- typing-extensions>=4.0.0
- pytest>=7.0.0 (csak fejlesztéshez)
- typing>=3.7.4

## [0.1.0] - 2025-04-15

### Hozzáadva
- Alap logger implementációk
- Színes konzol kimenet támogatás
- Fájl alapú logging
- Log rotáció támogatás
- Hierarchikus logger kezelés
- Dokumentáció
