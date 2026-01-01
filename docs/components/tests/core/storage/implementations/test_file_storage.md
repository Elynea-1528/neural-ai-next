# FileStorage Teszt Dokumentáció

## Áttekintés

Ez a dokumentáció a [`tests/core/storage/implementations/test_file_storage.py`](tests/core/storage/implementations/test_file_storage.py) tesztmodult ismerteti, amely a [`neural_ai/core/storage/implementations/file_storage.py`](neural_ai/core/storage/implementations/file_storage.py) osztály funkcionalitását teszteli.

## Tesztelt Funkcionalitás

A tesztmodul a következő fő területeket fedi le:

### 1. Alapvető Műveletek
- **Inicializálás**: Alapértelmezett és egyéni útvonalak beállítása
- **Létezés ellenőrzés**: Fájlok és könyvtárak létezésének ellenőrzése
- **Metaadatok lekérdezése**: Fájlméret, létrehozási és módosítási dátumok
- **Törlés**: Fájlok és könyvtárak törlése
- **Listázás**: Könyvtár tartalmának listázása

### 2. DataFrame Műveletek
- **Mentés**: CSV és Excel formátumban
- **Betöltés**: Különböző formátumokból
- **Formátum automatikus felismerés**: Kiterjesztés alapján
- **Hibakezelés**: Érvénytelen formátumok, nem létező fájlok
- **Paraméterezés**: Egyéni opciók átadása (kwargs)

### 3. Objektum Műveletek
- **Mentés**: JSON formátumban
- **Betöltés**: Objektumok visszaállítása
- **Szerializáció/Deszerializáció**: Hibakezelés
- **Paraméterezés**: Egyéni opciók (pl. indentáció)

### 4. Biztonsági és Rendszerfunkciók
- **Jogosultság ellenőrzés**: Olvasási és írási jogosultságok
- **Lemezterület ellenőrzés**: Szükséges tárterület vizsgálata
- **Atomi írás**: Temp fájl használata és átnevezés
- **Tároló információk**: Helyfoglalás és szabad terület lekérdezése

## Tesztesetek Részletezése

### Inicializálás Tesztek
- `test_init_default_path`: Ellenőrzi az alapértelmezett útvonal beállítását
- `test_init_custom_path`: Ellenőrzi az egyéni útvonal beállítását
- `test_init_with_logger`: Ellenőrzi a logger beállítását

### Path Kezelés Tesztek
- `test_get_full_path_absolute`: Abszolút útvonalak kezelése
- `test_get_full_path_relative`: Relatív útvonalak kezelése

### Létezés Ellenőrzés Tesztek
- `test_exists_true`: Létező fájl ellenőrzése
- `test_exists_false`: Nem létező fájl ellenőrzése

### DataFrame Tesztek
- `test_save_dataframe_csv`: DataFrame mentése CSV formátumban
- `test_save_dataframe_excel`: DataFrame mentése Excel formátumban (opcionális)
- `test_save_dataframe_invalid_format`: Érvénytelen formátum ellenőrzése
- `test_load_dataframe_not_found`: Nem létező fájl betöltésének ellenőrzése
- `test_save/load_dataframe_with_kwargs`: Egyéni paraméterek tesztelése
- `test_save_dataframe_format_detection_failure`: Formátum meghatározási hiba
- `test_save_dataframe_disk_space_check_failure`: Lemezterület ellenőrzési hiba
- `test_save_dataframe_io_error`: IO hiba kezelése
- `test_load_dataframe_format_detection_failure`: Betöltési formátum hiba
- `test_load_dataframe_io_error`: Betöltési IO hiba

### Objektum Tesztek
- `test_save_object_json`: Objektum mentése JSON formátumban
- `test_save_object_invalid_format`: Érvénytelen formátum ellenőrzése
- `test_load_object_not_found`: Nem létező fájl betöltése
- `test_load_object_invalid_json`: Érvénytelen JSON ellenőrzése
- `test_save/load_object_with_kwargs`: Egyéni paraméterek tesztelése
- `test_save_object_serialization_error`: Szerializációs hiba kezelése
- `test_save_object_io_error`: Mentési IO hiba
- `test_load_object_deserialization_error`: Deszerializációs hiba
- `test_load_object_os_error`: Betöltési OS hiba

### Metaadatok Tesztek
- `test_get_metadata_file`: Fájl metaadatainak lekérdezése
- `test_get_metadata_not_found`: Nem létező fájl metaadatainak lekérdezése
- `test_get_metadata_os_error`: OS hiba a metaadatok lekérdezésekor

### Törlés Tesztek
- `test_delete_file`: Fájl törlése
- `test_delete_not_found`: Nem létező fájl törlésének ellenőrzése
- `test_delete_directory`: Könyvtár törlése
- `test_delete_io_error`: Törlési IO hiba kezelése

