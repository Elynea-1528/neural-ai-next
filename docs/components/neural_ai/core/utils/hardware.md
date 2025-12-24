# Hardware Modul

## Áttekintés

A `neural_ai.core.utils.hardware` modul hardver-specifikus képességek detektálását valósítja meg, különös tekintettel a CPU utasításkészlet-bővítményekre, mint az AVX2. A modul célja, hogy a rendszer biztonságosan tudja kezelni azokat a hardver-gyorsított funkciókat, amelyek elérhetők lehetnek a futási környezetben, anélkül, hogy Illegal Instruction hibát okoznának.

## Motiváció

A modern CPU-k számos speciális utasításkészlet-bővítménnyel rendelkeznek (AVX2, SSE4, stb.), amelyek jelentős teljesítményjavulást nyújthatnak numerikus számításokhoz és adatfeldolgozáshoz. Azonban ezen utasítások használata olyan CPU-n, amely nem támogatja azokat, Illegal Instruction kivételt okozhat, ami a program összeomlásához vezet.

A modul biztonságos detekciós mechanizmust biztosít, amely fájlalapú elemzést használ a `/proc/cpuinfo` fájlon keresztül, így elkerülve a közvetlen utasításkészlet-használatot a detekció során.

## Funkciók

### `has_avx2() -> bool`

Ellenőrzi, hogy a CPU támogatja-e az AVX2 (Advanced Vector Extensions 2) utasításkészletet.

**Visszatérési érték:**
- `bool`: True, ha a CPU támogatja az AVX2-t, False egyébként

**Működés:**
- Linux rendszereken a `/proc/cpuinfo` fájlt elemzi
- Megkeresi a 'flags' sort és ellenőrzi az 'avx2' flag jelenlétét
- Nem Linux rendszereken automatikusan False-t ad vissza

**Példa:**
```python
from neural_ai.core.utils.hardware import has_avx2

if has_avx2():
    # Használhatunk AVX2-gyorsított műveleteket
    print("AVX2 támogatott")
    # Például: gyorsított mátrix műveletek
else:
    # Fallback implementáció használata
    print("AVX2 nem támogatott, standard műveletek használata")
```

### `get_cpu_features() -> set[str]`

Visszaadja a CPU által támogatott összes feature flag-et a `/proc/cpuinfo` fájlból.

**Visszatérési érték:**
- `set[str]`: A CPU által támogatott feature flag-ek halmaza
- Üres halmazt ad vissza, ha nem sikerült beolvasni a flag-eket

**Példa:**
```python
from neural_ai.core.utils.hardware import get_cpu_features

features = get_cpu_features()
print(f"CPU feature-ök: {features}")

if "avx2" in features:
    print("AVX2 támogatott")
if "sse4_2" in features:
    print("SSE4.2 támogatott")
```

### `supports_simd() -> bool`

Ellenőrzi, hogy a CPU támogatja-e az alapvető SIMD (Single Instruction, Multiple Data) utasításokat.

**Ellenőrzött flag-ek:**
- SSE, SSE2, SSE3, SSSE3, SSE4.1, SSE4.2, AVX

**Visszatérési érték:**
- `bool`: True, ha a CPU támogatja az alapvető SIMD utasításokat

**Példa:**
```python
from neural_ai.core.utils.hardware import supports_simd

if supports_simd():
    print("SIMD utasítások támogatottak, használhatunk vektorizált műveleteket")
else:
    print("SIMD nem támogatott, scalar műveletek használata")
```

## Platform támogatás

### Linux
- **Teljes támogatás:** Mindhárom függvény működik
- **Adatforrás:** `/proc/cpuinfo` fájl elemzése
- **Biztonságos:** Nem használ közvetlen CPUID utasítást

### Egyéb platformok (Windows, macOS)
- **Korlátozott támogatás:** A függvények False-t vagy üres halmazt adnak vissza
- **Biztonságos viselkedés:** Inkább a negatív válasz, mint a kockázatos detekció

## Biztonsági szempontok

### Illegal Instruction megelőzés
A modul legfontosabb célja, hogy megelőzze az Illegal Instruction kivételeket. Ezt a következőképp éri el:

1. **Fájlalapú detekció:** A `/proc/cpuinfo` olvasása helyett nem próbál végrehajtani AVX2 utasításokat
2. **Biztonságos visszatérés:** Ha bármilyen hiba történik, a függvények biztonságosan False-t adnak vissza
3. **Platform ellenőrzés:** Nem támogatott platformokon automatikusan False a válasz

### Hibakezelés
A modul robusztus hibakezelést valósít meg:
- Fájl nem létezik: `FileNotFoundError` -> False visszatérés
- Olvasási hiba: `IOError`, `PermissionError` -> False visszatérés
- Helytelen formátum: Automatikus False visszatérés

## Használati esetek

### 1. Numerikus számítások optimalizálása
```python
import numpy as np
from neural_ai.core.utils.hardware import has_avx2

# NumPy konfigurálása AVX2 használatára
if has_avx2():
    # NumPy automatikusan használja az AVX2-t, ha elérhető
    np.show_config()
    # Gyorsabb mátrix műveletek
    result = np.dot(large_matrix_a, large_matrix_b)
```

### 2. Polars optimalizálás
```python
import polars as pl
from neural_ai.core.utils.hardware import supports_simd

if supports_simd():
    # Polars SIMD-gyorsított műveletek használata
    df = pl.DataFrame(data)
    result = df.with_columns(
        (pl.col("x") * pl.col("y")).alias("product")
    )
```

### 3. Fallback stratégia
```python
from neural_ai.core.utils.hardware import has_avx2

def process_data(data):
    if has_avx2():
        # AVX2-gyorsított implementáció
        return process_with_avx2(data)
    else:
        # Standard implementáció
        return process_standard(data)
```

## Implementáció részletei

### `/proc/cpuinfo` formátum
A Linux `/proc/cpuinfo` fájl formátuma:
```
processor   : 0
vendor_id   : GenuineIntel
cpu family  : 6
model       : 158
flags       : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb invpcid_single pti ssbd ibrs ibpb stibp tpr_shadow vnmi flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid mpx rdseed adx smap clflushopt intel_pt xsaveopt xsavec xgetbv1 xsaves dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp
```

A `has_avx2()` függvény a `flags` sorban keresi az `avx2` sztringet.

## Függőségek

A modulnak nincsenek külső függőségei, csak a Python standard library-t használja:
- `os`: Fájlrendszer műveletek
- `platform`: Platform detekció

## Jövőbeli fejlesztések

### Tervezett funkciók
- [ ] Windows támogatás: WMI vagy CPUID használata
- [ ] macOS támogatás: sysctl hívások
- [ ] GPU detekció: CUDA, OpenCL támogatás ellenőrzése
- [ ] Memória detekció: RAM méret és sebesség
- [ ] Cache méret detekció: L1, L2, L3 cache információk

### Extrák
- [ ] CPU model és órajel lekérdezése
- [ ] Magok számának detektálása
- [ ] Hyperthreading ellenőrzése

## Kapcsolódó dokumentáció

- [Core Utils Áttekintés](../__init__.md)
- [Core Komponensek](../../base/core_components.md)
- [Rendszer Specifikációk](../../../planning/specs/01_system_architecture.md)

## Forráskód

- [hardware.py](https://github.com/neural-ai-next/neural-ai-next/blob/main/neural_ai/core/utils/hardware.py)

---

**Utolsó frissítés:** 2025-12-24  
**Verzió:** 1.0.0  
**Státusz:** ✅ Stabil