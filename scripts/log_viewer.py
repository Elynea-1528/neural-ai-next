#!/usr/bin/env python3
"""Log Viewer - Valós idejű log megjelenítő."""

import argparse
import os
import sys
import time
from datetime import datetime


class LogViewer:
    """Log megjelenítő osztály."""

    def __init__(self, log_file: str = None):
        # Alapértelmezett log fájlok
        if log_file is None:
            # Próbáljuk meg a kollektor logját
            possible_logs = [
                "data/logs/collector.log",
                "collector.log",
                "logs/collector.log",
                "/var/log/collector.log",
            ]

            for log in possible_logs:
                if os.path.exists(log):
                    log_file = log
                    break

        self.log_file = log_file
        self.last_position = 0

        if not log_file or not os.path.exists(log_file):
            print(f"❌ Log fájl nem található: {log_file}")
            print("Lehetséges log fájlok:")
            for log in possible_logs:
                print(f"  - {log}")
            sys.exit(1)

    def clear_screen(self):
        """Képernyő törlése."""
        os.system("cls" if os.name == "nt" else "clear")

    def print_header(self):
        """Fejléc kiírása."""
        print("=" * 80)
        print("NEURAL AI NEXT - LOG VIEWER")
        print("=" * 80)
        print(f"Log file: {self.log_file}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print()

    def tail_log(self, lines: int = 50):
        """Log fájl utolsó N sorának olvasása."""
        try:
            with open(self.log_file, encoding="utf-8", errors="ignore") as f:
                # Ugrás a fájl végére
                f.seek(0, 2)
                file_size = f.tell()

                # Visszafelé olvasás
                position = file_size
                line_count = 0
                lines_buffer = []

                while position > 0 and line_count < lines:
                    # Menjünk vissza 1024 byte-onként
                    position = max(0, position - 1024)
                    f.seek(position)

                    # Olvassuk ki a sorokat
                    chunk = f.read(file_size - position)
                    chunk_lines = chunk.split("\n")

                    # Adjuk hozzá a bufferhez
                    lines_buffer = chunk_lines + lines_buffer

                    # Számoljuk a sorokat
                    line_count = len(lines_buffer)

                # Utolsó N sor kiírása
                for line in lines_buffer[-lines:]:
                    print(line)

        except Exception as e:
            print(f"❌ Hiba a log olvasásakor: {e}")

    def follow_log(self):
        """Log fájl követése valós időben."""
        try:
            with open(self.log_file, encoding="utf-8", errors="ignore") as f:
                # Ugrás a fájl végére
                f.seek(0, 2)

                while True:
                    # Olvassuk az új sorokat
                    new_lines = f.read()

                    if new_lines:
                        print(new_lines, end="")

                    # Várjunk egy kicsit
                    time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n\n⏹️  Log követés leállítva")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Hiba a log követésekor: {e}")
            sys.exit(1)

    def run(self, follow: bool = False, lines: int = 50):
        """Log viewer futtatása."""
        if follow:
            # Valós idejű követés
            self.clear_screen()
            self.print_header()
            print("🎯 Valós idejű log követés (Ctrl+C a kilépéshez)")
            print("=" * 80)
            print()
            self.follow_log()
        else:
            # Utolsó N sor kiírása
            self.clear_screen()
            self.print_header()
            print(f"📄 Utolsó {lines} sor:")
            print("=" * 80)
            print()
            self.tail_log(lines)
            print()
            print("=" * 80)
            print("Használat: python scripts/log_viewer.py --follow (valós idejű követés)")


def main():
    """Főprogram."""
    parser = argparse.ArgumentParser(description="Log Viewer - Valós idejű log megjelenítő")
    parser.add_argument("--follow", "-f", action="store_true", help="Valós idejű log követés")
    parser.add_argument(
        "--lines",
        "-n",
        type=int,
        default=50,
        help="Megjelenítendő sorok száma (alapértelmezett: 50)",
    )
    parser.add_argument("--log-file", "-l", type=str, help="Log fájl elérési útja")

    args = parser.parse_args()

    # Log viewer létrehozása
    viewer = LogViewer(log_file=args.log_file)

    # Futtatás
    viewer.run(follow=args.follow, lines=args.lines)


if __name__ == "__main__":
    main()
