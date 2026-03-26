# 🔍 ARCHITECTURE AUDIT REPORT (DETAILED)

**Generálva:** 2026-03-26 16:00:11
**Elemző**: Roo Code (Code-New)
**Szkennelt fájlok:** 155
**Modulok:** 12

## 📊 Executive Summary

- 🔴 **Kritikus problémák:** 408
  - Structure: 5
  - Type: 368
  - DDD: 26
  - DI: 4
  - Import: 5
- 🟡 **Figyelmeztetések:** 40
  - Structure: 1
  - Mirror: 39

## 🔴 Kritikus Problémák (Rétegek szerint)

### Infrastructure Layer

#### DDD Problémák (24 db)

**[`neural_ai/core/__init__.py`](neural_ai/core/__init__.py:180)**
- **Probléma:** DDD megsértés: Infrastructure (0) → Persistence (2)
- **Javaslat:** Alsó réteg (Infrastructure) NEM hivatkozhat felső rétegre (Persistence). Fordítsd meg a függőséget vagy használj Dependency Injection-t.

**[`neural_ai/core/__init__.py`](neural_ai/core/__init__.py:181)**
- **Probléma:** DDD megsértés: Infrastructure (0) → Persistence (2)
- **Javaslat:** Alsó réteg (Infrastructure) NEM hivatkozhat felső rétegre (Persistence). Fordítsd meg a függőséget vagy használj Dependency Injection-t.

**[`neural_ai/core/__init__.py`](neural_ai/core/__init__.py:228)**
- **Probléma:** DDD megsértés: Infrastructure (0) → Persistence (2)
- **Javaslat:** Alsó réteg (Infrastructure) NEM hivatkozhat felső rétegre (Persistence). Fordítsd meg a függőséget vagy használj Dependency Injection-t.

**[`neural_ai/core/__init__.py`](neural_ai/core/__init__.py:248)**
- **Probléma:** DDD megsértés: Infrastructure (0) → Input (1)
- **Javaslat:** Alsó réteg (Infrastructure) NEM hivatkozhat felső rétegre (Input). Fordítsd meg a függőséget vagy használj Dependency Injection-t.

**[`neural_ai/core/__init__.py`](neural_ai/core/__init__.py:249)**
- **Probléma:** DDD megsértés: Infrastructure (0) → Input (1)
- **Javaslat:** Alsó réteg (Infrastructure) NEM hivatkozhat felső rétegre (Input). Fordítsd meg a függőséget vagy használj Dependency Injection-t.

**[`neural_ai/core/system/factory.py`](neural_ai/core/system/factory.py:23)**
- **Probléma:** DDD megsértés: Infrastructure (0) → Persistence (2)
- **Javaslat:** Alsó réteg (Infrastructure) NEM hivatkozhat felső rétegre (Persistence). Fordítsd meg a függőséget vagy használj Dependency Injection-t.

**[`neural_ai/core/base/factory.py`](neural_ai/core/base/factory.py:58)**
- **Probléma:** DDD megsértés: Infrastructure (0) → Persistence (2)
- **Javaslat:** Alsó réteg (Infrastructure) NEM hivatkozhat felső rétegre (Persistence). Fordítsd meg a függőséget vagy használj Dependency Injection-t.

**[`neural_ai/core/base/factory.py`](neural_ai/core/base/factory.py:118)**
- **Probléma:** DDD megsértés: Infrastructure (0) → Persistence (2)
- **Javaslat:** Alsó réteg (Infrastructure) NEM hivatkozhat felső rétegre (Persistence). Fordítsd meg a függőséget vagy használj Dependency Injection-t.

**[`neural_ai/core/base/factory.py`](neural_ai/core/base/factory.py:257)**
- **Probléma:** DDD megsértés: Infrastructure (0) → Persistence (2)
- **Javaslat:** Alsó réteg (Infrastructure) NEM hivatkozhat felső rétegre (Persistence). Fordítsd meg a függőséget vagy használj Dependency Injection-t.

**[`neural_ai/core/base/factory.py`](neural_ai/core/base/factory.py:332)**
- **Probléma:** DDD megsértés: Infrastructure (0) → Persistence (2)
- **Javaslat:** Alsó réteg (Infrastructure) NEM hivatkozhat felső rétegre (Persistence). Fordítsd meg a függőséget vagy használj Dependency Injection-t.

