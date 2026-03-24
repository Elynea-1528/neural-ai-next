# 🧪 Teszt: tests/neural_ai/core/config/interfaces/test_factory_interface.py

**Tesztelt modul:** [`neural_ai/core/config/interfaces/factory_interface.py`](../../neural_ai/core/config/interfaces/factory_interface.py)

ConfigManagerFactoryInterface tesztelése.

Ez a modul tartalmazza a ConfigManagerFactoryInterface interfész teszteit,
amelyek ellenőrzik a konfigurációkezelő factory interfész metódusainak
helyes definícióját és a megvalósító osztályok konzisztenciáját.

## Teszt Osztály: `DummyConfigManager`

Egyszerű konfigurációkezelő implementáció teszteléshez.

## Teszt Osztály: `DummyConfigFactory`

Egyszerű konfiguráció factory implementáció teszteléshez.

## Teszt Osztály: `_IncompleteConfigFactory`

## Teszt Osztály: `TestConfigManagerFactoryInterface`

ConfigManagerFactoryInterface interfész tesztjei.

### ✓ `test_interface_is_abstract()`

Teszteli, hogy az interfész absztrakt osztály-e.

### ✓ `test_interface_has_abstract_methods()`

Teszteli, hogy az interfész tartalmazza a szükséges absztrakt metódusokat.

### ✓ `test_interface_methods_are_classmethods()`

Teszteli, hogy az interfész metódusai classmethod-ok.

### ✓ `test_interface_method_signatures()`

Teszteli a metódusok aláírásainak helyességét.

### ✓ `test_implementation_can_be_instantiated()`

Teszteli, hogy az interfész implementálható-e.

### ✓ `test_implementation_has_all_methods()`

Teszteli, hogy az implementáció tartalmazza az összes szükséges metódust.

### ✓ `test_register_manager_method()`

Teszteli a register_manager metódust.

### ✓ `test_get_manager_method()`

Teszteli a get_manager metódust.

### ✓ `test_get_manager_with_type()`

Teszteli a get_manager metódust explicit típussal.

### ✓ `test_get_manager_with_invalid_extension()`

Teszteli a get_manager metódust érvénytelen kiterjesztéssel.

### ✓ `test_get_manager_with_invalid_type()`

Teszteli a get_manager metódust érvénytelen típussal.

### ✓ `test_create_manager_method()`

Teszteli a create_manager metódust.

### ✓ `test_create_manager_with_kwargs()`

Teszteli a create_manager metódust csak kulcsszavas argumentumokkal.

### ✓ `test_create_manager_with_invalid_type()`

Teszteli a create_manager metódust érvénytelen típussal.

### ✓ `test_interface_enforces_method_implementation()`

Teszteli, hogy az interfész kényszeríti a metódusok implementálását.

## Teszt Függvények

### ✓ `test_interface_docstrings_present()`

Teszteli, hogy az interfész metódusainak van docstringje.

### ✓ `test_interface_method_order()`

Teszteli, hogy az interfész metódusai logikus sorrendben vannak.

### ✓ `test_register_manager_raises_not_implemented_error()`

Teszteli, hogy a register_manager alapértelmezésben NotImplementedError-t dob.

### ✓ `test_get_manager_raises_not_implemented_error()`

Teszteli, hogy a get_manager alapértelmezésben NotImplementedError-t dob.

### ✓ `test_create_manager_raises_not_implemented_error()`

Teszteli, hogy a create_manager alapértelmezésben NotImplementedError-t dob.

### ✓ `test_factory_returns_config_manager_interface()`

Teszteli, hogy a factory ConfigManagerInterface-t ad vissza.

### ✓ `test_factory_creates_separate_instances()`

Teszteli, hogy a factory külön példányokat hoz létre.

### ✓ `test_factory_supports_multiple_manager_types()`

Teszteli, hogy a factory támogat több konfigurációkezelő típust.

---

**Teszt fájl:** [`tests/neural_ai/core/config/interfaces/test_factory_interface.py`](../../tests/neural_ai/core/config/interfaces/test_factory_interface.py)

**Tesztelt modul:** [`neural_ai/core/config/interfaces/factory_interface.py`](../../neural_ai/core/config/interfaces/factory_interface.py)
