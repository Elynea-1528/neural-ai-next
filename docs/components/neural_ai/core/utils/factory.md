# HardwareFactory

## Áttekintés

A `HardwareFactory` osztály a [`HardwareInfo`](implementations/hardware_info.md) implementáció példányosításáért felelős. Ez a Factory mintát követi, és a Dependency Injection elvet alkalmazza a hardverinformációk lekérdezéséhez.

## Cél

A fő cél a `HardwareInfo` osztály példányosításának centralizálása és egységesítése, valamint a függőségek injektálásának biztosítása.

## Metódusok

### `get_hardware_info() -> HardwareInfo`

Visszaad egy `HardwareInfo` példányt.

**Visszatérési érték:**
- [`HardwareInfo`](implementations/hardware_info.md): A hardverinformációkat tartalmazó osztály példánya.

**Példa:**
```python
from neural_ai.core.utils import HardwareFactory

hardware_info = HardwareFactory.get_hardware_info()

if hardware_info.has_avx2():
    print("AVX2 támogatott")
```

### `get_hardware_interface() -> HardwareInterface`

Visszaad egy `HardwareInterface`-t implementáló példányt.

**Visszatérési érték:**
- [`HardwareInterface`](interfaces/hardware_interface.md): A hardverinterfészt implementáló osztály példánya.

**Példa:**
```python
from neural_ai.core.utils import HardwareFactory

hardware_interface = HardwareFactory.get_hardware_interface()

if hardware_interface.supports_simd():
    print("SIMD támogatott")
```

## Használat

```python
from neural_ai.core.utils import HardwareFactory

# Factory-n keresztül kapjuk meg a példányt
hardware_info = HardwareFactory.get_hardware_info()

# Használjuk a metódusokat
if hardware_info.has_avx2():
    print("AVX2 támogatott")

features = hardware_info.get_cpu_features()
print(f"CPU feature-ök: {features}")

if hardware_info.supports_simd():
    print("SIMD támogatott")
```

## Architektúra

A `HardwareFactory` az architektúra Factory mintáját követi, és a Dependency Injection elvet alkalmazza. Ez biztosítja, hogy a kód egységesen és tesztelhető legyen.

- **Interfész**: [`HardwareInterface`](interfaces/hardware_interface.md)
- **Implementáció**: [`HardwareInfo`](implementations/hardware_info.md)
- **Factory**: `HardwareFactory` (ez a dokumentáció)