# scripts/migrate_structure.py

Adatstruktúra migrációs script.

Ez a szkript átszervezi a tick adatok tárolási szerkezetét.
A `data/tick/{SYMBOL}/tick/` mappák tartalmát egy szinttel feljebb helyezi,
és eltávolítja az üres `tick` almappákat.

A szkript használja a core komponenseket logging és konfiguráció céljából.

## Függvények

### `migrate_tick_structure`

Migrálja a tick adatok tárolási szerkezetét.

Iterál végig a szimbólum mappákon, és ha megtalálja a `tick` almappát,
áthelyezi annak tartalmát egy szinttel feljebb, majd törli az üres mappát.

    Args:
        logger: Logger példány a műveletek naplózásához

### `main`

Fő végrehajtási függvény.

Inicializálja a core komponenseket és futtatja a migrációt.

    Returns:
        int: Kilépési kód (0 = siker, 1 = hiba)


---

**Forrásfájl:** [`scripts/migrate_structure.py`](../../../scripts/migrate_structure.py)