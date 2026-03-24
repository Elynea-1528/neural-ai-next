# 🧪 Teszt: tests/neural_ai/ui/services/test_data_service.py

**Tesztelt modul:** [`neural_ai/ui/services/data_service.py`](../../neural_ai/ui/services/data_service.py)

Data Service tesztelése.

Ez a modul a DataService osztály tesztjeit tartalmazza.

## Teszt Osztály: `TestDataService`

DataService osztály tesztjei.

### ✓ `test_init()`

Teszteli a DataService inicializálását.

### ✓ `test_load_data()`

Teszteli az adatok betöltését.

### ✓ `test_load_data_invalid_source()`

Teszteli a hibakezelést érvénytelen adatforrás esetén.

### ✓ `test_get_data_sources()`

Teszteli az adatforrások lekérdezését.

### ✓ `test_get_data_info()`

Teszteli az adatforrás információk lekérdezését.

### ✓ `test_get_data_info_invalid_source()`

Teszteli a hibakezelést érvénytelen adatforrás esetén.

### ✓ `test_apply_filters()`

Teszteli a szűrők alkalmazását.

### ✓ `test_apply_filters_range()`

Teszteli a tartomány szűrést.

### ✓ `test_export_data()`

Teszteli az adatok exportálását.

### ✓ `test_export_data_invalid_format()`

Teszteli a hibakezelést érvénytelen formátum esetén.

### ✓ `test_export_data_empty()`

Teszteli az üres adatok exportálását.

### ✓ `test_list_available_data()`

Teszteli az elérhető adatok listázását (csak tick_data).

### ✓ `test_list_available_data_with_symbol()`

Teszteli az elérhető adatok listázását egyedi szimbólummal.

### ✓ `test_list_available_data_no_files()`

Teszteli az elérhető adatok listázását, ha nincs fájl.

### ✓ `test_get_storage_path()`

Teszteli a tárolási útvonal lekérdezését.

### ✓ `test_get_storage_path_default()`

Teszteli az alapértelmezett tárolási útvonal lekérdezését.

### ✓ `test_get_configured_symbols_with_valid_config()`

Teszteli a konfigurált szimbólumok lekérdezését érvényes konfiggal.

### ✓ `test_get_configured_symbols_with_empty_config()`

Teszteli a konfigurált szimbólumok lekérdezését üres konfiggal.

### ✓ `test_get_configured_symbols_with_none_config()`

Teszteli a konfigurált szimbólumok lekérdezését None konfiggal.

### ✓ `test_get_configured_symbols_with_invalid_config_type()`

Teszteli a konfigurált szimbólumok lekérdezését érvénytelen típusú konfiggal.

### ✓ `test_get_configured_symbols_with_no_config()`

Teszteli a konfigurált szimbólumok lekérdezését, ha nincs konfig.

### ✓ `test_get_configured_symbols_with_exception()`

Teszteli a konfigurált szimbólumok lekérdezését kivétel esetén.

### ✓ `test_generate_mock_data()`

Teszteli a mock adatok generálását.

### ✓ `test_generate_mock_data_with_filters()`

Teszteli a mock adatok generálását szűrőkkel.

### ✓ `test_download_history_with_existing_data_skip()`

Teszteli a download_history metódust, amikor az adat már létezik és skip-eli.

### ✓ `test_download_history_with_new_data_download()`

Teszteli a download_history metódust, amikor új adat letöltésre kerül.

---

**Teszt fájl:** [`tests/neural_ai/ui/services/test_data_service.py`](../../tests/neural_ai/ui/services/test_data_service.py)

**Tesztelt modul:** [`neural_ai/ui/services/data_service.py`](../../neural_ai/ui/services/data_service.py)
