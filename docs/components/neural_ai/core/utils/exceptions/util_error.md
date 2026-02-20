# neural_ai/core/utils/exceptions/util_error.py

Util-specifikus kivételek.

Ez a modul tartalmazza az összes utility-műveletekhez kapcsolódó kivételeket.

## Importok

```python
from neural_ai.core.base.exceptions import NeuralAIException
```

## Osztály: `UtilError(NeuralAIException)`

Általános utility hiba.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, details: str | None = None) -> None
```

Inicializálja a UtilError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet.
- **`details`** (`str | None`) = `None`: Opcionális részletes leírás a hibáról.

**Visszatérési érték:**

- Típus: `None`

## Osztály: `HardwareDetectionError(UtilError)`

Hardver detektálási hiba.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, hardware_type: str | None = None) -> None
```

Inicializálja a HardwareDetectionError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet.
- **`hardware_type`** (`str | None`) = `None`: A hardver típusa, amelynek detektálása során hiba történt.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/core/utils/exceptions/util_error.py`](../../neural_ai/core/utils/exceptions/util_error.py)
