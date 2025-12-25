# Core Utils

## Áttekintés

A `neural_ai.core.utils` csomag tartalmazza a Neural AI Next rendszer alapvető segédfunkcióit és utility osztályait. Ezek a komponensek általános célú eszközöket nyújtanak, amelyeket a rendszer különböző részei használhatnak.

## Architektúra

A csomag az alábbi architektúrát követi:

- **Interfészek**: Az [`interfaces/`](interfaces/) könyvtár tartalmazza az összes utility interfészt.
- **Implementációk**: A [`implementations/`](implementations/) könyvtár tartalmazza a konkrét implementációkat.
- **Factory**: A [`factory.py`](factory.md) fájl tartalmazza a Factory osztályokat a példányosításhoz.

## Almodulok

### Hardware

A hardver-specifikus képességek detektálását az alábbi komponensek valósítják meg:

- **Interfész**: [`HardwareInterface`](interfaces/hardware_interface.md) - A hardverinformációk lekérdezéséhez szükséges metódusokat definiálja.
- **Implementáció**: [`HardwareInfo`](implementations/hardware_info.md) - A hardverinformációk lekérdezését implementálja a `/proc/cpuinfo` fájl elemzésével.
- **Factory**: [`HardwareFactory`](factory.md) - A `HardwareInfo` példányosításáért felelős.

**Fő funkciók:**
- AVX2 támogatás ellenőrzése
- CPU feature flag-ek lekérdezése
- SIMD támogatás detektálása

## Használat

```python
from neural_ai.core.utils import HardwareFactory

# Factory-n keresztül kapjuk meg a példányt
hardware_info = HardwareFactory.get_hardware_info()

# AVX2 támogatás ellenőrzése
if hardware_info.has_avx2():
    print("AVX2 támogatott")

# CPU feature-ök lekérdezése
features = hardware_info.get_cpu_features()
print(f"CPU feature-ök: {features}")

# SIMD támogatás ellenőrzése
if hardware_info.supports_simd():
    print("SIMD támogatott")
```

## Jövőbeli bővítések

A következő utility modulok tervezettek:

### Type Utils
- Típuskonverziós segédfunkciók
- Validáció eszközök
- Adatszerkezet helperek

### Date Utils
- Időzóna kezelés
- Dátum formázás
- Időintervallum számítások

### File Utils
- Fájl műveletek
- Útvonal kezelés
- Mappa operációk

## Kapcsolódó dokumentáció

- [Core Komponensek](../base/core_components.md)
- [Rendszer Architektúra](../../../planning/specs/01_system_architecture.md)

---

**Utolsó frissítés:** 2025-12-25  
**Verzió:** 2.0.0  
**Státusz:** ✅ Aktív