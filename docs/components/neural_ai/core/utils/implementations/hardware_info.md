# HardwareInfo

## Áttekintés

A `HardwareInfo` osztály a [`HardwareInterface`](../interfaces/hardware_interface.md) interfészt implementálja, és a hardver-specifikus képességek (elsősorban CPU feature-ök) lekérdezését valósítja meg a `/proc/cpuinfo` fájl elemzésével.

## Cél

A fő cél a hardver-specifikus képességek (mint az AVX2, SIMD) biztonságos és egységes lekérdezése anélkül, hogy a rendszer Illegal Instruction hibát okozna olyan CPU-n, amely nem támogatja ezeket a képességeket.

## Implementáció részletei

Az osztály a `/proc/cpuinfo` fájlt elemzi Linux rendszereken, hogy detektálja a CPU feature-öket. Ez a módszer biztonságosabb, mint a CPUID utasítás közvetlen használata, mivel nem próbálja végrehajtani az utasításokat olyan CPU-n, amely nem támogatja azokat.

### Platform támogatás

- **Linux**: Teljes támogatás a `/proc/cpuinfo` elemzésével.
- **Windows, macOS**: A metódusok biztonságosan `False` értéket adnak vissza vagy üres halmazt, hogy elkerüljék a hibákat.

## Metódusok

### `has_avx2() -> bool`

Ellenőrzi, hogy a CPU támogatja-e az AVX2 utasításkészletet.

**Visszatérési érték:**
- `bool`: `True`, ha a CPU támogatja az AVX2-t, `False` egyébként.

**Példa:**
```python
from neural_ai.core.utils import HardwareFactory

hardware_info = HardwareFactory.get_hardware_info()

if hardware_info.has_avx2():
    # Használhatunk AVX2-gyorsított műveleteket
    pass
else:
    # Fallback implementáció használata
    pass
```

### `get_cpu_features() -> set[str]`

Visszaadja a CPU által támogatott összes feature flag-et.

**Visszatérési érték:**
- `set[str]`: A CPU által támogatott feature flag-ek halmaza. Üres halmazt ad vissza, ha nem sikerült beolvasni a flag-eket.

**Példa:**
```python
from neural_ai.core.utils import HardwareFactory

hardware_info = HardwareFactory.get_hardware_info()
features = hardware_info.get_cpu_features()
print(f"CPU feature-ök: {features}")
```

### `supports_simd() -> bool`

Ellenőrzi, hogy a CPU támogatja-e az alapvető SIMD utasításokat (SSE, SSE2, SSE3, SSE4.1, SSE4.2, AVX).

**Visszatérési érték:**
- `bool`: `True`, ha a CPU támogatja az alapvető SIMD utasításokat.

**Példa:**
```python
from neural_ai.core.utils import HardwareFactory

hardware_info = HardwareFactory.get_hardware_info()

if hardware_info.supports_simd():
    # Használhatunk SIMD-gyorsított műveleteket
    pass
else:
    # Fallback implementáció használata
    pass
```

## Használat

```python
from neural_ai.core.utils import HardwareFactory

# Factory-n keresztül kapjuk meg a példányt
hardware_info = HardwareFactory.get_hardware_info()

# Ellenőrizzük az AVX2 támogatást
if hardware_info.has_avx2():
    print("AVX2 támogatott")
else:
    print("AVX2 nem támogatott")

# Lekérjük az összes CPU feature-t
features = hardware_info.get_cpu_features()
print(f"CPU feature-ök: {features}")

# Ellenőrizzük az alapvető SIMD támogatást
if hardware_info.supports_simd():
    print("SIMD támogatott")
else:
    print("SIMD nem támogatott")
```

## Biztonsági megfontolások

- Az osztály csak fájlolvasást végez, nem pedig közvetlen utasításkészlet-használatot, így nem okozhat Illegal Instruction hibát.
- Ha bármilyen hiba történik a fájl olvasása közben, a metódusok biztonságosan `False` értéket adnak vissza vagy üres halmazt.