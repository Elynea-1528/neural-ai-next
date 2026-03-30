# 🧪 Teszt: tests/neural_ai/ui/test_app.py

**Tesztelt modul:** [`neural_ai/ui/app.py`](../../neural_ai/ui/app.py)

Unit tesztek az app modulhoz.

Ez a modul teszteli a UIApplication osztály funkcióit.

## Teszt Osztály: `TestUIApplicationInit`

Tesztek a UIApplication inicializálásához.

### ✓ `test_init_without_parameters()`

Ellenőrzi, hogy a UIApplication létrehozható paraméterek nélkül.

### ✓ `test_init_with_config()`

Ellenőrzi, hogy a UIApplication létrehozható konfigurációval.

### ✓ `test_init_with_logger()`

Ellenőrzi, hogy a UIApplication létrehozható loggerrel.

## Teszt Osztály: `TestUIApplicationInitialize`

Tesztek a UIApplication.initialize metódushoz.

### ✓ `test_initialize_success()`

Ellenőrzi, hogy az initialize sikeresen inicializálja az alkalmazást.

### ✓ `test_initialize_with_existing_logger()`

Ellenőrzi, hogy az initialize használja a meglévő loggert.

### ✓ `test_initialize_handles_exception()`

Ellenőrzi, hogy az initialize kezeli a kivételeket.

## Teszt Osztály: `TestUIApplicationRun`

Tesztek a UIApplication.run metódushoz.

### ✓ `test_run_without_initialization_raises_error()`

Ellenőrzi, hogy a run hibát dob inicializálás nélkül.

### ✓ `test_run_success()`

Ellenőrzi, hogy a run sikeresen elindítja az alkalmazást.

## Teszt Osztály: `TestUIApplicationStop`

Tesztek a UIApplication.stop metódushoz.

### ✓ `test_stop_success()`

Ellenőrzi, hogy a stop sikeresen leállítja az alkalmazást.

## Teszt Osztály: `TestUIApplicationGetters`

Tesztek a UIApplication getter metódusokhoz.

### ✓ `test_get_navigation_service_without_initialization_raises_error()`

Ellenőrzi, hogy a get_navigation_service hibát dob inicializálás nélkül.

### ✓ `test_get_factory_without_initialization_raises_error()`

Ellenőrzi, hogy a get_factory hibát dob inicializálás nélkül.

### ✓ `test_get_navigation_service_success()`

Ellenőrzi, hogy a get_navigation_service visszaadja a navigation service-t.

### ✓ `test_get_factory_success()`

Ellenőrzi, hogy a get_factory visszaadja a factory-t.

## Teszt Osztály: `TestUIApplicationProperties`

Tesztek a UIApplication property-khez.

### ✓ `test_is_running_default_false()`

Ellenőrzi, hogy az is_running alapértelmezetten False.

### ✓ `test_is_running_true_after_run()`

Ellenőrzi, hogy az is_running True a run után.

### ✓ `test_is_running_false_after_stop()`

Ellenőrzi, hogy az is_running False a stop után.

---

**Teszt fájl:** [`tests/neural_ai/ui/test_app.py`](../../tests/neural_ai/ui/test_app.py)

**Tesztelt modul:** [`neural_ai/ui/app.py`](../../neural_ai/ui/app.py)
