# D2 Config API Helytelen Használat - "unhashable type: 'dict'" Javítási Terv

## 🔍 Valódi Probléma Azonosítása

### Hiba Lokáció
**Fájl**: [`neural_ai/ui/pages/05_🪲_Strategy_Lab.py:680`](neural_ai/ui/pages/05_🪲_Strategy_Lab.py:680)

**Hibás kód**:
```python
d2_config = config.get("processors", {}).get("d02", {})
```

**Traceback**:
```
File "neural_ai/ui/pages/05_🪲_Strategy_Lab.py", line 680, in _load_and_visualize
    d2_config = config.get("processors", {}).get("d02", {})
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "neural_ai/core/config/implementations/yaml_config_manager.py", line 133, in get
    current = cast(dict[str, Any], current).get(key)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: unhashable type: 'dict'
```

## 🎯 Gyökérok

### ConfigManager API Félreértés

A [`YamlConfigManager.get()`](neural_ai/core/config/implementations/yaml_config_manager.py:119-141) metódus szignatúrája:

```python
def get(self, *keys: str, default: Any = None) -> Any:
    """Érték lekérése a konfigurációból.
    
    Args:
        *keys: A konfigurációs kulcsok hierarchiája
        default: Alapértelmezett érték, ha a kulcs nem található
    """
```

**Helyes használat**:
```python
config.get("processors", "d02")  # keys=("processors", "d02"), default=None
```

**Hibás használat** (Strategy Lab-ban):
```python
config.get("processors", {})  # keys=("processors", {}), default=None
```

### Mi történik?

1. A `config.get("processors", {})` hívás a `{}` dictionary-t **kulcsként** értelmezi (nem default értékként)
2. A ConfigManager.get() 133. sorában ez a `{}` dict lesz a `key` változó értéke
3. Amikor `current.get(key)` fut, a Python dict.get() metódust hívjuk egy dict objektummal kulcsként
4. **Dict objektumok nem hashable-ok** → TypeError

## 💡 Megoldás

### 1️⃣ Azonnali Javítás - Strategy Lab Oldal

**Fájl**: [`neural_ai/ui/pages/05_🪲_Strategy_Lab.py:680`](neural_ai/ui/pages/05_🪲_Strategy_Lab.py:680)

**Előtte**:
```python
config = self._bridge.get_component("config")
if config is not None:
    d2_config = config.get("processors", {}).get("d02", {})
    st.info(f"✓ D2 Config betöltve: {list(d2_config.keys())}")
```

**Utána**:
```python
config = self._bridge.get_component("config")
if config is not None:
    # ConfigManager.get() használja a *keys variadic argumentumot
    d2_config = config.get("processors", "d02")
    if d2_config is None:
        d2_config = {}
        st.warning("⚠️ D2 Config nem található, üres config használata")
    elif isinstance(d2_config, dict):
        st.info(f"✓ D2 Config betöltve: {list(d2_config.keys())}")
    else:
        st.error(f"❌ D2 Config helytelen típus: {type(d2_config)}")
        d2_config = {}
```

### 2️⃣ ConfigManager API Védelme

**Probléma**: A jelenlegi `get(*keys: str, default: Any = None)` szignatúra nem véd a helytelen használat ellen, mert a `*keys` bármilyen objektumot elfogad.

**Megoldás**: Típus validálás a get() metódusban

**Fájl**: [`neural_ai/core/config/implementations/yaml_config_manager.py:119-141`](neural_ai/core/config/implementations/yaml_config_manager.py:119-141)