*...és még 14 hasonló probléma*

#### Type Problémák (104 db)

**[`neural_ai/core/__init__.py`](neural_ai/core/__init__.py:184)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/core/__init__.py`](neural_ai/core/__init__.py:244)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/core/config/factory.py`](neural_ai/core/config/factory.py:213)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/core/config/factory.py`](neural_ai/core/config/factory.py:290)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/core/utils/decorators.py`](neural_ai/core/utils/decorators.py:20)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/core/utils/decorators.py`](neural_ai/core/utils/decorators.py:29)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/core/utils/decorators.py`](neural_ai/core/utils/decorators.py:86)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/core/utils/decorators.py`](neural_ai/core/utils/decorators.py:40)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/core/utils/decorators.py`](neural_ai/core/utils/decorators.py:86)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/core/utils/decorators.py`](neural_ai/core/utils/decorators.py:86)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

*...és még 94 hasonló probléma*

#### DI Problémák (1 db)

**[`neural_ai/core/logger/implementations/default_logger.py`](neural_ai/core/logger/implementations/default_logger.py:60)**
- **Probléma:** Service Locator pattern: DefaultLogger.__init__ hívja a Factory.get_logger() metódust
- **Javaslat:** Használj konstruktor injektálást: adj át logger/config paramétereket az __init__-nek

### Input Layer

#### DDD Problémák (2 db)

**[`neural_ai/collectors/jforex/factory.py`](neural_ai/collectors/jforex/factory.py:15)**
- **Probléma:** DDD megsértés: Input (1) → Persistence (2)
- **Javaslat:** Alsó réteg (Input) NEM hivatkozhat felső rétegre (Persistence). Fordítsd meg a függőséget vagy használj Dependency Injection-t.

**[`neural_ai/collectors/jforex/implementations/bi5_downloader.py`](neural_ai/collectors/jforex/implementations/bi5_downloader.py:23)**
- **Probléma:** DDD megsértés: Input (1) → Persistence (2)
- **Javaslat:** Alsó réteg (Input) NEM hivatkozhat felső rétegre (Persistence). Fordítsd meg a függőséget vagy használj Dependency Injection-t.

#### Type Problémák (4 db)

**[`neural_ai/collectors/jforex/factory.py`](neural_ai/collectors/jforex/factory.py:49)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/collectors/jforex/factory.py`](neural_ai/collectors/jforex/factory.py:118)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/collectors/jforex/factory.py`](neural_ai/collectors/jforex/factory.py:50)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/collectors/jforex/factory.py`](neural_ai/collectors/jforex/factory.py:119)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

#### Import Problémák (5 db)

**[`neural_ai/collectors/jforex/interfaces/__init__.py`](neural_ai/collectors/jforex/interfaces/__init__.py:6)**
- **Probléma:** Relatív import: .downloader_interface
- **Javaslat:** Használj abszolút importot: from neural_ai.X.Y import Z

**[`neural_ai/collectors/jforex/interfaces/__init__.py`](neural_ai/collectors/jforex/interfaces/__init__.py:7)**
- **Probléma:** Relatív import: .live_interface
- **Javaslat:** Használj abszolút importot: from neural_ai.X.Y import Z

**[`neural_ai/collectors/jforex/interfaces/__init__.py`](neural_ai/collectors/jforex/interfaces/__init__.py:8)**
- **Probléma:** Relatív import: .tick_data
- **Javaslat:** Használj abszolút importot: from neural_ai.X.Y import Z

**[`neural_ai/collectors/jforex/implementations/__init__.py`](neural_ai/collectors/jforex/implementations/__init__.py:3)**
- **Probléma:** Relatív import: .bi5_downloader
- **Javaslat:** Használj abszolút importot: from neural_ai.X.Y import Z

**[`neural_ai/collectors/jforex/implementations/__init__.py`](neural_ai/collectors/jforex/implementations/__init__.py:4)**
- **Probléma:** Relatív import: .live_feed
- **Javaslat:** Használj abszolút importot: from neural_ai.X.Y import Z

#### Structure Problémák (2 db)

**[`neural_ai/collectors/jforex/implementations/__init__.py`](neural_ai/collectors/jforex/implementations/__init__.py:3)**
- **Probléma:** implementations/__init__.py NEM lehet üres! Implementáció exportálás TILOS
- **Javaslat:** Töröld az összes importot ebből a fájlból. Csak a factory.py importálhatja az implementációkat.

