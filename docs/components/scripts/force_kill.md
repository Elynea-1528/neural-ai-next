# scripts/force_kill.py

Folyamat erőszakos leállító szkript a projekt folyamatainak tisztítására.

Ez a szkript psutil használatával azonosítja és leállítja azokat a folyamatokat,
amelyek foglalják a projekt kritikus portjait (8501, 5555-5558) vagy
tartalmazzák a "streamlit" vagy "neural_ai" neveket a parancsorban.

Használat:
    python scripts/force_kill.py

Author: Neural AI Next Team
Version: 1.0.0

## Importok

```python
import sys
import psutil
```

## Konstansok

- **`pid`**
: `proc.info['pid']`


- **`name`**
: `proc.info['name'] or ''`


- **`connections`**
: `proc.net_connections(kind='inet')`


- **`port`**
: `conn.laddr.port`


- **`kill_reason`**
: `f'port használat: {port}'`


- **`cmdline_str`**
: `' '.join(cmdline).lower()`


- **`name_lower`**
: `name.lower()`


- **`kill_reason`**
: `f'név egyezés: {keyword}'`


### `force_kill_processes()`

```python
def force_kill_processes() -> None
```

Folyamatok erőszakos leállítása. Iterál az összes futó folyamaton keresztül és leállítja azokat, amelyek egyeznek a kritériumokkal.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`scripts/force_kill.py`](../../scripts/force_kill.py)
