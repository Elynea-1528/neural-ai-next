# Hardware Interface - `neural_ai.core.utils.interfaces.hardware_interface`

## Áttekintés

Ez a modul az `HardwareInterface` absztrakt alaposztályt definiálja, amely a hardver-specifikus képességek (CPU feature-ök) lekérdezését standardizálja a rendszerben.

## Jellemzők

- **Absztrakt alaposztály**: Az `ABC` (Abstract Base Class) használatával
- **Típusbiztos**: Szigorú típusdefiníciók minden metódushoz
- **Standardizált API**: Egységes interfész a hardverdetektáláshoz

## Tartalom

### `HardwareInterface` Osztály

Absztrakt interfész a hardverinformációk lekérdezéséhez.

Ez az interfész definiálja azokat a metódusokat, amelyeket a hardverdetektáló osztályoknak implementálniuk kell. A cél a hardver-specifikus képességek (mint az AVX2, SIMD) biztonságos és egységes lekérdezése.

#### Metódusok

##### `has_avx2() -> bool` (abstract)

Ellenőrzi, hogy a CPU támogatja-e az AVX2 utasításkészletet.

**Visszatérési érték:**
- `bool`: True, ha a CPU támogatja az AVX2-t, False egyébként

**Implementáció követelmények:**
- Biztonságos detektálás (ne okozzon Illegal Instruction hibát)
- Platformfüggetlen viselkedés
- Gyors és hatékony működés

**Példa implementáció:**
```python
class HardwareInfo(HardwareInterface):
    def has_avx2(self) -> bool:
        """AVX2 támogatás ellenőrzése."""
        if platform.system() != "Linux":
            return False
        
        try:
            with open("/proc/cpuinfo", encoding="utf-8") as f:
                content = f.read()
            
            # Flag-ek kinyerése és ellenőrzés
            for line in content.splitlines():
                if line.startswith("flags"):
                    flags = line.split(":", 1)[1].strip().split()
                    return "avx2" in flags
            return False
        except (OSError, PermissionError):
            return False
```

##### `get_cpu_features() -> set[str]` (abstract)

Visszaadja a CPU által támogatott összes feature flag-et.

**Visszatérési érték:**
- `set[str]`: A CPU által támogatott feature flag-ek halmaza
  - Üres halmazt ad vissza, ha nem sikerült beolvasni a flag-eket

**Implementáció követelmények:**
- Minden elérhető CPU flag-et tartalmaznia kell
- Üres halmazt kell visszaadnia hibák esetén
- Platformfüggetlen viselkedés

**Példa implementáció:**
```python
class HardwareInfo(HardwareInterface):
    def get_cpu_features(self) -> set[str]:
        """CPU feature-ök lekérdezése."""
        if platform.system() != "Linux":
            return set()
        
        try:
            with open("/proc/cpuinfo", encoding="utf-8") as f:
                content = f.read()
            
            for line in content.splitlines():
                if line.startswith("flags"):
                    flags = line.split(":", 1)[1].strip().split()
                    return set(flags)
            return set()
        except (OSError, PermissionError):
            return set()
```

##### `supports_simd() -> bool` (abstract)

Ellenőrzi, hogy a CPU támogatja-e az alapvető SIMD utasításokat.

A függvény ellenőrzi az SSE, SSE2, SSE3, SSE4.1, SSE4.2 és AVX támogatását.

**Visszatérési érték:**
- `bool`: True, ha a CPU támogatja az alapvető SIMD utasításokat

**Ellenőrzött flag-ek:**
- `sse`, `sse2`, `sse3`, `ssse3`, `sse4_1`, `sse4_2`, `avx`

**Implementáció követelmények:**
- Legalább egy SIMD flag jelenlétének ellenőrzése
- Hatékony halmazműveletek használata

**Példa implementáció:**
```python
class HardwareInfo(HardwareInterface):
    def supports_simd(self) -> bool:
        """SIMD támogatás ellenőrzése."""
        features = self.get_cpu_features()
        simd_flags = {"sse", "sse2", "sse3", "ssse3", "sse4_1", "sse4_2", "avx"}
        return bool(features & simd_flags)
```

## Használat

### Interfész implementálása

```python
from abc import ABC, abstractmethod
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface

class MyHardwareInfo(HardwareInterface):
    """Saját hardverinformáció implementáció."""
    
    @abstractmethod
    def has_avx2(self) -> bool:
        """AVX2 támogatás ellenőrzése."""
        # Saját implementáció
        pass
    
    @abstractmethod
    def get_cpu_features(self) -> set[str]:
        """CPU feature-ök lekérdezése."""
        # Saját implementáció
        pass
    
    @abstractmethod
    def supports_simd(self) -> bool:
        """SIMD támogatás ellenőrzése."""
        # Saját implementáció
        pass
```

