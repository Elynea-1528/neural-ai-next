# Logger Tesztelés

## Áttekintés

A `neural_ai.core.logger` modul tesztsuite-je átfogó lefedettséget biztosít a naplózási rendszer minden komponenséhez. A tesztek szigorú típusellenőrzéssel készültek, és követik a projekt coding standardjait.

## Teszt Struktúra

A tesztek a következő szerkezetet követik:

```
tests/core/logger/
├── test_factory.py                          # LoggerFactory tesztek
├── formatters/
│   └── test_logger_formatters.py            # ColoredFormatter tesztek
├── implementations/
│   ├── test_colored_logger.py               # ColoredLogger implementáció tesztek
│   ├── test_default_logger.py               # DefaultLogger implementáció tesztek
│   └── test_rotating_file_logger.py         # RotatingFileLogger implementáció tesztek
└── interfaces/
    ├── test_factory_interface.py            # LoggerFactoryInterface tesztek
    └── test_logger_interface.py             # LoggerInterface tesztek
```

## Tesztlefedettség

### 1. Logger Factory Tesztek (`test_factory.py`)

A LoggerFactory összes alapvető funkcionalitását teszteli:

- **Logger létrehozás:**
  - Alapértelmezett logger (`test_get_logger_default`)
  - Színes logger (`test_get_logger_colored`)
  - Rotating file logger (`test_get_logger_rotating_with_file`)
  - Rotating logger hibakezelés (`test_get_logger_rotating_without_file`)

- **Gyorsítótárazás:**
  - Logger példányok gyorsítótárazása (`test_get_logger_caching`)

- **Bővíthetőség:**
  - Egyéni logger regisztráció (`test_register_logger`)
  - Regisztrált típusok lekérdezése (`test_get_registered_types`)
  - Logger típus ellenőrzés (`test_is_logger_registered`)

- **Életciklus:**
  - Logger példányok törlése (`test_clear_instances`)

- **Konfiguráció:**
  - Alap logger konfiguráció (`test_configure_basic`)

- **Sémakezelés:**
  - Sémaváltozat lekérdezése és beállítása (`test_get_set_schema_version`)

### 2. Formatter Tesztek (`test_logger_formatters.py`)

A ColoredFormatter minden színformázási szintjét teszteli:

- **Színes formázás:**
  - Debug szint (kék szín) (`test_format_debug`)
  - Info szint (zöld szín) (`test_format_info`)
  - Warning szint (sárga szín) (`test_format_warning`)
  - Error szint (piros szín) (`test_format_error`)
  - Critical szint (fehér szöveg piros háttéren) (`test_format_critical`)

- **Hibakezelés:**
  - Ismeretlen szint formázása (`test_format_unknown_level`)

### 3. Implementáció Tesztek

#### ColoredLogger (`test_colored_logger.py`)

- **Inicializálás:**
  - Alap inicializálás (`test_init_basic`)
  - Egyéni szinttel történő inicializálás (`test_init_with_custom_level`)

- **Naplózási metódusok:**
  - Debug üzenet (`test_debug_logging`)
  - Info üzenet (`test_info_logging`)
  - Warning üzenet (`test_warning_logging`)
  - Error üzenet (`test_error_logging`)
  - Critical üzenet (`test_critical_logging`)

- **Szintkezelés:**
  - Log szint módosítása (`test_set_level`)

- **Egyéb:**
  - Logger név ellenőrzés (`test_logger_name`)
  - Színes formázó jelenléte (`test_colored_formatter_present`)

#### DefaultLogger (`test_default_logger.py`)

- **Inicializálás:**
  - Alap inicializálás (`test_init_basic`)
  - Egyéni szinttel történő inicializálás (`test_init_with_custom_level`)

- **Naplózási metódusok:**
  - Debug üzenet (`test_debug_logging`)
  - Info üzenet (`test_info_logging`)
  - Warning üzenet (`test_warning_logging`)
  - Error üzenet (`test_error_logging`)
  - Critical üzenet (`test_critical_logging`)

- **Szintkezelés:**
  - Log szint módosítása (`test_set_level`)

- **Egyéb:**
  - Logger név ellenőrzés (`test_logger_name`)
  - Duplikált handler ellenőrzés (`test_no_duplicate_handlers`)

#### RotatingFileLogger (`test_rotating_file_logger.py`)

- **Inicializálás:**
  - Alap inicializálás (`test_init_basic`)
  - Hibakezelés fájl nélküli inicializálásnál (`test_init_without_file_raises_error`)
  - Egyéni szinttel történő inicializálás (`test_init_with_custom_level`)
  - Könyvtár automatikus létrehozása (`test_init_creates_directory`)

