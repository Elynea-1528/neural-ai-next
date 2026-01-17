#!/usr/bin/env python3
"""Adatstruktúra migrációs script a Neural AI Next rendszer számára.

Ez a szkript átszervezi a tick adatok tárolási szerkezetét.
A `data/tick/{SYMBOL}/tick/` mappák tartalmát egy szinttel feljebb helyezi,
és eltávolítja az üres `tick` almappákat.

A szkript használja a core komponenseket logging és konfiguráció céljából.
"""

import shutil
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


def migrate_tick_structure(logger: "LoggerInterface") -> bool:
    """Migrálja a tick adatok tárolási szerkezetét.

    Iterál végig a szimbólum mappákon, és ha megtalálja a `tick` almappát,
    áthelyezi annak tartalmát egy szinttel feljebb, majd törli az üres mappát.

    Args:
        logger: Logger példány a műveletek naplózásához

    Returns:
        bool: True ha sikeres, False ha hiba történt
    """
    tick_base_path = Path("data/tick")

    if not tick_base_path.exists():
        logger.warning("Tick adat könyvtár nem létezik", path=str(tick_base_path))
        return True

    success = True

    # Iterál végig a szimbólum mappákon
    for symbol_dir in tick_base_path.iterdir():
        if not symbol_dir.is_dir():
            continue

        tick_subdir = symbol_dir / "tick"
        if not tick_subdir.exists() or not tick_subdir.is_dir():
            continue

        logger.info("Migráció elkezdődött szimbólumhoz", symbol=str(symbol_dir.name))

        try:
            # Mozgatás minden fájlnak/térképtárnak a tick almappából a szimbólum mappába
            for item in tick_subdir.iterdir():
                dest_path = symbol_dir / item.name

                if dest_path.exists():
                    logger.warning("Célútvonal már létezik, átugrás", source=str(item), dest=str(dest_path))
                    continue

                if item.is_file():
                    shutil.move(str(item), str(dest_path))
                    logger.debug("Fájl áthelyezve", file=str(item.name), symbol=str(symbol_dir.name))
                elif item.is_dir():
                    shutil.move(str(item), str(dest_path))
                    logger.debug("Mappa áthelyezve", dir=str(item.name), symbol=str(symbol_dir.name))

            # Törölje az üres tick almappát
            if not any(tick_subdir.iterdir()):
                tick_subdir.rmdir()
                logger.info("Üres tick almappa törölve", symbol=str(symbol_dir.name))
            else:
                logger.warning("Tick almappa nem üres migráció után", symbol=str(symbol_dir.name), remaining=list(tick_subdir.iterdir()))

        except Exception as e:
            logger.error("Hiba a migráció során", symbol=str(symbol_dir.name), error=str(e))
            success = False

    return success


def main() -> int:
    """Fő végrehajtási függvény.

    Inicializálja a core komponenseket és futtatja a migrációt.

    Returns:
        int: Kilépési kód (0 = siker, 1 = hiba)
    """
    try:
        # Core komponensek inicializálása
        from neural_ai.core.logger.factory import LoggerFactory

        logger = LoggerFactory.get_logger("migrate_structure")

        logger.info("Adatstruktúra migráció elindítva")

        # Migráció futtatása
        if migrate_tick_structure(logger):
            logger.info("Adatstruktúra migráció sikeresen befejeződött")
            return 0
        else:
            logger.error("Adatstruktúra migráció hibákkal fejeződött be")
            return 1

    except Exception as e:
        print(f"Végzetes hiba a migráció során: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
