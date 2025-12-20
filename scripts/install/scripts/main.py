#!/usr/bin/env python3
"""Neural AI Next - Egységesített Telepítő

Ez a script interaktív módon telepíti a fejlesztői környezetet,
kihasználva az environment.yml-t és a pyproject.toml-t.
"""

import argparse
import subprocess
import sys
import time
from enum import Enum
from pathlib import Path
from typing import Any

# Globális verbose flag
verbose_mode = False


class InstallMode(Enum):
    """Telepítési módok."""

    MINIMAL = "minimal"
    DEV = "dev"
    DEV_TRADER = "dev+trader"
    FULL = "full"
    CHECK_ONLY = "check"
    TRADER_ONLY = "trader"
    JUPYTER_ONLY = "jupyter"


class PyTorchMode(Enum):
    """PyTorch telepítési módok."""

    CPU = "cpu"
    CUDA_12_1 = "cuda12.1"


class Colors:
    """Színes kimenetek."""

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


def print_error(message: str):
    """Hibaüzenet kiírása."""
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")


def print_success(message: str):
    """Sikerüzenet kiírása."""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")


def print_warning(message: str):
    """Figyelmeztető üzenet kiírása."""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")


def print_info(message: str):
    """Információs üzenet kiírása."""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.RESET}")


