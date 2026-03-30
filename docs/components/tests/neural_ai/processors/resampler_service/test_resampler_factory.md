# 🧪 Teszt: tests/neural_ai/processors/resampler_service/test_resampler_factory.py

**Tesztelt modul:** [`neural_ai/processors/resampler_service/resampler_factory.py`](../../neural_ai/processors/resampler_service/resampler_factory.py)

Unit tesztek a ResamplerServiceFactory-hoz.

## Teszt Osztály: `TestResamplerServiceFactory`

Tesztek a ResamplerServiceFactory osztályhoz.

### ✓ `test_create_returns_resampler_interface()`

Ellenőrzi, hogy a create metódus ResamplerInterface példányt ad vissza.

### ✓ `test_create_with_valid_dependencies()`

Ellenőrzi, hogy a create metódus megfelelő függőségekkel működik.

### ✓ `test_get_instance_returns_existing_instance()`

Ellenőrzi, hogy a get_instance visszaadja a meglévő példányt.

### ✓ `test_get_instance_creates_new_instance_if_not_exists()`

Ellenőrzi, hogy a get_instance létrehoz új példányt, ha nem létezik.

### ✓ `test_get_instance_uses_fallback_storage()`

Ellenőrzi, hogy a get_instance fallback storage-t használ, ha nincs a konténerben.

### ✓ `test_factory_create_is_static()`

Ellenőrzi, hogy a create metódus statikus.

### ✓ `test_factory_has_required_methods()`

Ellenőrzi, hogy a factory tartalmazza az összes szükséges metódust.

---

**Teszt fájl:** [`tests/neural_ai/processors/resampler_service/test_resampler_factory.py`](../../tests/neural_ai/processors/resampler_service/test_resampler_factory.py)

**Tesztelt modul:** [`neural_ai/processors/resampler_service/resampler_factory.py`](../../neural_ai/processors/resampler_service/resampler_factory.py)
