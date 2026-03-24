# 🧪 Teszt: tests/neural_ai/ui/interfaces/test_data_service_interface.py

**Tesztelt modul:** [`neural_ai/ui/interfaces/data_service_interface.py`](../../neural_ai/ui/interfaces/data_service_interface.py)

DataServiceInterface tesztelése.

Ez a tesztcsomag ellenőrzi a DataServiceInterface interfész megfelelő definícióját
és a Protocol szerződés betartását.

## Teszt Osztály: `MockDataService`

Mock implementáció a DataServiceInterface teszteléséhez.

## Teszt Osztály: `TestDataServiceInterface`

DataServiceInterface tesztosztály.

### ✓ `test_interface_is_protocol()`

Teszteli, hogy az interfész Protocol-t követ.

### ✓ `test_interface_is_runtime_checkable()`

Teszteli, hogy az interfész runtime_checkable.

### ✓ `test_mock_implements_interface()`

Teszteli, hogy a mock osztály implementálja az interfészt.

### ✓ `test_load_data_signature()`

Teszteli a load_data metódus szignatúráját.

### ✓ `test_get_data_sources_return_type()`

Teszteli a get_data_sources visszatérési értékét.

### ✓ `test_get_data_info_return_type()`

Teszteli a get_data_info visszatérési értékét.

### ✓ `test_apply_filters_functionality()`

Teszteli az apply_filters metódust.

### ✓ `test_export_data_return_type()`

Teszteli az export_data visszatérési értékét.

### ✓ `test_get_default_date_range()`

Teszteli a get_default_date_range metódust.

### ✓ `test_download_history_async()`

Teszteli a download_history aszinkron metódust.

### ✓ `test_list_available_data_return_type()`

Teszteli a list_available_data visszatérési értékét.

### ✓ `test_list_available_data_with_symbol_filter()`

Teszteli a list_available_data szűrést.

### ✓ `test_get_storage_path_return_type()`

Teszteli a get_storage_path visszatérési értékét.

### ✓ `test_get_configured_symbols()`

Teszteli a get_configured_symbols metódust.

### ✓ `test_interface_methods_exist()`

Teszteli, hogy az interfész minden metódusa létezik.

### ✓ `test_interface_type_hints()`

Teszteli a típusos megjelöléseket.

## Teszt Osztály: `TestDataServiceInterfaceIntegration`

Integrációs tesztek a DataServiceInterface-hez.

### ✓ `test_chunk_based_loading()`

Teszteli a chunk-based adatbetöltést.

### ✓ `test_data_pipeline_flow()`

Teszteli az adatfeldolgozási folyamatot.

### ✓ `test_async_data_download_flow()`

Teszteli az aszinkron adatletöltési folyamatot.

---

**Teszt fájl:** [`tests/neural_ai/ui/interfaces/test_data_service_interface.py`](../../tests/neural_ai/ui/interfaces/test_data_service_interface.py)

**Tesztelt modul:** [`neural_ai/ui/interfaces/data_service_interface.py`](../../neural_ai/ui/interfaces/data_service_interface.py)