**[`neural_ai/collectors/jforex/implementations/__init__.py`](neural_ai/collectors/jforex/implementations/__init__.py:4)**
- **Probléma:** implementations/__init__.py NEM lehet üres! Implementáció exportálás TILOS
- **Javaslat:** Töröld az összes importot ebből a fájlból. Csak a factory.py importálhatja az implementációkat.

### Persistence Layer

#### Type Problémák (97 db)

**[`neural_ai/data/ingestion/market_data_persister.py`](neural_ai/data/ingestion/market_data_persister.py:364)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/data/ingestion/market_data_persister.py`](neural_ai/data/ingestion/market_data_persister.py:342)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/data/ingestion/market_data_persister.py`](neural_ai/data/ingestion/market_data_persister.py:427)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/data/ingestion/market_data_persister.py`](neural_ai/data/ingestion/market_data_persister.py:382)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/data/ingestion/market_data_persister.py`](neural_ai/data/ingestion/market_data_persister.py:404)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/data/ingestion/market_data_persister.py`](neural_ai/data/ingestion/market_data_persister.py:445)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/data/storage/interfaces/storage_interface.py`](neural_ai/data/storage/interfaces/storage_interface.py:103)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/data/storage/interfaces/storage_interface.py`](neural_ai/data/storage/interfaces/storage_interface.py:26)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/data/storage/interfaces/storage_interface.py`](neural_ai/data/storage/interfaces/storage_interface.py:41)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/data/storage/interfaces/storage_interface.py`](neural_ai/data/storage/interfaces/storage_interface.py:59)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

*...és még 87 hasonló probléma*

#### DI Problémák (3 db)

**[`neural_ai/data/storage/implementations/parquet_storage.py`](neural_ai/data/storage/implementations/parquet_storage.py:116)**
- **Probléma:** Service Locator pattern: ParquetStorageService.__init__ hívja a Factory.get_section() metódust
- **Javaslat:** Használj konstruktor injektálást: adj át logger/config paramétereket az __init__-nek

**[`neural_ai/data/storage/implementations/parquet_storage.py`](neural_ai/data/storage/implementations/parquet_storage.py:135)**
- **Probléma:** Service Locator pattern: ParquetStorageService.__init__ hívja a Factory.get_hardware_interface() metódust
- **Javaslat:** Használj konstruktor injektálást: adj át logger/config paramétereket az __init__-nek

**[`neural_ai/data/storage/implementations/file_storage.py`](neural_ai/data/storage/implementations/file_storage.py:78)**
- **Probléma:** Service Locator pattern: FileStorage.__init__ hívja a Factory.get_hardware_interface() metódust
- **Javaslat:** Használj konstruktor injektálást: adj át logger/config paramétereket az __init__-nek

#### Structure Problémák (2 db)

**[`neural_ai/data/storage/implementations/__init__.py`](neural_ai/data/storage/implementations/__init__.py:3)**
- **Probléma:** implementations/__init__.py NEM lehet üres! Implementáció exportálás TILOS
- **Javaslat:** Töröld az összes importot ebből a fájlból. Csak a factory.py importálhatja az implementációkat.

**[`neural_ai/data/storage/implementations/__init__.py`](neural_ai/data/storage/implementations/__init__.py:4)**
- **Probléma:** implementations/__init__.py NEM lehet üres! Implementáció exportálás TILOS
- **Javaslat:** Töröld az összes importot ebből a fájlból. Csak a factory.py importálhatja az implementációkat.

### Domain Layer

#### Structure Problémák (1 db)

**[`neural_ai/processors/dimensions/d01_price`](neural_ai/processors/dimensions/d01_price:0)**
- **Probléma:** Factory.py létezik, de hiányzik az interfaces/ mappa
- **Javaslat:** Hozz létre interfaces/ mappát ABC osztályokkal

#### Type Problémák (5 db)

**[`neural_ai/processors/dimensions/base.py`](neural_ai/processors/dimensions/base.py:34)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/processors/dimensions/d02_support/implementations/support_processor.py`](neural_ai/processors/dimensions/d02_support/implementations/support_processor.py:432)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/processors/dimensions/d02_support/implementations/support_processor.py`](neural_ai/processors/dimensions/d02_support/implementations/support_processor.py:457)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/processors/dimensions/d02_support/implementations/support_processor.py`](neural_ai/processors/dimensions/d02_support/implementations/support_processor.py:176)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/processors/dimensions/d02_support/implementations/support_processor.py`](neural_ai/processors/dimensions/d02_support/implementations/support_processor.py:31)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

### Presentation Layer

#### Type Problémák (158 db)

**[`neural_ai/ui/factory.py`](neural_ai/ui/factory.py:45)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/ui/factory.py`](neural_ai/ui/factory.py:53)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/ui/factory.py`](neural_ai/ui/factory.py:54)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/ui/factory.py`](neural_ai/ui/factory.py:310)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/ui/factory.py`](neural_ai/ui/factory.py:46)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/ui/factory.py`](neural_ai/ui/factory.py:78)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/ui/factory.py`](neural_ai/ui/factory.py:79)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/ui/factory.py`](neural_ai/ui/factory.py:117)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/ui/factory.py`](neural_ai/ui/factory.py:118)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

**[`neural_ai/ui/factory.py`](neural_ai/ui/factory.py:156)**
- **Probléma:** Any típus használat (TILOS)
- **Javaslat:** Használj konkrét típust vagy Union[X, Y] típust

*...és még 148 hasonló probléma*

## 🟡 Figyelmeztetések

### Structure (1 db)

- [`neural_ai/processors/dimensions/d01_price`](neural_ai/processors/dimensions/d01_price:0): Hiányzik az exceptions/ mappa

### Mirror (39 db)

- [`ui/streamlit_app.py`](ui/streamlit_app.py:0): Hiányzó teszt fájl: tests/neural_ai/ui/test_streamlit_app.py
- [`core/logger/interfaces/factory_interface.py`](core/logger/interfaces/factory_interface.py:0): Hiányzó teszt fájl: tests/neural_ai/core/logger/interfaces/test_factory_interface.py
- [`core/system/exceptions/health_error.py`](core/system/exceptions/health_error.py:0): Hiányzó teszt fájl: tests/neural_ai/core/system/exceptions/test_health_error.py
- [`core/utils/exceptions/util_error.py`](core/utils/exceptions/util_error.py:0): Hiányzó teszt fájl: tests/neural_ai/core/utils/exceptions/test_util_error.py
- [`core/utils/implementations/hardware_info.py`](core/utils/implementations/hardware_info.py:0): Hiányzó teszt fájl: tests/neural_ai/core/utils/implementations/test_hardware_info.py
- *...és még 34 hasonló figyelmeztetés*

## 📋 Prioritizált Javítási Terv

### Fázis 1: Kritikus (1-3 nap)

1. **DDD Réteg Függőségek** (26 db)
   - Alsó rétegek felső rétegekre való hivatkozásainak megszüntetése
   - Dependency Injection bevezetése

2. **Dependency Injection** (4 db)
   - Service Locator pattern cseréje konstruktor injektálásra
   - Factory pattern helyes használata

3. **Import Szabályok** (5 db)
   - Relatív importok cseréje abszolút importokra
   - TYPE_CHECKING használata körkörös importoknál

### Fázis 2: Magas (3-7 nap)

1. **Type Safety** (368 db)
   - Any típus eliminálása
   - TypedDict → Pydantic migráció

2. **Modul Struktúra** (5 db)
   - Hiányzó interfaces/, implementations/, exceptions/ mappák létrehozása
   - Implementáció exportok megszüntetése

### Fázis 3: Közepes (1-2 hét)

1. **Mirror Testing** (39 db)
   - Hiányzó teszt fájlok létrehozása
   - 100% lefedettség elérése Domain rétegben

## 📈 Metrikák

| Réteg | Fájlok | Kritikus | Figyelmeztetés | Megfelelőség |
|:------|:-------|:---------|:---------------|:-------------|
| Infrastructure | 71 | 129 | 0 | 0.0% |
| Input | 12 | 13 | 0 | 0.0% |
| Persistence | 16 | 102 | 0 | 0.0% |
| Domain | 25 | 6 | 1 | 72.0% |
| Presentation | 30 | 158 | 0 | 0.0% |

---

**Következő lépés:** Fázis 1 implementálása (DDD, DI, Import javítások)
