# 🧪 Teszt: tests/neural_ai/collectors/jforex/test_live_feed_integration.py

**Tesztelt modul:** [`neural_ai/collectors/jforex/live_feed_integration.py`](../../neural_ai/collectors/jforex/live_feed_integration.py)

JForex Live Feed Integration Tests.

Ez a modul tartalmazza a JForexLiveFeed integrációs tesztjeit.
A tesztek a valós JForexLiveFeed logikát használják, de a ZMQ socketet mock-olják.

## Teszt Osztály: `TestJForexLiveFeedIntegration`

JForexLiveFeed integrációs tesztjei.

### ✓ `test_valid_json_creates_market_data_event()`

Teszteli, hogy érvényes JSON input MarketDataEvent-et hoz létre.

### ✓ `test_invalid_json_handles_gracefully()`

Teszteli, hogy hibás JSON string gracefully kezelődik.

### ✓ `test_missing_required_fields()`

Teszteli, hogy hiányzó kötelező mezők esetén error log történik.

### ✓ `test_negative_bid_price()`

Teszteli, hogy negatív bid ár Pydantic validáció hibát okoz.

### ✓ `test_multiple_ticks_sequential()`

Teszteli, hogy több tick egymás után feldolgozható.

### ✓ `test_zmq_socket_mock_full_flow()`

Teszteli a teljes flowt: ZMQ context → socket → recv_string → MarketDataEvent.

### ✓ `test_reconnect_on_socket_error()`

Teszteli, hogy socket ZMQError esetén a listen loop nem crashel, hanem logol.

### ✓ `test_event_bus_publish_called_with_correct_topic()`

Teszteli, hogy az event bus publish mindig 'market_data' topickal hívódik.

---

**Teszt fájl:** [`tests/neural_ai/collectors/jforex/test_live_feed_integration.py`](../../tests/neural_ai/collectors/jforex/test_live_feed_integration.py)

**Tesztelt modul:** [`neural_ai/collectors/jforex/live_feed_integration.py`](../../neural_ai/collectors/jforex/live_feed_integration.py)
