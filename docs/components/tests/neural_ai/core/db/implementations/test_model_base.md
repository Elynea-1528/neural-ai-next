# 🧪 Teszt: tests/neural_ai/core/db/implementations/test_model_base.py

**Tesztelt modul:** [`neural_ai/core/db/implementations/model_base.py`](../../neural_ai/core/db/implementations/model_base.py)

Tesztek a model_base modulhoz.

Ez a modul tartalmazza a Base osztály és annak metódusainak tesztjeit.

## Teszt Osztály: `DummyModel`

Teszt modell a Base osztály teszteléséhez.

## Teszt Osztály: `TestBase`

A Base osztály tesztjei.

### ✓ `test_base_initialization()`

Teszteli a Base osztály inicializálását.

### ✓ `test_id_column_properties()`

Teszteli az id oszlop tulajdonságait.

### ✓ `test_created_at_column_properties()`

Teszteli a created_at oszlop tulajdonságait.

### ✓ `test_updated_at_column_properties()`

Teszteli az updated_at oszlop tulajdonságait.

### ✓ `test_automatic_tablename_generation()`

Teszteli az automatikus táblanév generálást.

### ✓ `test_model_creation_with_defaults()`

Teszteli a modell létrehozását alapértelmezett értékekkel.

### ✓ `test_to_dict_method()`

Teszteli a to_dict metódust.

### ✓ `test_to_dict_datetime_isoformat()`

Teszteli, hogy a datetime értékek ISO formátumban vannak-e.

### ✓ `test_repr_method()`

Teszteli a __repr__ metódust.

### ✓ `test_updated_at_changes_on_update()`

Teszteli, hogy az updated_at módosul-e frissítéskor.

### ✓ `test_created_at_does_not_change_on_update()`

Teszteli, hogy a created_at ne változzon frissítéskor.

### ✓ `test_multiple_models_have_different_ids()`

Teszteli, hogy különböző modelleknek különböző id-ja van.

---

**Teszt fájl:** [`tests/neural_ai/core/db/implementations/test_model_base.py`](../../tests/neural_ai/core/db/implementations/test_model_base.py)

**Tesztelt modul:** [`neural_ai/core/db/implementations/model_base.py`](../../neural_ai/core/db/implementations/model_base.py)
