# Template Fájlok Kód Javítási Feladatok

## Problémák áttekintése

### 1. Docstring formázási hibák
- [ ] D212: Multi-line docstring summaries should start at first line
- [ ] D200: One-line docstrings should fit on one line
- [ ] D403: First word capitalization in docstrings
- [ ] D417: Missing argument descriptions

### 2. Nem használt importok
- [ ] typing importok tisztítása (List, Optional, Union, BinaryIO)
- [ ] numpy as np importok eltávolítása ahol nem használt
- [ ] Felesleges os, sys importok eltávolítása
- [ ] Nem használt egyéb importok (ConfigManagerFactory, DataLoader, stb.)

### 3. Hiányzó vagy hibás típusannotációk
- [ ] Hiányzó függvény paraméter típusok
- [ ] Hiányzó visszatérési érték típusok
- [ ] None visszatérési érték explicit jelölése (-> None)

### 4. Undefined nevek
- [ ] LoggerFactory importálása ahol használva van
- [ ] logging modul importálása
- [ ] StorageFactory referencia javítása

### 5. Kivétel osztályok
- [ ] ConfigNotFoundException létrehozása
- [ ] ConfigParseError létrehozása
- [ ] ConfigSectionNotFoundError létrehozása
- [ ] DataNotFoundError létrehozása
- [ ] InvalidFormatError létrehozása
- [ ] StorageWriteError létrehozása

### 6. Biztonsági problémák
- [ ] pickle használat felülvizsgálata
- [ ] Biztonságos szerializáció implementálása
- [ ] Deszerializáció validálással

## Javítási terv

### 1. Fázis: Docstring standardizálás
1. Google style docstring template létrehozása
2. Docstring checker script implementálása
3. Minden docstring javítása a szabványnak megfelelően

### 2. Fázis: Import optimalizálás
1. Import használat elemzése
2. Nem használt importok eltávolítása
3. Hiányzó importok hozzáadása
4. Import sorrend optimalizálása

### 3. Fázis: Típusrendszer javítások
1. Típusannotáció checker script implementálása
2. Hiányzó típusannotációk pótlása
3. Visszatérési értékek explicit jelölése
4. Type stub fájlok létrehozása ahol szükséges

### 4. Fázis: Kivételkezelés egységesítése
1. Kivétel osztályok implementálása
2. Kivételkezelési stratégia dokumentálása
3. Kivételek egységes használatának bevezetése

### 5. Fázis: Biztonsági fejlesztések
1. pickle alternatívák értékelése
2. Biztonságos szerializáció implementálása
3. Deszerializációs validátorok implementálása
4. Biztonsági dokumentáció frissítése

## Végrehajtási prioritások

1. Magas prioritás
   - Undefined nevek javítása
   - Hiányzó típusannotációk pótlása
   - Kritikus docstring hibák javítása

2. Közepes prioritás
   - Import tisztítás
   - Kivétel osztályok implementálása
   - Docstring formázási hibák javítása

3. Alacsony prioritás
   - Biztonsági fejlesztések
   - Type stub fájlok létrehozása
   - Dokumentáció frissítése

## CI/CD integráció

- [ ] pre-commit hook-ok bővítése
- [ ] Automatikus típusellenőrzés beállítása
- [ ] Docstring ellenőrzés automatizálása
- [ ] Biztonsági scan bevezetése
