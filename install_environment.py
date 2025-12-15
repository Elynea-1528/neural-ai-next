#!/usr/bin/env python3
"""
Neural AI Next - Automatikus környezet telepítő script

Ez a script automatikusan beállítja a fejlesztői környezetet:
- Conda környezet létrehozása
- Függőségek telepítése
- PyTorch CUDA támogatással
- Pre-commit konfiguráció
- Telepítés ellenőrzése
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Tuple


def run_command(
    command: str, check: bool = True, capture_output: bool = False
) -> subprocess.CompletedProcess:
    """Futtat egy shell parancsot."""
    print(f"$ {command}")
    try:
        result = subprocess.run(
            command, shell=True, check=check, capture_output=capture_output, text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"✗ Hiba a parancs futtatásakor: {e}")
        if capture_output and e.stderr:
            print(f"Stderr: {e.stderr}")
        raise


def check_conda() -> bool:
    """Ellenőrzi, hogy conda telepítve van-e."""
    try:
        result = run_command("conda --version", check=False, capture_output=True)
        if result.returncode == 0:
            print(f"✓ Conda telepítve: {result.stdout.strip()}")
            return True
        else:
            print("✗ Conda nincs telepítve")
            return False
    except Exception as e:
        print(f"✗ Conda ellenőrzés sikertelen: {e}")
        return False


def check_nvidia_driver() -> bool:
    """Ellenőrzi az NVIDIA driver telepítését."""
    try:
        result = run_command("nvidia-smi", check=False, capture_output=True)
        if result.returncode == 0:
            print("✓ NVIDIA driver telepítve")
            # Kinyerjük a CUDA verziót
            for line in result.stdout.split("\n"):
                if "CUDA Version" in line:
                    cuda_version = line.split("CUDA Version:")[1].strip().split()[0]
                    print(f"✓ CUDA Version: {cuda_version}")
                    break
            return True
        else:
            print("✗ NVIDIA driver nincs telepítve")
            return False
    except Exception as e:
        print(f"✗ NVIDIA driver ellenőrzés sikertelen: {e}")
        return False


def check_environment_exists() -> bool:
    """Ellenőrzi, hogy a környezet már létezik-e."""
    try:
        result = run_command("conda env list", capture_output=True)
        return "neural-ai-next" in result.stdout
    except Exception:
        return False


def remove_existing_environment():
    """Törli a meglévő környezetet."""
    print("\n🗑️  Meglévő környezet törlése...")
    run_command("conda env remove -n neural-ai-next -y", check=False)


def create_environment():
    """Létrehozza a conda környezetet."""
    print("\n🏗️  Környezet létrehozása...")

    # Ellenőrizzük, hogy létezik-e az environment.yml
    env_file = Path("environment.yml")
    if not env_file.exists():
        print("✗ environment.yml fájl nem található!")
        sys.exit(1)

    # Környezet létrehozása (3 próbálkozás)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Környezet létrehozása (próbálkozás {attempt + 1}/{max_retries})...")
            # Progress bar letiltása a "more hidden" üzenet elkerüléséhez
            run_command("conda env create -f environment.yml")
            print("✓ Környezet létrehozva")
            break
        except subprocess.CalledProcessError as e:
            if attempt < max_retries - 1:
                print(f"✗ Sikertelen, újrapróbálkozás {attempt + 1}/{max_retries}")
                import time

                time.sleep(5)
            else:
                print("✗ Környezet létrehozása sikertelen az összes próbálkozás után")
                print("\nAlternatív megoldás: próbáld manuálisan:")
                print("  conda create -n neural-ai-next python=3.12 -y")
                print("  conda activate neural-ai-next")
                print("  conda install -c conda-forge pytorch=2.5.1 lightning=2.5.5 -y")
                print("  pip install vectorbt jupyterlab pytest black flake8 mypy pre-commit")
                raise


def install_pytorch():
    """Telepíti a PyTorch-ot CUDA támogatással."""
    print("\n🔥 PyTorch telepítése CUDA 12.1 támogatással...")

    # PyTorch már telepítve van conda-val, csak ellenőrizzük
    print("\n🔍 PyTorch verzió ellenőrzése...")
    run_command("python -c \"import torch; print(f'PyTorch verzió: {torch.__version__}')\"")
    print("✓ PyTorch telepítve (conda)")


def setup_precommit():
    """Beállítja a pre-commit hookokat."""
    print("\n🔧 Pre-commit beállítása...")

    # Pre-commit telepítése
    run_command("pre-commit install")
    print("✓ Pre-commit telepítve")


def verify_installation():
    """Ellenőrzi a telepítést."""
    print("\n🔍 Telepítés ellenőrzése...")

    # Ellenőrző script futtatása
    check_script = Path("scripts/check_installation.py")
    if check_script.exists():
        run_command("python scripts/check_installation.py")
    else:
        # Alapvető ellenőrzés
        checks = [
            ("Python", "python --version"),
            ("PyTorch", "python -c \"import torch; print(f'PyTorch: {torch.__version__}')\""),
            (
                "CUDA",
                "python -c \"import torch; print(f'CUDA available: {torch.cuda.is_available()}')\"",
            ),
            (
                "Lightning",
                "python -c \"import lightning; print(f'Lightning: {lightning.__version__}')\"",
            ),
        ]

        for name, command in checks:
            try:
                run_command(command)
                print(f"✓ {name} OK")
            except Exception as e:
                print(f"✗ {name} ellenőrzés sikertelen: {e}")


def print_next_steps():
    """Kiírja a következő lépéseket."""
    print("\n" + "=" * 60)
    print("🎉 Telepítés sikeres!")
    print("=" * 60)
    print("\nKövetkező lépések:")
    print("1. Környezet aktiválása:")
    print("   conda activate neural-ai-next")
    print("\n2. JupyterLab indítása:")
    print("   jupyter lab")
    print("\n3. Tesztek futtatása:")
    print("   pytest")
    print("\n4. Fejlesztés megkezdése:")
    print("   code .")
    print("\n" + "=" * 60)


def main():
    """Fő telepítési funkció."""
    print("=" * 60)
    print("Neural AI Next - Automatikus Telepítő")
    print("=" * 60)

    # Ellenőrzések
    print("\n🔍 Előzetes ellenőrzések...")

    if not check_conda():
        print("\n✗ Conda nincs telepítve!")
        print("Kérlek telepítsd a Miniconda-t:")
        print("wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh")
        print("bash Miniconda3-latest-Linux-x86_64.sh")
        sys.exit(1)

    if not check_nvidia_driver():
        print("\n⚠️  NVIDIA driver nem található")
        print("A GPU gyorsítás nem lesz elérhető")
        response = input("Folytatod a telepítést? (y/n): ")
        if response.lower() != "y":
            sys.exit(1)

    # Környezet ellenőrzése
    if check_environment_exists():
        print("\n⚠️  A neural-ai-next környezet már létezik")
        response = input("Szeretnéd törölni és újra létrehozni? (y/n): ")
        if response.lower() == "y":
            remove_existing_environment()
        else:
            print("Telepítés megszakítva")
            sys.exit(0)

    # Telepítés
    try:
        create_environment()
        install_pytorch()
        setup_precommit()
        verify_installation()
        print_next_steps()

    except Exception as e:
        print(f"\n✗ Telepítés sikertelen: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