**Kiegészítés**:
```python
def get(self, *keys: str, default: Any = None) -> Any:
    """Érték lekérése a konfigurációból.
    
    Args:
        *keys: A konfigurációs kulcsok hierarchiája
        default: Alapértelmezett érték, ha a kulcs nem található
    
    Returns:
        A konfigurációs érték vagy az alapértelmezett érték
        
    Raises:
        TypeError: Ha bármelyik kulcs nem string típusú
    """
    # Típus validálás
    for i, key in enumerate(keys):
        if not isinstance(key, str):
            error_msg = (
                f"ConfigManager.get() csak string kulcsokat fogad el. "
                f"Hibás kulcs index {i}: {type(key).__name__} = {key!r}\n"
                f"Helyes használat: config.get('processors', 'd02')\n"
                f"Helytelen: config.get('processors', {{}}).get('d02', {{}})"
            )
            if self._logger:
                self._logger.error(error_msg)
            raise TypeError(error_msg)
    
    current: dict[str, Any] | Any = self._config
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = cast(dict[str, Any], current).get(key)
        if current is None:
            return default

    # DEBUG log
    if self._logger:
        self._logger.debug(f"Config get: {'.'.join(keys)} -> {current}")

    return current
```

### 3️⃣ Egyéb Helyek Ellenőrzése

**Keresési parancs**:
```bash
grep -r "config.get.*{}" neural_ai/ui/
```

**Várható találatok ellenőrzése és javítása**.

## 📋 Implementációs Lépések

### Fázis 1: Gyorsjavítás (15 perc)

1. ✅ [`Strategy_Lab.py:680`](neural_ai/ui/pages/05_🪲_Strategy_Lab.py:680) sor javítása
2. ✅ Manuális teszt a Strategy Lab oldalon
3. ✅ Git commit: `fix(ui): ConfigManager API helyes használata Strategy Lab-ban`

### Fázis 2: API Védelem (30 perc)

1. ✅ Típus validálás a ConfigManager.get() metódusban
2. ✅ Unit teszt írása a típus validáláshoz
3. ✅ Git commit: `feat(config): Típus validálás a ConfigManager.get() metódusban`

### Fázis 3: Kódbázis Átvizsgálás (30 perc)

1. ✅ Grep keresés az összes hasonló hibás használatra
2. ✅ Javítások alkalmazása
3. ✅ Regressziós tesztek futtatása
4. ✅ Git commit: `refactor(ui): ConfigManager API használat javítások`

## 🧪 Tesztelési Stratégia

### 1. Unit Teszt - ConfigManager Típus Validálás

**Fájl**: `tests/core/config/test_yaml_config_manager_validation.py`

```python
"""YamlConfigManager típus validálás tesztek."""

import pytest
from neural_ai.core.config.implementations.yaml_config_manager import YamlConfigManager


def test_get_with_valid_string_keys():
    """Teszteljük, hogy string kulcsokkal működik."""
    config = YamlConfigManager()
    config._config = {"processors": {"d02": {"swing_window": 5}}}
    
    result = config.get("processors", "d02")
    assert result == {"swing_window": 5}


def test_get_with_invalid_dict_key_raises_type_error():
    """Teszteljük, hogy dict kulcs TypeError-t dob."""
    config = YamlConfigManager()
    config._config = {"processors": {"d02": {"swing_window": 5}}}
    
    with pytest.raises(TypeError) as exc_info:
        config.get("processors", {})
    
    assert "csak string kulcsokat fogad el" in str(exc_info.value)
    assert "Helytelen:" in str(exc_info.value)


def test_get_with_invalid_int_key_raises_type_error():
    """Teszteljük, hogy int kulcs TypeError-t dob."""
    config = YamlConfigManager()
    
    with pytest.raises(TypeError) as exc_info:
        config.get("processors", 123)
    
    assert "csak string kulcsokat fogad el" in str(exc_info.value)


def test_get_with_none_key_raises_type_error():
    """Teszteljük, hogy None kulcs TypeError-t dob."""
    config = YamlConfigManager()
    
    with pytest.raises(TypeError) as exc_info:
        config.get("processors", None)
    
    assert "csak string kulcsokat fogad el" in str(exc_info.value)
```

### 2. Integrációs Teszt - Strategy Lab

