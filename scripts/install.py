#!/usr/bin/env python3
"""Neural AI Next - Unified Zero-Touch Installer
=============================================

Automatizált telepítő a teljes környezet és brókerek beállításához.
Hardver detektálás, GPU ellenőrzés, AVX2 támogatás és automatikus bróker telepítés.

Használat:
    python scripts/install.py

Követelmények:
    - Conda/Miniconda telepítve kell legyen
    - Internet kapcsolat
    - Sudo jogosultság (csak Wine telepítéséhez)
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# ============================================================================
# KONFIGURÁCIÓ
# ============================================================================

CONDA_ENV_NAME = "neural-ai-next"
PYTHON_VERSION = "3.12"
PROJECT_ROOT = Path(__file__).parent.parent

# Bróker letöltési URL-ek
BROKER_URLS = {
    "jforex4": "https://dukascopy-eu.cdn.online-trading-solutions.com/installer4/dukascopy-eu/JForex4_unix_64_JRE_bundled.sh",
    "tws": "https://download2.interactivebrokers.com/installers/tws/latest/tws-latest-linux-x64.sh",
    "mt5_dukascopy": "https://download.mql5.com/cdn/web/dukascopy.bank.sa/mt5/dukascopy5setup.exe",
}


# Színek a konzolhoz
class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color


# ============================================================================
# SEGÉDFÜGGVÉNYEK
# ============================================================================


def print_banner() -> None:
    """Kiírja a telepítő bannerét."""
    print(f"{Colors.BLUE}{'=' * 60}")
    print("Neural AI Next - Unified Zero-Touch Installer")
    print(f"{'=' * 60}{Colors.NC}")
    print()


def print_success(message: str) -> None:
    """Zöld színnel kiírja a sikeres üzenetet."""
    print(f"{Colors.GREEN}✓ {message}{Colors.NC}")


def print_error(message: str) -> None:
    """Piros színnel kiírja a hibát."""
    print(f"{Colors.RED}✗ {message}{Colors.NC}")


def print_warning(message: str) -> None:
    """Sárga színnel kiírja a figyelmeztetést."""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.NC}")


def print_info(message: str) -> None:
    """Kék színnel kiírja az információt."""
    print(f"{Colors.BLUE}ℹ {message}{Colors.NC}")


def run_command(
    command: str, shell: bool = True, check: bool = True
) -> "subprocess.CompletedProcess[str]":
    """Lefuttat egy shell parancsot és visszaadja az eredményt.

    Args:
        command: A futtatandó parancs
        shell: Használjon-e shell-t
        check: Dobjon-e kivételt, ha a parancs sikertelen

    Returns:
        A lefuttatott parancs eredménye
    """
    return subprocess.run(command, shell=shell, check=check, capture_output=True, text=True)


def command_exists(command: str) -> bool:
    """Ellenőrzi, hogy egy parancs elérhető-e a rendszeren.

    Args:
        command: Az ellenőrizendő parancs

    Returns:
        True, ha a parancs elérhető
    """
    return shutil.which(command) is not None


# ============================================================================
# HARDVER DETEKTÁLÁS
# ============================================================================


def check_conda() -> bool:
    """Ellenőrzi, hogy Conda telepítve van-e.

    Returns:
        True, ha Conda elérhető
    """
    return command_exists("conda")


def check_nvidia_gpu() -> bool:
    """Ellenőrzi, hogy NVIDIA GPU van-e a rendszerben.

    Returns:
        True, ha NVIDIA GPU található
    """
    if not command_exists("nvidia-smi"):
        return False

    try:
        result = run_command("nvidia-smi --query-gpu=name --format=csv,noheader", check=False)
        return result.returncode == 0 and result.stdout.strip() != ""
    except Exception:
        return False


def check_avx2_support() -> bool:
    """Ellenőrzi, hogy a CPU támogatja-e az AVX2 utasításkészletet.

    Returns:
        True, ha AVX2 támogatott
    """
    try:
        with open("/proc/cpuinfo") as f:
            cpuinfo = f.read()
            return "avx2" in cpuinfo.lower()
    except Exception:
        return False


def check_wine() -> bool:
    """Ellenőrzi, hogy Wine telepítve van-e.

    Returns:
        True, ha Wine elérhető
    """
    return command_exists("wine")


def get_conda_path() -> str:
    """Visszaadja a Conda bináris elérési útját.

    Returns:
        A Conda bináris elérési útja
    """
    return "/home/elynea/miniconda3/bin/conda"


# ============================================================================
# KÖRNYEZET BEÁLLÍTÁSA
# ============================================================================


def create_conda_env() -> None:
    """Létrehozza a neural-ai-next Conda környezetet, ha még nem létezik."""
    print_info("Conda környezet ellenőrzése...")

    # Ellenőrizzük, hogy létezik-e a környezet
    try:
        result = run_command(f"{get_conda_path()} env list | grep {CONDA_ENV_NAME}", check=False)

        if CONDA_ENV_NAME in result.stdout:
            print_success(f"A(z) '{CONDA_ENV_NAME}' környezet már létezik")
            return
    except Exception:
        pass

    # Környezet létrehozása
    print_info(f"A(z) '{CONDA_ENV_NAME}' környezet létrehozása...")
    run_command(f"{get_conda_path()} create -n {CONDA_ENV_NAME} python={PYTHON_VERSION} -y")
    print_success(f"A(z) '{CONDA_ENV_NAME}' környezet létrejött")


def install_pytorch(gpu_available: bool) -> None:
    """Telepíti a PyTorch-ot GPU vagy CPU verzióban.

    Args:
        gpu_available: True, ha GPU elérhető
    """
    print_info("PyTorch telepítése...")

    if gpu_available:
        print_info("GPU verzió telepítése (CUDA 12.1)...")
        run_command(
            f"{get_conda_path()} run -n {CONDA_ENV_NAME} "
            "conda install pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 pytorch-cuda=12.1 -c pytorch -c nvidia"
        )
    else:
        print_info("CPU verzió telepítése...")
        run_command(
            f"{get_conda_path()} run -n {CONDA_ENV_NAME} "
            "conda install pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 cpuonly -c pytorch"
        )

    print_success("PyTorch telepítve")


def install_lightning() -> None:
    """Telepíti a PyTorch Lightning-ot."""
    print_info("PyTorch Lightning telepítése...")

    run_command(
        f"{get_conda_path()} run -n {CONDA_ENV_NAME} conda install lightning=2.5.5 -c conda-forge"
    )

    print_success("PyTorch Lightning telepítve")


def install_data_libraries(avx2_supported: bool) -> None:
    """Telepíti az adatkezelő könyvtárakat (Polars/PyArrow vagy fastparquet).

    Args:
        avx2_supported: True, ha AVX2 támogatott
    """
    print_info("Adatkezelő könyvtárak telepítése...")

    if avx2_supported:
        print_info("AVX2 támogatott: Polars + PyArrow telepítése...")
        run_command(f"{get_conda_path()} run -n {CONDA_ENV_NAME} pip install polars pyarrow")
    else:
        print_warning("AVX2 nem támogatott: fastparquet fallback telepítése...")
        run_command(f"{get_conda_path()} run -n {CONDA_ENV_NAME} pip install fastparquet")

    print_success("Adatkezelő könyvtárak telepítve")


def install_base_packages() -> None:
    """Telepíti az alap csomagokat (NumPy, Pandas, Scikit-learn)."""
    print_info("Alap csomagok telepítése...")

    run_command(
        f"{get_conda_path()} run -n {CONDA_ENV_NAME} conda install -y numpy pandas scikit-learn"
    )

    print_success("Alap csomagok telepítve")


def install_project_packages() -> None:
    """Telepíti a projekt csomagjait az összes opcionális függőséggel."""
    print_info("Projekt csomagok telepítése (dev + trader + jupyter)...")

    # A projekt telepítése fejlesztői és kereskedői csomagokkal
    run_command(f"{get_conda_path()} run -n {CONDA_ENV_NAME} pip install -e .[dev,trader,jupyter]")

    print_success("Projekt csomagok telepítve")


# ============================================================================
# BRÓKER TELEPÍTÉS
# ============================================================================


def create_downloads_dir() -> Path:
    """Létrehozza a downloads mappát, ha nem létezik.

    Returns:
        A downloads mappa Path objektuma
    """
    downloads_dir = PROJECT_ROOT / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    return downloads_dir


def download_file(url: str, output_path: Path) -> None:
    """Letölt egy fájlt a megadott URL-ről.

    Args:
        url: A letöltendő fájl URL-je
        output_path: A cél fájl elérési útja
    """
    print_info(f"Letöltés: {url}")

    try:
        run_command(f"curl -L {url} --output {output_path}")
        print_success(f"Fájl letöltve: {output_path.name}")
    except Exception as e:
        print_error(f"Hiba a letöltéskor: {e}")
        raise


def install_jforex4(downloads_dir: Path) -> None:
    """Telepíti a JForex4-et háttérfolyamatként."""
    print_info("JForex4 telepítése...")

    installer_path = downloads_dir / "JForex4_unix_64_JRE_bundled.sh"

    # Letöltés
    download_file(BROKER_URLS["jforex4"], installer_path)

    # Futtathatóvá tétel
    installer_path.chmod(0o755)

    # Háttérfolyamatként indítás
    print_info("JForex4 indítása háttérfolyamatként...")
    subprocess.Popen(
        [str(installer_path)],
        cwd=str(downloads_dir),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print_success("JForex4 telepítő elindítva háttérben")


def install_tws(downloads_dir: Path) -> None:
    """Telepíti az IBKR TWS-t háttérfolyamatként."""
    print_info("IBKR TWS telepítése...")

    installer_path = downloads_dir / "tws-latest-linux-x64.sh"

    # Letöltés
    download_file(BROKER_URLS["tws"], installer_path)

    # Futtathatóvá tétel
    installer_path.chmod(0o755)

    # Háttérfolyamatként indítás
    print_info("TWS indítása háttérfolyamatként...")
    subprocess.Popen(
        [str(installer_path)],
        cwd=str(downloads_dir),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print_success("TWS telepítő elindítva háttérben")


def install_mt5_dukascopy(downloads_dir: Path) -> None:
    """Telepíti a MetaTrader 5-öt (Dukascopy) Wine-on keresztül."""
    print_info("MetaTrader 5 (Dukascopy) telepítése...")

    if not check_wine():
        print_error("Wine nincs telepítve! Az MT5 telepítését kihagyjuk.")
        print_info("Telepítsd Wine-t: sudo apt install wine-stable (Ubuntu/Debian)")
        return

    installer_path = downloads_dir / "dukascopy5setup.exe"

    # Letöltés
    download_file(BROKER_URLS["mt5_dukascopy"], installer_path)

    # Wine prefix beállítása
    wineprefix = Path.home() / ".mt5"
    wineprefix.mkdir(exist_ok=True)

    # MT5 telepítése Wine-on keresztül háttérben
    print_info("MT5 telepítése Wine-on keresztül háttérben...")
    env = os.environ.copy()
    env["WINEPREFIX"] = str(wineprefix)

    subprocess.Popen(
        ["wine", str(installer_path)], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    print_success("MT5 telepítő elindítva háttérben")
    print_info(f"Wine prefix: {wineprefix}")


# ============================================================================
# FŐ TELEPÍTŐ FOLYAMAT
# ============================================================================


def run_hardware_detection() -> tuple[bool, bool]:
    """Lefuttatja a hardver detektálást.

    Returns:
        Tuple: (gpu_available, avx2_supported)
    """
    print_banner()
    print_info("Hardver detektálás indítása...")
    print()

    # Conda ellenőrzés
    if not check_conda():
        print_error("Conda nincs telepítve!")
        print_info(
            "Telepítsd Conda-t: https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html"
        )
        sys.exit(1)

    print_success("Conda telepítve van")

    # GPU ellenőrzés
    gpu_available = check_nvidia_gpu()
    if gpu_available:
        print_success("NVIDIA GPU észlelve")
    else:
        print_warning("NVIDIA GPU nem található, CPU mód használata")

    # AVX2 ellenőrzés
    avx2_supported = check_avx2_support()
    if avx2_supported:
        print_success("AVX2 támogatott")
    else:
        print_warning("AVX2 nem támogatott, fastparquet fallback használata")

    print()
    return gpu_available, avx2_supported


def install_core_environment(gpu_available: bool, avx2_supported: bool) -> None:
    """Telepíti a core környezetet.

    Args:
        gpu_available: True, ha GPU elérhető
        avx2_supported: True, ha AVX2 támogatott
    """
    print_info("Core környezet telepítése...")
    print()

    # Conda környezet létrehozása
    create_conda_env()
    print()

    # PyTorch telepítése
    install_pytorch(gpu_available)
    print()

    # PyTorch Lightning telepítése
    install_lightning()
    print()

    # Adatkezelő könyvtárak
    install_data_libraries(avx2_supported)
    print()

    # Alap csomagok
    install_base_packages()
    print()

    # Projekt csomagok
    install_project_packages()
    print()

    print_success("Core környezet telepítése sikeres!")
    print()


def install_brokers() -> None:
    """Telepíti az összes brókert automatikusan."""
    print_info("Bróker telepítők indítása...")
    print()

    # Downloads mappa létrehozása
    downloads_dir = create_downloads_dir()
    print_success(f"Downloads mappa: {downloads_dir}")
    print()

    # JForex4 telepítése
    try:
        install_jforex4(downloads_dir)
        print()
    except Exception as e:
        print_error(f"JForex4 telepítése sikertelen: {e}")
        print()

    # TWS telepítése
    try:
        install_tws(downloads_dir)
        print()
    except Exception as e:
        print_error(f"TWS telepítése sikertelen: {e}")
        print()

    # MT5 telepítése
    try:
        install_mt5_dukascopy(downloads_dir)
        print()
    except Exception as e:
        print_error(f"MT5 telepítése sikertelen: {e}")
        print()

    print_success("Bróker telepítők elindítva!")
    print()


def print_completion_message() -> None:
    """Kiírja a telepítés befejezési üzenetét."""
    print(f"{Colors.GREEN}{'=' * 60}")
    print("✓ TELJES TELEPÍTÉS SIKERES!")
    print(f"{'=' * 60}{Colors.NC}")
    print()
    print("Következő lépések:")
    print()
    print("1. Aktiváld a Conda környezetet:")
    print(f"   conda activate {CONDA_ENV_NAME}")
    print()
    print("2. Ellenőrizd a telepítést:")
    print("   python -c 'import torch; print(f\"PyTorch: {torch.__version__}\")'")
    print()
    print("3. Bróker telepítők állapota:")
    print("   - JForex4: A telepítő ablakban kövesd az utasításokat")
    print("   - TWS: A telepítő ablakban kövesd az utasításokat")
    print("   - MT5: Wine-on keresztül települ, ellenőrizd a ~/.mt5 mappát")
    print()
    print("4. Indítsd el a fejlesztést:")
    print("   python main.py")
    print()
    print("További információ: docs/INSTALLATION_GUIDE.md")
    print()


def main() -> None:
    """A fő telepítési folyamat."""
    try:
        # Hardver detektálás
        gpu_available, avx2_supported = run_hardware_detection()

        # Core környezet telepítése
        install_core_environment(gpu_available, avx2_supported)

        # Bróker telepítés
        install_brokers()

        # Befejezési üzenet
        print_completion_message()

    except KeyboardInterrupt:
        print()
        print_warning("Telepítés megszakítva a felhasználó által")
        sys.exit(1)
    except Exception as e:
        print_error(f"Váratlan hiba: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
