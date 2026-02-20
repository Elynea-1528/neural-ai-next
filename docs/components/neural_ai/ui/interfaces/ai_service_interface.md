# neural_ai/ui/interfaces/ai_service_interface.py

AI Service interfész definíciója.

Ez az interfész definiálja a mesterséges intelligencia szolgáltatás szerződését,
amely a modellek kezelését és futtatását végzi.

## Importok

```python
from typing import TYPE_CHECKING
from typing import Any
from typing import Protocol
from typing import runtime_checkable
```

## Osztály: `AIServiceInterface(Protocol)`

AI Service interfész - Mesterséges intelligencia kezeléséért felelős.

Ez az interfész definiálja a modellek betöltését, konfigurálását és
futtatását végző metódusokat.

### Metódusok

#### `get_available_models()`

```python
def get_available_models(self) -> list[dict[str, str]]
```

Elérhető AI modellek lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `list[dict[str, str]]`
- List[Dict[str, str]]: A modellek listája

#### `load_model()`

```python
def load_model(self, model_id: str, config: dict[str, Any] | None = None) -> bool
```

AI modell betöltése.

**Paraméterek:**

- **`self`**
- **`model_id`** (`str`): A modell azonosítója
- **`config`** (`dict[str, Any] | None`) = `None`: A modell konfigurációja

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha sikeres a betöltés

#### `run_inference()`

```python
def run_inference(self, model_id: str, input_data: dict[str, Any]) -> dict[str, Any]
```

Inferencia futtatása a modellen.

**Paraméterek:**

- **`self`**
- **`model_id`** (`str`): A modell azonosítója
- **`input_data`** (`dict[str, Any]`): A bemeneti adatok

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: Az inferencia eredménye

#### `get_model_info()`

```python
def get_model_info(self, model_id: str) -> dict[str, Any]
```

Modell információk lekérdezése.

**Paraméterek:**

- **`self`**
- **`model_id`** (`str`): A modell azonosítója

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: A modell metaadatai

#### `train_model()`

```python
def train_model(self, model_id: str, training_data: list[dict[str, Any]], config: dict[str, Any] | None = None) -> dict[str, Any]
```

Modell betanítása.

**Paraméterek:**

- **`self`**
- **`model_id`** (`str`): A modell azonosítója
- **`training_data`** (`list[dict[str, Any]]`): A tanítóadatok
- **`config`** (`dict[str, Any] | None`) = `None`: A tanítás konfigurációja

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: A tanítás eredménye

#### `get_training_status()`

```python
def get_training_status(self, training_id: str) -> dict[str, Any]
```

Tanítás állapotának lekérdezése.

**Paraméterek:**

- **`self`**
- **`training_id`** (`str`): A tanítás azonosítója

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: A tanítás állapota

---

**Forrásfájl:** [`neural_ai/ui/interfaces/ai_service_interface.py`](../../neural_ai/ui/interfaces/ai_service_interface.py)
