# core/utils/exceptions/util_error.py

Util-specifikus kivételek.

Ez a modul tartalmazza az összes utility-műveletekhez kapcsolódó kivételeket.

## Osztályok

### `UtilError`

Általános utility hiba.

### `HardwareDetectionError`

Hardver detektálási hiba.


## Függvények

### `__init__`

Inicializálja a HardwareDetectionError kivételt.

        Args:
            message: A hibaüzenet.
            hardware_type: A hardver típusa, amelynek detektálása során hiba történt.


---

**Forrásfájl:** [`core/utils/exceptions/util_error.py`](../../../neural_ai/core/utils/exceptions/util_error.py)
