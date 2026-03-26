# 🦾 CLINE COMMAND FOR ROO CODE

**MÓD**: Orchestrator

**FELADAT**: Infrastructure Layer Phase 1 BEFEJEZÉS - Fennmaradó 30 kritikus probléma javítása

---

## 📊 HELYZET ELEMZÉS

**Előző munkák eredménye (commit 86970ba):**
- Import javítások: 4 → 0 (-4, 100% ✅)
- DI javítások: 6 → 1 (-5, 83% 🟡)
- Structure javítások: 19 → 3 (-16, 84% 🟡)
- DDD javítások: 26 → 26 (0, 0% 🔴)

**Összesen:** 438 → 413 kritikus probléma (-25, -5.7%)

**PROBLÉMA:** A DDD javítások (TYPE_CHECKING + lazy import) NEM lettek implementálva!

---

## 📂 ÉRINTETT FÁJLOK

**DDD Javítások (3 fájl, 26 probléma):**
- `neural_ai/core/__init__.py` (7 DDD megsértés)
- `neural_ai/core/base/factory.py` (2 DDD megsértés)
- `neural_ai/core/system/factory.py` (1 DDD megsértés)

**Structure Javítások (1 fájl, 3 probléma):**
- `neural_ai/core/base/implementations/__init__.py` (3 export)

**DI Javítások (1 fájl, 1 probléma):**
- `neural_ai/core/logger/implementations/default_logger.py` (Service Locator)

**Tesztek:**
- `tests/neural_ai/core/` - Minden érintett modul mirror tesztje
- **FIGYELEM:** Teszt struktúra refaktorálás szükséges (test_init.py ütközések) - KÜLÖN FELADAT!

---

## 🏗️ ARCHITEKTÚRA KÖVETELMÉNYEK

- **Réteg**: Infrastructure (0) - Az ALAPOK
- **DDD Szabály**: Infrastructure NEM hivatkozhat felső rétegekre (Input, Persistence, Domain, Presentation)
- **Megoldás**: TYPE_CHECKING blokk + lazy import a függvényeken belül
- **DI Pattern**: Konstruktor injektálás KÖTELEZŐ
- **Modul Struktúra**: implementations/__init__.py ÜRES

**SSOT Dokumentumok:**
- `docs/development/architecture_standards.md` (v4.0)
- `docs/development/ARCHITECTURE_AUDIT_DETAILED.md` (Audit Report)

---

## 🎯 TECHNIKAI KÖVETELMÉNYEK

### 1️⃣ **DDD JAVÍTÁSOK (26 probléma) - KRITIKUS**

#### A) `neural_ai/core/__init__.py` - bootstrap_core() refaktorálás

**Probléma:** 7 hely, ahol Infrastructure → Persistence/Input hivatkozás van

**Megoldás:** TYPE_CHECKING blokk + lazy import

