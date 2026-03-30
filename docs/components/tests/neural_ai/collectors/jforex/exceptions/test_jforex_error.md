# 🧪 Teszt: tests/neural_ai/collectors/jforex/exceptions/test_jforex_error.py

**Tesztelt modul:** [`neural_ai/collectors/jforex/exceptions/jforex_error.py`](../../neural_ai/collectors/jforex/exceptions/jforex_error.py)

Unit tesztek a JForex Exception osztályokhoz.

## Teszt Osztály: `TestJForexError`

Tesztek a JForexError alap kivételhez.

### ✓ `test_jforex_error_is_exception()`

Ellenőrzi, hogy JForexError az Exception leszármazottja.

### ✓ `test_jforex_error_can_be_raised()`

Ellenőrzi, hogy JForexError dobható.

### ✓ `test_jforex_error_with_message()`

Ellenőrzi, hogy JForexError üzenettel dobható.

## Teszt Osztály: `TestDownloadError`

Tesztek a DownloadError kivételhez.

### ✓ `test_download_error_is_jforex_error()`

Ellenőrzi, hogy DownloadError a JForexError leszármazottja.

### ✓ `test_download_error_can_be_raised()`

Ellenőrzi, hogy DownloadError dobható.

### ✓ `test_download_error_with_message()`

Ellenőrzi, hogy DownloadError üzenettel dobható.

### ✓ `test_download_error_caught_as_jforex_error()`

Ellenőrzi, hogy DownloadError elkapható JForexError-ként.

## Teszt Osztály: `TestDecodeError`

Tesztek a DecodeError kivételhez.

### ✓ `test_decode_error_is_jforex_error()`

Ellenőrzi, hogy DecodeError a JForexError leszármazottja.

### ✓ `test_decode_error_can_be_raised()`

Ellenőrzi, hogy DecodeError dobható.

### ✓ `test_decode_error_with_message()`

Ellenőrzi, hogy DecodeError üzenettel dobható.

### ✓ `test_decode_error_caught_as_jforex_error()`

Ellenőrzi, hogy DecodeError elkapható JForexError-ként.

## Teszt Osztály: `TestDataNotAvailableError`

Tesztek a DataNotAvailableError kivételhez.

### ✓ `test_data_not_available_error_is_jforex_error()`

Ellenőrzi, hogy DataNotAvailableError a JForexError leszármazottja.

### ✓ `test_data_not_available_error_can_be_raised()`

Ellenőrzi, hogy DataNotAvailableError dobható.

### ✓ `test_data_not_available_error_with_message()`

Ellenőrzi, hogy DataNotAvailableError üzenettel dobható.

### ✓ `test_data_not_available_error_caught_as_jforex_error()`

Ellenőrzi, hogy DataNotAvailableError elkapható JForexError-ként.

---

**Teszt fájl:** [`tests/neural_ai/collectors/jforex/exceptions/test_jforex_error.py`](../../tests/neural_ai/collectors/jforex/exceptions/test_jforex_error.py)

**Tesztelt modul:** [`neural_ai/collectors/jforex/exceptions/jforex_error.py`](../../neural_ai/collectors/jforex/exceptions/jforex_error.py)
