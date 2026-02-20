# neural_ai/core/utils/interfaces/hardware_interface.py

Hardverinformációk lekérdezéséhez szükséges interfész.

Ez a modul az `HardwareInterface` absztrakt alaposztályt definiálja,
amely a hardver-specifikus képességek (CPU feature-ök) lekérdezését
standardizálja a rendszerben.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
```

## Osztály: `HardwareInterface(ABC)`

Absztrakt interfész a hardverinformációk lekérdezéséhez.

Ez az interfész definiálja azokat a metódusokat, amelyeket a
hardverdetektáló osztályoknak implementálniuk kell. A cél a
hardver-specifikus képességek (mint az AVX2, SIMD) biztonságos
és egységes lekérdezése.

### Metódusok

#### `has_avx2()`

```python
def has_avx2(self) -> bool
```

Ellenőrzi, hogy a CPU támogatja-e az AVX2 utasításkészletet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha a CPU támogatja az AVX2-t, False egyébként.

#### `get_cpu_features()`

```python
def get_cpu_features(self) -> set[str]
```

Visszaadja a CPU által támogatott összes feature flag-et.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `set[str]`
- set[str]: A CPU által támogatott feature flag-ek halmaza.

#### `supports_simd()`

```python
def supports_simd(self) -> bool
```

Ellenőrzi, hogy a CPU támogatja-e az alapvető SIMD utasításokat.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha a CPU támogatja az alapvető SIMD utasításokat.

---

**Forrásfájl:** [`neural_ai/core/utils/interfaces/hardware_interface.py`](../../neural_ai/core/utils/interfaces/hardware_interface.py)
