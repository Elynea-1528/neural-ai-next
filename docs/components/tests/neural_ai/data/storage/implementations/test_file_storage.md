# 🧪 Teszt: tests/neural_ai/data/storage/implementations/test_file_storage.py

**Tesztelt modul:** [`neural_ai/data/storage/implementations/file_storage.py`](../../neural_ai/data/storage/implementations/file_storage.py)

FileStorage teszt modul.

# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# File storage fixture type inference hibák.

Ez a modul tartalmazza a FileStorage osztály tesztjeit.

## Teszt Osztály: `NonSerializable`

## Teszt Osztály: `TestFileStorage`

FileStorage osztály tesztjei.

### ✓ `test_init_default_path()`

Teszteli az alapértelmezett útvonal beállítását.

### ✓ `test_init_custom_path()`

Teszteli az egyéni útvonal beállítását.

### ✓ `test_init_with_logger()`

Teszteli a logger beállítását.

### ✓ `test_get_full_path_absolute()`

Teszteli az abszolút útvonal kezelését.

### ✓ `test_get_full_path_relative()`

Teszteli a relatív útvonal kezelését.

### ✓ `test_exists_true()`

Teszteli a létező fájl ellenőrzését.

### ✓ `test_exists_false()`

Teszteli a nem létező fájl ellenőrzését.

### ✓ `test_save_dataframe_parquet()`

Teszteli a DataFrame mentését Parquet formátumban.

### ✓ `test_save_dataframe_invalid_format()`

Teszteli a DataFrame mentését érvénytelen formátumban.

### ✓ `test_load_dataframe_not_found()`

Teszteli a DataFrame betöltését nem létező fájlból.

### ✓ `test_save_object_pickle()`

Teszteli a Python objektum mentését pickle formátumban.

### ✓ `test_save_object_invalid_format()`

Teszteli a Python objektum mentését érvénytelen formátumban.

### ✓ `test_load_object_not_found()`

Teszteli a Python objektum betöltését nem létező fájlból.

### ✓ `test_get_metadata_file()`

Teszteli a fájl metaadatok lekérdezését.

### ✓ `test_get_metadata_not_found()`

Teszteli a metaadatok lekérdezését nem létező fájlból.

### ✓ `test_delete_file()`

Teszteli a fájl törlését.

### ✓ `test_delete_not_found()`

Teszteli a nem létező fájl törlését.

### ✓ `test_list_dir()`

Teszteli a könyvtár listázását.

### ✓ `test_list_dir_with_pattern()`

Teszteli a könyvtár listázását mintával.

### ✓ `test_list_dir_not_found()`

Teszteli a könyvtár listázását nem létező könyvtárból.

### ✓ `test_check_permissions_read_only()`

Teszteli az olvasási jogosultság ellenőrzését.

### ✓ `test_get_storage_info()`

Teszteli a tároló információk lekérdezését.

### ✓ `test_save_dataframe_with_kwargs()`

Teszteli a DataFrame mentését **kwargs paraméterekkel.

### ✓ `test_load_dataframe_with_kwargs()`

Teszteli a DataFrame betöltését **kwargs paraméterekkel.

### ✓ `test_save_object_with_kwargs()`

Teszteli a Python objektum mentését **kwargs paraméterekkel.

### ✓ `test_load_object_with_kwargs()`

Teszteli a Python objektum betöltését **kwargs paraméterekkel.

### ✓ `test_check_disk_space_sufficient()`

Teszteli a lemezterület ellenőrzését elegendő terület esetén.

### ✓ `test_check_disk_space_insufficient()`

Teszteli a lemezterület ellenőrzését elégtelen terület esetén.

### ✓ `test_check_disk_space_os_error()`

Teszteli a lemezterület ellenőrzését OS hiba esetén.

### ✓ `test_check_permissions_write_denied()`

Teszteli a jogosultság ellenőrzését írási jog nélkül.

### ✓ `test_check_permissions_read_denied()`

Teszteli a jogosultság ellenőrzését olvasási jog nélkül.

### ✓ `test_check_permissions_parent_not_exists()`

Teszteli a jogosultság ellenőrzését nem létező szülőkönyvtár esetén.

### ✓ `test_get_storage_info_os_error()`

Teszteli a tároló információk lekérdezését OS hiba esetén.

### ✓ `test_atomic_write_bytes()`

Teszteli az atomi írást bytes tartalommal (bináris mód).

### ✓ `test_save_dataframe_format_detection_failure()`

Teszteli a DataFrame mentését formátum meghatározási hiba esetén.

### ✓ `test_save_dataframe_excel_format_detection()`

Teszteli a DataFrame mentését Excel formátum automatikus felismerésével.

### ✓ `test_save_dataframe_disk_space_check_failure()`

Teszteli a DataFrame mentését lemezterület ellenőrzési hiba esetén.

### ✓ `test_save_dataframe_io_error()`

Teszteli a DataFrame mentését IO hiba esetén.

### ✓ `test_load_dataframe_format_detection_failure()`

Teszteli a DataFrame betöltését formátum meghatározási hiba esetén.

### ✓ `test_load_dataframe_excel_format_detection()`

Teszteli a DataFrame betöltését Excel formátum automatikus felismerésével.

### ✓ `test_load_dataframe_io_error()`

Teszteli a DataFrame betöltését IO hiba esetén.

### ✓ `test_save_object_format_detection_failure()`

Teszteli az objektum mentését formátum meghatározási hiba esetén.

### ✓ `test_save_object_serialization_error()`

Teszteli az objektum mentését szerializációs hiba esetén.

## Teszt Függvények

### ✓ `test_save_object_io_error()`

Teszteli az objektum mentését IO hiba esetén.

### ✓ `test_load_object_format_detection_failure()`

Teszteli az objektum betöltését formátum meghatározási hiba esetén.

### ✓ `test_load_object_deserialization_error()`

Teszteli az objektum betöltését deszerializációs hiba esetén.

### ✓ `test_load_object_os_error()`

Teszteli az objektum betöltését OS hiba esetén.

### ✓ `test_get_metadata_os_error()`

Teszteli a metaadatok lekérdezését OS hiba esetén.

### ✓ `test_delete_directory()`

Teszteli a könyvtár törlését.

### ✓ `test_delete_io_error()`

Teszteli a fájl törlését IO hiba esetén.

### ✓ `test_list_dir_not_directory()`

Teszteli a könyvtár listázását, ha az útvonal nem könyvtár.

### ✓ `test_list_dir_glob_error()`

Teszteli a könyvtár listázását glob hiba esetén.

---

**Teszt fájl:** [`tests/neural_ai/data/storage/implementations/test_file_storage.py`](../../tests/neural_ai/data/storage/implementations/test_file_storage.py)

**Tesztelt modul:** [`neural_ai/data/storage/implementations/file_storage.py`](../../neural_ai/data/storage/implementations/file_storage.py)
