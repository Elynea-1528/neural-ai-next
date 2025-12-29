# core/utils/interfaces/hardware_interface.py

Hardverinformációk lekérdezéséhez szükséges interfész.

Ez a modul az `HardwareInterface` absztrakt alaposztályt definiálja,
amely a hardver-specifikus képességek (CPU feature-ök) lekérdezését
standardizálja a rendszerben.

## Osztályok

### `HardwareInterface`

Absztrakt interfész a hardverinformációk lekérdezéséhez.

    Ez az interfész definiálja azokat a metódusokat, amelyeket a
    hardverdetektáló osztályoknak implementálniuk kell. A cél a
    hardver-specifikus képességek (mint az AVX2, SIMD) biztonságos
    és egységes lekérdezése.


## Függvények

### `has_avx2`

Ellenőrzi, hogy a CPU támogatja-e az AVX2 utasításkészletet.

        Returns:
            bool: True, ha a CPU támogatja az AVX2-t, False egyébként.

### `get_cpu_features`

Visszaadja a CPU által támogatott összes feature flag-et.

        Returns:
            set[str]: A CPU által támogatott feature flag-ek halmaza.

### `supports_simd`

Ellenőrzi, hogy a CPU támogatja-e az alapvető SIMD utasításokat.

        Returns:
            bool: True, ha a CPU támogatja az alapvető SIMD utasításokat.


---

**Forrásfájl:** [`core/utils/interfaces/hardware_interface.py`](../../../neural_ai/core/utils/interfaces/hardware_interface.py)
