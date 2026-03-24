# 🧪 Teszt: tests/neural_ai/core/base/implementations/test_di_container.py

**Tesztelt modul:** [`neural_ai/core/base/implementations/di_container.py`](../../neural_ai/core/base/implementations/di_container.py)

Dependency injection konténer tesztjei.

## Teszt Osztály: `MockComponent`

Mock komponens teszteléshez.

## Teszt Osztály: `TestLazyComponent`

LazyComponent tesztjei.

### ✓ `test_initialization()`

Teszteli a lusta komponens inicializálását.

### ✓ `test_get_multiple_times()`

Teszteli a többszöri get hívást.

### ✓ `test_lazy_component_factory_returns_none()`

LazyComponent factory_func None visszatérése → ComponentNotFoundError.

## Teszt Osztály: `TestDIContainer`

DIContainer tesztjei.

### ✓ `test_initialization()`

Teszteli a konténer inicializálását.

### ✓ `test_register_instance()`

Teszteli az instance regisztrálását.

### ✓ `test_register_factory()`

Teszteli a factory regisztrálását.

### ✓ `test_resolve_instance()`

Teszteli az instance feloldását.

### ✓ `test_resolve_factory()`

Teszteli a factory feloldását.

### ✓ `test_resolve_not_found()`

Teszteli a nem létező komponens feloldását.

### ✓ `test_register_lazy()`

Teszteli a lusta komponens regisztrálását.

### ✓ `test_register_lazy_invalid_name()`

Teszteli az érvénytelen névvel való regisztrálást.

### ✓ `test_register_lazy_invalid_factory()`

Teszteli az érvénytelen factory-val való regisztrálást.

### ✓ `test_get_regular_instance()`

Teszteli a reguláris instance lekérését.

### ✓ `test_get_lazy_component()`

Teszteli a lusta komponens lekérését.

### ✓ `test_get_not_found()`

Teszteli a nem létező komponens lekérését.

### ✓ `test_get_lazy_components_status()`

Teszteli a lusta komponensek státuszának lekérését.

### ✓ `test_preload_components()`

Teszteli a komponensek előtöltését.

### ✓ `test_preload_components_not_found()`

Teszteli a komponensek előtöltését nem létező komponenssel.

### ✓ `test_clear()`

Teszteli a konténer ürítését.

### ✓ `test_register_method()`

Teszteli a register metódust.

### ✓ `test_register_invalid_name()`

Teszteli az érvénytelen névvel való regisztrálást.

### ✓ `test_register_none_instance()`

Teszteli a None instance regisztrálását.

### ✓ `test_enforce_singleton_violation()`

Teszteli a singleton megsértését.

### ✓ `test_enforce_singleton_no_violation()`

Teszteli, hogy azonos instance regisztrálása nem okoz problémát.

### ✓ `test_get_memory_usage()`

Teszteli a memória használat lekérését.

---

**Teszt fájl:** [`tests/neural_ai/core/base/implementations/test_di_container.py`](../../tests/neural_ai/core/base/implementations/test_di_container.py)

**Tesztelt modul:** [`neural_ai/core/base/implementations/di_container.py`](../../neural_ai/core/base/implementations/di_container.py)
