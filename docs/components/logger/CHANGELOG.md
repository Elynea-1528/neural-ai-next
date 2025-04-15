# Változási Napló

## [1.0.0] - 2025-04-15

### Hozzáadva
- Alap logger implementáció
- Színes konzol logger támogatás
- Fájl alapú logger rotációs támogatással
- Logger Factory a példányosításhoz
- Színes formázó implementáció
- Részletes dokumentáció és példák
- Egységtesztek teljes lefedettséggel

### Támogatott Funkciók
- Különböző log szintek (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Színes konzol kimenet ANSI színkódokkal
- Méret alapú log rotáció
- Idő alapú log rotáció
- Automatikus log tömörítés
- Testreszabható formátumok
- Extra kontextus információk támogatása

### Technikai Részletek
- Python 3.12+ kompatibilitás
- Típus annotációk
- Nincsenek külső függőségek
- Thread-safe működés

### Ismert Problémák
- Windows rendszereken a színes kimenet extra konfigurációt igényelhet
- A log rotáció atomi műveletei nagy terhelés esetén blokkolhatnak