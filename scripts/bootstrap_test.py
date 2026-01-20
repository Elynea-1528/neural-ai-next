#!/usr/bin/env python3
"""Bootstrap Teszt Script.

Ez a script egyszerűen futtatja a bootstrap_core() függvényt és kiírja az eredményt,
hogy ellenőrizzük, működik-e a bootstrap folyamat.
"""

from neural_ai.core import bootstrap_core


def main() -> None:
    """Fő függvény."""
    try:
        print("🧠 NEURAL AI NEXT - BOOTSTRAP TESZT")
        print("=" * 50)

        print("⏳ Bootstrap inicializálása...")
        core = bootstrap_core()

        print("✅ Bootstrap sikeres!")
        print(f"Core komponensek: {core}")

        # Komponensek ellenőrzése
        if core.logger:
            core.logger.info("Bootstrap teszt sikeres")
            print("✅ Logger elérhető")
        else:
            print("⚠️ Logger nem elérhető")

        if core.config:
            print("✅ Config elérhető")
        else:
            print("⚠️ Config nem elérhető")

        if core.event_bus:
            print("✅ EventBus elérhető")
        else:
            print("⚠️ EventBus nem elérhető")

        if core.database:
            print("✅ Database elérhető")
        else:
            print("⚠️ Database nem elérhető")

        if core.storage:
            print("✅ Storage elérhető")
        else:
            print("⚠️ Storage nem elérhető")

        print("🎉 Bootstrap teszt befejezve sikerrel!")

    except Exception as e:
        print(f"❌ Hiba a bootstrap során: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()