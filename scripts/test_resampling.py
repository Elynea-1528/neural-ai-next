#!/usr/bin/env python3
"""Tick -> OHLCV Resampling Demo Script

Ez a szkript demonstrálja a Tick adatok OHLCV (Open, High, Low, Close, Volume)
formátumba való konvertálását 1 perces (M1) és 1 órás (H1) időkeretekben.

A szkript a következő lépéseket hajtja végre:
1. Bootstrap: Rendszer inicializálása
2. Discovery: Elérhető dátumok lekérdezése
3. Load: Tick adatok betöltése
4. Resample M1: 1 perces OHLCV generálás
5. Resample H1: 1 órás OHLCV generálás
6. Display: Eredmények színes megjelenítése
7. Export: CSV fájlba mentés

Author: Neural AI Next Team
Version: 1.0.0
"""

import asyncio
import sys
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING, cast

# A projekt gyökérkönyvtárának hozzáadása a Python path-hoz
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Importok a TYPE_CHECKING blokkban
if TYPE_CHECKING:
    import polars as pl
    from neural_ai.core.storage.implementations.parquet_storage import ParquetStorageService

import colorama
from colorama import Fore, Style

# Inicializálás a színes konzolhoz
colorama.init(autoreset=True)

# Importok a saját modulokból
from neural_ai.core.storage.factory import StorageFactory
from neural_ai.core.utils.factory import HardwareFactory