def run_command(command: str, check: bool = True, shell: bool = True) -> bool:
    """Futtat egy shell parancsot.

    Args:
        command: A végrehajtandó parancs
        check: Ha True, kivételt dob hibakód esetén
        shell: Ha True, shell-en keresztül hajtja végre

    Returns:
        True ha sikeres, False ha sikertelen
    """
    global verbose_mode
    print(f"$ {command}")
    try:
        if verbose_mode:
            # Valós idejű kimenet - stdout és stderr egyből a konzolra
            process = subprocess.Popen(
                command,
                shell=shell,
                stdout=None,  # Közvetlenül a konzolra
                stderr=None,  # Közvetlenül a konzolra
            )

            # Várjuk meg a folyamat végét
            process.wait()
            return process.returncode == 0
        else:
            # Csak a parancs és az eredmény
            result = subprocess.run(
                command,
                shell=shell,
                check=check,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print_error(f"Parancs sikertelen (exit code: {e.returncode})")
        if verbose_mode and hasattr(e, "stdout") and e.stdout:
            print_error("Részletes hiba:")
            for line in e.stdout.splitlines():
                print_error(f"  {line}")
        elif e.stderr:
            print_error(f"Hiba: {e.stderr}")
        return False
    except Exception as e:
        print_error(f"Váratlan hiba: {e}")
        return False


def check_conda() -> bool:
    """Ellenőrzi, hogy conda telepítve van-e.

    Returns:
        True ha conda telepítve van, False egyébként
    """
    if not run_command("conda --version", check=False):
        print_error("Conda nincs telepítve!")
        print_info("Telepítsd a Miniconda-t:")
        print_info("  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh")
        print_info("  bash Miniconda3-latest-Linux-x86_64.sh")
        print_info("\nUtána inicializáld:")
        print_info("  conda init bash  # vagy conda init zsh")
        print_info("  source ~/.bashrc")
        return False
    print_success("Conda telepítve van")
    return True


def check_conda_initialized() -> bool:
    """Ellenőrzi, hogy conda inicializálva van-e.

    Returns:
        True ha conda inicializálva van, False egyébként
    """
    # Ellenőrizzük a .bashrc-ban
    bashrc = Path.home() / ".bashrc"
    if bashrc.exists():
        with open(bashrc) as f:
            content = f.read()
            if "conda initialize" in content:
                print_success("Conda inicializálva van")
                return True

    print_warning("Conda nincs inicializálva!")
    print_info("Futtasd: conda init bash  # vagy conda init zsh")
    print_info("Utána: source ~/.bashrc")
    return False


def check_environment() -> bool:
    """Ellenőrzi, hogy a környezet létezik-e.

    Returns:
        True ha a környezet létezik, False egyébként
    """
    try:
        result = subprocess.run("conda env list", shell=True, capture_output=True, text=True)
        return "neural-ai-next" in result.stdout
    except:
        return False


def update_environment_yml(pytorch_mode: PyTorchMode) -> str:
    """Frissíti a projekt environment.yml fájlját a kiválasztott PyTorch mód szerint.

    A függvény mindig legenerálja a dinamikus environment.yml tartalmat
    a kiválasztott PyTorch konfigurációnak megfelelően, és felülírja
    a projekt gyökerében lévő environment.yml fájlt.

    Args:
        pytorch_mode: A PyTorch telepítési mód (CPU vagy CUDA 12.1)

    Returns:
        Az environment.yml fájl elérési útja
    """
    # Projektben lévő environment.yml elérési útja
    project_env_path = Path(__file__).parent.parent.parent.parent / "environment.yml"

    print_info(f"Environment.yml frissítése a következő mód szerint: {pytorch_mode.value}")

    # Dinamikus environment.yml tartalom generálása
    env_content = """name: neural-ai-next
channels:
  - pytorch
  - nvidia
  - conda-forge
  - defaults
dependencies:
  # === CRITIKUS CONDÁS CSOMAGOK ===
  - python=3.12.*
  - pytorch=2.5.1
  - torchvision=0.20.1
  - torchaudio=2.5.1
"""

    # PyTorch konfiguráció a kiválasztott mód szerint
    if pytorch_mode == PyTorchMode.CPU:
        env_content += "  - cpuonly\n"
    else:
        pytorch_mode = PyTorchMode.CUDA_12_1
        env_content += "  - pytorch-cuda=12.1\n"

    # További conda csomagok
    env_content += """  - lightning=2.5.5
  - numpy>=1.24.3,<3.0
  - pandas>=2.0.3,<3.0
  - scikit-learn>=1.3.0
  
  # === PIP CSOMAGOK (PYPROJECT.TOML-BÓL) ===
  - pip:
      - -e .
"""

    # Fájl létrehozása/felülírása a projektben
    with open(project_env_path, "w") as f:
        f.write(env_content)

    print_info(f"Environment.yml sikeresen frissítve: {project_env_path}")
    return str(project_env_path)


def install_environment(config: dict[str, Any]) -> bool:
    """Telepíti a környezetet a megadott konfiguráció szerint.

    Args:
        config: Telepítési konfiguráció

    Returns:
        True ha sikeres, False ha sikertelen
    """
    install_mode: InstallMode = config["install_mode"]
    pytorch_mode: PyTorchMode = config["pytorch_mode"]

    print_info("=" * 60)
    print_info("Telepítés megkezdése...")
    print_info("=" * 60)

    # 1. Conda ellenőrzés
    if not check_conda():
        return False

    if not check_conda_initialized():
        print_warning("Folytatás előtt inicializáld a conda-t!")
        response = input("Szeretnéd, hogy megpróbáljam inicializálni? [y/N]: ").strip().lower()
        if response == "y":
            run_command("conda init bash", check=False)
            print_warning("Indítsd újra a terminált, majd futtasd újra a scriptet!")
            return False
        else:
            return False

    # 2. Környezet ellenőrzése
    if check_environment():
        print_warning("A neural-ai-next környezet már létezik")
        response = input("Szeretnéd törölni és újra létrehozni? [y/N]: ").strip().lower()
        if response == "y":
            print_info("Környezet törlése...")

            # Először deaktiváljuk a környezetet, ha az aktív
            print_info("Környezet deaktiválása...")
            run_command("conda deactivate", check=False)

            # Várunk egy kicsit, hogy a deaktiválás befejeződjön
            time.sleep(2)

            if not run_command("conda env remove -n neural-ai-next -y", check=False):
                print_error("Környezet törlése sikertelen!")
                print_info(
                    "Próbáld manuálisan: conda deactivate && conda env remove -n neural-ai-next -y"
                )
                return False
            print_success("Környezet törölve")
        else:
            print_info("Meglévő környezet használata...")
            # CHECK_ONLY módban ne térjünk vissza itt, hanem folytassuk az ellenőrzéssel
            if install_mode != InstallMode.CHECK_ONLY:
                return True

    # 3. Environment.yml használata (csak ha nem CHECK_ONLY mód)
    if install_mode != InstallMode.CHECK_ONLY:
        print_info("Környezet létrehozása environment.yml-ből...")
        env_file = update_environment_yml(pytorch_mode)

        if not run_command(f"conda env create -f {env_file}"):
            print_error("Környezet létrehozása sikertelen!")
            return False

        print_success("Környezet létrehozva")
        run_command("conda activate neural-ai-next")

        # 4. Opcionális függőségek telepítése
        print_info("Opcionális függőségek telepítése...")

        if install_mode == InstallMode.MINIMAL:
            print_info("Minimal mód - csak alap függőségek")
        elif install_mode == InstallMode.DEV:
            print_info("Dev mód - fejlesztői eszközök telepítése...")
            if not run_command("conda run -n neural-ai-next pip install -e .[dev]"):
                print_error("Dev függőségek telepítése sikertelen!")
                return False
            print_success("Dev függőségek telepítve")
        elif install_mode == InstallMode.DEV_TRADER:
            print_info("Dev+Trader mód - fejlesztői + trader eszközök...")
            if not run_command("conda run -n neural-ai-next pip install -e .[dev,trader]"):
                print_error("Dev+Trader függőségek telepítése sikertelen!")
                return False
            print_success("Dev+Trader függőségek telepítve")

            print_info("Broker telepítő indítása...")
            run_command("bash scripts/install/scripts/setup_brokers.sh")
        elif install_mode == InstallMode.FULL:
            print_info("Full mód - minden függőség telepítése...")
            if not run_command("conda run -n neural-ai-next pip install -e .[full]"):
                print_error("Full függőségek telepítése sikertelen!")
                return False
            print_success("Full függőségek telepítve")

            print_info("Broker telepítő indítása...")
            run_command("bash scripts/install/scripts/setup_brokers.sh")
        elif install_mode == InstallMode.TRADER_ONLY:
            print_info("Csak Trader Engine telepítése...")
            if not run_command("conda run -n neural-ai-next pip install -e .[trader]"):
                print_error("Trader függőségek telepítése sikertelen!")
                return False
            print_success("Trader függőségek telepítve")

            print_info("Broker telepítő indítása...")
            run_command("bash scripts/install/scripts/setup_brokers.sh")
        elif install_mode == InstallMode.JUPYTER_ONLY:
            print_info("Csak Jupyter környezet telepítése...")
            if not run_command("conda run -n neural-ai-next pip install -e .[jupyter]"):
                print_error("Jupyter függőségek telepítése sikertelen!")
                return False
            print_success("Jupyter függőségek telepítve")

        # 5. Pre-commit beállítás
        if install_mode in [InstallMode.DEV, InstallMode.DEV_TRADER, InstallMode.FULL]:
            print_info("Pre-commit beállítása...")
            run_command("conda run -n neural-ai-next pre-commit install")
            print_success("Pre-commit beállítva")

        # 6. Ellenőrzés
        if install_mode not in [InstallMode.MINIMAL]:
            print_info("Telepítés ellenőrzése...")
            run_command(
                "conda run -n neural-ai-next python scripts/install/scripts/check_installation.py"
            )
    else:
        # CHECK_ONLY mód: csak ellenőrzés, nincs telepítés
        print_info("Csak ellenőrzés mód")
        print_info("Telepítés ellenőrzése...")
        if not run_command(
            "conda run -n neural-ai-next python scripts/install/scripts/check_installation.py"
        ):
            print_error("Az ellenőrzés során hibák merültek fel!")
            return False
        print_success("Az ellenőrzés sikeresen lefutott")
        return True

    return True


def interactive_setup() -> dict[str, Any] | None:
    """Interaktív telepítési menü.

    Returns:
        Telepítési konfiguráció, vagy None ha a felhasználó megszakítja
    """
    print("=" * 60)
    print("Neural AI Next - Egységesített Telepítő")
    print("=" * 60)

    # 1. Telepítési mód választás
    print("\n1. Telepítési mód:")
    print("   [1] Minimal (csak alapok)")
    print("   [2] Fejlesztői környezet")
    print("   [3] Fejlesztői + Trader Engine")
    print("   [4] Teljes telepítés")
    print("   [5] Csak Trader Engine")
    print("   [6] Csak Jupyter környezet")
    print("   [7] Csak ellenőrzés")

    mode_choice = input("Válassz opciót [1-7] (alapértelmezett: 2): ").strip()
    mode_map = {
        "1": InstallMode.MINIMAL,
        "2": InstallMode.DEV,
        "3": InstallMode.DEV_TRADER,
        "4": InstallMode.FULL,
        "5": InstallMode.TRADER_ONLY,
        "6": InstallMode.JUPYTER_ONLY,
        "7": InstallMode.CHECK_ONLY,
    }
    install_mode = mode_map.get(mode_choice, InstallMode.DEV)

    # 2. PyTorch mód
    print("\n2. PyTorch konfiguráció:")
    print("   [1] CUDA 12.1 (ajánlott GTX 1050 Ti-hez)")
    print("   [2] CPU only (laptopokhoz)")

    pytorch_choice = input("Válassz opciót [1-2] (alapértelmezett: 1): ").strip()
    pytorch_map = {"1": PyTorchMode.CUDA_12_1, "2": PyTorchMode.CPU}
    pytorch_mode = pytorch_map.get(pytorch_choice, PyTorchMode.CUDA_12_1)

    # 3. Megerősítés
    print("\n" + "=" * 60)
    print("Telepítési beállítások:")
    print(f"  - Mód: {install_mode.value}")
    print(f"  - PyTorch: {pytorch_mode.value}")
    print("=" * 60)

    confirm = input("\nFolytatod a telepítést? [y/N]: ").strip().lower()
    if confirm != "y":
        print_info("Telepítés megszakítva.")
        return None

    return {"install_mode": install_mode, "pytorch_mode": pytorch_mode}


def main():
    """Fő belépési pont."""
    parser = argparse.ArgumentParser(description="Neural AI Next egységesített telepítő")
    parser.add_argument("--interactive", action="store_true", help="Interaktív mód")
    parser.add_argument(
        "--mode",
        choices=["minimal", "dev", "dev+trader", "full", "trader", "jupyter", "check"],
        help="Telepítési mód: minimal, dev, dev+trader, full, trader, jupyter, check",
    )
    parser.add_argument(
        "--pytorch",
        choices=["cpu", "cuda12.1"],
        help="PyTorch konfiguráció: cpu vagy cuda12.1",
    )
    parser.add_argument(
        "--verbose",
        "-vvv",
        action="store_true",
        help="Részletes kimenet (melyik package-nél tart)",
    )

    args = parser.parse_args()

    # Globális verbose flag
    global verbose_mode
    verbose_mode = args.verbose

    # Konfiguráció létrehozása
    config: dict[str, Any] | None = None

    if args.interactive or (args.mode is None and args.pytorch is None):
        # Interaktív mód
        config = interactive_setup()
        if config is None:
            return
    else:
        # Parancssori mód
        config = {
            "install_mode": InstallMode(args.mode or "dev"),
            "pytorch_mode": PyTorchMode(args.pytorch or "cuda12.1"),
        }

    # Telepítés végrehajtása
    success = install_environment(config)

    # Eredmény kiírása
    if success:
        print_success("=" * 60)
        print_success("✓ Telepítés sikeres!")
        print_success("=" * 60)
        print_info("\nKövetkező lépések:")
        print_info("1. Környezet aktiválása:")
        print_info("   conda activate neural-ai-next")
        print_info("\n2. Fejlesztés megkezdése:")
        print_info("   code .")

        # Extra információk a telepítési mód alapján
        if config and config["install_mode"] in [
            InstallMode.DEV,
            InstallMode.DEV_TRADER,
            InstallMode.FULL,
        ]:
            print_info("\n3. JupyterLab indítása (ha Full mód):")
            if config["install_mode"] == InstallMode.FULL:
                print_info("   jupyter lab")
    else:
        print_error("\n✗ Telepítés sikertelen!")
        print_info("Nézd meg a hibaüzeneteket, és próbáld újra.")
        print_info("Ha conda probléma van, futtasd: conda init bash && source ~/.bashrc")
        sys.exit(1)


if __name__ == "__main__":
    main()
