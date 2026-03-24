# 🧪 Teszt: tests/neural_ai/core/base/exceptions/test_base_error.py

**Tesztelt modul:** [`neural_ai/core/base/exceptions/base_error.py`](../../neural_ai/core/base/exceptions/base_error.py)

Base kivételek tesztelése.

Ez a modul tartalmazza a neural_ai.core.base.exceptions modulban
definiált összes kivétel osztály tesztjeit.

## Teszt Osztály: `TestNeuralAIException`

NeuralAIException alap kivétel tesztjei.

### ✓ `test_base_exception_can_be_raised()`

Teszteli, hogy az alap kivétel dobható-e.

### ✓ `test_base_exception_with_message()`

Teszteli a kivételt üzenettel.

### ✓ `test_base_exception_inheritance()`

Teszteli, hogy a kivétel az Exception osztályból származik.

## Teszt Osztály: `TestStorageException`

StorageException kivétel tesztjei.

### ✓ `test_storage_exception_can_be_raised()`

Teszteli, hogy a tároló kivétel dobható-e.

### ✓ `test_storage_exception_inheritance()`

Teszteli, hogy a kivétel a NeuralAIException-ből származik.

### ✓ `test_storage_exception_with_message()`

Teszteli a kivételt üzenettel.

## Teszt Osztály: `TestStorageWriteError`

StorageWriteError kivétel tesztjei.

### ✓ `test_storage_write_error_can_be_raised()`

Teszteli, hogy az írási hiba dobható-e.

### ✓ `test_storage_write_error_inheritance()`

Teszteli az öröklődést.

### ✓ `test_storage_write_error_message()`

Teszteli a hibaüzenetet.

## Teszt Osztály: `TestStorageReadError`

StorageReadError kivétel tesztjei.

### ✓ `test_storage_read_error_can_be_raised()`

Teszteli, hogy az olvasási hiba dobható-e.

### ✓ `test_storage_read_error_inheritance()`

Teszteli az öröklődést.

### ✓ `test_storage_read_error_message()`

Teszteli a hibaüzenetet.

## Teszt Osztály: `TestStoragePermissionError`

StoragePermissionError kivétel tesztjei.

### ✓ `test_storage_permission_error_can_be_raised()`

Teszteli, hogy a jogosultsági hiba dobható-e.

### ✓ `test_storage_permission_error_inheritance()`

Teszteli az öröklődést.

### ✓ `test_storage_permission_error_message()`

Teszteli a hibaüzenetet.

## Teszt Osztály: `TestConfigurationError`

ConfigurationError kivétel tesztjei.

### ✓ `test_configuration_error_can_be_raised()`

Teszteli, hogy a konfigurációs hiba dobható-e.

### ✓ `test_configuration_error_inheritance()`

Teszteli az öröklődést.

### ✓ `test_configuration_error_message()`

Teszteli a hibaüzenetet.

## Teszt Osztály: `TestDependencyError`

DependencyError kivétel tesztjei.

### ✓ `test_dependency_error_can_be_raised()`

Teszteli, hogy a függőségi hiba dobható-e.

### ✓ `test_dependency_error_inheritance()`

Teszteli az öröklődést.

### ✓ `test_dependency_error_message()`

Teszteli a hibaüzenetet.

## Teszt Osztály: `TestSingletonViolationError`

SingletonViolationError kivétel tesztjei.

### ✓ `test_singleton_violation_error_can_be_raised()`

Teszteli, hogy a singleton megsértésének hibája dobható-e.

### ✓ `test_singleton_violation_error_inheritance()`

Teszteli az öröklődést.

### ✓ `test_singleton_violation_error_message()`

Teszteli a hibaüzenetet.

## Teszt Osztály: `TestComponentNotFoundError`

ComponentNotFoundError kivétel tesztjei.

### ✓ `test_component_not_found_error_can_be_raised()`

Teszteli, hogy a komponens nem található hiba dobható-e.

### ✓ `test_component_not_found_error_inheritance()`

Teszteli az öröklődést.

### ✓ `test_component_not_found_error_message()`

Teszteli a hibaüzenetet.

## Teszt Osztály: `TestNetworkException`

NetworkException kivétel tesztjei.

### ✓ `test_network_exception_can_be_raised()`

Teszteli, hogy a hálózati kivétel dobható-e.

### ✓ `test_network_exception_inheritance()`

Teszteli az öröklődést.

### ✓ `test_network_exception_message()`

Teszteli a hibaüzenetet.

## Teszt Osztály: `TestTimeoutError`

TimeoutError kivétel tesztjei.

### ✓ `test_timeout_error_can_be_raised()`

Teszteli, hogy az időtúllépési hiba dobható-e.

### ✓ `test_timeout_error_inheritance()`

Teszteli az öröklődést.

### ✓ `test_timeout_error_message()`

Teszteli a hibaüzenetet.

## Teszt Osztály: `TestConnectionError`

ConnectionError kivétel tesztjei.

### ✓ `test_connection_error_can_be_raised()`

Teszteli, hogy a kapcsolódási hiba dobható-e.

### ✓ `test_connection_error_inheritance()`

Teszteli az öröklődést.

### ✓ `test_connection_error_message()`

Teszteli a hibaüzenetet.

## Teszt Osztály: `TestInsufficientDiskSpaceError`

InsufficientDiskSpaceError kivétel tesztjei.

### ✓ `test_insufficient_disk_space_error_can_be_raised()`

Teszteli, hogy a lemezterület hiány hiba dobható-e.

### ✓ `test_insufficient_disk_space_error_inheritance()`

Teszteli az öröklődést.

### ✓ `test_insufficient_disk_space_error_message()`

Teszteli a hibaüzenetet.

## Teszt Osztály: `TestPermissionDeniedError`

PermissionDeniedError kivétel tesztjei.

### ✓ `test_permission_denied_error_can_be_raised()`

Teszteli, hogy a jogosultság megtagadva hiba dobható-e.

### ✓ `test_permission_denied_error_inheritance()`

Teszteli az öröklődést.

### ✓ `test_permission_denied_error_message()`

Teszteli a hibaüzenetet.

---

**Teszt fájl:** [`tests/neural_ai/core/base/exceptions/test_base_error.py`](../../tests/neural_ai/core/base/exceptions/test_base_error.py)

**Tesztelt modul:** [`neural_ai/core/base/exceptions/base_error.py`](../../neural_ai/core/base/exceptions/base_error.py)
