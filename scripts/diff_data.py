#!/usr/bin/env python3
"""Parquet Diff Generator - Forensic Analysis Script

Összehasonlítja a nyers .bi5 adatokat a tárolt Parquet adatokkal,
és kilistázza a hiányzó sorokat a diagnosztika céljából.
"""

import lzma
import struct
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import polars as pl


def detect_format(decompressed: bytes) -> tuple[int, str]:
    """Detektálja a .bi5 rekordformátumot (12 vagy 20 bájtos).

    Args:
        decompressed: Dekompresszált .bi5 bináris adat

    Returns:
        Tuple of (record_size, unpack_format)
    """
    # Alapértelmezett: 12 bájtos formátum (timestamp_delta, ask, bid)
    record_size = 12
    unpack_format = ">III"

    # Heurisztika: ha a hossz osztható 20-szal, ellenőrizzük a 20 bájtos formátumot
    if len(decompressed) % 20 == 0:
        # Smart Check: elemzzük az első néhány rekordot
        try:
            # Legalább 2 rekord kell a validációhoz
            if len(decompressed) >= 40:
                # Első rekord: delta, ask, bid, ask_vol, bid_vol
                first_record = decompressed[0:20]
                delta1, ask1, bid1, ask_vol1, bid_vol1 = struct.unpack(">IIIff", first_record)

                # Második rekord első 4 bájtja (delta)
                second_record = decompressed[20:24]
                (delta2,) = struct.unpack(">I", second_record)

                # Validáció: volume és delta értékek ellenőrzése
                # Volume-oknak "normális" float-nak kell lenniük (0 és 100M között)
                # Delta-nak kis egész számnak kell lenniük (0 és 3600000 között, azaz 1 óra)
                is_valid_volume = (
                    0.0 <= ask_vol1 <= 100_000_000.0 and 0.0 <= bid_vol1 <= 100_000_000.0
                )
                is_valid_delta = 0 <= delta1 <= 3_600_000 and 0 <= delta2 <= 3_600_000

                if is_valid_volume and is_valid_delta:
                    # A delta2 - delta1 különbségnek is ésszerűnek kell lenni
                    delta_diff = abs(delta2 - delta1)
                    if delta_diff <= 1000:  # Maximum 1 másodperc különbség
                        record_size = 20
                        unpack_format = ">IIIff"

        except struct.error:
            # Hiba esetén marad a 12 bájtos alapértelmezett
            pass

    return record_size, unpack_format


def process_bi5_file(file_path: Path) -> list[dict[str, Any]]:
    """Feldolgoz egy .bi5 fájlt és visszaadja a tick adatokat.

    Args:
        file_path: Az elérési út a .bi5 fájlhoz

    Returns:
        Lista TickData objektumokkal (timestamp, bid, ask)
    """
    # Fájlnév elemzése: EURUSD_2024_03_20_00h.bi5
    filename = file_path.stem  # EURUSD_2024_03_20_00h
    parts = filename.split("_")

    if len(parts) < 5:
        print(f"⚠️  Helytelen fájlnév formátum: {filename}")
        return []

    year = int(parts[1])
    month = int(parts[2])
    day = int(parts[3])
    hour_str = parts[4].replace("h", "")
    hour = int(hour_str)

    date = datetime(year, month, day, hour)

    # Fájl beolvasása
    with open(file_path, "rb") as f:
        data = f.read()

    # Check for empty file before attempting decompression
    if not data or len(data) == 0:
        print(f"⚠️  Üres fájl: {file_path.name}")
        return []

    # LZMA dekompresszió
    try:
        decompressed = lzma.decompress(data)
    except lzma.LZMAError as e:
        print(f"⚠️  LZMA hiba {file_path.name}: {e}")
        return []

    # Formátum detektálás
    record_size, unpack_format = detect_format(decompressed)
    num_records = len(decompressed) // record_size

    # Base timestamp: az óra eleje milliszekundumban
    base_timestamp = int(date.replace(minute=0, second=0, microsecond=0).timestamp()) * 1000

    ticks: list[dict[str, Any]] = []

    # Metrikaváltozók a statisztikákhoz
    total_records = 0
    skipped_price = 0
    valid_ticks = 0

    for i in range(num_records):
        total_records += 1

        offset = i * record_size
        record = decompressed[offset : offset + record_size]

        # Dinamikus unpakolás a detektált formátum alapján
        if record_size == 20:
            # 20 bájtos formátum: delta, ask, bid, ask_vol, bid_vol
            timestamp_delta, ask_int, bid_int, ask_vol, bid_vol = struct.unpack(
                unpack_format, record
            )
        else:
            # 12 bájtos formátum: delta, ask, bid
            timestamp_delta, ask_int, bid_int = struct.unpack(unpack_format, record)

        # Átváltás integer árakból float-ba
        ask = ask_int / 100000.0
        bid = bid_int / 100000.0

        # Ár szűrés: csak a nullánál nagyobb árakat fogadjuk el
        if bid <= 0.0 or ask <= 0.0:
            skipped_price += 1
            continue

        # Dátum validáció: a timestamp_delta nem lehet negatív
        if timestamp_delta < 0:
            continue

        # Aktuális timestamp számítása
        timestamp_ms = base_timestamp + timestamp_delta
        timestamp = datetime.fromtimestamp(timestamp_ms / 1000, tz=UTC)

        # Dátum validáció: a timestamp a kért dátum napján belül kell legyen
        # Megengedjük, hogy az óra végén lévő tick-ek a következő órába essenek
        if timestamp.date() != date.date():
            continue

        # Tick hozzáadása
        tick = {
            "timestamp": timestamp,
            "bid": round(bid, 5),
            "ask": round(ask, 5),
        }
        ticks.append(tick)
        valid_ticks += 1

    print(
        f"✅ {file_path.name}: {len(ticks)} tick feldolgozva (összes: {total_records}, ár-szűrés: {skipped_price})"
    )
    return ticks