- **Naplózási metódusok:**
  - Debug üzenet (`test_debug_logging`)
  - Info üzenet (`test_info_logging`)
  - Warning üzenet (`test_warning_logging`)
  - Error üzenet (`test_error_logging`)
  - Critical üzenet (`test_critical_logging`)

- **Szintkezelés:**
  - Log szint módosítása (`test_set_level`)

- **Egyéb:**
  - Logger név ellenőrzés (`test_logger_name`)
  - Érvénytelen rotáció típus hibakezelés (`test_invalid_rotation_type_raises_error`)
  - Régi log fájlok törlése (`test_clean_old_logs`)

### 4. Interfész Tesztek

#### LoggerFactoryInterface (`test_factory_interface.py`)

- **Absztrakció ellenőrzés:**
  - Interfész absztrakt osztály-e (`test_interface_is_abstract`)

- **Metódusok ellenőrzése:**
  - Szükséges metódusok jelenléte (`test_interface_has_required_methods`)

#### LoggerInterface (`test_logger_interface.py`)

- **Absztrakció ellenőrzés:**
  - Interfész absztrakt osztály-e (`test_interface_is_abstract`)

- **Metódusok ellenőrzése:**
  - Szükséges metódusok jelenléte (`test_interface_has_required_methods`)

## Típusellenőrzés

Minden tesztmetódus szigorú típusannotációkat használ:

```python
def test_example_method(self) -> None:
    """Teszt metódus leírása."""
    # Teszt logika
```

A pytest fixture-ök is típusosak:

```python
def test_with_monkeypatch(self, monkeypatch: pytest.MonkeyPatch) -> None:
    """Teszt monkeypatch használatával."""
    # Teszt logika

def test_with_capsys(self, capsys: pytest.CaptureFixture[str]) -> None:
    """Teszt capsys használatával."""
    # Teszt logika
```

## Futtatás és Coverge

### Tesztek futtatása

```bash
# Összes logger teszt futtatása
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/logger/ -v

# Coverage jelentés készítése
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/logger/ \
    --cov=neural_ai/core/logger \
    --cov-report=term-missing
```

### Aktuális Coverage

- **Összesített coverage:** 87%
- **Tesztelt sorok:** 261 / 299
- **Hiányzó sorok:** 38

#### Coverage részletek

| Modul | Sorok | Hiányzó | Coverage |
|-------|-------|---------|----------|
| `neural_ai/core/logger/__init__.py` | 13 | 2 | 85% |
| `neural_ai/core/logger/exceptions/logger_error.py` | 6 | 0 | 100% |
| `neural_ai/core/logger/factory.py` | 85 | 15 | 82% |
| `neural_ai/core/logger/formatters/logger_formatters.py` | 9 | 0 | 100% |
| `neural_ai/core/logger/implementations/colored_logger.py` | 36 | 1 | 97% |
| `neural_ai/core/logger/implementations/default_logger.py` | 34 | 0 | 100% |
| `neural_ai/core/logger/implementations/rotating_file_logger.py` | 56 | 7 | 88% |
| `neural_ai/core/logger/interfaces/factory_interface.py` | 16 | 3 | 81% |
| `neural_ai/core/logger/interfaces/logger_interface.py` | 28 | 8 | 71% |

## Best Practices

### 1. Típusannotációk

- Minden tesztmetódusnak legyen `-> None` visszatérési típusa
- Pytest fixture-öknek legyen explicit típusa (pl. `pytest.MonkeyPatch`, `pytest.CaptureFixture[str]`)
- Használjunk abszolút importokat a konzisztencia érdekében

### 2. Tesztelési minták

- **AAA minta (Arrange, Act, Assert):** Minden teszt legyen logikailag tagolva
- **Egy assert per teszt:** Egy tesztmetódus egy dolgot teszteljen
- **Magyar docstring:** Minden tesztmetódusnak legyen magyar nyelvű leírása

### 3. Fixture használat

- **MonkeyPatch:** A stdout/stderr átirányításához
- **Capsys:** A kimenet rögzítéséhez
- **tmp_path:** Ideiglenes fájlok létrehozásához

### 4. Hibakezelés

- Használj `pytest.raises`-t a várt kivételek teszteléséhez
- Ellenőrizd a hibaüzeneteket is (`match` paraméter)

## Jövőbeli fejlesztések

### Coverage javítás

A következő területeken lehetne javítani a coverage-t:

1. **Factory életciklus:** További tesztelés a factory állapotváltozásainak
2. **Interfész metódusok:** További tesztelés az interfészek absztrakt metódusainak
3. **RotatingFileLogger speciális esetek:** További rotációs stratégiák tesztelése

### Tesztbővítés

- **Aszinkron tesztelés:** Async logger metódusok tesztelése
- **Teljesítménytesztek:** Nagy mennyiségű naplóüzenet teljesítményének mérése
- **Integrációs tesztek:** Logger konfiguráció teljes integrációs tesztelése