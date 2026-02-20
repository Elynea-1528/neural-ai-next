# neural_ai/collectors/jforex/interfaces/live_interface.py

Live Feed Interface for JForex Live Data Collection.

Ez az interfész definiálja a JForex live adatfolyam fogadásához szükséges metódusokat.
Az implementációk ezt az interfészt használják a ZMQ-alapú tick fogadáshoz.

## Importok

```python
from abc import ABC
from abc import abstractmethod
```

## Osztály: `ILiveFeed(ABC)`

Absztrakt osztály a JForex live adatfolyam kezeléséhez.

Ez az interfész felelős a Java Bridge-el (NeuralBridgeStrategy) való kommunikációért
ZMQ socketeken keresztül. A start() metódus indítja el a tick fogadást, a stop() pedig
leállítja azt.

### Metódusok

#### `start()`

```python
async def start(self) -> None
```

Indítja a live adatfolyam fogadását. Létrehozza a ZMQ SUB socketet, csatlakozik a megadott portra, és elindítja a háttérfolyamatot (_listen_loop) a tickek folyamatos fogadásához.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`LiveFeedError`**: Ha a csatlakozás vagy a fogadás során hiba történik.

#### `stop()`

```python
async def stop(self) -> None
```

Leállítja a live adatfolyam fogadását. Megszünteti a ZMQ kapcsolatot és leállítja a háttérfolyamatot.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `is_running()`

```python
def is_running(self) -> bool
```

Visszaadja, hogy a live feed jelenleg fut-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha a feed fut, False egyébként.

---

**Forrásfájl:** [`neural_ai/collectors/jforex/interfaces/live_interface.py`](../../neural_ai/collectors/jforex/interfaces/live_interface.py)