**Manuális teszt checklist**:
- [ ] Strategy Lab oldal betöltése
- [ ] Szimbólum kiválasztása (EURUSD)
- [ ] Dátum kiválasztása
- [ ] "Adatok Betöltése" gomb kattintás
- [ ] D2 elemzés futtatása
- [ ] Ellenőrizni: "✓ D2 Config betöltve" üzenet jelenik meg
- [ ] Ellenőrizni: Nincs "unhashable type: 'dict'" hiba
- [ ] Ellenőrizni: Chart renderelődik swing pontokkal

### 3. Regressziós Tesztek

**Parancs**:
```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/config/ -v
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/ui/ -v
```

## ✅ Sikerkritériumok

1. ✅ Nincs "unhashable type: 'dict'" hiba a Strategy Lab oldalon
2. ✅ ConfigManager.get() TypeError-t dob nem-string kulcs esetén
3. ✅ Informatív hibaüzenet a helyes használattal
4. ✅ Unit tesztek lefedik a típus validálást
5. ✅ Nincs regresszió más UI oldalakon

## 📊 Érintett Fájlok

### Módosítandó
- [`neural_ai/ui/pages/05_🪲_Strategy_Lab.py:680`](neural_ai/ui/pages/05_🪲_Strategy_Lab.py:680) - Hibás API használat javítása
- [`neural_ai/core/config/implementations/yaml_config_manager.py:119`](neural_ai/core/config/implementations/yaml_config_manager.py:119) - Típus validálás

### Új Fájl
- `tests/core/config/test_yaml_config_manager_validation.py` - Validálási tesztek

### Ellenőrzendő (grep keresés)
- Minden fájl a `neural_ai/ui/` mappában, ahol `config.get()` szerepel

## 🔄 Git Commit Stratégia

### Commit 1: Gyorsjavítás
```bash
git add neural_ai/ui/pages/05_🪲_Strategy_Lab.py
git commit -m "fix(ui): ConfigManager API helyes használata Strategy Lab-ban

- config.get('processors', {}).get('d02', {}) helyett
  config.get('processors', 'd02') használata
- Típus ellenőrzés és hibaüzenetek
- Fixes: unhashable type: 'dict' hiba a D2 elemzés során
"
```

### Commit 2: API Védelem
```bash
git add neural_ai/core/config/implementations/yaml_config_manager.py
git add tests/core/config/test_yaml_config_manager_validation.py
git commit -m "feat(config): Típus validálás a ConfigManager.get() metódusban

- Típus ellenőrzés minden kulcs argumentumra
- Informatív hibaüzenet a helyes használattal
- Unit tesztek a validáláshoz
"
```

## 🔗 Kapcsolódó Dokumentáció

### API Dokumentáció Frissítés

**Fájl**: `docs/components/core/config/yaml_config_manager.md`

Hozzáadandó példák:

```markdown
## Használati Példák

### ✅ Helyes Használat

```python
# Egyszerű kulcs
value = config.get("system")

# Nested kulcsok
value = config.get("processors", "d02", "swing_window")

# Default érték használata
value = config.get("processors", "d15", default={})
```

### ❌ Helytelen Használat

```python
# ROSSZ: dict használata kulcsként
value = config.get("processors", {}).get("d02", {})
# TypeError: ConfigManager.get() csak string kulcsokat fogad el

# HELYES:
value = config.get("processors", "d02")
if value is None:
    value = {}
```
```

## 📝 Tanulságok

1. **API Szignatúra Félreértés**: A `*args` paraméter nem egyértelmű külső nézőpontból
2. **Típus Rendszer Korlátai**: A `*keys: str` annotáció nem véd runtime-ban
3. **Explicit Validation Szükséges**: Runtime típus ellenőrzés kritikus közös API-knál

## 🚀 Jövőbeli Fejlesztések

1. **Type Stubs**: `.pyi` fájlok generálása mypy-hoz
2. **Pydantic Validálás**: ConfigManager átírása Pydantic BaseModel-re
3. **Deprecation Warning**: `get()` metódus deprecated, helyette `get_nested()` és `get_value()`
