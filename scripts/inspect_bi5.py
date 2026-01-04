#!/usr/bin/env python3
"""Forensic hex inspection script for .bi5 files.

This script decompresses a .bi5 file from data/debug_raw, analyzes its structure,
and provides a hex dump of the first bytes to diagnose data alignment issues.
"""

import lzma
import struct
from pathlib import Path

# KONFIGURÁCIÓ
DEBUG_DIR = Path("data/debug_raw")
PREFERRED_FILE = "EURUSD_2024_03_20_18h.bi5"


def find_bi5_file() -> Path | None:
    """Megkeresi a preferált vagy az első elérhető .bi5 fájlt.

    Returns:
        A fájl Path objektuma, vagy None ha nincs fájl
    """
    if not DEBUG_DIR.exists():
        print(f"❌ A {DEBUG_DIR} mappa nem létezik!")
        return None

    # Először próbáljuk a preferált fájlt
    preferred_path = DEBUG_DIR / PREFERRED_FILE
    if preferred_path.exists():
        print(f"✅ Preferált fájl megtalálva: {PREFERRED_FILE}")
        return preferred_path

    # Ha nincs, keressük az első .bi5 fájlt
    bi5_files = list(DEBUG_DIR.glob("*.bi5"))
    if not bi5_files:
        print(f"❌ Nincs .bi5 fájl a {DEBUG_DIR} mappában!")
        return None

    first_file = bi5_files[0]
    print(f"⚠️  Preferált fájl nem található, az első fájlt használom: {first_file.name}")
    return first_file


def analyze_bi5_file(filepath: Path) -> None:
    """Elemzi a .bi5 fájlt és kiírja a struktúra információkat.

    Args:
        filepath: Az elemzendő .bi5 fájl elérési útja
    """
    print("=" * 80)
    print("🔍 FORENSIC HEX INSPECTION")
    print("=" * 80)
    print(f"Fájl: {filepath.name}")
    print(f"Teljes elérési út: {filepath.absolute()}")
    print("-" * 80)

    try:
        # Fájl betöltése
        raw_content = filepath.read_bytes()
        print(f"📦 Nyers fájl mérete: {len(raw_content):,} bájt")

        # LZMA decompress
        try:
            decompressed = lzma.decompress(raw_content)
        except lzma.LZMAError as e:
            print(f"❌ LZMA decompressziós hiba: {e}")
            return

        decompressed_len = len(decompressed)
        print(f"✅ Dekomprimált méret: {decompressed_len:,} bájt")
        print("-" * 80)

        # Oszthatóság ellenőrzése
        print("📏 STRUKTÚRA ELLENŐRZÉS")
        print("-" * 80)

        divisible_12 = decompressed_len % 12 == 0
        divisible_20 = decompressed_len % 20 == 0

        print(f"Osztható 12-vel (Standard Tick: 3x uint32): {'✅' if divisible_12 else '❌'}")
        print(
            f"  {decompressed_len} / 12 = {decompressed_len / 12 if divisible_12 else decompressed_len // 12}"
        )
        print(f"  Maradék: {decompressed_len % 12}")

        print(f"\nOsztható 20-vel (Tick + Volume: 5x uint32): {'✅' if divisible_20 else '❌'}")
        print(
            f"  {decompressed_len} / 20 = {decompressed_len / 20 if divisible_20 else decompressed_len // 20}"
        )
        print(f"  Maradék: {decompressed_len % 20}")

        if not divisible_12 and not divisible_20:
            print("\n⚠️  FIGYELEM: A fájl mérete nem osztható sem 12-vel, sem 20-cal!")
            print("   Ez azt jelenti, hogy az adatstruktúra valószínűleg nem standard.")

        print("-" * 80)

        # HEX DUMP az első 48 bájtból
        print("🔢 HEX DUMP (első 48 bájt)")
        print("-" * 80)
        print("Offset  | Hex Dump                                      | >III (Big Endian uint32)")
        print("-" * 80)

        bytes_to_dump = min(48, decompressed_len)
        for i in range(0, bytes_to_dump, 12):
            # Hex dump sor
            hex_part = decompressed[i : i + 12].hex(" ", 4)
            hex_padded = hex_part.ljust(47)

            # >III értelmezés (3 darab big-endian uint32)
            offset_str = f"{i:06X}h"

            if i + 12 <= decompressed_len:
                try:
                    values = struct.unpack(">III", decompressed[i : i + 12])
                    values_str = f"[{values[0]:>10}, {values[1]:>10}, {values[2]:>10}]"
                except struct.error as e:
                    values_str = f"[STRUCT ERROR: {e}]"
            else:
                values_str = "[NEM TELJES RECORD]"

            print(f"{offset_str} | {hex_padded} | {values_str}")

        print("-" * 80)

        # További elemzés, ha szükséges
        if decompressed_len > 48:
            print("\n📊 TELJES FAJL TARTALOM:")
            print(f"Összes record (12 bájtos feltételezéssel): {decompressed_len // 12}")
            print(f"Utolsó record offsetje: {decompressed_len - 12:06X}h")

            # Utolsó 12 bájt is
            print("\n🔚 UTOLSÓ 12 BÁJT:")
            last_12 = decompressed[-12:]
            hex_part = last_12.hex(" ", 4)
            try:
                values = struct.unpack(">III", last_12)
                values_str = f"[{values[0]:>10}, {values[1]:>10}, {values[2]:>10}]"
            except struct.error as e:
                values_str = f"[STRUCT ERROR: {e}]"

            print(f"Hex: {hex_part}")
            print(f">III: {values_str}")

        print("=" * 80)

    except Exception as e:
        print(f"❌ Váratlan hiba: {e}")
        import traceback

        traceback.print_exc()


def main():
    """Főprogram."""
    print("🚀 FORENSIC HEX INSPECTION SCRIPT")
    print("=" * 80)

    # Fájl keresése
    filepath = find_bi5_file()
    if filepath is None:
        print("❌ Kilépek...")
        return

    # Elemzés
    analyze_bi5_file(filepath)

    print("\n✅ Elemzés befejezve.")


if __name__ == "__main__":
    main()
