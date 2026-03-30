# 🧪 Teszt: tests/neural_ai/ui/services/test_ai_service.py

**Tesztelt modul:** [`neural_ai/ui/services/ai_service.py`](../../neural_ai/ui/services/ai_service.py)

Unit tesztek az ai_service modulhoz.

# pyright: reportUnknownArgumentType=false
# Mock config dict type inference hibák.

Ez a modul teszteli az AIService osztály funkcióit.

## Teszt Osztály: `TestAIServiceInit`

Tesztek az AIService inicializálásához.

### ✓ `test_init_creates_instance()`

Ellenőrzi, hogy az AIService létrehozható.

## Teszt Osztály: `TestAIServiceGetAvailableModels`

Tesztek a get_available_models metódushoz.

### ✓ `test_get_available_models_returns_list()`

Ellenőrzi, hogy a modellek listáját adja vissza.

## Teszt Osztály: `TestAIServiceLoadModel`

Tesztek a load_model metódushoz.

### ✓ `test_load_model_raises_error_for_unknown_model()`

Ellenőrzi, hogy hiba dobódik ismeretlen modellre.

### ✓ `test_load_model_raises_error_for_unavailable_model()`

Ellenőrzi, hogy hiba dobódik nem elérhető modellre.

### ✓ `test_load_model_success()`

Ellenőrzi, hogy a modell betöltése sikeres.

### ✓ `test_load_model_with_config()`

Ellenőrzi, hogy a modell betöltése konfigurációval működik.

## Teszt Osztály: `TestAIServiceRunInference`

Tesztek a run_inference metódushoz.

### ✓ `test_run_inference_raises_error_for_unloaded_model()`

Ellenőrzi, hogy hiba dobódik nem betöltött modellre.

### ✓ `test_run_inference_success()`

Ellenőrzi, hogy az inferencia futtatása sikeres.

## Teszt Osztály: `TestAIServiceGetModelInfo`

Tesztek a get_model_info metódushoz.

### ✓ `test_get_model_info_raises_error_for_unknown_model()`

Ellenőrzi, hogy hiba dobódik ismeretlen modellre.

### ✓ `test_get_model_info_success()`

Ellenőrzi, hogy a modell információk lekérdezése sikeres.

## Teszt Osztály: `TestAIServiceTrainModel`

Tesztek a train_model metódushoz.

### ✓ `test_train_model_raises_error_for_unknown_model()`

Ellenőrzi, hogy hiba dobódik ismeretlen modellre.

### ✓ `test_train_model_success()`

Ellenőrzi, hogy a modell tanítása sikeres.

### ✓ `test_train_model_with_config()`

Ellenőrzi, hogy a modell tanítása konfigurációval működik.

## Teszt Osztály: `TestAIServiceGetTrainingStatus`

Tesztek a get_training_status metódushoz.

### ✓ `test_get_training_status_raises_error_for_unknown_training()`

Ellenőrzi, hogy hiba dobódik ismeretlen tanításra.

### ✓ `test_get_training_status_success()`

Ellenőrzi, hogy a tanítás állapotának lekérdezése sikeres.

---

**Teszt fájl:** [`tests/neural_ai/ui/services/test_ai_service.py`](../../tests/neural_ai/ui/services/test_ai_service.py)

**Tesztelt modul:** [`neural_ai/ui/services/ai_service.py`](../../neural_ai/ui/services/ai_service.py)