### Típusellenőrzés

```python
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface
from neural_ai.core.utils.implementations.hardware_info import HardwareInfo

# Típusellenőrzés
def check_hardware(hardware: HardwareInterface) -> None:
    """Hardver képességek ellenőrzése."""
    if hardware.has_avx2():
        print("AVX2 támogatott")
    
    features = hardware.get_cpu_features()
    print(f"CPU feature-ök: {features}")
    
    if hardware.supports_simd():
        print("SIMD támogatott")

# Használat
hardware_info = HardwareInfo()
check_hardware(hardware_info)  # Típusellenőrzés OK
```

### Tesztelés

```python
from unittest.mock import Mock
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface

# Mock objektum létrehozása az interfész alapján
mock_hardware = Mock(spec=HardwareInterface)

# Metódusok konfigurálása
mock_hardware.has_avx2.return_value = True
mock_hardware.get_cpu_features.return_value = {"avx2", "sse", "sse2"}
mock_hardware.supports_simd.return_value = True

# Tesztelés
assert mock_hardware.has_avx2() is True
assert "avx2" in mock_hardware.get_cpu_features()
assert mock_hardware.supports_simd() is True
```

## Előnyök

### 1. Standardizált API

Az interfész garantálja, hogy minden implementáció ugyanazokat a metódusokat tartalmazza:

```python
# Minden HardwareInterface implementációnak rendelkeznie kell ezekkel:
- has_avx2() -> bool
- get_cpu_features() -> set[str]
- supports_simd() -> bool
```

### 2. Típusbiztonság

A típusellenőrzés segít elkerülni a futási idejű hibákat:

```python
# Fordítási hiba, ha a metódus nem létezik
hardware: HardwareInterface = get_hardware()
hardware.nonexistent_method()  # mypy hiba!
```

### 3. Könnyű tesztelés

Az interfész használatával könnyen cserélhető a teszteléshez:

```python
# Valódi implementáció
hardware = HardwareInfo()

# Teszt implementáció
test_hardware = TestHardwareInfo()

# Mindkettő ugyanúgy használható
def process(hardware: HardwareInterface):
    # ...
```

### 4. Laza csatolás

Az interfész használatával a kód nem függ a konkrét implementációtól:

```python
# JÓ: Interfész használata
def process_data(hardware: HardwareInterface):
    if hardware.has_avx2():
        # AVX2 kód
        pass

# ROSSZ: Konkrét osztály használata
def process_data(hardware: HardwareInfo):
    # Szoros csatolás!
    pass
```

## Implementáció követelmények

### 1. Metódus szignatúrák

Minden metódusnak pontosan meg kell felelnie az interfészben definiált szignatúrának:

```python
# HELYES
def has_avx2(self) -> bool:
    return True

# HELYES
def has_avx2(self) -> bool:
    return False

# HIBÁS: Visszatérési érték típusa nem bool
def has_avx2(self) -> str:
    return "true"

# HIBÁS: Paraméterek eltérnek
def has_avx2(self, check_all: bool) -> bool:
    return True
```

### 2. Absztrakt metódusok

Minden absztrakt metódust implementálni kell:

```python
# HIBÁS: Hiányzó metódus
class IncompleteHardwareInfo(HardwareInterface):
    def has_avx2(self) -> bool:
        return True
    # get_cpu_features() és supports_simd() hiányzik!

# HELYES: Minden metódus implementálva
class CompleteHardwareInfo(HardwareInterface):
    def has_avx2(self) -> bool:
        return True
    
    def get_cpu_features(self) -> set[str]:
        return {"avx2", "sse"}
    
    def supports_simd(self) -> bool:
        return True
```

### 3. Hibakezelés

Az implementációknak biztonságosan kell kezelniük a hibákat:

```python
# HELYES: Biztonságos hibakezelés
def has_avx2(self) -> bool:
    try:
        # Kockázatos művelet
        return check_avx2()
    except Exception:
        # Biztonságos visszatérési érték
        return False

# HIBÁS: Kivétel nem kezelése
def has_avx2(self) -> bool:
    # Kivételt dobhat, ha nem létezik a fájl
    return check_avx2()
```

## Függőségek

- `abc.ABC`: Absztrakt alaposztály létrehozásához
- `abc.abstractmethod`: Absztrakt metódusok definiálásához
- `typing.TYPE_CHECKING`: Körkörös importok elkerüléséhez

## Kapcsolódó dokumentáció

- [Hardware Info](../hardware_info.md)
- [Hardware Factory](../factory.md)
- [Dekorátorok](../decorators.md)
- [Architektúra szabványok](../../development/architecture_standards.md)