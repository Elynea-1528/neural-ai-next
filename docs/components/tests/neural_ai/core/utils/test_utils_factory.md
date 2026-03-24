# 🧪 Teszt: tests/neural_ai/core/utils/test_utils_factory.py

**Tesztelt modul:** [`neural_ai/core/utils/utils_factory.py`](../../neural_ai/core/utils/utils_factory.py)

Tesztek a HardwareFactory osztályhoz.

Ez a modul a `HardwareFactory` osztály tesztjeit tartalmazza, amelyek ellenőrzik
a hardverinformációk lekérdezéséhez szükséges factory metódusok helyes működését.

## Teszt Osztály: `TestHardwareFactory`

Tesztosztály a HardwareFactory metódusainak teszteléséhez.

### ✓ `test_get_hardware_info_returns_hardware_info_instance()`

Teszteli, hogy a get_hardware_info visszaad-e HardwareInfo példányt.

### ✓ `test_get_hardware_info_returns_new_instance()`

Teszteli, hogy a get_hardware_info mindig új példányt ad-e vissza.

### ✓ `test_get_hardware_interface_returns_hardware_interface()`

Teszteli, hogy a get_hardware_interface visszaad-e HardwareInterface-t.

### ✓ `test_get_hardware_interface_returns_new_instance()`

Teszteli, hogy a get_hardware_interface mindig új példányt ad-e vissza.

### ✓ `test_get_hardware_info_and_interface_return_different_instances()`

Teszteli, hogy a factory különböző példányokat ad-e vissza.

### ✓ `test_hardware_info_implements_hardware_interface()`

Teszteli, hogy a HardwareInfo implementálja-e a HardwareInterface-t.

### ✓ `test_get_hardware_info_imports_correctly()`

Teszteli, hogy a get_hardware_info helyesen importálja-e a HardwareInfo osztályt.

### ✓ `test_get_hardware_interface_imports_correctly()`

Teszteli, hogy a get_hardware_interface helyesen importálja-e a HardwareInfo osztályt.

### ✓ `test_factory_methods_are_static()`

Teszteli, hogy a factory metódusok statikusak-e.

## Teszt Osztály: `TestHardwareFactoryIntegration`

Integrációs tesztek a HardwareFactory-hez.

### ✓ `test_factory_creates_working_hardware_info_instance()`

Teszteli, hogy a factory által létrehozott példány működőképes-e.

### ✓ `test_factory_creates_working_hardware_interface()`

Teszteli, hogy a factory által létrehozott interfész működőképes-e.

---

**Teszt fájl:** [`tests/neural_ai/core/utils/test_utils_factory.py`](../../tests/neural_ai/core/utils/test_utils_factory.py)

**Tesztelt modul:** [`neural_ai/core/utils/utils_factory.py`](../../neural_ai/core/utils/utils_factory.py)
