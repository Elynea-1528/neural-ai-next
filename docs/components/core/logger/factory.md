# Logger Factory

## Áttekintés

A `neural_ai.core.logger.factory` modul felelős a naplózási rendszer (logger) egységes létrehozásáért és konfigurálásáért az egész Neural AI Next alkalmazásban. A factory mintát alkalmazva biztosítja, hogy a logger példányok konzisztensen legyenek inicializálva a `configs/logging.yaml` konfiguráció alapján.

## Konfiguráció (`configs/logging.yaml`)

A naplózás működését a `configs/logging.yaml` fájl szabályozza. A konfiguráció a következő fő részekből áll:

*   **Handlers:** Meghatározzák, hova kerüljenek a naplóüzenetek (konzol, fájl).
*   **Loggers:** Meghatározzák a különböző modulok és komponensek naplózási szintjét.

### Elérhető Logger-ek

*   **`neural_ai`:** Az alkalmazás fő loggere. Alapértelmezett szintje `DEBUG`.
*   **`neural_ai.trace`:** Speciális logger a nyomkövetési (tracing) üzenetekhez. Alapértelmezett szintje `DEBUG`, de könnyen átállítható `INFO` vagy magasabb szintre a zaj csökkentése érdekében a fejlesztés vagy a produkciós környezet igényei szerint.
*   **Külső könyvtárak:** A `aiosqlite`, `asyncio`, `parso` és más külső könyvtárak naplózási szintje `WARNING`-ra van állítva a zaj minimalizálása érdekében.

## Használat

### Alapvető használat

A logger használatához egyszerűen importáld a `get_logger` függvényt a factory-ból, és hozz létre egy logger példányt a saját modulod nevével.

```python
from neural_ai.core.logger.factory import get_logger

# Logger létrehozása a saját modulhoz
logger = get_logger("my_module")

# Naplóüzenetek küldése
logger.debug("Ez egy debug üzenet.")
logger.info("Az alkalmazás elindult.")
logger.warning("Figyelmeztetés, valami szokatlan történt.")
logger.error("Hiba történt a feldolgozás során.")
```

### Nyomkövetés (Tracing) használata

A `neural_ai.trace` logger segítségével részletesebb műveleti nyomkövetést lehet naplózni. Ez különösen hasznos a komplex adatfolyamok vagy az aszinkron műveletek hibakereséséhez.

```python
from neural_ai.core.logger.factory import get_logger

# Dedikált trace logger létrehozása
trace_logger = get_logger("neural_ai.trace")

# Nyomkövetési események naplózása
trace_logger.debug("Adatcsomag érkezett a hálózatról.", packet_id=123)
trace_logger.info("Feldolgozási lépés elkezdődött.", step="data_validation")
trace_logger.debug("Feldolgozási lépés befejeződött.", step="data_validation", duration_ms=15.4)
```

**Fontos:** A trace logger szintjét a `configs/logging.yaml` fájlban lehet módosítani. Fejlesztés közben hasznos a `DEBUG` szint, míg éles rendszerben érdemes lehet `INFO`-ra állítani a teljesítmény és a naplófájlok mérete érdekében.

## Implementációk

A factory a következő logger implementációkat támogatja:

*   **ColoredLogger:** Színes kimenetet jelenít meg a konzolon. Alapértelmezett a fejlesztői környezetben.
*   **DefaultLogger:** Egyszerű, szöveges kimenet.
*   **RotatingFileLogger:** Naplófájlba ír, és automatikusan rotálja a fájlokat, amikor elérik a maximális méretet.

A megfelelő implementáció kiválasztása automatikusan történik a `configs/logging.yaml` konfiguráció alapján.