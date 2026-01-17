#!/usr/bin/env python3
"""Adatintegritási audit script.

Összehasonlítja a nyers .bi5 fájlokban lévő adatokat a feldolgozott Parquet
fájlokkal óránkénti bontásban, hogy feltérképezze a hiányzó adatokat.
"""

import lzma
import struct
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

import polars as pl


def parse_bi5_file(file_path: Path) -> list[datetime]:
    """Kicsomagolja és feldolgozza a .bi5 fájlt, visszaadja az összes tick timestamp-et.

    A .bi5 fájl LZMA tömörített bináris adatot tartalmaz, ahol minden rekord
    12 bájt (timestamp_delta: 4 bájt, ask: 4 bájt, bid: 4 bájt) vagy 20 bájt lehet.
    A timestamp_delta az óra elejétől mért ezredmásodpercben.
    """
    timestamps = []

    try:
        with lzma.open(file_path, "rb") as f:
            data = f.read()

        if len(data) == 0:
            print(f"  ⚠️  Üres fájl: {file_path.name}")
            return timestamps

        # Fájlnévből kinyerjük a dátumot és órát
        # Formátum: EURUSD_2024_03_20_00h.bi5
        filename = file_path.stem  # EURUSD_2024_03_20_00h
        parts = filename.split("_")

        if len(parts) < 5:
            print(f"  ❌ Hibás fájlnév formátum: {file_path.name}")
            return timestamps

        year = int(parts[1])
        month = int(parts[2])
        day = int(parts[3])
        hour = int(parts[4].replace("h", ""))

        # Base timestamp: az óra eleje (ezredmásodpercben)
        base_timestamp = int(datetime(year, month, day, hour, 0, 0, tzinfo=UTC).timestamp()) * 1000

        # Rekord méret detektálása (12 vagy 20 bájt)
        record_size = 12  # Alapértelmezett
        if len(data) % 20 == 0:
            record_size = 20

        num_records = len(data) // record_size

        for i in range(num_records):
            offset = i * record_size
            # Első 4 bájt a timestamp_delta (ezredmásodpercben az óra elejétől)
            timestamp_delta = struct.unpack(">I", data[offset : offset + 4])[0]

            # Kiszámoljuk a tényleges timestampet
            timestamp_ms = base_timestamp + timestamp_delta
            timestamp = datetime.fromtimestamp(timestamp_ms / 1000, tz=UTC)
            timestamps.append(timestamp)

        print(f"  ✓ {file_path.name}: {num_records} rekord ({record_size} bájtos formátum)")

    except Exception as e:
        print(f"  ❌ Hiba a {file_path.name} feldolgozásakor: {e}")

    return timestamps


def analyze_raw_data(raw_dir: Path) -> dict[str, int]:
    """Analizálja a nyers .bi5 fájlokat és visszaadja óránkénti darabszámot.

    Args:
        raw_dir: A data/debug_raw mappa útvonala

    Returns:
        Dict ahol a kulcs az óra (pl. "00", "01", ..., "23"), az érték a darabszám
    """
    print("\n[1/3] Nyers adatok elemzése...")
    print(f"Keresés a mappában: {raw_dir}")

    if not raw_dir.exists():
        print(f"❌ A {raw_dir} mappa nem létezik!")
        return {}

    bi5_files = sorted(raw_dir.glob("*.bi5"))
    print(f"Talált fájlok: {len(bi5_files)} db .bi5 fájl")

    raw_counts: dict[str, int] = defaultdict(int)

    for bi5_file in bi5_files:
        timestamps = parse_bi5_file(bi5_file)

        for ts in timestamps:
            hour = ts.strftime("%H")
            raw_counts[hour] += 1

    print(f"✓ Nyers adatok feldolgozva. Összesen {sum(raw_counts.values())} rekord.")
    return dict(raw_counts)


