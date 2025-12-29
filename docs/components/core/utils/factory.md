# core/utils/factory.py

Hardverinformációk lekérdezéséhez szükséges Factory osztály.

Ez a modul a `HardwareFactory` osztályt tartalmazza, amely a
`HardwareInfo` implementáció példányosításáért felelős.

## Osztályok

### `HardwareFactory`

Factory osztály a `HardwareInfo` példányosításához.


## Függvények

### `get_hardware_info`

Visszaad egy `HardwareInfo` példányt.

        Returns:
            HardwareInfo: A hardverinformációkat tartalmazó osztály példánya.

### `get_hardware_interface`

Visszaad egy `HardwareInterface`-t implementáló példányt.

        Returns:
            HardwareInterface: A hardverinterfészt implementáló osztály példánya.


---

**Forrásfájl:** [`core/utils/factory.py`](../../../neural_ai/core/utils/factory.py)
