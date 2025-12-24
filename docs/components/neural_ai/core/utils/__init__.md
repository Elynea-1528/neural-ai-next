# Core Utils

## Áttekintés

A `neural_ai.core.utils` csomag tartalmazza a Neural AI Next rendszer alapvető segédfunkcióit és utility osztályait. Ezek a komponensek általános célú eszközöket nyújtanak, amelyeket a rendszer különböző részei használhatnak.

## Almodulok

### Hardware
A [`hardware`](hardware.md) modul hardver-specifikus képességek detektálását valósítja meg, különös tekintettel a CPU utasításkészlet-bővítményekre.

**Fő funkciók:**
- AVX2 támogatás ellenőrzése
- CPU feature flag-ek lekérdezése
- SIMD támogatás detektálása

## Használat

```python
from neural_ai.core.utils.hardware import has_avx2, get_cpu_features

# AVX2 támogatás ellenőrzése
if has_avx2():
    print("AVX2 támogatott")

# CPU feature-ök lekérdezése
features = get_cpu_features()
print(f"CPU feature-ök: {features}")
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

**Utolsó frissítés:** 2025-12-24  
**Verzió:** 1.0.0  
**Státusz:** 🚧 Fejlesztés alatt