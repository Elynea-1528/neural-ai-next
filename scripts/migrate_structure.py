"""Adatstruktúra migrációs szkript.

Ez a szkript a tick adatokat migrálja az új mappa szerkezetbe.
Az új szerkezet: data/tick/SYMBOL/YEAR/MONTH/DAY/ fájlok
"""

import sys
from pathlib import Path
from typing import Any

from neural_ai.core.base.implementations.component_bundle import CoreComponentFactory


def migrate_tick_structure(logger: Any) -> None:
    """Tick adatstruktúra migrálása.

    Az új szerkezet: data/tick/SYMBOL/YEAR/MONTH/DAY/ fájlok
    A régi szerkezet: data/tick/SYMBOL/tick/YEAR/... fájlok

    Args:
        logger: A logger példány
    """
    base_dir = Path("data/tick")

    if not base_dir.exists():
        logger.error(f"Az alapkönyvtár nem létezik: {base_dir}")
        return

    logger.info("Tick adatstruktúra migráció megkezdése")

    # Szimbólum könyvtárak feldolgozása
    symbols_processed = 0
    symbols_migrated = 0

    for symbol_dir in base_dir.iterdir():
        if not symbol_dir.is_dir():
            continue

        symbols_processed += 1
        symbol_name = symbol_dir.name
        logger.info(f"Szimbólum feldolgozása: {symbol_name}")

        # Tick almappa keresése
        tick_subdir = symbol_dir / "tick"
        if not tick_subdir.exists():
            logger.debug(f"Nincs tick almappa a szimbólumnál: {symbol_name}")
            continue

        if not tick_subdir.is_dir():
            logger.warning(f"A tick 'útvonal' nem mappa: {tick_subdir}")
            continue

        # Tick almappa tartalmának ellenőrzése
        tick_contents = list(tick_subdir.iterdir())
        if not tick_contents:
            # Üres tick mappa - töröljük
            try:
                logger.info(f"Üres tick mappa törlésre kerül: {tick_subdir}")
                tick_subdir.rmdir()
                logger.info(f"Sikeresen törölve: {tick_subdir}")
                symbols_migrated += 1
                continue
            except OSError as e:
                logger.error(f"Hiba a tick mappa törlésekor {tick_subdir}: {e}")
                continue

        # Tartalom áthelyezése
        logger.info(f"Tartalom áthelyezése: {tick_subdir} -> {symbol_dir}")

        for item in tick_contents:
            if not item.is_dir():
                logger.warning(f"Nem mappa elem kihagyva: {item}")
                continue

            # Év könyvtár
            year_name = item.name
            target_year_dir = symbol_dir / year_name

            if target_year_dir.exists():
                logger.warning(f"A célmappa már létezik, átugrás: {target_year_dir}")
                continue

            try:
                logger.info(f"Áthelyezve: {item} -> {target_year_dir}")
                # Path objektumok használata
                import shutil

                shutil.move(str(item), str(target_year_dir))
            except OSError as e:
                logger.error(f"Hiba az áthelyezéskor {item} -> {target_year_dir}: {e}")
                continue

        # Tick mappa törlése
        try:
            logger.info(f"Tick mappa törölve: {tick_subdir}")
            tick_subdir.rmdir()
            symbols_migrated += 1
        except OSError as e:
            logger.error(f"Hiba a tick mappa törlésekor {tick_subdir}: {e}")

    if symbols_processed == 0:
        logger.warning("Nem található szimbólum mappa a tick könyvtárban")

    logger.info(
        f"Migráció befejezve. Feldolgozott: {symbols_processed}, Migrált: {symbols_migrated}"
    )


def main() -> int:
    """Fő függvény a szkript futtatásához.

    Returns:
        int: Kilépési kód (0 = siker, 1 = hiba)
    """
    try:
        # Minimal core komponensek létrehozása
        components = CoreComponentFactory.create_minimal()

        # Logger lekérése
        logger = components.logger
        if logger is None:
            print("Hiba: Logger komponens nem inicializálódott")
            return 1

        # Migráció futtatása
        migrate_tick_structure(logger)

        return 0

    except Exception as e:
        print(f"Váratlan hiba: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