class ResamplingDemo:
    """Tick -> OHLCV resampling demo osztály.

    Ez az osztály felelős a Tick adatok betöltéséért és konvertálásáért
    OHLCV formátumba különböző időkeretekben.
    """

    def __init__(self) -> None:
        """Inicializálja a ResamplingDemo-t.

        Létrehozza a szükséges factory-kat és inicializálja a tárolót.
        """
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}🚀 TICK -> OHLCV RESAMPLING DEMO")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

        # Hardware factory létrehozása
        self.hardware = HardwareFactory.get_hardware_interface()

        # Storage factory létrehozása Parquet tárolóval
        # Megadjuk a helyes base_path-ot, ahol a tick adatok vannak
        data_path = PROJECT_ROOT / "data" / "tick"
        self.storage = StorageFactory.get_storage(
            storage_type="parquet",
            base_path=str(data_path),
            hardware=self.hardware
        )
        
        print(f"{Fore.CYAN}ℹ️  Adat elérési út: {data_path.absolute()}")
        print(f"{Fore.CYAN}ℹ️  Adat elérési út létezik: {data_path.exists()}\n")

        print(f"{Fore.GREEN}✅ Rendszer inicializálva")
        print(f"{Fore.GREEN}   - Hardware: {self.hardware.__class__.__name__}")
        print(f"{Fore.GREEN}   - Storage: {self.storage.__class__.__name__}")
        
        # Type cast to access backend-specific attributes
        from neural_ai.core.storage.implementations.parquet_storage import ParquetStorageService
        if isinstance(self.storage, ParquetStorageService):
            print(f"{Fore.GREEN}   - Backend: {self.storage.backend.name}\n")
        else:
            print(f"{Fore.GREEN}   - Backend: N/A\n")

    async def run(self) -> None:
        """Futtatja a resampling demo teljes folyamatát.

        Ez a metódus vezérli a teljes folyamatot:
        1. Dátumok felfedezése
        2. Adatok betöltése
        3. Resampling M1 és H1
        4. Eredmények megjelenítése
        5. Exportálás
        """
        try:
            # 1. DISCOVERY: Elérhető dátumok lekérdezése
            print(f"{Fore.YELLOW}{'─'*80}")
            print(f"{Fore.YELLOW}🔍 1. FÁZIS: DÁTUMOK FELFEDEZÉSE")
            print(f"{Fore.YELLOW}{'─'*80}{Style.RESET_ALL}\n")

            from neural_ai.core.storage.implementations.parquet_storage import ParquetStorageService
            storage = cast(ParquetStorageService, self.storage)
            
            available_dates = await storage.get_available_dates("EURUSD")

            if not available_dates:
                print(f"{Fore.RED}❌ Hiba: Nincsenek elérhető dátumok az EURUSD szimbólumhoz!")
                print(f"{Fore.RED}   Kérjük, először töltsön le adatokat a scripts/download_history.py szkripttel.\n")
                return

            print(f"{Fore.GREEN}✅ Elérhető dátumok megtalálva: {len(available_dates)} nap\n")
            for i, date in enumerate(available_dates, 1):
                print(f"   {i}. {date.strftime('%Y-%m-%d')} ({date.strftime('%A')})")

            # Az első elérhető nap kiválasztása
            first_date = available_dates[0]
            print(f"\n{Fore.CYAN}📅 Kiválasztott dátum: {first_date.strftime('%Y-%m-%d')}\n")

            # 2. LOAD: Tick adatok betöltése
            print(f"{Fore.YELLOW}{'─'*80}")
            print(f"{Fore.YELLOW}📂 2. FÁZIS: TICK ADATOK BETÖLTÉSE")
            print(f"{Fore.YELLOW}{'─'*80}{Style.RESET_ALL}\n")

            start_date = first_date
            end_date = start_date + timedelta(days=1)

            print(f"{Fore.CYAN}⏳ Betöltés folyamatban...")
            print(f"   - Szimbólum: EURUSD")
            print(f"   - Dátumtartomány: {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}\n")

            tick_data = await storage.read_tick_data("EURUSD", start_date, end_date)

            if len(tick_data) == 0:
                print(f"{Fore.RED}❌ Hiba: Nincsenek tick adatok a kiválasztott dátumhoz!")
                return

            print(f"{Fore.GREEN}✅ Tick adatok sikeresen betöltve")
            print(f"   - Sorok száma: {len(tick_data):,}")
            
            # Convert to Polars for timestamp operations
            import polars as pl
            if not isinstance(tick_data, pl.DataFrame):
                pl_data = pl.from_pandas(tick_data)
            else:
                pl_data = tick_data
            
            timestamp_min = pl_data["timestamp"].min()
            timestamp_max = pl_data["timestamp"].max()
            print(f"   - Időtartomány: {timestamp_min} - {timestamp_max}\n")

            # 3. RESAMPLE: OHLCV konverzió
            print(f"{Fore.YELLOW}{'─'*80}")
            print(f"{Fore.YELLOW}🔄 3. FÁZIS: OHLCV KONVERZIÓ (RESAMPLING)")
            print(f"{Fore.YELLOW}{'─'*80}{Style.RESET_ALL}\n")

            # 3.1 M1 (1 perces) resampling
            print(f"{Fore.CYAN}🕐 3.1 M1 (1 perces) OHLCV generálása...")
            ohlcv_m1 = self._resample_to_ohlcv(pl_data, "1m")
            print(f"{Fore.GREEN}✅ M1 OHLCV kész: {len(ohlcv_m1)} sor\n")

            # 3.2 H1 (1 órás) resampling
            print(f"{Fore.CYAN}🕐 3.2 H1 (1 órás) OHLCV generálása...")
            ohlcv_h1 = self._resample_to_ohlcv(pl_data, "1h")
            print(f"{Fore.GREEN}✅ H1 OHLCV kész: {len(ohlcv_h1)} sor\n")

            # 4. DISPLAY: Eredmények megjelenítése
            print(f"{Fore.YELLOW}{'─'*80}")
            print(f"{Fore.YELLOW}📊 4. FÁZIS: EREDMÉNYEK MEGJELENÍTÉSE")
            print(f"{Fore.YELLOW}{'─'*80}{Style.RESET_ALL}\n")

            self._display_ohlcv_data(ohlcv_m1, "M1 (1 perces)", 5)
            print()
            self._display_ohlcv_data(ohlcv_h1, "H1 (1 órás)", 5)

            # 5. EXPORT: CSV fájlba mentés
            print(f"{Fore.YELLOW}{'─'*80}")
            print(f"{Fore.YELLOW}💾 5. FÁZIS: EXPORTÁLÁS CSV FÁJLBA")
            print(f"{Fore.YELLOW}{'─'*80}{Style.RESET_ALL}\n")

            output_dir = PROJECT_ROOT / "output"
            output_dir.mkdir(exist_ok=True)

            output_file_m1 = output_dir / "test_candles_m1.csv"
            output_file_h1 = output_dir / "test_candles_h1.csv"

            # M1 export
            print(f"{Fore.CYAN}⏳ M1 adatok exportálása: {output_file_m1}")
            ohlcv_m1.write_csv(output_file_m1)
            print(f"{Fore.GREEN}✅ M1 exportálás kész\n")

            # H1 export
            print(f"{Fore.CYAN}⏳ H1 adatok exportálása: {output_file_h1}")
            ohlcv_h1.write_csv(output_file_h1)
            print(f"{Fore.GREEN}✅ H1 exportálás kész\n")

            # Összefoglaló
            print(f"{Fore.CYAN}{'='*80}")
            print(f"{Fore.CYAN}✅ DEMO SIKERESEN BEFEJEZVE!")
            print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
            print(f"{Fore.GREEN}📈 Összefoglaló:")
            print(f"   - Betöltött tick-ek: {len(tick_data):,}")
            print(f"   - M1 gyertya: {len(ohlcv_m1):,}")
            print(f"   - H1 gyertya: {len(ohlcv_h1):,}")
            print(f"   - Exportált fájlok: {output_file_m1.name}, {output_file_h1.name}")
            print(f"   - Kimeneti könyvtár: {output_dir}\n")

        except Exception as e:
            print(f"\n{Fore.RED}{'='*80}")
            print(f"{Fore.RED}❌ HIBA TÖRTÉNT!")
            print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}\n")
            print(f"{Fore.RED}Hibaüzenet: {str(e)}\n")
            import traceback
            print(f"{Fore.RED}Traceback:")
            traceback.print_exc()
            print()

    def _resample_to_ohlcv(self, df: "pl.DataFrame", timeframe: str) -> "pl.DataFrame":
        """Tick adatok konvertálása OHLCV formátumba.

        Ez a metódus végzi el a varázslatot: a Polars group_by_dynamic
        funkcióját használva aggregálja a tick adatokat OHLCV gyertyákba.

        Args:
            df: A bemeneti Tick adatok Polars DataFrame-ben
            timeframe: Az időkeret (pl. "1m", "1h", "1d")

        Returns:
            Az OHLCV adatok Polars DataFrame-ben
        """
        import polars as pl

        # A "varázslat" magja: group_by_dynamic + aggregáció
        ohlcv = df.group_by_dynamic("timestamp", every=timeframe).agg([
            # Open: az első bid ár az időkeretben
            pl.col("bid").first().alias("open"),
            # High: a legmagasabb bid ár az időkeretben
            pl.col("bid").max().alias("high"),
            # Low: a legalacsonyabb bid ár az időkeretben
            pl.col("bid").min().alias("low"),
            # Close: az utolsó bid ár az időkeretben
            pl.col("bid").last().alias("close"),
            # Volume: tick-ek száma az időkeretben
            pl.col("bid").count().alias("ticks")
        ])

        return ohlcv

    def _display_ohlcv_data(self, df: "pl.DataFrame", title: str, rows: int = 5) -> None:
        """OHLCV adatok színes megjelenítése a konzolon.

        Args:
            df: Az OHLCV adatok Polars DataFrame-ben
            title: A megjelenítendő cím
            rows: A megjelenítendő sorok száma
        """
        print(f"{Fore.MAGENTA}📊 {title} OHLCV adatok (első {rows} sor):")
        print(f"{Fore.MAGENTA}{'─'*80}{Style.RESET_ALL}\n")

        # Fejléc
        print(f"{Fore.CYAN}{'Időbélyeg':<25} {'Open':<12} {'High':<12} {'Low':<12} {'Close':<12} {'Ticks':<10}")
        print(f"{Fore.CYAN}{'─'*80}{Style.RESET_ALL}")

        # Adatok - első N sor kiválasztása és iterálás
        df_head = df.head(rows)
        for i in range(len(df_head)):
            row = df_head[i]
            # Polars Series-ből érték kinyerése .item() metódussal
            timestamp = row['timestamp'].item()
            open_price = row['open'].item()
            high_price = row['high'].item()
            low_price = row['low'].item()
            close_price = row['close'].item()
            ticks = row['ticks'].item()

            # Színezés az ár változás alapján
            if close_price > open_price:
                color = Fore.GREEN  # Növekedés
            elif close_price < open_price:
                color = Fore.RED  # Csökkenés
            else:
                color = Fore.YELLOW  # Változatlan

            print(f"{color}{str(timestamp):<25} {open_price:<12.5f} {high_price:<12.5f} "
                  f"{low_price:<12.5f} {close_price:<12.5f} {ticks:<10,}{Style.RESET_ALL}")


async def main() -> None:
    """Fő belépési pont a demo szkripthez.

    Ez a függvény inicializálja és futtatja a ResamplingDemo-t.
    """
    demo = ResamplingDemo()
    await demo.run()


if __name__ == "__main__":
    """Szkript belépési pont.

    Ez a blokk biztosítja, hogy a szkript csak akkor fusson,
    ha közvetlenül hívják (nem importálják).
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠️  A szkriptet a felhasználó megszakította.{Style.RESET_ALL}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n{Fore.RED}❌ Váratlan hiba: {str(e)}{Style.RESET_ALL}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)