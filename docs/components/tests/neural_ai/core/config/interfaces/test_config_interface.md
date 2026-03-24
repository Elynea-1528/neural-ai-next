# 🧪 Teszt: tests/neural_ai/core/config/interfaces/test_config_interface.py

**Tesztelt modul:** [`neural_ai/core/config/interfaces/config_interface.py`](../../neural_ai/core/config/interfaces/config_interface.py)

ConfigManagerInterface tesztelése.

Ez a modul tartalmazza a ConfigManagerInterface interfész teszteit,
amelyek ellenőrzik az interfész metódusainak helyes definícióját és
a megvalósító osztályok konzisztenciáját.

## Teszt Osztály: `DummyConfigManager`

Egyszerű konfigurációkezelő implementáció teszteléshez.

## Teszt Osztály: `_IncompleteConfigManager`

## Teszt Osztály: `TestConfigManagerInterface`

ConfigManagerInterface interfész tesztjei.

### ✓ `test_interface_is_abstract()`

Teszteli, hogy az interfész absztrakt osztály-e.

### ✓ `test_interface_has_abstract_methods()`

Teszteli, hogy az interfész tartalmazza a szükséges absztrakt metódusokat.

### ✓ `test_interface_method_signatures()`

Teszteli a metódusok aláírásainak helyességét.

### ✓ `test_implementation_can_be_instantiated()`

Teszteli, hogy az interfész implementálható-e.

### ✓ `test_implementation_has_all_methods()`

Teszteli, hogy az implementáció tartalmazza az összes szükséges metódust.

### ✓ `test_get_method_accepts_variable_keys()`

Teszteli, hogy a get metódus elfogad változó számú kulcsot.

### ✓ `test_get_method_returns_default()`

Teszteli, hogy a get metódus visszaadja az alapértelmezett értéket.

### ✓ `test_set_method_accepts_variable_keys()`

Teszteli, hogy a set metódus elfogad változó számú kulcsot.

### ✓ `test_get_section_returns_dict()`

Teszteli, hogy a get_section metódus dictionary-t ad vissza.

### ✓ `test_validate_returns_tuple()`

Teszteli, hogy a validate metódus tuple-t ad vissza.

### ✓ `test_save_accepts_optional_filename()`

Teszteli, hogy a save metódus elfogad opcionális fájlnevet.

### ✓ `test_load_accepts_filename()`

Teszteli, hogy a load metódus elfogad fájlnevet.

### ✓ `test_load_directory_accepts_path()`

Teszteli, hogy a load_directory metódus elfogad elérési utat.

### ✓ `test_interface_enforces_method_implementation()`

Teszteli, hogy az interfész kényszeríti a metódusok implementálását.

## Teszt Függvények

### ✓ `test_implementation_preserves_type_hints()`

Teszteli, hogy az implementáció megőrzi a típusjelzéseket.

### ✓ `test_interface_docstrings_present()`

Teszteli, hogy az interfész metódusainak van docstringje.

### ✓ `test_interface_method_order()`

Teszteli, hogy az interfész metódusai logikus sorrendben vannak.

---

**Teszt fájl:** [`tests/neural_ai/core/config/interfaces/test_config_interface.py`](../../tests/neural_ai/core/config/interfaces/test_config_interface.py)

**Tesztelt modul:** [`neural_ai/core/config/interfaces/config_interface.py`](../../neural_ai/core/config/interfaces/config_interface.py)
