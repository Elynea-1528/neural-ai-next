# tests/scripts/test_validation_end_to_end.py

End-to-End validációs teszt a CORE DATA PIPELINE számára.

Ez a teszt végrehajtja a teljes end-to-end validációs folyamatot,
beleértve az adat letöltést, dashboard indítást és adat validálást.

A teszt 100% coverage-t biztosít a validation_end_to_end.py szkriptre.

## Importok

```python
import subprocess
import sys
from pathlib import Path
import pytest
```

## Konstansok

- **`script_path`**
: `Path(__file__).parent.parent.parent / 'scripts' / 'validation_end_to_end.py'`


- **`python_cmd`**
: `'/home/elynea/miniconda3/envs/neural-ai-next/bin/python'`


- **`result`**
: `subprocess.run([python_cmd, str(script_path)], capture_output=True, text=True, timeout=300, cwd=Path(__file__).parent.parent)`


- **`success_indicators`**
: `['✅ Adat letöltés sikeres', '✅ Dashboard sikeresen indult', '✅ Minden adat validáció sikeres', '✅ Minden új oszlop jelen van', '✅ Spread értékek rendben', '✅ Z-Score értékek rendben', '✅ D2 Swing Engine validáció sikeres', '✅ Minden D2 kimeneti oszlop jelen van', '✅ Swing pontok megtalálva', '✅ Support/Resistance szintek rendben']`


- **`error_indicators`**
: `['❌ Adat letöltés sikertelen', '❌ Dashboard indítása sikertelen', '❌ Hiba az adatok validálása közben', '❌ Hiányzó kötelező oszlopok', '❌ Hiányzó új oszlopok', '❌ Validáció sikertelen']`


- **`script_path`**
: `Path(__file__).parent.parent.parent / 'scripts' / 'validation_end_to_end.py'`


- **`script_path`**
: `Path(__file__).parent.parent.parent / 'scripts' / 'validation_end_to_end.py'`


### `test_end_to_end_validation()`

```python
def test_end_to_end_validation()
```

Teljes end-to-end validációs teszt futtatása. Ez a teszt futtatja a validation_end_to_end.py szkriptet, és ellenőrzi hogy minden lépés sikeresen végbement.

### `test_validation_script_exists()`

```python
def test_validation_script_exists()
```

Ellenőrzi, hogy a validációs szkript létezik.

### `test_validation_script_executable()`

```python
def test_validation_script_executable()
```

Ellenőrzi, hogy a validációs szkript futtatható.

---

**Forrásfájl:** [`tests/scripts/test_validation_end_to_end.py`](../../tests/scripts/test_validation_end_to_end.py)
