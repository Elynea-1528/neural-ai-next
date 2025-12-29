# core/events/factory.py

EventBus factory a Neural AI Next rendszerhez.

Ez a modul biztosítja az EventBus létrehozását a konfiguráció alapján.
A factory mintázatot követi, lehetővé téve a különböző EventBus implementációk
egyszerű cseréjét.

Author: Neural AI Next Team
Version: 1.0.0

## Osztályok

### `EventBusFactory`

EventBus factory osztály.

    Ez az osztály felelős az EventBus példányok létrehozásáért.
    Jelenleg csak a ZeroMQ-s implementációt támogatja, de a jövőben
    más implementációk is hozzáadhatók (pl. Redis, Kafka, stb.).


## Függvények

### `create`

Létrehozza az EventBus példányt.

        Args:
            config: EventBus konfiguráció (opcionális)

        Returns:
            EventBusInterface: Az EventBus példány

        Note:
            Jelenleg csak a ZeroMQ-s implementációt támogatja.

### `create_and_start`

Létrehozza és elindítja az EventBus példányt.

        Args:
            config: EventBus konfiguráció (opcionális)

        Returns:
            EventBusInterface: Az elindított EventBus példány

### `create_from_config`

Létrehozza az EventBus példányt konfigurációkezelő alapján.

        Args:
            config_manager: Konfigurációkezelő, amelyből az EventBus beállításokat olvassuk

        Returns:
            EventBusInterface: Az EventBus példány

        Note:
            A metódus biztonságosan kezeli a konfiguráció hiányát,
            alapértelmezett értékeket használva.


---

**Forrásfájl:** [`core/events/factory.py`](../../../neural_ai/core/events/factory.py)
