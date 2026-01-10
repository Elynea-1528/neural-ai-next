#!/usr/bin/env python3
"""Adat reset szkript tick adatok és logok törléséhez.

Ez a szkript törli az összes tick adatot és logokat a tiszta validáció érdekében.
Cél: CORE DATA PIPELINE refaktorálás támogatása.

Törölt könyvtárak/fájlok:
- data/tick/ (teljes könyvtár)
- logs/* (minden fájl és alkönyvtár a logs könyvtárban)
"""

import os
import shutil
import sys
from pathlib import Path


def check_directory_exists(path: str) -> bool:
    """Ellenőrzi, hogy a könyvtár létezik-e.

    Args:
        path: A könyvtár útvonala.

    Returns:
        True ha létezik, különben False.
    """
    return os.path.exists(path) and os.path.isdir(path)


def remove_tick_data() -> bool:
    """Törli a data/tick könyvtárat teljes mértékben.

    Returns:
        True ha sikeres, különben False.
    """
    tick_path = "data/tick"
    if check_directory_exists(tick_path):
        try:
            shutil.rmtree(tick_path)
            print(f"✅ Tick adatok törölve: {tick_path}")
            return True
        except Exception as e:
            print(f"❌ Hiba a tick adatok törlésekor: {e}")
            return False
    else:
        print(f"⚠ Tick adatok könyvtára nem található: {tick_path}")
        return True  # Nem hiba, ha nem létezik


def remove_logs() -> bool:
    """Törli az összes fájlt és alkönyvtárat a logs könyvtárban.

    Returns:
        True ha sikeres, különben False.
    """
    logs_path = "logs"
    if check_directory_exists(logs_path):
        try:
            # Törli az összes fájlt és alkönyvtárat a logs-ban
            for item in os.listdir(logs_path):
                item_path = os.path.join(logs_path, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            print(f"✅ Logok törölve: {logs_path}/*")
            return True
        except Exception as e:
            print(f"❌ Hiba a logok törlésekor: {e}")
            return False
    else:
        print(f"⚠ Logs könyvtár nem található: {logs_path}")
        return True  # Nem hiba, ha nem létezik


def create_directories_if_needed() -> None:
    """Létrehozza a szükséges könyvtárakat, ha nem léteznek."""
    Path("data/tick").parent.mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)
    print("✅ Szükséges könyvtárak ellenőrizve/létrehozva")


def main() -> None:
    """Fő végrehajtási függvény az adat reset-hez."""
    print(f"\n{'=' * 60}")
    print("🗑️  ADAT RESET - Tick adatok és logok törlése")
    print(f"{'=' * 60}\n")

    # Könyvtárak előkészítése
    create_directories_if_needed()

    # Tick adatok törlése
    tick_success = remove_tick_data()

    # Logok törlése
    logs_success = remove_logs()

    print(f"\n{'=' * 60}")
    if tick_success and logs_success:
        print("✅ Adat reset sikeres! Tiszta állapot a validációhoz.")
    else:
        print("❌ Adat reset részben vagy teljesen sikertelen.")
        sys.exit(1)
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
