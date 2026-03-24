# 🧪 Teszt: tests/scripts/test_download_history.py

**Tesztelt modul:** [`scripts/download_history.py`](../../scripts/download_history.py)

Tesztek a scripts/download_history.py scripthez.

## Teszt Osztály: `TestSmartResumeLogic`

Smart Resume logika tesztelése.

### ✓ `test_hour_dir_path_construction()`

Teszteli az óra mappa útvonalának helyes összeállítását.

### ✓ `test_smart_resume_debug_log_exists()`

Teszteli, hogy a debug log megtalálható a forráskódban.

### ✓ `test_hour_dir_exists_check()`

Teszteli, hogy a logika ellenőrzi a mappa létezését.

### ✓ `test_master_filename_generation()`

Teszteli, hogy a master fájlnév generálása benne van.

### ✓ `test_expected_path_check()`

Teszteli, hogy az expected_path ellenőrzés benne van.

## Teszt Osztály: `TestDownloadHistoryImports`

Import tesztek.

### ✓ `test_type_checking_block_exists()`

Teszteli, hogy a TYPE_CHECKING blokk létezik.

### ✓ `test_required_imports()`

Teszteli a kötelező importokat.

## Teszt Osztály: `TestArgumentParsing`

Argumentum feldolgozás tesztek.

### ✓ `test_parse_arguments_function_exists()`

Teszteli a parse_arguments függvény létezését.

## Teszt Osztály: `TestMainFunction`

Fő függvény tesztek.

### ✓ `test_main_function_exists()`

Teszteli a main függvény létezését.

## Teszt Osztály: `TestSaveTicksDirect`

_save_ticks_direct függvény tesztek.

### ✓ `test_save_ticks_direct_function_exists()`

Teszteli a _save_ticks_direct függvény létezését.

### ✓ `test_save_ticks_direct_creates_correct_dataframe_columns()`

Teszteli, hogy a _save_ticks_direct függvény helyesen hozza létre a DataFrame-et.

---

**Teszt fájl:** [`tests/scripts/test_download_history.py`](../../tests/scripts/test_download_history.py)

**Tesztelt modul:** [`scripts/download_history.py`](../../scripts/download_history.py)