### Listázás Tesztek
- `test_list_dir`: Könyvtár tartalmának listázása
- `test_list_dir_with_pattern`: Mintával történő listázás
- `test_list_dir_not_found`: Nem létező könyvtár listázása
- `test_list_dir_not_directory`: Nem könyvtár listázásának ellenőrzése
- `test_list_dir_glob_error`: Glob hiba kezelése

### Biztonsági Tesztek
- `test_check_permissions_read_only`: Olvasási jogosultság ellenőrzése
- `test_check_permissions_write_denied`: Írási jog megtagadása
- `test_check_permissions_read_denied`: Olvasási jog megtagadása
- `test_check_permissions_parent_not_exists`: Nem létező szülőkönyvtár

### Lemezterület Tesztek
- `test_check_disk_space_sufficient`: Elegendő lemezterület ellenőrzése
- `test_check_disk_space_insufficient`: Elégtelen lemezterület ellenőrzése
- `test_check_disk_space_os_error`: OS hiba a lemezterület ellenőrzésekor

### Atomi Írás Tesztek
- `test_atomic_write_json`: JSON objektum atomi mentése
- `test_atomic_write_dataframe`: DataFrame atomi mentése
- `test_atomic_write_bytes`: Bytes tartalom atomi mentése
- `test_atomic_write_string`: String tartalom atomi mentése
- `test_atomic_write_invalid_format`: Érvénytelen formátum ellenőrzése
- `test_atomic_write_os_error_save`: Mentési hiba kezelése

### Tároló Információk Tesztek
- `test_get_storage_info`: Tároló információk lekérdezése
- `test_get_storage_info_os_error`: OS hiba a tároló információk lekérdezésekor

### Formátum Kezelők Tesztek
- `test_setup_format_handlers`: Formátum kezelők beállításának ellenőrzése

## Tesztlefedettség

A tesztmodul célja a FileStorage osztály **100%-os tesztlefedettségének** elérése. A jelenlegi állapot:

- **Átmenő tesztek**: 57
- **Kihagyott tesztek**: 3 (Excel formátumhoz kötődő, opcionális függőség miatt)
- **Coverage**: ~82%

### Hiányzó Sorok (Coverage Report)
A coverage report alapján a következő sorok nincsenek teljesen lefedve:

```
70-72, 75, 148, 228, 248, 253-256, 288, 302, 304, 307, 314, 316-321, 
359, 362, 374, 376-379, 425-429, 475, 484, 487-489, 492, 494-497, 541-542
```

Ezek a sorok főleg:
- Bizonyos exception catch blokkok
- Logger hívások
- Speciális edge case-ek
- Opcionális funkcionalitások

## Futtatás

### Egyszerű Futtatás
```bash
pytest tests/core/storage/implementations/test_file_storage.py -v
```

### Coverage Report-tal
```bash
pytest tests/core/storage/implementations/test_file_storage.py \
  --cov=neural_ai.core.storage.implementations.file_storage \
  --cov-report=term-missing
```

### Egyedi Teszt Futtatása
```bash
pytest tests/core/storage/implementations/test_file_storage.py::TestFileStorage::test_save_dataframe_csv -v
```

## Fixture-ök

A tesztmodul a következő fixture-öket használja:

- `temp_dir`: Ideiglenes könyvtár létrehozása a tesztekhez
- `storage`: FileStorage példány létrehozása
- `sample_dataframe`: Minta DataFrame (3 sor, 3 oszlop)
- `sample_object`: Minta Python objektum (dict)

## Hibakezelés

A tesztek a következő kivételeket ellenőrzik:

- `StorageNotFoundError`: Fájl nem található
- `StorageFormatError`: Érvénytelen formátum
- `StorageIOError`: IO művelet sikertelen
- `StorageSerializationError`: Szerializációs hiba
- `PermissionDeniedError`: Jogosultsági hiba
- `InsufficientDiskSpaceError`: Nincs elég lemezterület

## Mocking

A tesztmodul bizonyos esetekben mocking-ot használ:

- **OS hívások**: `os.statvfs`, `os.replace` mockolása
- **Fájlműveletek**: `open`, `Path.mkdir`, `Path.unlink` mockolása
- **Pandas műveletek**: `pd.read_csv`, `df.memory_usage` mockolása
- **Permission ellenőrzés**: `os.access` mockolása

## Kapcsolódó Dokumentáció

- [FileStorage Implementáció](components/core/storage/implementations/file_storage.md)
- [Storage Interface](components/core/storage/interfaces/storage_interface.md)
- [Storage Exceptions](components/core/storage/exceptions/index.md)

## Frissítés Dátuma

2026-01-01

## Verzió

1.0.0