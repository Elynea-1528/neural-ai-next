# Storage Komponens Tervezési Specifikáció

## 1. Áttekintés

A storage komponens feladata az adatok perzisztens tárolásának és betöltésének biztosítása a Neural AI rendszer számára. A komponens támogatja különböző formátumú adatok kezelését, automatikus formátum felismerést és hierarchikus szervezést.

## 2. Követelmények

### 2.1 Funkcionális követelmények

- DataFrame-ek mentése és betöltése különböző formátumokban
- Python objektumok szerializációja és deszerializációja
- Hierarchikus fájlrendszer kezelése
- Metaadatok kezelése
- Könyvtár listázás szűrési lehetőséggel
- Automatikus formátum felismerés

### 2.2 Nem-funkcionális követelmények

- Típusbiztonság és statikus típusellenőrzés
- Robosztus hibakezelés részletes hibaüzenetekkel
- Bővíthetőség új formátumok támogatásához
- Részletes dokumentáció és példák
- 90%+ tesztlefedettség

## 3. Architektúrális döntések

### 3.1 Interfész alapú tervezés

- Absztrakt StorageInterface definiálja a kötelező műveleteket
- Különböző implementációk támogatása (pl. FileStorage)
- Factory pattern használata az implementációk létrehozásához

### 3.2 Kivételkezelési hierarchia

```
StorageError
├── StorageFormatError     # Formátum problémák
├── StorageNotFoundError   # Nem létező erőforrások
├── StorageSerializationError # Szerializációs hibák
└── StorageIOError        # I/O műveletek hibái
```

### 3.3 Formátumkezelés

- Regisztrált formátumok és kezelőik központi tárolása
- Automatikus formátum felismerés kiterjesztés alapján
- Konfigurálható formátum-specifikus paraméterek

### 3.4 Path kezelés

- Egységes string alapú útvonal paraméterezés
- Path objektumok használata a belső műveleteknél
- Path objektumok visszaadása a könyvtár listázásnál

## 4. API tervezés

### 4.1 Útvonalkezelés

- Bemeneti paraméterek: str típusú útvonalak
- Relatív útvonalak kezelése base_path-hoz képest
- Path objektumok használata a belső logikában

### 4.2 DataFrame műveletek

- Automatikus formátum felismerés
- Index kezelés testreszabhatósága
- Formátum-specifikus paraméterek támogatása

### 4.3 Objektum szerializáció

- JSON alapértelmezett formátum
- Típusbiztos deszerializáció
- Kivételkezelés szerializációs hibáknál

### 4.4 Könyvtár műveletek

- Path objektumok visszaadása list_dir műveletben
- Opcionális szűrési minták támogatása
- Rekurzív műveletek biztonságos kezelése

## 5. Implementációs részletek

### 5.1 FileStorage

```python
class FileStorage:
    _DATAFRAME_FORMATS = {
        "csv": {
            "save": lambda df, path, **kwargs: df.to_csv(path, **kwargs),
            "load": lambda path, **kwargs: pd.read_csv(path, **kwargs),
        },
        "excel": {
            "save": lambda df, path, **kwargs: df.to_excel(path, **kwargs),
            "load": lambda path, **kwargs: pd.read_excel(path, **kwargs),
        },
    }

    _OBJECT_FORMATS = {
        "json": {
            "save": json.dump,
            "load": json.load,
        }
    }
```

### 5.2 Base Path kezelés

- Alapértelmezett: aktuális könyvtár
- Abszolút útvonalak megtartása
- Relatív útvonalak base_path-hoz képest

## 6. Hibakezelési stratégiák

### 6.1 Általános elvek

- Specifikus kivételek használata
- Eredeti kivételek megőrzése
- Részletes hibaüzenetek
- Biztonságos erőforrás felszabadítás

### 6.2 Kivételek használata

```python
try:
    # művelet végrehajtása
except SpecificError as e:
    raise StorageError("Részletes hibaüzenet", original_error=e)
```

## 7. Teljesítmény optimalizáció

### 7.1 DataFrame műveletek

- Chunked olvasás nagy fájloknál
- Index optimalizáció
- Formátum-specifikus optimalizációk

### 7.2 I/O műveletek

- Könyvtár cache használata
- Hatékony path művelet
- Erőforrások megfelelő lezárása

## 8. Tesztelés

### 8.1 Unit tesztek

- Minden publikus metódus tesztelése
- Edge case-ek lefedése
- Mock fájlrendszer használata

### 8.2 Integrációs tesztek

- Valós fájlrendszer műveletek
- Különböző formátumok tesztelése
- Nagy adathalmazok kezelése

## 9. Továbbfejlesztési lehetőségek

- Távoli storage támogatás (S3, GCS)
- Aszinkron műveletek
- Cache réteg bevezetése
- Tömörítés támogatása
- Új formátumok hozzáadása
- Batch műveletek
- Verziókezelés integrálása
