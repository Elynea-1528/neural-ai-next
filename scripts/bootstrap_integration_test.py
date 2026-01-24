#!/usr/bin/env python3
"""Bootstrap integrációs teszt szkript.

Ez a szkript végrehajtja a neural_ai.core.bootstrap_core() függvényt,
és ellenőrzi a rendszer komponenseinek helyes inicializálását.
"""

import sys
import traceback
from pathlib import Path

# Projekt gyökér hozzáadása a path-hoz
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def main() -> int:
    """Fő teszt függvény.

    Returns:
        0 ha sikeres, 1 ha hiba történt
    """
    try:
        print("🚀 Bootstrap Integrációs Teszt Indítása...")
        print("==========================================")

        # Bootstrap core import és futtatás
        from neural_ai.core import bootstrap_core

        print("⏳ bootstrap_core() hívása...")
        core = bootstrap_core()

        print("✅ Bootstrap sikeres!")
        print("==========================================")

        # Komponens validáció
        print("📋 Komponens validáció:")

        # Logger ellenőrzés
        if core.logger:
            print("✅ Logger: Inicializálva")
        else:
            print("❌ Logger: Hiányzik")
            return 1

        # Config ellenőrzés
        if core.config:
            print("✅ ConfigManager: Inicializálva")
        else:
            print("❌ ConfigManager: Hiányzik")
            return 1

        # Hardware ellenőrzés
        if core.hardware:
            print("✅ HardwareInfo: Inicializálva")
        else:
            print("❌ HardwareInfo: Hiányzik")
            return 1

        # Database ellenőrzés
        if core.database:
            print("✅ DatabaseManager: Inicializálva")
        else:
            print("❌ DatabaseManager: Hiányzik")
            return 1

        # EventBus ellenőrzés
        if core.event_bus:
            print("✅ EventBus: Inicializálva")
        else:
            print("❌ EventBus: Hiányzik")
            return 1

        # Storage ellenőrzés
        if core.storage:
            print("✅ Storage: Inicializálva")
        else:
            print("❌ Storage: Hiányzik")
            return 1

        # System health monitor ellenőrzés
        if core.health_monitor:
            print("✅ HealthMonitor: Inicializálva")
        else:
            print("❌ HealthMonitor: Hiányzik")
            return 1

        # MarketDataPersister ellenőrzés
        if core.persister:
            print("✅ MarketDataPersister: Inicializálva")
        else:
            print("❌ MarketDataPersister: Hiányzik")
            return 1

        print("==========================================")
        print("✅ INTEGRÁCIÓS TESZT SIKERES!")
        print("Minden komponens helyesen inicializálva.")
        return 0

    except Exception as e:
        print("==========================================")
        print("❌ INTEGRÁCIÓS TESZT SIKERTELEN!")
        print(f"Hiba: {e}")
        print("Stack trace:")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
