# core/db/implementations/models.py

Adatbázis modellek a Neural AI Next rendszerhez.

Ez a modul definiálja az összes adatbázis táblát és modellt a rendszerben,
beleértve a DynamicConfig és LogEntry modelleket.

## Osztályok

### `DynamicConfig`

Dinamikus konfigurációs értékek tárolására szolgáló modell.

    Ez a modell tárolja a futás közben módosítható konfigurációs értékeket,
    amelyek hot reload támogatással rendelkeznek.

    Attributes:
        key: A konfigurációs kulcs (egyedi).
        value: A konfigurációs érték (JSON formátumban).
        value_type: Az érték típusa (int, float, str, bool, list, dict).
        category: A konfiguráció kategóriája (risk, strategy, trading, system).
        description: A konfiguráció leírása.
        is_active: A konfiguráció aktív-e.

### `LogEntry`

Rendszer naplóbejegyzéseket tároló modell.

    Ez a modell tárolja a rendszer által generált naplóbejegyzéseket
    strukturált formában az adatbázisban.

    Attributes:
        level: A napló szintje (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        logger_name: A logger neve.
        message: A naplóüzenet.
        module: A modul neve, ahonnan a napló született.
        function: A függvény neve, ahonnan a napló született.
        line_number: A sor száma, ahonnan a napló született.
        process_id: A folyamat azonosítója.
        thread_id: A szál azonosítója.
        exception_type: A kivétel típusa (ha van).
        exception_message: A kivétel üzenete (ha van).
        traceback: A traceback információ (ha van).
        extra_data: További egyéni adatok (JSON formátumban).


## Függvények

### `__repr__`

Modell string reprezentációja.

        Returns:
            A modell rövid string reprezentációja.


---

**Forrásfájl:** [`core/db/implementations/models.py`](../../../neural_ai/core/db/implementations/models.py)
