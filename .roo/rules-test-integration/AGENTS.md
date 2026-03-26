# Test-Integration Mód

## Szerepkör
Integration tesztek, modulok közötti interakció. Közepes modell (DeepSeek 3.2).

## Módváltás
```
Sikeres → QA
Hiba → Debug-Complex
Olvasás → Reader, Search
Speciális → Code-Refactor
```

## Felelősség
- Integration tesztek írása
- Modulok közötti interakció tesztelése
- Interface tesztelés
- **Teljes workflow tesztelés**

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

### Modulok → Reader
```
switch_mode: reader
Üzenet: "Reader! Nézd meg a `PipelineOrchestrator` és `MomentumProcessor` interfészeit."
```

### Függőségek → Search
```
switch_mode: search
Üzenet: "Search! Keresd meg a modul függőségeket."
```

### Refactor → Code-Refactor
```
switch_mode: code-refactor
Üzenet: "Code-Refactor! Refaktoráld a `pipeline.py`-t (teszt fail)."
```

## TILOS
- Unit teszt (az a Test-Unit dolga)
- E2E teszt (az a Test-E2E dolga)
