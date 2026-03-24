# 🧪 Teszt: tests/neural_ai/core/utils/test_decorators.py

**Tesztelt modul:** [`neural_ai/core/utils/decorators.py`](../../neural_ai/core/utils/decorators.py)

Tesztek a neural_ai.core.utils.decorators modulhoz.

Ez a modul tartalmazza a @trace dekorátor tesztjeit, beleértve a
normál működést, hibakezelést, argumentum szerializálást és teljesítményt.

## Teszt Osztály: `TestTraceDecorator`

Tesztek a @trace dekorátorhoz.

### ✓ `test_trace_successful_execution()`

Teszteli a sikeres függvényhívás logolását.

### ✓ `test_trace_with_kwargs()`

Teszteli a kulcsszavas argumentumokkal történő hívást.

### ✓ `test_trace_with_unsafe_args()`

Teszteli a nem biztonságos argumentumok logolását.

### ✓ `test_trace_function_name_preserved()`

Teszteli, hogy a függvény neve megőrződik a dekorálás után.

### ✓ `test_trace_docstring_preserved()`

Teszteli, hogy a függvény docstringje megőrződik.

### ✓ `test_trace_exception_handling()`

Teszteli a kivételkezelést és logolást.

### ✓ `test_trace_call_id_uniqueness()`

Teszteli, hogy minden hívás egyedi call_id-t kap.

### ✓ `test_trace_duration_measurement()`

Teszteli a futási idő mérésének helyességét.

### ✓ `test_trace_with_mixed_args()`

Teszteli a vegyes típusú argumentumok kezelését.

### ✓ `test_trace_no_args_function()`

Teszteli az argumentumok nélküli függvényt.

### ✓ `test_trace_with_safe_types()`

Teszteli a biztonságos típusok logolását.

## Teszt Osztály: `TestTraceDecoratorIntegration`

Integrációs tesztek a @trace dekorátorhoz.

### ✓ `test_trace_real_logger()`

Teszteli a dekorátort valós loggerrel.

### ✓ `test_trace_performance_overhead()`

Teszteli a dekorátor teljesítménybeli hatását.

---

**Teszt fájl:** [`tests/neural_ai/core/utils/test_decorators.py`](../../tests/neural_ai/core/utils/test_decorators.py)

**Tesztelt modul:** [`neural_ai/core/utils/decorators.py`](../../neural_ai/core/utils/decorators.py)