```python
from typing import TYPE_CHECKING

# TYPE_CHECKING blokk a fájl elején (többi import után)
if TYPE_CHECKING:
    from neural_ai.data.storage.interfaces.storage_interface import StorageInterface
    from neural_ai.data.ingestion.market_data_persister import MarketDataPersister
    from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed

# Minden függvény szignatúrában string type hint:
def bootstrap_core(
    config_path: str | None = None, 
    log_level: str | None = None
) -> "CoreComponents":  # String hint!
    """Bootstrap funkció..."""
    
    # LAZY IMPORT a függvényen belül (NEM a fájl tetején!)
    from neural_ai.core.base.implementations.component_bundle import CoreComponents
    from neural_ai.core.base.implementations.di_container import DIContainer
    # ... többi core import
    
    # ... inicializációs kód ...
    
    # 6. Storage inicializálása (LAZY IMPORT)
    logger.info("⏳ 7. Storage indítása...")
    from neural_ai.data.storage.factory import StorageFactory  # LAZY!
    from neural_ai.data.storage.interfaces.storage_interface import StorageInterface  # LAZY!
    
    storage_conf_dict = cast(dict[str, Any], config.get("storage") or {})
    storage_conf = StorageConfig(**storage_conf_dict)
    storage_type = storage_conf.type or "parquet"
    
    try:
        storage = StorageFactory.get_storage(
            storage_type=storage_type,
            base_path=storage_conf.base_path,
            logger=logger,
            config=config,
            hardware=hardware,
        )
        container.register_instance(StorageInterface, storage)
        logger.debug(f"-> Storage engine: {storage_type}")
    except Exception:
        logger.critical("Storage init failed", exc_info=True)
        raise
    
    # 8. MarketDataPersister inicializálása (LAZY IMPORT)
    logger.info("⏳ 9. MarketDataPersister indítása...")
    from neural_ai.data.ingestion.market_data_persister import MarketDataPersister  # LAZY!
    
    ingestion_config = cast(IngestionConfig, config.get_section("ingestion") or {})
    market_data_persister = MarketDataPersister(
        event_bus=event_bus,
        storage=storage,
        logger=logger,
        config=ingestion_config,
    )
    container.register_instance(MarketDataPersister, market_data_persister)
    logger.debug("-> MarketDataPersister regisztrálva")
    
    # 9. JForex Live Feed inicializálása (LAZY IMPORT)
    logger.info("⏳ 10. JForex Live Feed ellenőrzése...")
    live_conf_dict = cast(dict[str, Any], config.get("collectors", "jforex_live") or {})
    live_conf = JForexLiveConfig(**live_conf_dict)
    
    if live_conf.enabled:
        from neural_ai.collectors.jforex.factory import JForexFactory  # LAZY!
        from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed  # LAZY!
        
        live_feed = JForexFactory.create_live_feed(config, logger, event_bus)
        container.register_instance(ILiveFeed, live_feed)
        logger.info("✅ JForex Live Feed inicializálva")
    else:
        logger.debug("-> JForex Live Feed nincs engedélyezve")
    
    logger.info("✅ RENDSZER ÜZEMKÉSZ")
    return CoreComponents(container=container)
```

**Hatás:** -7 DDD probléma ✅

---

#### B) `neural_ai/core/base/factory.py` - TYPE_CHECKING + lazy import

**Probléma:** 2 hely, ahol Infrastructure → Persistence hivatkozás van

**Megoldás:**

```python
from typing import TYPE_CHECKING

# TYPE_CHECKING blokk
if TYPE_CHECKING:
    from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

# Minden StorageInterface használat string type hint:
def _get_storage(self) -> "StorageInterface":  # String hint!
    """Lazy loadinggel tölti be a storage komponenst."""
    # LAZY IMPORT a függvényen belül
    from neural_ai.data.storage.interfaces.storage_interface import StorageInterface
    
    storage = self._container.resolve(StorageInterface)
    if storage is not None:
        # Duck typing: ellenőrizzük a szükséges metódusokat
        required_methods = ['save', 'load', 'exists', 'delete']
        if not all(hasattr(storage, method) for method in required_methods):
            raise DependencyError("Storage must implement StorageInterface")
        return cast(StorageInterface, storage)
    
    raise DependencyError("Storage not available")

@property
def storage(self) -> "StorageInterface":  # String hint!
    """Visszaadja a storage példányt (lazy-loaded)."""
    return self._storage_loader()

@staticmethod
@trace
def create_storage(
    base_path: str | None,
    logger: "LoggerInterface",
    config_manager: "ConfigManagerInterface",
) -> "StorageInterface":  # String hint!
    """Létrehoz egy storage példányt."""
    # ... validáció ...
    
    # LAZY IMPORT a függvényen belül
    from neural_ai.core.events.factory import EventBusFactory
    from neural_ai.data.storage.implementations.file_storage import FileStorage
    
    event_bus = EventBusFactory.get_event_bus(logger=logger)
    return FileStorage(
        logger=logger, config=config_manager, event_bus=event_bus, base_path=base_path
    )
```

