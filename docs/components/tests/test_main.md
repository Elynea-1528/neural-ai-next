# 🧪 Teszt: tests/test_main.py

**Tesztelt modul:** [`main.py`](../../main.py)

Unit tesztek a main.py modulhoz.

Ez a modul teszteli a CLI belépési pont összes funkcióját:
- Live mód indítása
- Download mód (történeti adatok)
- Dashboard mód (Streamlit)
- Argumentum parsing
- Dátum parsing
- Hibakezelés

## Teszt Osztály: `TestParseDateFunction`

Tesztek a parse_date() függvényhez.

### ✓ `test_parse_date_valid_format()`

Helyes dátum formátum parse-olása.

### ✓ `test_parse_date_invalid_format()`

Érvénytelen dátum formátum ValueError-t dob.

### ✓ `test_parse_date_wrong_separator()`

Rossz elválasztó karakter ValueError-t dob.

## Teszt Osztály: `TestParseArgumentsFunction`

Tesztek a parse_arguments() függvényhez.

### ✓ `test_parse_arguments_live_mode()`

Live mód argumentum parsing.

### ✓ `test_parse_arguments_download_mode()`

Download mód argumentum parsing.

### ✓ `test_parse_arguments_dashboard_mode_defaults()`

Dashboard mód alapértelmezett értékekkel.

### ✓ `test_parse_arguments_dashboard_mode_custom()`

Dashboard mód egyedi értékekkel.

## Teszt Osztály: `TestRunLiveMode`

Tesztek a run_live_mode() függvényhez.

### ✓ `test_run_live_mode_success()`

Live mód sikeres indítása és leállítása.

### ✓ `test_run_live_mode_none_components()`

Live mód None komponensekkel (graceful degradation).

## Teszt Osztály: `TestRunDownloadMode`

Tesztek a run_download_mode() függvényhez.

### ✓ `test_run_download_mode_success()`

Download mód sikeres futása.

## Teszt Osztály: `TestRunDashboardMode`

Tesztek a run_dashboard_mode() függvényhez.

### ✓ `test_run_dashboard_mode_success()`

Dashboard mód sikeres indítása.

### ✓ `test_run_dashboard_mode_headless()`

Dashboard mód headless flag-gel.

### ✓ `test_run_dashboard_mode_subprocess_error()`

Dashboard mód subprocess hiba kezelése.

### ✓ `test_run_dashboard_mode_keyboard_interrupt()`

Dashboard mód KeyboardInterrupt kezelése.

## Teszt Osztály: `TestMainFunction`

Tesztek a main() függvényhez.

### ✓ `test_main_live_mode()`

Main függvény live móddal.

### ✓ `test_main_live_mode_keyboard_interrupt()`

Main függvény live mód KeyboardInterrupt kezelése.

### ✓ `test_main_live_mode_exception()`

Main függvény live mód exception kezelése.

### ✓ `test_main_download_mode_success()`

Main függvény download móddal.

### ✓ `test_main_download_mode_invalid_date_format()`

Main függvény download mód érvénytelen dátum formátummal.

### ✓ `test_main_download_mode_start_after_end()`

Main függvény download mód kezdő dátum > záró dátum.

### ✓ `test_main_download_mode_future_date()`

Main függvény download mód jövőbeli dátummal.

### ✓ `test_main_download_mode_keyboard_interrupt()`

Main függvény download mód KeyboardInterrupt kezelése.

### ✓ `test_main_download_mode_exception()`

Main függvény download mód exception kezelése.

### ✓ `test_main_dashboard_mode()`

Main függvény dashboard móddal.

### ✓ `test_main_dashboard_mode_keyboard_interrupt()`

Main függvény dashboard mód KeyboardInterrupt kezelése.

### ✓ `test_main_dashboard_mode_exception()`

Main függvény dashboard mód exception kezelése.

### ✓ `test_main_invalid_command()`

Main függvény érvénytelen paranccsal.

### ✓ `test_main_no_command()`

Main függvény parancs nélkül.

### ✓ `test_main_logger_assertion()`

Main függvény logger None esetén assertion error.

---

**Teszt fájl:** [`tests/test_main.py`](../../tests/test_main.py)

**Tesztelt modul:** [`main.py`](../../main.py)
