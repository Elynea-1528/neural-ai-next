# neural_ai/collectors/jforex/exceptions/jforex_error.py

JForex Collector Exceptions.

## Osztály: `JForexError(Exception)`

Alap kivétel minden JForex Collector hibához.

## Osztály: `DownloadError(JForexError)`

Adat letöltési hiba esetén dobódik.

Ide tartoznak a hálózati hibák, szerverhibák és időtúllépések.

## Osztály: `DecodeError(JForexError)`

.bi5 adat dekódolási hiba esetén dobódik.

Ide tartoznak az LZMA dekompressziós hibák és a struct kicsomagolási hibák.

## Osztály: `DataNotAvailableError(JForexError)`

A kért dátumhoz nem elérhető adat esetén dobódik.

Ez általában hétvégéken, ünnepeken vagy amikor a piac zárva volt történik.

---

**Forrásfájl:** [`neural_ai/collectors/jforex/exceptions/jforex_error.py`](../../neural_ai/collectors/jforex/exceptions/jforex_error.py)
