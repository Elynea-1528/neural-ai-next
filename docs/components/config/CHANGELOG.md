# Változási Napló

## [1.0.0] - 2025-04-15

### Hozzáadva
- Alap konfiguráció kezelő interfész
- YAML konfiguráció kezelő implementáció
- Konfiguráció kezelő factory
- Séma alapú validáció
- Hierarchikus konfiguráció támogatás
- Típus-biztos konfigurációs értékek
- Konfigurációs fájlok betöltése és mentése
- Alapértelmezett értékek kezelése
- Részletes dokumentáció

### Támogatott Funkciók
- YAML formátum támogatása
- Beágyazott konfigurációs értékek
- Több szintű validáció:
  - Típus ellenőrzés
  - Érték korlátok
  - Választható értékek
  - Kötelező mezők
- Konfigurációk mentése és betöltése
- Factory pattern alapú manager létrehozás
- Bővíthető formátum támogatás

### Technikai Részletek
- Python 3.12+ kompatibilitás
- PyYAML függőség
- Típus annotációk
- Tiszta kód elvek
- SOLID alapelvek
- Teljes teszt lefedettség

### Ismert Problémák
- Nagy méretű konfigurációs fájlok memória használata
- YAML fájlok biztonságos betöltése körültekintést igényel
