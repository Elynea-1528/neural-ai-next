#!/usr/bin/env python3
"""Adat reset szkript a Neural AI Next rendszer számára.

Ez a script végrehajtja az adat reset műveletet, törölve az összes tick adatot és logokat
a tiszta validáció érdekében.

Használat:
    python scripts/data_reset.py
"""

import os
import shutil
import sys
from pathlib import Path


def check_directory_exists(path: str) -> bool:
    """Ellenőrzi, hogy a megadott könyvtár létezik-e és könyvtár-e.

    Args:
        path: A könyvtár elérési útja.

    Returns:
        True ha létezik és könyvtár, különben False.
    """
    return os.path.exists(path) and os.path.isdir(path)


def create_directories_if_needed() -> None:
    """Létrehozza a szükséges könyvtárakat, ha nem léteznek."""
    directories = ["data/tick", "logs"]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ Szükséges könyvtárak ellenőrizve/létrehozva")


def remove_tick_data() -> bool:
    """Eltávolítja a teljes tick adat könyvtárat.

    Returns:
        True ha sikeres, False ha hiba történt.
    """
    tick_dir = "data/tick"
    if not check_directory_exists(tick_dir):
        print("ℹ️  Tick adat könyvtár nem létezik, kihagyva")
        return True

    try:
        shutil.rmtree(tick_dir)
        print(f"✅ Tick adatok törölve: {tick_dir}")
        return True
    except Exception as e:
        print(f"❌ Hiba a tick adatok törlésekor: {e}")
        return False


def remove_logs() -> bool:
    """Eltávolítja az összes fájlt és alkönyvtárat a logs könyvtárban.

    Returns:
        True ha sikeres, False ha hiba történt.
    """
    logs_dir = "logs"
    if not check_directory_exists(logs_dir):
        print("ℹ️  Logs könyvtár nem létezik, kihagyva")
        return True

    try:
        for item in os.listdir(logs_dir):
            item_path = os.path.join(logs_dir, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        print(f"✅ Logok törölve: {logs_dir}/*")
        return True
    except Exception as e:
        print(f"❌ Hiba a logok törlésekor: {e}")
        return False


def main() -> None:
    """Fő függvény az adat reset végrehajtásához."""
    print("=" * 60)
    print("🗑️  ADAT RESET - Tick adatok és logok törlése")
    print("=" * 60)
    print()

    # 1. Könyvtárak létrehozása
    create_directories_if_needed()
    print()

    # 2. Tick adatok törlése
    tick_success = remove_tick_data()

    # 3. Logok törlése
    logs_success = remove_logs()
    print()

    # 4. Eredmény riport
    print("=" * 60)
    if tick_success and logs_success:
        print("✅ Adat reset sikeres! Tiszta állapot a validációhoz.")
    else:
        print("❌ Adat reset részben vagy teljesen sikertelen.")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
