# Hardver Információ - `neural_ai.core.utils.implementations.hardware_info`

## Áttekintés

Ez a modul a `HardwareInfo` osztályt tartalmazza, amely a `HardwareInterface` interfészt implementálja, és a hardver-specifikus képességek (CPU feature-ök) lekérdezését valósítja meg a `/proc/cpuinfo` fájl elemzésével.

## Jellemzők

- **Biztonságos detektálás**: Nem okozhat Illegal Instruction hibát, mivel csak fájlolvasást végez
- **Platformfüggetlen**: Automatikusan kezeli a nem Linux rendszereket
- **Strukturált logolás**: A `@trace` dekorátorral ellátott metódusok automatikusan logolják a hívásokat
- **Típusbiztos**: Szigorú típusellenőrzés és Type Hints

## Tartalom

### `HardwareInfo` Osztály

A hardverinformációk lekérdezését implementáló osztály.

#### Metódusok

##### `has_avx2() -> bool`

Ellenőrzi, hogy a CPU támogatja-e az AVX2 utasításkészletet.

**Visszatérési érték:**
- `bool`: True, ha a CPU támogatja az AVX2-t, False egyébként

**Plattform támogatás:**
- ✅ Linux (teljes támogatás)
- ❌ Windows, macOS (mindig False)

**Példa:**
```python
from neural_ai.core.utils.factory import HardwareFactory

hardware_info = HardwareFactory.get_hardware_info()

if hardware_info.has_avx2():
    # Használhatunk AVX2-gyorsított műveleteket
    print("AVX2 támogatott")
else:
    # Fallback implementáció használata
    print("AVX2 nem támogatott")
```

**Logolás:**
A metódus `@trace` dekorátorral van ellátva, ezért minden hívás automatikusan logolásra kerül:
```
call_id=123e4567-e89b-12d3-a456-426614174000 
function=has_avx2 
args=[] 
kwargs={} 
duration_ms=0.123
```

##### `get_cpu_features() -> set[str]`

Visszaadja a CPU által támogatott összes feature flag-et.

**Visszatérési érték:**
- `set[str]`: A CPU által támogatott feature flag-ek halmaza
  - Üres halmazt ad vissza, ha nem sikerült beolvasni a flag-eket

**Plattform támogatás:**
- ✅ Linux (teljes támogatás)
- ❌ Windows, macOS (üres halmaz)

**Példa:**
```python
from neural_ai.core.utils.factory import HardwareFactory

hardware_info = HardwareFactory.get_hardware_info()
features = hardware_info.get_cpu_features()

print(f"CPU feature-ök: {features}")
# Példa kimenet: {'avx2', 'sse', 'sse2', 'sse3', 'avx', 'fma', ...}
```

**Logolás:**
A metódus `@trace` dekorátorral van ellátva, ezért minden hívás automatikusan logolásra kerül.

##### `supports_simd() -> bool`

Ellenőrzi, hogy a CPU támogatja-e az alapvető SIMD utasításokat.

A függvény ellenőrzi az SSE, SSE2, SSE3, SSE4.1, SSE4.2 és AVX támogatását.

**Visszatérési érték:**
- `bool`: True, ha a CPU támogatja az alapvető SIMD utasításokat

**Ellenőrzött flag-ek:**
- `sse`, `sse2`, `sse3`, `ssse3`, `sse4_1`, `sse4_2`, `avx`

**Példa:**
```python
from neural_ai.core.utils.factory import HardwareFactory

hardware_info = HardwareFactory.get_hardware_info()

if hardware_info.supports_simd():
    # Használhatunk SIMD-gyorsított műveleteket
    print("SIMD támogatott")
else:
    # Fallback implementáció
    print("SIMD nem támogatott")
```

**Logolás:**
A metódus `@trace` dekorátorral van ellátva, ezért minden hívás automatikusan logolásra kerül.

## Implementáció részletek

### Fájlalapú detektálás

A modul a `/proc/cpuinfo` fájlt elemzi Linux rendszereken, ami biztonságosabb megoldás, mint a CPUID utasítás közvetlen használata:

```python
# Biztonságos fájlolvasás
with open("/proc/cpuinfo", encoding="utf-8") as f:
    cpuinfo_content = f.read()

# Flag-ek kinyerése
lines = cpuinfo_content.splitlines()
for line in lines:
    if line.startswith("flags"):
        flags_part = line.split(":", 1)
        if len(flags_part) == 2:
            flags = flags_part[1].strip().split()
            return "avx2" in flags
```

### Hibakezelés

A modul robusztus hibakezelést valósít meg:

- **Fájl nem létezik**: Visszaadja az alapértelmezett értéket (False vagy üres halmaz)
- **Olvasási hiba**: Elfogadja a kivételt és visszaadja az alapértelmezett értéket
- **Nem Linux rendszer**: Automatikusan visszaadja az alapértelmezett értéket

```python
try:
    with open(cpuinfo_path, encoding="utf-8") as f:
        cpuinfo_content = f.read()
    # Feldolgozás...
except (OSError, PermissionError):
    # Biztonságos visszatérési érték
    return False
```

## Használat

### Factory használata

A modul használatához mindig a Factory-t használd:

```python
from neural_ai.core.utils.factory import HardwareFactory

# HardwareInfo példány létrehozása
hardware_info = HardwareFactory.get_hardware_info()

# Hardver képességek ellenőrzése
if hardware_info.has_avx2():
    print("AVX2 támogatott")

features = hardware_info.get_cpu_features()
print(f"CPU feature-ök: {features}")

if hardware_info.supports_simd():
    print("SIMD támogatott")
```

### Direkt példányosítás (nem ajánlott)

```python
from neural_ai.core.utils.implementations.hardware_info import HardwareInfo

hardware_info = HardwareInfo()
# ... használat
```

## Teljesítmény

- **Gyors fájlolvasás**: A `/proc/cpuinfo` fájl kis méretű és gyorsan beolvasható
- **Hatékony elemzés**: Egyszerű szöveges elemzés, nincs szükség komplex parsolásra
- **Minimális erőforrás**: A metódusok csak akkor olvassák be a fájlt, amikor ténylegesen szükség van rá

## Biztonság

- **Nincs Illegal Instruction**: A modul soha nem próbál végrehajtani olyan utasításkészlet-bővítményt, amely nem támogatott
- **Adatvédelem**: Nem gyűjt semmilyen személyes vagy bizalmas adatot
- **Platform biztonság**: Automatikusan érzékeli a platformot és alkalmazkodik

## Függőségek

- `os`: Fájl létezésének ellenőrzéséhez
- `platform`: Platform detektáláshoz
- `structlog`: Logoláshoz
- `neural_ai.core.utils.decorators.trace`: Nyomon követéshez

## Kapcsolódó dokumentáció

- [Hardware Interface](../utils/interfaces/hardware_interface.md)
- [Hardware Factory](../utils/factory.md)
- [Dekorátorok](decorators.md)
- [Structlog Konfiguráció](../../../configs/logging.yaml)