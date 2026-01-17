#!/usr/bin/env python3
"""JForex Auto-Deploy Script.

Automatically builds the JForex bridge and deploys it to the JForex Strategies folder.
Provides an MT5-like seamless installation experience.

Author: Neural AI Team
Version: 1.0.0
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_jforex_folder() -> Path:
    """Megkeresi a JForex telepítési mappát.

    Returns:
        Path: A JForex Strategies mappa útvonala

    Raises:
        FileNotFoundError: Ha nem található JForex mappa
    """
    # Lehetséges JForex mappa helyek (JForex4 elsőbbséggel)
    possible_paths = [
        # JForex4 prioritásban előrébb
        Path.home() / "JForex4" / "Strategies",
        Path.home() / "Documents" / "JForex4" / "Strategies",
        Path.home() / "JForex4",
        Path.home() / "Documents" / "JForex4",
        # Régi JForex mappák (backward compatibility)
        Path.home() / "JForex" / "Strategies",
        Path.home() / "Documents" / "JForex" / "Strategies",
        Path.home() / "JForex",
        Path.home() / "Documents" / "JForex",
    ]

    for path in possible_paths:
        if path.exists():
            # Ha a Strategies mappa létezik, használjuk azt
            if path.name == "Strategies":
                return path
            # Ha a JForex mappa létezik, nézzük meg van-e Strategies almappa
            strategies_path = path / "Strategies"
            if strategies_path.exists():
                return strategies_path
            # Ha nincs Strategies almappa, használjuk a JForex mappát
            return path

    # Ha nem találtuk meg, kérjük be a felhasználótól
    print("❌ JForex mappa nem található az alábbi helyeken:")
    for path in possible_paths:
        print(f"   - {path}")

    user_input = input("\n📁 Kérem adja meg a JForex mappa teljes útvonalát: ").strip()
    if not user_input:
        raise FileNotFoundError("JForex mappa megadása kötelező!")

    jforex_path = Path(user_input)
    if not jforex_path.exists():
        raise FileNotFoundError(f"A megadott mappa nem létezik: {jforex_path}")

    return jforex_path


def run_gradle_build(bridge_path: Path) -> bool:
    """Lefuttatja a Gradle buildet a JForex bridge mappában.

    Args:
        bridge_path: A jforex-bridge mappa útvonala

    Returns:
        bool: True ha a build sikeres, False egyébként
    """
    print(f"\n🔨 Gradle build futtatása: {bridge_path}")

    try:
        # Belépés a bridge mappába
        original_cwd = os.getcwd()
        os.chdir(bridge_path)

        # Gradle build futtatása
        result = subprocess.run(
            ["gradle", "build"],
            capture_output=True,
            text=True,
            timeout=300  # 5 perc timeout
        )

        # Visszatérés az eredeti mappába
        os.chdir(original_cwd)

        if result.returncode == 0:
            print("✅ Gradle build sikeres!")
            return True
        else:
            print("❌ Gradle build hibával lefutott!")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Gradle build túllépte az időkorlátot!")
        return False
    except FileNotFoundError:
        print("❌ Gradle parancs nem található!")
        print("   Telepítse a Gradle-t vagy használja a Gradle Wrapper-t (./gradlew)")
        return False
    except Exception as e:
        print(f"❌ Váratlan hiba a Gradle build során: {e}")
        return False


def deploy_files(bridge_path: Path, jforex_path: Path) -> bool:
    """Bemásolja a szükséges fájlokat a JForex mappába.

    Args:
        bridge_path: A jforex-bridge mappa útvonala
        jforex_path: A JForex Strategies mappa útvonala

    Returns:
        bool: True ha a telepítés sikeres, False egyébként
    """
    print(f"\n🚀 Fájlok telepítése: {bridge_path} -> {jforex_path}")

    try:
        # 1. Java stratégia fájl másolása
        java_source = (
            bridge_path / "src" / "main" / "java" / "com" / "neuralai" /
            "bridge" / "NeuralBridgeStrategy.java"
        )
        if not java_source.exists():
            print(f"❌ Java forrásfájl nem található: {java_source}")
            return False

        # Másolás a JForex mappába
        destination_file = jforex_path / "NeuralBridgeStrategy.java"
        print(f"   📄 Java fájl másolása: {destination_file}")
        shutil.copy2(java_source, destination_file)

        # 2. JAR függőségek másolása
        libs_dir = bridge_path / "build" / "libs"
        if not libs_dir.exists():
            print(f"❌ Build/libs mappa nem található: {libs_dir}")
            return False

        # JForex mappában létrehozzuk a files vagy libs almappát
        jforex_libs = jforex_path / "files"
        jforex_libs.mkdir(exist_ok=True)

        # Összes JAR fájl másolása
        jar_files = list(libs_dir.glob("*.jar"))
        if not jar_files:
            print("⚠️  Nincs JAR fájl a build/libs mappában!")
            print("   Ellenőrizze, hogy a 'gradle build' sikeresen lefutott-e!")
            return False

        for jar_file in jar_files:
            if jar_file.name != "jforex-bridge.jar":  # Ne másoljuk a fő JAR-t, csak a függőségeket
                destination_jar = jforex_libs / jar_file.name
                print(f"   📦 JAR másolása: {destination_jar.name}")
                shutil.copy2(jar_file, destination_jar)

        print("✅ Összes fájl sikeresen telepítve!")
        return True

    except Exception as e:
        print(f"❌ Hiba a fájlok telepítése során: {e}")
        return False


def print_summary(jforex_path: Path):
    """Kiírja a telepítés utáni összefoglalót.

    Args:
        jforex_path: A JForex Strategies mappa útvonala
    """
    print("\n" + "="*60)
    print("🎉 JFOREX BRIDGE TELEPÍTÉS SIKERES!")
    print("="*60)
    print(f"\n📁 Telepítési mappa: {jforex_path}")
    print("\n📋 Telepített fájlok:")
    print(f"   ✓ {jforex_path / 'NeuralBridgeStrategy.java'}")

    libs_dir = jforex_path / "files"
    if libs_dir.exists():
        jar_files = list(libs_dir.glob("*.jar"))
        for jar_file in jar_files:
            print(f"   ✓ {jar_file}")

    print("\n🚀 Következő lépések:")
    print("   1. Indítsa el a JForex platformot")
    print("   2. Nyissa meg a Strategy Manager-t")
    print("   3. Importálja a NeuralBridgeStrategy.java fájlt")
    print("   4. Futtassa a stratégia egy demo számlán")
    print("\n⚠️  FIGYELEM: A stratégia csak demo módban futtatható!")
    print("="*60 + "\n")


def main():
    """Fő végrehajtási függvény."""
    print("\n" + "="*60)
    print("🧠 NEURAL AI - JFOREX BRIDGE AUTO-DEPLOY")
    print("="*60)

    try:
        # 1. JForex mappa keresése
        print("\n🔍 JForex mappa keresése...")
        jforex_path = find_jforex_folder()
        print(f"✅ JForex mappa megtalálva: {jforex_path}")

        # 2. Bridge mappa ellenőrzése
        bridge_path = Path(__file__).parent.parent / "external" / "jforex-bridge"
        if not bridge_path.exists():
            print(f"❌ Bridge mappa nem található: {bridge_path}")
            return 1

        print(f"✅ Bridge mappa megtalálva: {bridge_path}")

        # 3. Gradle build futtatása
        if not run_gradle_build(bridge_path):
            print("❌ A telepítés megszakadt a build hiba miatt!")
            return 1

        # 4. Fájlok telepítése
        if not deploy_files(bridge_path, jforex_path):
            print("❌ A telepítés megszakadt a fájlok másolása során!")
            return 1

        # 5. Összefoglaló kiírása
        print_summary(jforex_path)

        return 0

    except FileNotFoundError as e:
        print(f"\n❌ Hiba: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Telepítés megszakítva a felhasználó által!")
        return 1
    except Exception as e:
        print(f"\n❌ Váratlan hiba: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
