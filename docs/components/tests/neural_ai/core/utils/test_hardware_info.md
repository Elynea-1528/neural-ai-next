# tests/neural_ai/core/utils/test_hardware_info.py

HardwareInfo teszt modul.

Ez a modul a HardwareInfo osztály tesztjeit tartalmazza.

## Importok

```python
from unittest.mock import mock_open
from unittest.mock import patch
from neural_ai.core.utils.implementations.hardware_info import HardwareInfo
```

## Osztály: `TestHardwareInfo`

HardwareInfo osztály tesztjei.

### Metódusok

#### `test_has_avx2_linux_with_avx2()`

```python
def test_has_avx2_linux_with_avx2(self) -> None
```

Teszteli az AVX2 támogatás detektálását AVX2-es CPU-n.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_has_avx2_linux_without_avx2()`

```python
def test_has_avx2_linux_without_avx2(self) -> None
```

Teszteli az AVX2 támogatás detektálását AVX2 nélküli CPU-n.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_has_avx2_non_linux()`

```python
def test_has_avx2_non_linux(self) -> None
```

Teszteli az AVX2 támogatás detektálását nem Linux rendszeren.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_has_avx2_file_not_found()`

```python
def test_has_avx2_file_not_found(self) -> None
```

Teszteli az AVX2 támogatás detektálását, ha a /proc/cpuinfo nem létezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_cpu_features_linux()`

```python
def test_get_cpu_features_linux(self) -> None
```

Teszteli a CPU feature-ök lekérdezését Linux rendszeren.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_cpu_features_non_linux()`

```python
def test_get_cpu_features_non_linux(self) -> None
```

Teszteli a CPU feature-ök lekérdezését nem Linux rendszeren.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_cpu_features_file_not_found()`

```python
def test_get_cpu_features_file_not_found(self) -> None
```

Teszteli a CPU feature-ök lekérdezését, ha a /proc/cpuinfo nem létezik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_supports_simd_with_simd()`

```python
def test_supports_simd_with_simd(self) -> None
```

Teszteli a SIMD támogatás detektálását SIMD-s CPU-n.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_supports_simd_without_simd()`

```python
def test_supports_simd_without_simd(self) -> None
```

Teszteli a SIMD támogatás detektálását SIMD nélküli CPU-n.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_supports_simd_partial_simd()`

```python
def test_supports_simd_partial_simd(self) -> None
```

Teszteli a SIMD támogatás detektálását részleges SIMD támogatással.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_interface_implementation()`

```python
def test_interface_implementation(self) -> None
```

Teszteli, hogy az osztály megfelelően implementálja-e az interfészt.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_has_avx2_file_read_error()`

```python
def test_has_avx2_file_read_error(self) -> None
```

Teszteli az AVX2 támogatás detektálását fájlolvasási hiba esetén.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_cpu_features_file_read_error()`

```python
def test_get_cpu_features_file_read_error(self) -> None
```

Teszteli a CPU feature-ök lekérdezését fájlolvasási hiba esetén.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_has_avx2_linux_no_flags_line()`

```python
def test_has_avx2_linux_no_flags_line(self) -> None
```

Teszteli az AVX2 támogatás detektálását, ha nincs 'flags' sor a cpuinfo-ban.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_cpu_features_linux_no_flags_line()`

```python
def test_get_cpu_features_linux_no_flags_line(self) -> None
```

Teszteli a CPU feature-ök lekérdezését, ha nincs 'flags' sor a cpuinfo-ban.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/utils/test_hardware_info.py`](../../tests/neural_ai/core/utils/test_hardware_info.py)