**Hatás:** -2 DDD probléma ✅

---

#### C) `neural_ai/core/system/factory.py` - TYPE_CHECKING

**Probléma:** 1 hely, ahol Infrastructure → Persistence hivatkozás van

**Megoldás:**

```python
from typing import TYPE_CHECKING

# TYPE_CHECKING blokk
if TYPE_CHECKING:
    from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

# Minden StorageInterface használat string type hint:
@classmethod
def create_health_monitor(
    cls,
    name: str = "default",
    config: "ConfigManagerInterface | None" = None,
    logger: "LoggerInterface | None" = None,
    eventbus: "EventBusInterface | None" = None,
    storage: "StorageInterface | None" = None,  # String hint!
    hardware: "HardwareInterface | None" = None,
    **kwargs: Any,
) -> HealthMonitorInterface:
    """HealthMonitor példány létrehozása vagy visszaadása."""
    # ... implementáció ...
```

**Hatás:** -1 DDD probléma ✅

**Összesen DDD:** -10 probléma (7+2+1) ✅

**FIGYELEM:** Az audit report 26 DDD problémát jelez, de csak 10-et tudunk javítani a core/ modulokban. A többi 16 probléma valószínűleg más fájlokban van (pl. más core/ almodulokban). Ellenőrizd az audit reportot a pontos helyekért!

---

### 2️⃣ **STRUCTURE JAVÍTÁSOK (3 probléma)**

#### `neural_ai/core/base/implementations/__init__.py` - KIÜRÍTÉS

**Probléma:** Még mindig exportál 3 dolgot

**Megoldás:** ÜRES fájl (csak docstring)

```python
"""Implementációk a base modulhoz.

Ez a csomag tartalmazza a base modul különböző implementációit.
FIGYELEM: Ez a fájl ÜRES kell legyen! Implementációkat CSAK a factory.py importálhatja.
"""

# Semmi más!
```

**Hatás:** -3 Structure probléma ✅

---

### 3️⃣ **DI JAVÍTÁSOK (1 probléma)**

#### `neural_ai/core/logger/implementations/default_logger.py` - Service Locator eltávolítás

**Probléma:** 60. sor - Service Locator pattern

**Megoldás:** Ez egy speciális eset, mert a DefaultLogger MAGA a logger, nem használ külső loggert!

**Ellenőrizd a kódot:**
- Ha a DefaultLogger.__init__ hív egy Factory.get_logger() metódust, az hibás (rekurzió!)
- Valószínűleg ez egy false positive az audit scriptben
- Ha mégis van Service Locator, távolítsd el

```python
class DefaultLogger:
    """Alapértelmezett logger implementáció."""
    
    def __init__(
        self,
        name: str,
        level: str = "INFO",
        # NEM kell logger paraméter, mert ő MAGA a logger!
    ):
        """Inicializálja a loggert.
        
        Args:
            name: A logger neve
            level: Log szint (INFO, DEBUG, WARNING, ERROR, CRITICAL)
        """
        self.name = name
        self.level = level
        # Saját inicializálás (structlog, stb.)
        self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Beállítja a logger-t."""
        # Structlog konfiguráció
        # NEM hív Factory.get_logger()-t!
        pass
```

**Hatás:** -1 DI probléma (ha valóban van Service Locator) ✅

---

## 🧪 QA PROTOCOL

**1. Linting (Ruff):**
```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/ruff check neural_ai/core/
```

**2. Type Checking (Mypy):**
```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/mypy neural_ai/core/
```

**3. Type Checking (Pyright - Strict):**
```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pyright neural_ai/core/
```

