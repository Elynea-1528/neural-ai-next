# HardwareInterface

## Áttekintés

Az `HardwareInterface` egy absztrakt alaposztály (ABC), amely a hardver-specifikus képességek (elsősorban CPU feature-ök) lekérdezését standardizálja a rendszerben. Ez az interfész biztosítja, hogy a hardverdetektáló osztályok egységes módon implementálják a szükséges metódusokat.

## Cél

A fő cél a hardver-specifikus képességek (mint az AVX2, SIMD) biztonságos és egységes lekérdezése anélkül, hogy a rendszer Illegal Instruction hibát okozna olyan CPU-n, amely nem támogatja ezeket a képességeket.

## Metódusok

### `has_avx2() -> bool`

Ellenőrzi, hogy a CPU támogatja-e az AVX2 utasításkészletet.

**Visszatérési érték:**
- `bool`: `True`, ha a CPU támogatja az AVX2-t, `False` egyébként.

### `get_cpu_features() -> set[str]`

Visszaadja a CPU által támogatott összes feature flag-et.

**Visszatérési érték:**
- `set[str]`: A CPU által támogatott feature flag-ek halmaza. Üres halmazt ad vissza, ha nem sikerült beolvasni a flag-eket.

### `supports_simd() -> bool`

Ellenőrzi, hogy a CPU támogatja-e az alapvető SIMD utasításokat (SSE, SSE2, SSE3, SSE4.1, SSE4.2, AVX).

**Visszatérési érték:**
- `bool`: `True`, ha a CPU támogatja az alapvető SIMD utasításokat.

## Használat

```python
from neural_ai.core.utils import HardwareFactory

# Factory-n keresztül kapjuk meg a példányt
hardware_info = HardwareFactory.get_hardware_interface()

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

## Implementáció

Az interfészt a [`HardwareInfo`](../implementations/hardware_info.md) osztály implementálja.