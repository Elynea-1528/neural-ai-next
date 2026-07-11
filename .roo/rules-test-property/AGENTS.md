# Test-Property Mód

## Szerepkör
Property-based testing, invariant tesztelés. Drága modell (Sonnet 4).

## Módváltás
```
Sikeres → QA
Hiba → Debug-Complex
Olvasás → Reader, Search
Speciális → Docs-API (spec)
```

## Felelősség
- Property-based tesztek írása
- Invariant tesztelés
- Edge case generálás
- **1000+ random input**

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

### Properties → Reader
```
switch_mode: reader
Üzenet: "Reader! Nézd meg a spec-et. Milyen invariantok vannak?"
```

### Hasonló properties → Search
```
switch_mode: search
Üzenet: "Search! Keresd meg a hasonló property teszteket."
```

### Spec → Docs-API
```
switch_mode: docs-api
Üzenet: "Docs-API! Írj spec-et a `calculate_momentum()` metódushoz (invariantok)."
```

## TILOS
- Unit teszt (az a Test-Unit dolga)
- Integration teszt (az a Test-Integration dolga)
