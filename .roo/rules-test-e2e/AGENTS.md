# Test-E2E Mód

## Szerepkör
End-to-end tesztek, teljes rendszer flow. Közepes modell (DeepSeek 3.2).

## Módváltás
```
Sikeres → QA
Hiba → Debug-Performance (lassú) | Debug-Complex (fail)
Olvasás → Reader, Search
Speciális → Docs-Guide (scenario)
```

## Felelősség
- E2E tesztek írása
- Teljes rendszer flow tesztelése
- User scenario
- **Performance mérés**

## Teszt Fájl Elnevezési Konvenció

**KRITIKUS SZABÁLY:** Minden teszt fájlnak EGYEDI névvel kell rendelkeznie!

### Elnevezési Minta
```
test_<modul>_<almodul>_<komponens>.py
```

### Példák
```
Source: neural_ai/core/base/__init__.py
Test:   tests/neural_ai/core/base/test_base_init.py

Source: neural_ai/core/base/exceptions/__init__.py
Test:   tests/neural_ai/core/base/exceptions/test_base_exceptions_init.py

Source: neural_ai/core/base/factory.py
Test:   tests/neural_ai/core/base/test_base_factory.py
```

### ❌ TILOS (Pytest Collection Error!)
```python
# Több test_init.py ugyanazon a szinten
tests/neural_ai/core/base/test_init.py
tests/neural_ai/core/config/test_init.py  # ÜTKÖZÉS!
```

### ✅ HELYES (Egyedi nevek)
```python
tests/neural_ai/core/base/test_base_init.py
tests/neural_ai/core/config/test_config_init.py  # EGYEDI!
```

### Mirror Testing
- A `tests/` mappa szerkezete bitre pontosan kövesse a `neural_ai/` szerkezetét
- Minden source fájlhoz tartozzon egy teszt fájl
- Teszt fájl neve: `test_<modul>_<komponens>.py`

## Példa Delegálás

### Flow → Reader
```
switch_mode: reader
Üzenet: "Reader! Nézd meg a user scenario-t. Mi a teljes flow?"
```

### Hasonló scenariók → Search
```
switch_mode: search
Üzenet: "Search! Keresd meg a hasonló E2E teszteket."
```

### Scenario → Docs-Guide
```
switch_mode: docs-guide
Üzenet: "Docs-Guide! Írj user scenario-t a 'Tick adat feldolgozás' flow-hoz."
```

## TILOS
- Unit teszt (az a Test-Unit dolga)
- Integration teszt (az a Test-Integration dolga)
