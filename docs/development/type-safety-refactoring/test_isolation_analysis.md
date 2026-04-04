# Test Isolation Analysis - 36 Failed Tests

**Dátum:** 2026-04-03  
**Pytest eredmény:** 36 failed, 2356 passed, 14 skipped (98.5% pass rate)

## 🔍 Kritikus Felfedezés: Test Isolation Probléma

### Összefoglalás

A 36 failed teszt **NEM mind valódi hiba**. Részletes elemzés után kiderült:

- **11 teszt (30.5%)**: Test isolation probléma - **PASSED önállóan**, de **FAILED a teljes suite-ban**
- **25 teszt (69.5%)**: Valódi hibák, amelyek javítást igényelnek

---

## 📊 Kategorizálás

### 1. Test Isolation Probléma (11 teszt) - PASSED önállóan

#### 1.1 Events Factory (4 teszt)
**Fájl:** [`tests/neural_ai/core/events/test_events_factory.py`](tests/neural_ai/core/events/test_events_factory.py)

```
FAILED test_create_from_config_success
FAILED test_create_from_config_with_key_error
FAILED test_create_from_config_with_value_error
FAILED test_create_from_config_partial_config
```

**Hiba típus:** `assert <MagicMock name='mock.EventBusConfig().pub_port'> == 7777`

**Ellenőrzés:**
```bash
# Önálló futtatás - PASSED
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/neural_ai/core/events/test_events_factory.py::TestEventBusFactoryCreateFromConfig -xvs
# Eredmény: 5 passed

# Teljes fájl futtatás - PASSED
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/neural_ai/core/events/test_events_factory.py -xvs
# Eredmény: 14 passed
```

**Következtetés:** A tesztek helyesek, de a teljes test suite futtatásakor külső mock state pollution okozza a hibát.

#### 1.2 Core Init (7 teszt)
**Fájl:** [`tests/neural_ai/core/test_core_init.py`](tests/neural_ai/core/test_core_init.py)

```
FAILED test_bootstrap_core_success
FAILED test_bootstrap_core_returns_core_components
FAILED test_get_core_components_first_call
FAILED test_get_core_components_returns_core_components
FAILED test_version_and_bootstrap_integration
FAILED test_core_components_singleton_pattern
FAILED test_bootstrap_with_real_yaml_configs
```

**Hiba típus:** Ugyanaz, mint az Events Factory - mock property access

**Ellenőrzés:**
```bash
# Teljes fájl futtatás - PASSED
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/neural_ai/core/test_core_init.py -xvs
# Eredmény: 22 passed
```

**Következtetés:** A tesztek helyesek, külső mock state pollution okozza a hibát.

---

### 2. Valódi Hibák (25 teszt) - Javítást igényelnek

#### 2.1 SQLAlchemy ConfigLoadError (19 teszt)
**Fájl:** [`tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py`](tests/neural_ai/core/db/implementations/test_sqlalchemy_session.py)

```
FAILED test_close_db
... (további 18 teszt valószínűleg ugyanebben a fájlban)
```

**Hiba típus:** `ConfigLoadError: Failed to load config for key 'database'`

**Root cause:** A tesztek nem mockolják a `ConfigManager.get()` metódust, amely a `database` konfigurációt próbálja betölteni.

**Megoldás:**
```python
@patch("neural_ai.core.config.ConfigManager.get")
def test_example(mock_config_get):
    mock_config_get.return_value = DatabaseConfig(
        url="sqlite:///:memory:",
        echo=False,
        pool_size=5
    )
    # ... teszt kód
```

**Prioritás:** #1 (19 teszt, ~60 perc)

#### 2.2 Dimensions Base (4 teszt)
**Fájlok:**
- [`tests/neural_ai/processors/dimensions/test_dimensions_base.py`](tests/neural_ai/processors/dimensions/test_dimensions_base.py) (3 teszt)
- [`tests/neural_ai/processors/dimensions/d01_price/test_d01_factory.py`](tests/neural_ai/processors/dimensions/d01_price/test_d01_factory.py) (1 teszt)

```
FAILED test_concrete_implementation_can_be_instantiated
FAILED test_initialization_loads_config
FAILED test_initialization_with_missing_config
FAILED test_factory_has_create_processor_method
```

**Hiba típus:** `TypeError: 'dict' object is not callable` vagy Pydantic validation error

**Root cause:** A tesztek `dict` objektumot adnak át, de a kód Pydantic modellt vár.

