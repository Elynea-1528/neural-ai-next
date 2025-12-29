# core/utils/implementations/hardware_info.py

Hardverinformációk lekérdezését implementáló osztály.

Ez a modul a `HardwareInfo` osztályt tartalmazza, amely a
`HardwareInterface` interfészt implementálja, és a hardver-specifikus
képességek (CPU feature-ök) lekérdezését valósítja meg a `/proc/cpuinfo`
fájl elemzésével.

## Osztályok

### `HardwareInfo`

Hardverinformációk lekérdezését implementáló osztály.

    Ez az osztály a `HardwareInterface` interfészt implementálja, és
    a hardver-specifikus képességek (mint az AVX2, SIMD) biztonságos
    és egységes lekérdezését valósítja meg a `/proc/cpuinfo` fájl
    elemzésével.


## Függvények

### `has_avx2`

Ellenőrzi, hogy a CPU támogatja-e az AVX2 utasításkészletet.

        A függvény a `/proc/cpuinfo` fájlt elemzi Linux rendszereken, hogy
        detektálja az AVX2 támogatást. Ez a metódus nem okozhat Illegal
        Instruction hibát, mivel csak fájlolvasást végez, nem pedig közvetlen
        utasításkészlet-használatot.

        Returns:
            bool: True, ha a CPU támogatja az AVX2-t, False egyébként.

        Examples:
            >>> hardware_info = HardwareInfo()
            >>> if hardware_info.has_avx2():
            ...     # Használhatunk AVX2-gyorsított műveleteket
            ...     pass
            ... else:
            ...     # Fallback implementáció használata
            ...     pass

        Note:
            Jelenleg csak Linux rendszereken támogatott. Más platformokon
            (Windows, macOS) a függvény False értéket ad vissza.

            Ez a metódus biztonságosabb, mint a CPUID utasítás közvetlen
            használata, mivel nem próbálja végrehajtani az AVX2 utasításokat
            olyan CPU-n, amely nem támogatja azokat.

### `get_cpu_features`

Visszaadja a CPU által támogatott összes feature flag-et.

        A függvény a `/proc/cpuinfo` fájlból kinyeri az összes elérhető
        processzor-feature-t Linux rendszereken.

        Returns:
            set[str]: A CPU által támogatott feature flag-ek halmaza.
                Üres halmazt ad vissza, ha nem sikerült beolvasni a flag-eket.

        Note:
            Csak Linux rendszereken működik. Más platformokon üres halmazt ad vissza.

### `supports_simd`

Ellenőrzi, hogy a CPU támogatja-e az alapvető SIMD utasításokat.

        A függvény ellenőrzi az SSE, SSE2, SSE3, SSE4.1, SSE4.2 és AVX
        támogatását. Ezek az utasításkészlet-bővítmények gyakran hasznosak
        numerikus számításokhoz és adatfeldolgozáshoz.

        Returns:
            bool: True, ha a CPU támogatja az alapvető SIMD utasításokat.

        Note:
            Csak Linux rendszereken működik. Más platformokon False-t ad vissza.


---

**Forrásfájl:** [`core/utils/implementations/hardware_info.py`](../../../neural_ai/core/utils/implementations/hardware_info.py)