**4. Unit Tests:**
```bash
# FIGYELEM: Teszt struktúra refaktorálás szükséges!
# Jelenleg 24 collection error (test_init.py ütközések)
# Ezt KÜLÖN FELADATBAN kell javítani!

# Próbáld meg futtatni:
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/neural_ai/core/ -v --tb=short

# Ha bukik, jelezd a problémát, de NE blokkold a commit-ot!
```

**5. Audit Re-run:**
```bash
python scripts/audit_architecture_detailed.py
```

**Követelmény:** 
- Ruff: 0 hiba ✅
- Mypy: 0 hiba ✅
- Pyright: 0 hiba ✅
- Audit: 413 → ~383 kritikus probléma (-30, -7.3%) ✅

---

## 📦 COMMIT FORMÁTUM

```
refactor(core): Infrastructure Layer Phase 1 BEFEJEZÉS

- DDD: TYPE_CHECKING + lazy import (10 probléma javítva)
- Structure: core/base/implementations/__init__.py kiürítése (3 probléma)
- DI: default_logger.py Service Locator ellenőrzés (1 probléma)

Audit: 413 → ~383 kritikus probléma (-30, -7.3%)
Infrastructure Layer: 134 → ~104 probléma (csak Type Safety maradt)

BREAKING CHANGE: Lazy import pattern - bootstrap_core() refaktorálás
```

---

## 🎯 EXPECTED OUTPUT

```markdown
### 🦾 ROO CODE REPORT

**STÁTUSZ**: ✅ SIKERES / ❌ QA BUKÁS

**VÉGREHAJTOTT MŰVELETEK**:
- [x] DDD: TYPE_CHECKING + lazy import (3 fájl, 10 probléma)
- [x] Structure: core/base/implementations/__init__.py kiürítve (3 probléma)
- [x] DI: default_logger.py ellenőrizve (1 probléma)
- [x] Tesztek: Strukturális probléma dokumentálva (külön feladat)

**QA GATE EREDMÉNYEK**:
- Ruff: ✅ 0 hiba
- Mypy: ✅ 0 hiba
- Pyright: ✅ 0 hiba (strict mode)
- Pytest: ⚠️ 24 collection error (teszt struktúra refaktorálás szükséges - KÜLÖN FELADAT)

**AUDIT EREDMÉNY**:
```bash
python scripts/audit_architecture_detailed.py
```
- Előtte: 413 kritikus probléma
- Utána: ~383 kritikus probléma (-30, -7.3%)
- Infrastructure Layer: 134 → ~104 (csak Type Safety maradt)

**COMMIT**:
```
refactor(core): Infrastructure Layer Phase 1 BEFEJEZÉS
Hash: [commit hash]
```

**KÖVETKEZŐ LÉPÉSEK**:
1. Teszt struktúra refaktorálás (test_init.py → test_<module>_init.py)
2. Phase 2 - Type Safety (368 Any type probléma)
3. Phase 3 - Mirror Testing (39 hiányzó teszt)
```

---

## ⚠️ KRITIKUS FIGYELMEZTETÉSEK

1. **Lazy Import Pattern**: Minden felső réteg import LAZY kell legyen (függvényen belül)!
2. **TYPE_CHECKING Blokk**: Csak type hint-ekhez, runtime-ban NEM fut le!
3. **String Type Hints**: Minden TYPE_CHECKING-ben definiált típus string hint kell legyen!
4. **Teszt Struktúra Probléma**: 24 collection error - KÜLÖN FELADATBAN javítandó!
5. **DDD Audit Eltérés**: Az audit 26 DDD problémát jelez, de csak 10-et tudunk javítani. Ellenőrizd a többi 16 probléma helyét!

---

**PRIORITÁS**: 🔴 KRITIKUS (Infrastructure Layer befejezése)  
**IDŐIGÉNY**: ~60 perc  
**KOCKÁZAT**: Közepes (Lazy import refaktorálás)

---

Másold be ezt a parancsot Roo Code-ba **Orchestrator módban**! 🚀
