"""Logger használati példák.

Ez a modul bemutatja a különböző logger implementációk használatát.
"""

import os
import time
from pathlib import Path

from neural_ai.core.logger.implementations.colored_logger import ColoredLogger
from neural_ai.core.logger.implementations.default_logger import DefaultLogger
from neural_ai.core.logger.implementations.rotating_file_logger import RotatingFileLogger


def main() -> None:
    """Logger példák futtatása."""
    # Default logger példa
    print("\n=== Default Logger ===")
    default_logger = DefaultLogger("example.default")
    default_logger.info("Ez egy egyszerű info üzenet")
    default_logger.warning("Ez egy figyelmeztetés")
    default_logger.error("Ez egy hibaüzenet")

    # Színes logger példa
    print("\n=== Colored Logger ===")
    color_logger = ColoredLogger("example.color")
    color_logger.debug("Debug üzenet kék színnel")
    color_logger.info("Info üzenet zöld színnel")
    color_logger.warning("Figyelmeztetés sárga színnel")
    color_logger.error("Hibaüzenet piros színnel")
    color_logger.critical("Kritikus hiba fehér szöveggel piros háttéren")

    # Rotáló fájl logger példa
    print("\n=== Rotating File Logger ===")
    log_dir = Path("example_logs")
    log_dir.mkdir(exist_ok=True)

    # Méret alapú rotáció példa
    size_logger = RotatingFileLogger(
        name="example.size_rotation",
        filename=str(log_dir / "size_rotation.log"),
        max_bytes=1024,  # 1KB
        backup_count=3
    )
    print("Méret alapú rotáció teszt...")
    for i in range(50):
        size_logger.info(f"Ez egy nagyobb üzenet a méret alapú rotáció teszteléséhez: {i}")

    # Idő alapú rotáció példa
    time_logger = RotatingFileLogger(
        name="example.time_rotation",
        filename=str(log_dir / "time_rotation.log"),
        rotation_type="time",
        when="S",  # Másodpercenkénti rotáció a demonstrációhoz
        backup_count=3
    )
    print("Idő alapú rotáció teszt...")
    for i in range(3):
        time_logger.info(f"Üzenet a(z) {i + 1}. másodpercben")
        time.sleep(1.1)

    # Tömörítés példa
    print("Log fájlok tömörítése...")
    RotatingFileLogger.compress_old_logs(str(log_dir))

    # Log fájlok listázása
    print("\nLétrehozott log fájlok:")
    for file in sorted(os.listdir(log_dir)):
        print(f"  - {file}")


if __name__ == "__main__":
    main()
