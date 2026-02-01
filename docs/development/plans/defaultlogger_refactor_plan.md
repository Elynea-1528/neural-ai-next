# DefaultLogger Refactoring Plan - Structlog API Compliance

**Verzió:** 1.0 | **Státusz:** 📋 TERVEZÉS | **Dátum:** 2026-02-01  
**Prioritás:** 🟡 P1 - KRITIKUS (M2 Milestone)

---

## 📊 Jelenlegi Helyzet

### Implementáció Állapot
**Fájl:** [`neural_ai/core/logger/implementations/default_logger.py`](../../../neural_ai/core/logger/implementations/default_logger.py)

**Sor 60:**
```python
self.logger = structlog.get_logger(name)  # ← STRUCTLOG használat!
```

**Típus:**
- `structlog.BoundLoggerLazyProxy` objektum
- **NEM** `logging.Logger`

### Teszt Állapot
**Fájl:** [`tests/core/logger/implementations/test_default_logger.py`](../../../tests/core/logger/implementations/test_default_logger.py)

**Jelenlegi tesztek (73 sor):**
- `test_init_basic` - Attribútum ellenőrzés
- `test_init_with_custom_level` - Szint konfiguráció
- `test_debug/info/warning/error/critical_logging` - Output capture (capsys)
- `test_set_level` - Szint módosítás
- `test_di_dependencies_none` - DI kompatibilitás

---

## 🔍 Structlog vs Logging.Logger API Különbségek

### 1. Típus & Attribútumok

| Aspektus | `logging.Logger` | `structlog.BoundLoggerLazyProxy` |
|----------|------------------|----------------------------------|
| **Típus** | `<class 'logging.Logger'>` | `<class 'BoundLoggerLazyProxy'>` |
| `.name` | ✅ Van | ❌ Nincs |
| `.handlers` | ✅ Van (list) | ❌ Nincs |
| `.level` | ✅ Van | ❌ Nincs (központi config) |
| `.debug()`, `.info()`, stb. | ✅ Van | ✅ Van |

### 2. Kimenet Stream

| Logger Típus | Alapértelmezett Output |
|--------------|------------------------|
| `logging.Logger` | **stderr** |
| `structlog` | **stdout** |

### 3. Formázás

```python
# logging.Logger
logger.info("Message", extra={"key": "value"})
# Output: "2026-02-01 12:00:00 - my_app - INFO - Message"

# structlog
logger.info("Message", key="value")
# Output (JSON): {"event": "Message", "key": "value", "timestamp": "2026-02-01T12:00:00"}
```

---

## 🚨 Várható Problémák (TEST_ANALYSIS.md szerint)

### 8 FAILED Teszt Kategóriái:

#### 1. Típus Ellenőrzés (`test_init_basic`)
**Probléma:**
```python
assert isinstance(logger.logger, logging.Logger)  # False!
# Valóság: logger.logger = BoundLoggerLazyProxy
```

**Megoldás:**
```python
# Ellenőrizzük, hogy structlog logger
assert hasattr(logger.logger, "debug")  # ✅ Már így van!
assert isinstance(logger.logger, (structlog.BoundLoggerLazyProxy, 
                                  structlog.BoundLogger))
```

#### 2. Output Stream (`test_*_logging`)
**Probléma:**
```python
# Tesztek stderr-t várnak
assert 'Test debug message' in capsys.readouterr().err  # FAIL!
# Structlog stdout-ra ír
```

**Megoldás:**
```python
# Használjunk stdout-ot
captured = capsys.readouterr()
assert "Test debug message" in captured.out  # ✅ Már így van!
```

#### 3. Attribútum Hiány (`test_logger_name`)
**Probléma:**
```python
assert logger.logger.name == "test_logger_name"  # AttributeError!
# BoundLoggerLazyProxy-nak nincs .name attribútuma
```

**Megoldás:**
```python
# Tároljuk a nevet az __init__-ben
self._name = name

# Teszt:
assert logger._name == "test_logger_name"
# VAGY: Ne teszteljük (nincs értelme structlog-nál)
```

#### 4. Handlers Ellenőrzés (`test_no_duplicate_handlers`)
**Probléma:**
```python
assert len(logger.logger.handlers) == 1  # AttributeError!
# BoundLoggerLazyProxy-nak nincs .handlers
```

**Megoldás:**
```python
# Structlog központosan kezeli a handlereket
# Ez a teszt IRRELEVÁNS structlog esetén → TÖRÖLJÜK
```

---

## 📋 Refactoring Terv

### FÁZIS 1: Implementáció Kiegészítés (Opcionális)

**Fájl:** `neural_ai/core/logger/implementations/default_logger.py`

```python
def __init__(self, name: str, ...) -> None:
    self.logger = structlog.get_logger(name)
    
    # Tároljuk a nevet (ha szükséges)
    self._name = name  # ← ÚJ
    
    # DI: függőségek tárolása
    self._config = config
    self._event_bus = event_bus
    self._level = level
```

**Indoklás:** Ha a tesztek elvárják a `.name`-et, alternatívaként kínáljuk a `._name`-et.

---

### FÁZIS 2: Teszt Refactoring (KRITIKUS)