def main() -> None:
    """Fő futtató metódus."""
    print("=" * 80)
    print("🔍 PARQUET DIFF GENERATOR - FORENSIC ANALYSIS")
    print("=" * 80)
    print()

    # 1. CONTROL (Nyers) Betöltése
    print("1️⃣  CONTROL (Nyers) adatok betöltése...")
    debug_raw_path = Path("data/debug_raw")

    if not debug_raw_path.exists():
        print(f"❌ A {debug_raw_path} mappa nem létezik!")
        return

    bi5_files = sorted(debug_raw_path.glob("*.bi5"))
    print(f"   📁 {len(bi5_files)} .bi5 fájl található")

    all_raw_ticks: list[dict[str, Any]] = []

    for bi5_file in bi5_files:
        ticks = process_bi5_file(bi5_file)
        all_raw_ticks.extend(ticks)

    # DataFrame létrehozása
    raw_df = pl.DataFrame(all_raw_ticks)
    print(f"   ✅ Összesen {len(raw_df)} tick a nyers adatokban")
    print()

    # 2. SYSTEM (Parquet) Betöltése
    print("2️⃣  SYSTEM (Parquet) adatok betöltése...")
    parquet_pattern = "data/tick/EURUSD/**/*.parquet"

    try:
        parquet_df = pl.read_parquet(parquet_pattern)
        print(f"   ✅ Összesen {len(parquet_df)} tick a Parquet adatokban")
    except Exception as e:
        print(f"❌ Hiba a Parquet betöltésénél: {e}")
        return

    print()

    # 3. Összehasonlítás (Anti-Join)
    print("3️⃣  Összehasonlítás (Anti-Join)...")

    # Ellenőrizzük, hogy a Parquet DataFrame-ben vannak-e a szükséges oszlopok
    required_columns = {"timestamp", "bid", "ask"}
    if not required_columns.issubset(parquet_df.columns):
        print(
            f"❌ Hiányzó oszlopok a Parquet adatokban: {required_columns - set(parquet_df.columns)}"
        )
        return

    # Anti-join: keresd azokat, amik a raw-ban megvannak, de a parquet-ben nincsenek
    missing_df = raw_df.join(
        parquet_df.select(["timestamp", "bid", "ask"]), on=["timestamp", "bid", "ask"], how="anti"
    )

    print(f"   🔍 Hiányzó sorok száma: {len(missing_df)}")
    print()

    # 4. Kimenet
    print("=" * 80)
    print("📊 STATISZTIKA")
    print("=" * 80)
    print(f"   Összes nyers tick: {len(raw_df)}")
    print(f"   Összes Parquet tick: {len(parquet_df)}")
    print(f"   Hiányzó tick-ek: {len(missing_df)}")
    print()

    if len(missing_df) > 0:
        print("=" * 80)
        print("⚠️  HIÁNYZÓ SOROK")
        print("=" * 80)
        print(missing_df)
        print()

        # Elemzés
        print("=" * 80)
        print("🔬 ELEMZÉS")
        print("=" * 80)

        # Ellenőrizzük, hogy a hiányzó sorokban vannak-e érvénytelen árak
        invalid_bid_count = missing_df.filter(pl.col("bid") <= 0.0).height
        invalid_ask_count = missing_df.filter(pl.col("ask") <= 0.0).height

        if invalid_bid_count > 0 or invalid_ask_count > 0:
            print("✅ A hiányzó sorok érvénytelen árakat tartalmaznak (0 vagy negatív).")
            print("   Ez a szűrés HELYES - ezeket az adatokat nem szabad tárolni!")
        else:
            print("⚠️  A hiányzó sorok érvényes árakat tartalmaznak!")
            print("   Ez a szűrés HIBÁS - valódi adatvesztésről van szó!")
            print()
            print("   Példák a hiányzó sorokra:")
            print(missing_df.head(10))
    else:
        print("✅ NINCS ELTÉRÉS! Minden nyers adat megtalálható a Parquet tárolóban.")

    print()
    print("=" * 80)
    print("🎯 ELEMZÉS BEFEJEZVE")
    print("=" * 80)


if __name__ == "__main__":
    main()
