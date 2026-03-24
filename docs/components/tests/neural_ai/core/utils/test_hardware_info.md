# 🧪 Teszt: tests/neural_ai/core/utils/test_hardware_info.py

**Tesztelt modul:** [`neural_ai/core/utils/hardware_info.py`](../../neural_ai/core/utils/hardware_info.py)

HardwareInfo teszt modul.

Ez a modul a HardwareInfo osztály tesztjeit tartalmazza.

## Teszt Osztály: `TestHardwareInfo`

HardwareInfo osztály tesztjei.

### ✓ `test_has_avx2_linux_with_avx2()`

Teszteli az AVX2 támogatás detektálását AVX2-es CPU-n.

### ✓ `test_has_avx2_linux_without_avx2()`

Teszteli az AVX2 támogatás detektálását AVX2 nélküli CPU-n.

### ✓ `test_has_avx2_non_linux()`

Teszteli az AVX2 támogatás detektálását nem Linux rendszeren.

### ✓ `test_has_avx2_file_not_found()`

Teszteli az AVX2 támogatás detektálását, ha a /proc/cpuinfo nem létezik.

### ✓ `test_get_cpu_features_linux()`

Teszteli a CPU feature-ök lekérdezését Linux rendszeren.

### ✓ `test_get_cpu_features_non_linux()`

Teszteli a CPU feature-ök lekérdezését nem Linux rendszeren.

### ✓ `test_get_cpu_features_file_not_found()`

Teszteli a CPU feature-ök lekérdezését, ha a /proc/cpuinfo nem létezik.

### ✓ `test_supports_simd_with_simd()`

Teszteli a SIMD támogatás detektálását SIMD-s CPU-n.

### ✓ `test_supports_simd_without_simd()`

Teszteli a SIMD támogatás detektálását SIMD nélküli CPU-n.

### ✓ `test_supports_simd_partial_simd()`

Teszteli a SIMD támogatás detektálását részleges SIMD támogatással.

### ✓ `test_interface_implementation()`

Teszteli, hogy az osztály megfelelően implementálja-e az interfészt.

### ✓ `test_has_avx2_file_read_error()`

Teszteli az AVX2 támogatás detektálását fájlolvasási hiba esetén.

### ✓ `test_get_cpu_features_file_read_error()`

Teszteli a CPU feature-ök lekérdezését fájlolvasási hiba esetén.

### ✓ `test_has_avx2_linux_no_flags_line()`

Teszteli az AVX2 támogatás detektálását, ha nincs 'flags' sor a cpuinfo-ban.

### ✓ `test_get_cpu_features_linux_no_flags_line()`

Teszteli a CPU feature-ök lekérdezését, ha nincs 'flags' sor a cpuinfo-ban.

---

**Teszt fájl:** [`tests/neural_ai/core/utils/test_hardware_info.py`](../../tests/neural_ai/core/utils/test_hardware_info.py)

**Tesztelt modul:** [`neural_ai/core/utils/hardware_info.py`](../../neural_ai/core/utils/hardware_info.py)