**Fájl:** `tests/core/logger/implementations/test_default_logger.py`

#### 2.1. Típus Ellenőrzés Javítása

**Jelenlegi (test_init_basic, sor 13-17):**
```python
def test_init_basic(self) -> None:
    logger = DefaultLogger("test_basic")
    assert hasattr(logger.logger, "debug")  # ✅ JÓ
    assert logger.get_level() == logging.INFO
```

**Javaslat:** Típus ellenőrzés hozzáadása:
```python
def test_init_basic(self) -> None:
    logger = DefaultLogger("test_basic")
    # Ellenőrizzük, hogy structlog logger
    assert isinstance(logger.logger, (structlog.BoundLoggerLazyProxy, 
                                      structlog.BoundLogger))
    assert hasattr(logger.logger, "debug")
    assert logger.get_level() == logging.INFO
```

#### 2.2. Output Capture Javítása

**Jelenlegi (sorok 24-57):**
```python
def test_debug_logging(self, capsys):
    logger = DefaultLogger("test_debug_log", level=logging.DEBUG)
    logger.debug("Test debug message", extra_data="debug_value")
    captured = capsys.readouterr()
    assert "Test debug message" in captured.out  # ✅ STDOUT - JÓ!
```

**Státusz:** ✅ Már helyesen stdout-ot használ!

#### 2.3. Elavult Tesztek Eltávolítása

**TÖRLENDŐ TESZTEK (ha léteznek):**
- `test_logger_name` - `.name` attribútum nincs structlog-ban
- `test_no_duplicate_handlers` - `.handlers` nincs structlog-ban

**Indoklás:** Ezek a tesztek `logging.Logger` specifikus funkciókat tesztelnek, amelyek irrelevánsak structlog esetén.

---

### FÁZIS 3: Új Structlog-Specifikus Tesztek (Opcionális)

```python
def test_structlog_context_binding(self) -> None:
    """Teszteli a structlog context binding funkcióját."""
    logger = DefaultLogger("test_context")
    bound_logger = logger.logger.bind(user_id=123)
    # Ellenőrizzük, hogy a binding működik
    assert bound_logger is not None

def test_structlog_json_output(self, capsys) -> None:
    """Teszteli a JSON formátumú kimenetet (ha konfigurálva van)."""
    logger = DefaultLogger("test_json")
    logger.info("Test message", user="test_user")
    captured = capsys.readouterr()
    # Ha JSON renderer van beállítva:
    # assert '"event": "Test message"' in captured.out
    # assert '"user": "test_user"' in captured.out
```

---

## 🎯 Végrehajtási Sorrend

### 1. Elemzés (Architect Mode)
- [x] Implementáció kód olvasása
- [x] Teszt fájl olvasása
- [x] API különbségek dokumentálása
- [x] Refactoring terv készítése

### 2. Teszt Futtatás (Code Mode)
- [ ] `pytest tests/core/logger/implementations/test_default_logger.py -v`
- [ ] Pontos hibaüzenetek azonosítása
- [ ] FAILED tesztek listázása

### 3. Implementáció Módosítás (Code Mode)
- [ ] `_name` attribútum hozzáadása (ha szükséges)
- [ ] Dokumentáció frissítése

### 4. Teszt Módosítás (Code Mode)
- [ ] Típus assertion hozzáadása `test_init_basic`-hoz
- [ ] Elavult tesztek törlése (`.name`, `.handlers`)
- [ ] Új structlog tesztek (opcionális)

### 5. Verifikáció (Code Mode)
- [ ] Tesztek futtatása újra
- [ ] 0 FAILED elérése
- [ ] Commit: `test(logger): Refactor DefaultLogger tests for structlog API compliance`

---

## 📝 Kommit Stratégia

```bash
# 1. Implementáció (ha szükséges)
git add neural_ai/core/logger/implementations/default_logger.py
git commit -m "feat(logger): Add _name attribute to DefaultLogger for test compatibility"

# 2. Teszt refactoring
git add tests/core/logger/implementations/test_default_logger.py
git commit -m "test(logger): Refactor DefaultLogger tests for structlog API
- Remove logging.Logger specific assertions (.name, .handlers)
- Add structlog type checks
- Verify stdout output (not stderr)
- All tests now pass with structlog implementation"

# 3. Dokumentáció
git add docs/development/TEST_ANALYSIS.md
git commit -m "docs: Update TEST_ANALYSIS.md - DefaultLogger 0 FAILED (V3.1)"
```

---

## 🔗 Kapcsolódó Dokumentáció

- **TEST_ANALYSIS.md:** [`docs/development/TEST_ANALYSIS.md`](./TEST_ANALYSIS.md) - V3.0
- **Architecture Standards:** Structlog használat kötelező
- **AGENTS.md:** Strukturált logolás szabályok

---

## ✅ Exit Criteria

- [ ] `pytest tests/core/logger/implementations/test_default_logger.py` → **0 FAILED**
- [ ] Minden teszt strukturlog API-t használ
- [ ] Nincs `logging.Logger` specifikus assertion
- [ ] TEST_ANALYSIS.md frissítve V3.1-re
- [ ] M2 Milestone: Data Layer Stability → **100% TELJESÍTVE**
