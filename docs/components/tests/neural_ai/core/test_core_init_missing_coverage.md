# 🧪 Teszt: tests/neural_ai/core/test_core_init_missing_coverage.py

**Tesztelt modul:** [`neural_ai/core/core_init_missing_coverage.py`](../../neural_ai/core/core_init_missing_coverage.py)

Tesztek a neural_ai.core.__init__.py hiányzó coverage ágaihoz.

Ez a tesztmodul kiegészíti a test_core_init.py-t, és a következő
hiányzó ágakat fedi le:
- Storage inicializálási hiba (144-147)
- JForex Live Feed inicializálás (200-202)

## Teszt Osztály: `TestBootstrapCoreStorageError`

Tesztek a bootstrap_core storage hibakezelésére.

### ✓ `test_bootstrap_core_storage_init_failure()`

Teszteli a bootstrap_core függvényt storage inicializálási hiba esetén. Ez a teszt lefedi a 144-147 sorokat (storage exception handling).

## Teszt Osztály: `TestBootstrapCoreJForexLiveFeed`

Tesztek a bootstrap_core JForex Live Feed inicializálására.

### ✓ `test_bootstrap_core_jforex_live_feed_enabled()`

Teszteli a bootstrap_core függvényt JForex Live Feed engedélyezve esetén. Ez a teszt lefedi a 200-202 sorokat (JForex live feed init).

---

**Teszt fájl:** [`tests/neural_ai/core/test_core_init_missing_coverage.py`](../../tests/neural_ai/core/test_core_init_missing_coverage.py)

**Tesztelt modul:** [`neural_ai/core/core_init_missing_coverage.py`](../../neural_ai/core/core_init_missing_coverage.py)
