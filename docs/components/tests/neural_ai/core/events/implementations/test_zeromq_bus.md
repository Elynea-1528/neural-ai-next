# 🧪 Teszt: tests/neural_ai/core/events/implementations/test_zeromq_bus.py

**Tesztelt modul:** [`neural_ai/core/events/implementations/zeromq_bus.py`](../../neural_ai/core/events/implementations/zeromq_bus.py)

Tesztek a ZeroMQBus implementációhoz.

Ez a modul tartalmazza a ZeroMQBus tesztjeit, ZMQ mocking-gal.

Author: Neural AI Next Team
Version: 1.0.0

## Teszt Osztály: `TestEventBusInitialization`

EventBus inicializálás tesztek.

### ✓ `test_default_initialization()`

Teszteli az alapértelmezett inicializálást.

### ✓ `test_custom_config_initialization()`

Teszteli az egyéni konfigurációval történő inicializálást.

### ✓ `test_external_zmq_context()`

Teszteli a külső ZMQ kontextus használatát.

### ✓ `test_zmq_import_error()`

Teszteli a ZMQ import hibát.

## Teszt Osztály: `TestEventBusStartStop`

EventBus indítás és leállítás tesztek.

### ✓ `test_start_success()`

Teszteli a sikeres indítást.

### ✓ `test_start_with_inproc()`

Teszteli az indítást inproc transporttal.

### ✓ `test_start_twice()`

Teszteli a többszöri indítást.

### ✓ `test_stop_success()`

Teszteli a sikeres leállítást.

### ✓ `test_stop_without_start()`

Teszteli a leállítást indítás nélkül.

### ✓ `test_stop_twice()`

Teszteli a többszöri leállítást.

## Teszt Osztály: `TestEventBusPublish`

EventBus publish tesztek.

### ✓ `test_publish_success()`

Teszteli a sikeres esemény közzétételt.

### ✓ `test_publish_not_started()`

Teszteli a közzétételt indítás nélkül.

### ✓ `test_publish_no_publisher()`

Teszteli a közzétételt publisher socket nélkül.

### ✓ `test_publish_batch_events()`

Teszteli a batch (lista) események közzétételét.

## Teszt Osztály: `TestEventBusSubscribeUnsubscribe`

EventBus feliratkozás és leiratkozás tesztek.

### ✓ `test_subscribe_new_event_type()`

Teszteli az új eseménytípusra való feliratkozást.

### ✓ `test_subscribe_multiple_callbacks()`

Teszteli több callback feliratkozását ugyanarra az eseménytípusra.

### ✓ `test_unsubscribe_existing()`

Teszteli a létező feliratkozás lemondását.

### ✓ `test_unsubscribe_non_existing()`

Teszteli a nem létező feliratkozás lemondását.

### ✓ `test_unsubscribe_non_existing_event_type()`

Teszteli a nem létező eseménytípus lemondását.

## Teszt Osztály: `TestEventBusContextManager`

EventBus context manager tesztek.

### ✓ `test_async_context_manager()`

Teszteli az aszinkron context managert.

## Teszt Osztály: `TestEventBusDeserialization`

EventBus deszerializáció tesztek.

### ✓ `test_deserialize_market_data()`

Teszteli a MarketDataEvent deszerializációját.

### ✓ `test_deserialize_unknown_event_type()`

Teszteli az ismeretlen eseménytípus deszerializációját.

### ✓ `test_deserialize_invalid_data()`

Teszteli az érvénytelen adat deszerializációját.

## Teszt Osztály: `TestEventBusDispatch`

EventBus esemény továbbítás tesztek.

### ✓ `test_dispatch_event_success()`

Teszteli a sikeres esemény továbbítást.

### ✓ `test_dispatch_event_no_subscribers()`

Teszteli az esemény továbbítást feliratkozók nélkül.

### ✓ `test_dispatch_event_callback_error()`

Teszteli a callback hibát.

## Teszt Osztály: `TestEventBusDeserializationAdditional`

További deszerializáció tesztek a hiányzó sorok lefedésére.

### ✓ `test_deserialize_trade_event()`

Teszteli a TradeEvent deszerializációját.

### ✓ `test_deserialize_signal_event()`

Teszteli a SignalEvent deszerializációját.

### ✓ `test_deserialize_system_log_event()`

Teszteli a SystemLogEvent deszerializációját.

### ✓ `test_deserialize_order_event()`

Teszteli a OrderEvent deszerializációját.

### ✓ `test_deserialize_position_event()`

Teszteli a PositionEvent deszerializációját.

## Teszt Osztály: `TestEventBusDispatchExceptionHandling`

Esemény továbbítás kivételkezelés tesztek.

### ✓ `test_dispatch_event_deserialization_error()`

Teszteli a deserializálási hiba kezelését.

### ✓ `test_dispatch_event_deserialization_returns_none()`

Teszteli a None visszatérési érték kezelését.

### ✓ `test_dispatch_event_outer_exception_handling()`

Teszteli a külső try-except blokk kivételkezelését (219-220. sorok).

## Teszt Osztály: `TestEventBusRunForever`

EventBus run_forever metódus tesztek.

### ✓ `test_run_forever_success()`

Teszteli a run_forever sikeres futását.

### ✓ `test_run_forever_timeout_handling()`

Teszteli a timeout kezelését a run_forever-ben.

### ✓ `test_run_forever_not_started()`

Teszteli a run_forever hívását indítás nélkül.

### ✓ `test_run_forever_message_processing()`

Teszteli az üzenet feldolgozást a run_forever-ben.

### ✓ `test_run_forever_invalid_message_format()`

Teszteli az érvénytelen üzenet formátum kezelését.

### ✓ `test_run_forever_json_decode_error()`

Teszteli a JSON decode hiba kezelését.

### ✓ `test_run_forever_general_exception_handling()`

Teszteli az általános kivétel kezelését a run_forever-ben.

### ✓ `test_run_forever_with_inproc()`

Teszteli a run_forever-t inproc transporttal (284. sor lefedése).

## Teszt Osztály: `TestEventBusErrorHandling`

EventBus hiba kezelés tesztek a lefedettség növelésére.

### ✓ `test_publish_error_zmq_exception()`

Teszteli a publish során fellépő ZMQError kezelését.

### ✓ `test_publish_error_general_exception()`

Teszteli a publish során fellépő általános kivétel kezelését.

### ✓ `test_publish_error_with_callback()`

Teszteli a publish hibakezelését callbackkel együtt.

### ✓ `test_subscribe_error_setsockopt_exception()`

Teszteli a subscribe során fellépő setsockopt hiba kezelését.

### ✓ `test_subscribe_error_setsockopt_general_exception()`

Teszteli a subscribe során fellépő általános setsockopt hiba kezelését.

### ✓ `test_start_error_socket_bind_failure()`

Teszteli a socket bind hiba kezelését az indításkor.

### ✓ `test_stop_error_socket_close_failure()`

Teszteli a socket close hiba kezelését a leállításkor.

---

**Teszt fájl:** [`tests/neural_ai/core/events/implementations/test_zeromq_bus.py`](../../tests/neural_ai/core/events/implementations/test_zeromq_bus.py)

**Tesztelt modul:** [`neural_ai/core/events/implementations/zeromq_bus.py`](../../neural_ai/core/events/implementations/zeromq_bus.py)
