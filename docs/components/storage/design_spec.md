# Storage Komponens Tervezési Specifikáció

## 1. Áttekintés

A storage komponens feladata az adatok perzisztens tárolásának és betöltésének biztosítása a Neural AI rendszer számára. A komponens támogatja különböző formátumú adatok kezelését és hierarchikus szervezését.

## 2. Követelmények

### 2.1 Funkcionális követelmények

- DataFrame-ek mentése és betöltése különböző formátumokban
- Python objektumok szerializációja és deszerializációja
- Hierarchikus fájlrendszer kezelése
- Metaadatok kezelése
- Abszolút és relatív útvonalak támogatása

### 2.2 Nem-funkcionális követelmények

- Típusbiztonság
- Robosztus hibakezelés
- Bővíthetőség új formátumok támogatásához
- Megfelelő dokumentáció és példák
- 80%+ tesztlefedettség

## 3. Architektúrális döntések

### 3.1 Interfész alapú tervezés

A komponens interfész alapú tervezést használ a rugalmasság és a különböző implementációk támogatása érdekében.

### 3.2 Kivételkezelési hierarchia

Specifikus kivételosztályok a különböző hibatípusok kezelésére:
- StorageError: Alap kivétel osztály
- StorageFormatError: Formátum hibák
- StorageNotFoundError: Nem létező erőforrások
- StorageSerializationError: Szerializációs hibák
- StorageIOError: I/O műveletek hibái

### 3.3 Formátumkezelés

- Regisztrált formátumok és kezelőik központi tárolása
- Automatikus formátum felismerés kiterjesztés alapján
- Bővíthető formátum támogatás

## 4. Komponens struktúra

```
neural_ai/core/storage/
├── __init__.py
├── exceptions.py
├── implementations/
│   ├── __init__.py
│   └── file_storage.py
└── interfaces/
    ├── __init__.py
    └── storage_interface.py
```

## 5. API tervezés

### 5.1 Fő interfész

```python
class StorageInterface(ABC):
    def save_dataframe(...)
    def load_dataframe(...)
    def save_object(...)
    def load_object(...)
    def exists(...)
    def get_metadata(...)
    def delete(...)
    def list_dir(...)
```

### 5.2 Implementációk

#### FileStorage

- Alapértelmezett implementáció fájlrendszer alapú tároláshoz
- Támogatott DataFrame formátumok: CSV, JSON, Excel
- Támogatott objektum formátumok: JSON

## 6. Adatformátumok

### 6.1 DataFrame formátumok

- CSV (.csv): Alapértelmezett, széles körben támogatott
- JSON (.json): Komplex struktúrák megőrzésére
- Excel (.xlsx): Opcionális, függ a pandas támogatástól

### 6.2 Objektum formátumok

- JSON (.json): Alapértelmezett, széles körben támogatott

## 7. Hibakezelés

### 7.1 Kivételek hierarchiája

```
Exception
└── StorageError
    ├── StorageFormatError
    ├── StorageNotFoundError
    ├── StorageSerializationError
    └── StorageIOError
```

### 7.2 Hibakezelési stratégiák

- Explicit kivételtípusok a különböző hibák azonosításához
- Eredeti kivételek megőrzése a hibakereséshez
- Világos hibaüzenetek a felhasználók számára

## 8. Teljesítmény megfontolások

### 8.1 Memóriahasználat

- Nagy fájlok kezelése chunkolással (DataFrame-ek esetén)
- Metaadatok lusta betöltése

### 8.2 I/O műveletek

- Könyvtárstruktúra cache-elése
- Batch műveletek támogatása

## 9. Biztonsági megfontolások

- Útvonal manipuláció elleni védelem
- Jogosultságok ellenőrzése műveletek előtt
- Biztonságos fájlkezelés (atomic műveletek)

## 10. Tesztelési stratégia

### 10.1 Unit tesztek

- Mock fájlrendszer a tesztekhez
- Minden API metódus tesztelése
- Hibakezelés tesztelése
- Edge case-ek lefedése

### 10.2 Integrációs tesztek

- Valós fájlrendszer műveletek
- Különböző formátumok együttműködése
- Nagy adatmennyiségek kezelése

## 11. Továbbfejlesztési lehetőségek

- Távoli storage támogatás (S3, GCS)
- További formátumok (HDF5, Feather)
- Aszinkron műveletek
- Tömörítés támogatása
- Verziókezelés