def analyze_system_data(tick_dir: Path) -> dict[str, int]:
    """Analizálja a feldolgozott Parquet fájlokat és visszaadja óránkénti darabszámot.

    Args:
        tick_dir: A data/tick mappa útvonala

    Returns:
        Dict ahol a kulcs az óra (pl. "00", "01", ..., "23"), az érték a darabszám
    """
    print("\n[2/3] Rendszer adatok elemzése...")
    print(f"Keresés a mappában: {tick_dir}")

    if not tick_dir.exists():
        print(f"❌ A {tick_dir} mappa nem létezik!")
        return {}

    parquet_files = sorted(tick_dir.glob("**/*.parquet"))
    print(f"Talált fájlok: {len(parquet_files)} db .parquet fájl")

    if not parquet_files:
        print("⚠️  Nincsenek Parquet fájlok a mappában!")
        return {}

    sys_counts: dict[str, int] = defaultdict(int)

    for parquet_file in parquet_files:
        try:
            df = pl.read_parquet(parquet_file)

            # Ellenőrizzük, hogy van-e timestamp oszlop
            if "timestamp" not in df.columns:
                print(f"  ⚠️  {parquet_file.name}: nincs 'timestamp' oszlop")
                continue

            # Csoportosítás óránként
            hourly_counts = df.group_by(pl.col("timestamp").dt.hour().alias("hour")).len()

            for row in hourly_counts.iter_rows():
                hour = str(row[0]).zfill(2)
                count = row[1]
                sys_counts[hour] += count

            print(f"  ✓ {parquet_file.name}: {len(df)} rekord")

        except Exception as e:
            print(f"  ❌ Hiba a {parquet_file.name} feldolgozásakor: {e}")

    print(f"✓ Rendszer adatok feldolgozva. Összesen {sum(sys_counts.values())} rekord.")
    return dict(sys_counts)


def compare_data(raw_counts: dict[str, int], sys_counts: dict[str, int]) -> None:
    """Összehasonlítja a nyers és rendszer adatokat, kiírja a táblázatot.

    Args:
        raw_counts: Nyers adatok óránkénti darabszáma
        sys_counts: Rendszer adatok óránkénti darabszáma
    """
    print("\n[3/3] Összehasonlítás...")
    print("\n" + "=" * 70)
    print("ÓRA | NYERS (db) | SYSTEM (db) | ELTÉRÉS |")
    print("=" * 70)

    all_hours = sorted(set(list(raw_counts.keys()) + list(sys_counts.keys())))
    total_raw = 0
    total_sys = 0
    missing_hours = []
    partial_missing = []

    for hour in all_hours:
        raw_count = raw_counts.get(hour, 0)
        sys_count = sys_counts.get(hour, 0)
        total_raw += raw_count
        total_sys += sys_count

        if raw_count == 0 and sys_count == 0:
            status = "ÜRES"
        elif raw_count > 0 and sys_count == 0:
            status = "❌ HIÁNYZIK"
            missing_hours.append(hour)
        elif raw_count == sys_count:
            status = "✅ OK"
        else:
            diff = raw_count - sys_count
            status = f"⚠️  -{diff}"
            partial_missing.append((hour, diff))

        print(f"{hour:>3} | {raw_count:>9} | {sys_count:>10} | {status:<7} |")

    print("=" * 70)
    print(
        f"ÖSSZESEN: {total_raw} (nyers) vs {total_sys} (rendszer) | "
        f"KÜLÖNBSÉG: {total_raw - total_sys}"
    )
    print("=" * 70)

    # Diagnosztika
    print("\n🔍 DIAGNOSZTIKA:")

    if missing_hours:
        print(f"\n  ❌ Teljesen hiányzó órák ({len(missing_hours)} db):")
        print(f"     {', '.join(missing_hours)}")
        print("\n     → Lehetséges okok:")
        print("       • A base_timestamp vagy fájlnév generálás hibás")
        print("       • A dátum validáció túl szigorú (pl. timezone probléma)")

    if partial_missing:
        print(f"\n  ⚠️  Részben hiányzó adatok ({len(partial_missing)} órában):")
        for hour, diff in partial_missing[:5]:  # Csak az első 5
            print(f"     Óra {hour}: -{diff} db")
        if len(partial_missing) > 5:
            print(f"     ... és még {len(partial_missing) - 5} óra")
        print("\n     → Lehetséges okok:")
        print("       • A szűrő (validátor) vágja le a széleket")
        print("       • Duplikáció szűrés miatt")

    if not missing_hours and not partial_missing:
        print("\n  ✅ Nincs eltérés! Az adatok teljesek.")


def main():
    """Fő végrehajtási függvény."""
    print("\n" + "=" * 70)
    print("🛠️  ADATINTEGRITÁSI AUDIT (RAW vs PARQUET)")
    print("=" * 70)

    # Mappa útvonalak
    project_root = Path(__file__).parent.parent
    raw_dir = project_root / "data" / "debug_raw"
    tick_dir = project_root / "data" / "tick"

    # 1. Nyers adatok elemzése
    raw_counts = analyze_raw_data(raw_dir)

    # 2. Rendszer adatok elemzése
    sys_counts = analyze_system_data(tick_dir)

    # 3. Összehasonlítás és jelentés
    compare_data(raw_counts, sys_counts)

    print("\n✓ Audit befejezve.\n")


if __name__ == "__main__":
    main()
