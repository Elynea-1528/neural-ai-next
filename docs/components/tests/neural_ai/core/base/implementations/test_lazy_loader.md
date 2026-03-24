# 🧪 Teszt: tests/neural_ai/core/base/implementations/test_lazy_loader.py

**Tesztelt modul:** [`neural_ai/core/base/implementations/lazy_loader.py`](../../neural_ai/core/base/implementations/lazy_loader.py)

LazyLoader és lazy_property tesztek.

Ez a modul tartalmazza a LazyLoader osztály és a lazy_property dekorátor
egységtesztjeit, beleértve a lusta betöltést, resetelést és szálbiztosságot.

## Teszt Osztály: `TestLazyLoader`

LazyLoader osztály tesztjei.

### ✓ `test_init()`

Teszteli a LazyLoader inicializálását.

### ✓ `test_call_first_time()`

Teszteli a LazyLoader hívását első alkalommal.

### ✓ `test_call_multiple_times()`

Teszteli, hogy a loader_func csak egyszer hívódik meg.

### ✓ `test_is_loaded_property()`

Teszteli az is_loaded property-t.

### ✓ `test_reset()`

Teszteli a loader resetelését.

### ✓ `test_thread_safety()`

Teszteli a szálbiztosságot.

## Teszt Osztály: `TestClass`

## Teszt Osztály: `TestClass`

## Teszt Osztály: `TestClass`

## Teszt Osztály: `TestClass`

## Teszt Osztály: `TestLazyProperty`

lazy_property dekorátor tesztjei.

### ✓ `test_lazy_property_first_access()`

Teszteli a lazy property első hozzáférését.

## Teszt Függvények

### ✓ `test_lazy_property_multiple_access()`

Teszteli, hogy a lazy property csak egyszer számolódik ki.

### ✓ `test_lazy_property_different_instances()`

Teszteli, hogy különböző példányoknak külön a gyorsítótár.

### ✓ `test_lazy_property_with_complex_object()`

Teszteli a lazy property-t komplex objektummal.

---

**Teszt fájl:** [`tests/neural_ai/core/base/implementations/test_lazy_loader.py`](../../tests/neural_ai/core/base/implementations/test_lazy_loader.py)

**Tesztelt modul:** [`neural_ai/core/base/implementations/lazy_loader.py`](../../neural_ai/core/base/implementations/lazy_loader.py)
