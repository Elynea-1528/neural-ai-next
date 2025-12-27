# Utils Factory - `neural_ai.core.utils.factory`

## Áttekintés

Ez a modul a `HardwareFactory` osztályt tartalmazza, amely a `HardwareInfo` implementáció példányosításáért felelős.

## Jellemzők

- **Dependency Injection**: A Factory mintával biztosítja a laza csatolást
- **Típusbiztos**: Szigorú típusellenőrzés minden visszatérési értékre
- **Egyszerű használat**: Statikus metódusokkal könnyen elérhető

## Tartalom

### `HardwareFactory` Osztály

Factory osztály a `HardwareInfo` példányosításához.

#### Metódusok

##### `get_hardware_info() -> HardwareInfo`

Visszaad egy `HardwareInfo` példányt.

**Visszatérési érték:**
- `HardwareInfo`: A hardverinformációkat tartalmazó osztály példánya

**Példa:**
```python
from neural_ai.core.utils.factory import HardwareFactory

hardware_info = HardwareFactory.get_hardware_info()

# Használat
if hardware_info.has_avx2():
    print("AVX2 támogatott")
```

**Implementáció:**
```python
@staticmethod
def get_hardware_info() -> "HardwareInfo":
    """Visszaad egy `HardwareInfo` példányt.

    Returns:
        HardwareInfo: A hardverinformációkat tartalmazó osztály példánya.
    """
    from neural_ai.core.utils.implementations.hardware_info import HardwareInfo
    return HardwareInfo()
```

##### `get_hardware_interface() -> HardwareInterface`

Visszaad egy `HardwareInterface`-t implementáló példányt.

**Visszatérési érték:**
- `HardwareInterface`: A hardverinterfészt implementáló osztály példánya

**Példa:**
```python
from neural_ai.core.utils.factory import HardwareFactory
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface

hardware: HardwareInterface = HardwareFactory.get_hardware_interface()

# Használat az interfészen keresztül
if hardware.has_avx2():
    print("AVX2 támogatott")
```

**Implementáció:**
```python
@staticmethod
def get_hardware_interface() -> "HardwareInterface":
    """Visszaad egy `HardwareInterface`-t implementáló példányt.

    Returns:
        HardwareInterface: A hardverinterfészt implementáló osztály példánya.
    """
    from neural_ai.core.utils.implementations.hardware_info import HardwareInfo
    return HardwareInfo()
```

## Használat

### Alap használat

```python
from neural_ai.core.utils.factory import HardwareFactory

# HardwareInfo példány létrehozása
hardware_info = HardwareFactory.get_hardware_info()

# Metódusok használata
avx2_supported = hardware_info.has_avx2()
cpu_features = hardware_info.get_cpu_features()
simd_supported = hardware_info.supports_simd()

print(f"AVX2 támogatott: {avx2_supported}")
print(f"CPU feature-ök: {cpu_features}")
print(f"SIMD támogatott: {simd_supported}")
```

### Interfész használata

```python
from neural_ai.core.utils.factory import HardwareFactory
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface

# Interfészen keresztül történő használat
hardware: HardwareInterface = HardwareFactory.get_hardware_interface()

# Ugyanazok a metódusok érhetők el
if hardware.has_avx2():
    # AVX2-gyorsított kód
    pass
```

### Dependency Injection

```python
from neural_ai.core.utils.factory import HardwareFactory
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface

class DataProcessor:
    """Adatfeldolgozó osztály, amely hardverinformációkat használ."""
    
    def __init__(self, hardware: HardwareInterface):
        """Konstruktor.
        
        Args:
            hardware: Hardverinterfész implementáció
        """
        self._hardware = hardware
    
    def process(self, data):
        """Adatok feldolgozása hardver képességek alapján."""
        if self._hardware.has_avx2():
            # AVX2-gyorsított feldolgozás
            return self._process_avx2(data)
        else:
            # Alap feldolgozás
            return self._process_basic(data)

# Használat
hardware = HardwareFactory.get_hardware_interface()
processor = DataProcessor(hardware)
result = processor.process(data)
```

## Előnyök

### 1. Laza csatolás

A Factory minta lehetővé teszi, hogy a kód ne függjön közvetlenül a konkrét implementációtól:

```python
# JÓ: Factory használata
hardware = HardwareFactory.get_hardware_interface()

# ROSSZ: Direkt példányosítás
from neural_ai.core.utils.implementations.hardware_info import HardwareInfo
hardware = HardwareInfo()  # Szoros csatolás!
```

### 2. Könnyű tesztelés

A Factory használatával könnyen cserélhető a teszteléshez:

```python
from unittest.mock import Mock

# Tesztesetben
mock_hardware = Mock(spec=HardwareInterface)
mock_hardware.has_avx2.return_value = True

processor = DataProcessor(mock_hardware)
```

### 3. Típusbiztonság

A Factory garantálja, hogy a visszaadott objektum megfelel az interfésznek:

```python
# Típusellenőrzés fordítási időben
hardware: HardwareInterface = HardwareFactory.get_hardware_interface()
# A mypy ellenőrzi, hogy a HardwareInfo valóban implementálja-e az interfészt
```

## Függőségek

- `typing.TYPE_CHECKING`: Körkörös importok elkerüléséhez
- `neural_ai.core.utils.implementations.hardware_info`: A konkrét implementáció
- `neural_ai.core.utils.interfaces.hardware_interface`: Az interfész definíció

## Kapcsolódó dokumentáció

- [Hardware Info](hardware_info.md)
- [Hardware Interface](interfaces/hardware_interface.md)
- [Dekorátorok](decorators.md)
- [Architektúra szabványok](../../development/architecture_standards.md)