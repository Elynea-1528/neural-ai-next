# Core Utils Tesztek

Ez a dokumentáció a `neural_ai.core.utils` modul tesztelését írja le.

## Áttekintés

A utils modul tesztelése három fő részből áll:
1. **Dekorátor tesztek** (`test_decorators.py`) - A `@trace` dekorátor funkcionalitásának ellenőrzése
2. **Hardver info tesztek** (`test_hardware_info.py`) - A `HardwareInfo` osztály metódusainak tesztelése
3. **Factory tesztek** (`test_factory.py`) - A `HardwareFactory` működésének ellenőrzése

## Teszt Struktúra

### 1. Dekorátor Tesztek (`test_decorators.py`)

#### Osztály: `TestTraceDecorator`
A `@trace` dekorátor alapvető funkcionalitását teszteli:

- **Sikeres végrehajtás**: Ellenőrzi a függvényhívás logolását
- **Kulcsszavas argumentumok**: Teszteli a kwargs kezelését
- **Nem biztonságos argumentumok**: Ellenőrzi az unsafe argok logolását
- **Függvénynév megőrzés**: Bizonyítja, hogy a dekorátor megőrzi a függvény nevét
- **Docstring megőrzés**: Bizonyítja, hogy a dekorátor megőrzi a docstringet
- **Kivételkezelés**: Teszteli a hibák logolását
- **Call ID egyediség**: Ellenőrzi, hogy minden hívás egyedi azonosítót kap
- **Időmérés**: Teszteli a futási idő mérésének helyességét
- **Vegyes argumentumok**: Kezeli a különböző típusú argumentumokat
- **Argumentum nélküli függvény**: Teszteli az üres függvényeket
- **Biztonságos típusok**: Ellenőrzi a safe típusok logolását

#### Osztály: `TestTraceDecoratorIntegration`
Integrációs tesztek a valós loggerrel és teljesítménytesztek.

### 2. Hardver Info Tesztek (`test_hardware_info.py`)

#### Osztály: `TestHardwareInfo`
A `HardwareInfo` osztály metódusainak tesztelése:

- **AVX2 támogatás Linuxon**: AVX2 flag jelenlétének ellenőrzése
- **AVX2 hiánya Linuxon**: AVX2 flag hiányának ellenőrzése
- **Nem Linux rendszer**: Nem Linux platformok kezelése
- **Fájl nem található**: Hiányzó cpuinfo fájl kezelése
- **CPU feature-ök Linuxon**: Összes feature flag lekérdezése
- **CPU feature-ök nem Linuxon**: Nem Linux platformok feature kezelése
- **SIMD támogatás**: Alapvető SIMD utasítások ellenőrzése
- **Interfész implementáció**: Interfész megfelelő implementálásának bizonyítása

### 3. Factory Tesztek (`test_factory.py`)

#### Osztály: `TestHardwareFactory`
A `HardwareFactory` alapvető funkcionalitását teszteli:

- **HardwareInfo példányosítás**: Ellenőrzi a helyes példányosítást
- **Új példányok**: Bizonyítja, hogy minden hívás új példányt ad vissza
- **HardwareInterface példányosítás**: Interfész implementáció ellenőrzése
- **Különböző példányok**: Ellenőrzi, hogy a két factory metódus különböző példányokat ad
- **Interfész implementáció**: Interfész megfelelő implementálásának bizonyítása
- **Import helyesség**: Ellenőrzi a helyes importálást
- **Statikus metódusok**: Bizonyítja, hogy a factory metódusok statikusak

#### Osztály: `TestHardwareFactoryIntegration`
Integrációs tesztek a factory működőképességének ellenőrzésére.

## Teszt Futtatása

### Egyedi tesztfájl futtatása

```bash
pytest tests/core/utils/test_decorators.py -v
pytest tests/core/utils/test_hardware_info.py -v
pytest tests/core/utils/test_factory.py -v
```

### Összes utils teszt futtatása

```bash
pytest tests/core/utils/ -v
```

### Coverage jelentés generálása

```bash
pytest tests/core/utils/ --cov=neural_ai.core.utils --cov-report=term-missing
```

## Teszt Eredmények

### Átlagos teszt futási idő
- Összes teszt: ~0.5-1 másodperc
- Egyedi teszt: ~0.01-0.1 másodperc

### Coverage statisztikák

| Modul | Statement Coverage | Branch Coverage |
|-------|-------------------|-----------------|
| decorators.py | 100% | 100% |
| factory.py | 100% | 100% |
| hardware_info.py | 89% | 85% |
| **Összesen** | **83%** | **82%** |

### Ismétlődő hibák és megoldások

1. **Long line errors**: A docstringek túl hosszúak voltak
   - **Megoldás**: Rövidítettük a docstringeket és sortörést alkalmaztunk

2. **Unused variables**: A `getattr` eredményeit nem használtuk
   - **Megoldás**: Átírtuk `_` változóra, jelezve, hogy szándékosan nem használjuk

3. **Blank line whitespace**: Üres sorokban szóközök voltak
   - **Megoldás**: Eltávolítottuk a felesleges whitespace-t

## Teszt Adatok

### Mock adatok a HardwareInfo tesztekhez

A tesztek mockolt `cpuinfo` tartalmat használnak:

```python
cpuinfo_content = (
    "flags\t\t: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca "
    "cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall "
    "nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good "
    "nopl xtopology nonstop_tsc cpuid aperfmperf tsc_known_freq pni "
    "pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr "
    "pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes "
    "xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb "
    "invpcid_single pti ssbd ibrs ibpb stibp tpr_shadow vnmi flexpriority "
    "ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid "
    "mpx rdseed adx smap clflushopt intel_pt xsaveopt xsavec xgetbv1 xsaves "
    "dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp"
)
```

## Teszt Elvek

1. **Type Safety**: Minden tesztmetódusnak explicit `-> None` visszatérési típussal kell rendelkeznie
2. **Mock Annotáció**: Minden mock objektumot ki kell annotálni (`mock_obj: MagicMock`)
3. **Async támogatás**: Async tesztekhez `@pytest.mark.asyncio` dekorátor kötelező
4. **Magyar docstring**: Minden teszt metódus magyar docstringgel rendelkezik
5. **100% Coverage**: Cél a lehető legmagasabb coverage elérése

## Kapcsolódó Dokumentációk

- [Dekorátorok](decorators.md) - A `@trace` dekorátor dokumentációja
- [Hardver Info](hardware_info.md) - A `HardwareInfo` osztály dokumentációja
- [Factory](factory.md) - A `HardwareFactory` dokumentációja
- [Hardver Interface](../utils/interfaces/hardware_interface.md) - A `HardwareInterface` dokumentációja