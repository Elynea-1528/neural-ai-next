#!/usr/bin/env python3
"""Adatstruktúra migrációs script.

Ez a szkript átszervezi a tick adatok tárolási szerkezetét.
A `data/tick/{SYMBOL}/tick/` mappák tartalmát egy szinttel feljebb helyezi,
és eltávolítja az üres `tick` almappákat.

A szkript használja a core komponenseket logging és konfiguráció céljából.

Author: Neural AI Team
Version: 1.0.0
"""

import shutil
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from neural_ai.core.base.factory import CoreComponentFactory

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


def migrate_tick_structure(logger: "LoggerInterface") -> None:
    """Migrálja a tick adatok tárolási szerkezetét.

    Iterál végig a szimbólum mappákon, és ha megtalálja a `tick` almappát,
    áthelyezi annak tartalmát egy szinttel feljebb, majd törli az üres mappát.

    Args:
        logger: Logger példány a műveletek naplózásához
    """
    base_dir = Path("data/tick")

    if not base_dir.exists():
        logger.error(f"Az alapkönyvtár nem létezik: {base_dir}")
        return

    logger.info(f"Tick adat migráció megkezdése: {base_dir}")

    # Szimbólum mappák keresése
    symbol_dirs = [d for d in base_dir.iterdir() if d.is_dir()]

    if not symbol_dirs:
        logger.warning("Nem található szimbólum mappa a tick könyvtárban")
        return

    migrated_count = 0
    processed_count = 0

    for symbol_dir in symbol_dirs:
        symbol_name = symbol_dir.name
        processed_count += 1

        logger.info(f"Szimbólum feldolgozása: {symbol_name}")

        tick_dir = symbol_dir / "tick"

        if not tick_dir.exists():
            logger.debug(f"Nincs tick almappa a szimbólumnál: {symbol_name}")
            continue

        if not tick_dir.is_dir():
            logger.warning(f"A tick 'útvonal' nem mappa: {tick_dir}")
            continue

        # Tartalom ellenőrzése
        subdirs = [d for d in tick_dir.iterdir() if d.is_dir()]

        if not subdirs:
            logger.info(f"Üres tick mappa törlésre kerül: {tick_dir}")
            try:
                tick_dir.rmdir()
                logger.info(f"Sikeresen törölve: {tick_dir}")
                migrated_count += 1
            except OSError as e:
                logger.error(f"Hiba a tick mappa törlésekor {tick_dir}: {e}")
            continue

        # Tartalom áthelyezése
        logger.info(f"Tartalom áthelyezése: {tick_dir} -> {symbol_dir}")

        for subdir in subdirs:
            target_dir = symbol_dir / subdir.name

            if target_dir.exists():
                logger.warning(f"A célmappa már létezik, átugrás: {target_dir}")
                continue

            try:
                shutil.move(str(subdir), str(target_dir))
                logger.info(f"Áthelyezve: {subdir} -> {target_dir}")
            except OSError as e:
                logger.error(f"Hiba az áthelyezéskor {subdir} -> {target_dir}: {e}")
                continue

        # Üres tick mappa törlése
        try:
            tick_dir.rmdir()
            logger.info(f"Tick mappa törölve: {tick_dir}")
            migrated_count += 1
        except OSError as e:
            logger.error(f"Hiba a tick mappa törlésekor {tick_dir}: {e}")

    logger.info(
        f"Migráció befejezve. Feldolgozott szimbólumok: {processed_count}, "
        f"Migrált: {migrated_count}"
    )


def main() -> int:
    """Fő végrehajtási függvény.

    Inicializálja a core komponenseket és futtatja a migrációt.

    Returns:
        int: Kilépési kód (0 = siker, 1 = hiba)
    """
    try:
        # Core komponensek inicializálása
        components = CoreComponentFactory.create_minimal()
        logger = components.logger

        if logger is None:
            print("Hiba: Logger komponens nem inicializálódott")
            return 1

        logger.info("Tick adatstruktúra migrációs script indítása")

        # Migráció futtatása
        migrate_tick_structure(logger)

        logger.info("Migrációs script sikeresen befejezve")
        return 0

    except Exception as e:
        print(f"Váratlan hiba: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