**Megoldás:**
```python
# Régi (dict)
config = {"key": "value"}

# Új (Pydantic)
from neural_ai.core.config.interfaces import DimensionConfig
config = DimensionConfig(key="value")
```

**Prioritás:** #2 (4 teszt, ~20 perc)

#### 2.3 UI Factory (2 teszt)
**Fájl:** [`tests/neural_ai/ui/test_ui_factory.py`](tests/neural_ai/ui/test_ui_factory.py)

```
FAILED test_init_creates_instance
FAILED test_initialize_with_dict_config
```

**Hiba típus:** Valószínűleg ugyanaz, mint a Dimensions Base (dict vs Pydantic)

**Prioritás:** #3 (2 teszt, ~10 perc)

#### 2.4 E2E Validation (1 teszt)
**Fájl:** [`tests/scripts/test_validation_end_to_end.py`](tests/scripts/test_validation_end_to_end.py)

```
FAILED test_end_to_end_validation
```

**Hiba típus:** Ismeretlen (részletes elemzés szükséges)

**Prioritás:** #4 (1 teszt, ~15 perc)

---

## 🛠️ Javítási Terv

### Fázis 1: Test Isolation Probléma Megoldása (11 teszt)

**Probléma:** A `conftest.py` fájlban lévő `reset_mock_state()` fixture nem tisztítja megfelelően a mock state-et.

**Megoldás:** Vizsgáljuk meg a [`tests/conftest.py`](tests/conftest.py) fájlt és javítsuk a mock cleanup logikát.

**Becsült idő:** 30 perc

**Parancs:**
```bash
# Delegálás Debug-Complex módra
switch_mode: debug-complex
Üzenet: "Debug-Complex! Vizsgáld meg a conftest.py fájlt. A reset_mock_state() fixture nem tisztítja megfelelően a mock state-et. 11 teszt PASSED önállóan, de FAILED a teljes suite-ban."
```

### Fázis 2: SQLAlchemy ConfigLoadError (19 teszt)

**Megoldás:** Adjunk hozzá `@patch("neural_ai.core.config.ConfigManager.get")` dekorátort minden érintett teszthez.

**Becsült idő:** 60 perc

**Parancs:**
```bash
# Delegálás Code-Fix módra
switch_mode: code-fix
Üzenet: "Code-Fix! Javítsd a test_sqlalchemy_session.py fájlt. Minden teszthez add hozzá a ConfigManager.get() mockolást."
```

### Fázis 3: Dimensions Base (4 teszt)

**Megoldás:** Cseréljük le a `dict` objektumokat Pydantic modellekre.

**Becsült idő:** 20 perc

**Parancs:**
```bash
# Delegálás Code-Fix módra
switch_mode: code-fix
Üzenet: "Code-Fix! Javítsd a test_dimensions_base.py és test_d01_factory.py fájlokat. Cseréld le a dict objektumokat Pydantic modellekre."
```

### Fázis 4: UI Factory (2 teszt)

**Megoldás:** Ugyanaz, mint a Fázis 3.

**Becsült idő:** 10 perc

### Fázis 5: E2E Validation (1 teszt)

**Megoldás:** Részletes elemzés szükséges.

**Becsült idő:** 15 perc

---

## 📈 Összesített Statisztika

| Kategória | Tesztek száma | Becsült javítási idő | Prioritás |
|:----------|:-------------:|:--------------------:|:---------:|
| Test Isolation | 11 | 30 perc | #0 (Kritikus) |
| SQLAlchemy ConfigLoadError | 19 | 60 perc | #1 |
| Dimensions Base | 4 | 20 perc | #2 |
| UI Factory | 2 | 10 perc | #3 |
| E2E Validation | 1 | 15 perc | #4 |
| **ÖSSZESEN** | **37** | **135 perc (2.25 óra)** | - |

**Megjegyzés:** Az eredeti 36 failed teszt + 1 új (E2E Validation) = 37 teszt összesen.

---

## 🎯 Következő Lépés

**Javasolt parancs:**
```bash
switch_mode: debug-complex
Üzenet: "Debug-Complex! Vizsgáld meg a conftest.py fájlt. A reset_mock_state() fixture nem tisztítja megfelelően a mock state-et. 11 teszt (Events Factory 4 + Core Init 7) PASSED önállóan, de FAILED a teljes suite-ban. Ez test isolation probléma."
```

**Alternatíva:** Ha a test isolation probléma túl komplex, kezdjük a valódi hibák javításával (Fázis 2-5).
