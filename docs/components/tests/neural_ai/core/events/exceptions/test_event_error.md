# 🧪 Teszt: tests/neural_ai/core/events/exceptions/test_event_error.py

**Tesztelt modul:** [`neural_ai/core/events/exceptions/event_error.py`](../../neural_ai/core/events/exceptions/event_error.py)

EventBus kivételek tesztek.

## Teszt Osztály: `TestEventBusError`

EventBusError osztály tesztei.

### ✓ `test_event_bus_error_creation()`

EventBusError létrehozásának tesztelése.

### ✓ `test_event_bus_error_with_details()`

EventBusError létrehozása részletekkel.

### ✓ `test_event_bus_error_is_neural_ai_exception()`

EventBusError NeuralAIException-ből származik.

## Teszt Osztály: `TestPublishError`

PublishError osztály tesztei.

### ✓ `test_publish_error_creation()`

PublishError létrehozásának tesztelése.

### ✓ `test_publish_error_with_event_type()`

PublishError létrehozása event type-nal.

### ✓ `test_publish_error_inheritance()`

PublishError EventBusError-ből származik.

## Teszt Osztály: `TestSubscriberError`

SubscriberError osztály tesztei.

### ✓ `test_subscriber_error_creation()`

SubscriberError létrehozásának tesztelése (47-48. sorok).

### ✓ `test_subscriber_error_with_subscriber_id()`

SubscriberError létrehozása subscriber ID-vel (47-48. sorok).

### ✓ `test_subscriber_error_inheritance()`

SubscriberError EventBusError-ből származik.

---

**Teszt fájl:** [`tests/neural_ai/core/events/exceptions/test_event_error.py`](../../tests/neural_ai/core/events/exceptions/test_event_error.py)

**Tesztelt modul:** [`neural_ai/core/events/exceptions/event_error.py`](../../neural_ai/core/events/exceptions/event_error.py)
