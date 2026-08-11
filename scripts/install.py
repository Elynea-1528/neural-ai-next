#!/usr/bin/env python3
"""Neural AI Next - Unified Zero-Touch Installer.

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

import argparse
import os
import shutil
import subprocess
import sys
import traceback
from pathlib import Path

# ============================================================================
# KONFIGURÁCIÓ
# ============================================================================

CONDA_ENV_NAME = "neural-ai-next"
PYTHON_VERSION = "3.12"
PROJECT_ROOT = Path(__file__).parent.parent

# Globális verbose flag
_verbose = False

# Bróker letöltési URL-ek
BROKER_URLS = {
    "jforex4": "https://dukascopy-eu.cdn.online-trading-solutions.com/installer4/dukascopy-eu/JForex4_unix_64_JRE_bundled.sh",
    "tws": "https://download2.interactivebrokers.com/installers/tws/latest/tws-latest-linux-x64.sh",
    "mt5_dukascopy": "https://download.mql5.com/cdn/web/dukascopy.bank.sa/mt5/dukascopy5setup.exe",
}

# A befejezési üzenetben verzióval megjelenített kulcs csomagok (conda csomagnév)
VERSION_WHITELIST = [
    "python", "pytorch", "torchvision", "torchaudio", "pytorch-cuda",
    "lightning", "polars", "pyarrow", "fastparquet", "pandas", "numpy",
    "scikit-learn", "pydantic", "pydantic-settings", "sqlalchemy", "structlog",
    "fastapi", "uvicorn", "streamlit", "pyzmq", "psutil", "tenacity",
    "aiohttp", "requests", "vectorbt",
]


# Színek a konzolhoz
class Colors:
    """Színek a konzol kimenethez."""

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
    if _verbose:
        print_info(f"Futtatás: {command}")
    # Always capture output; hiba esetén írjuk ki, hogy a valódi ok látható legyen
    result = subprocess.run(command, shell=shell, check=False, capture_output=True, text=True)

    if check and result.returncode != 0:
        # A CalledProcessError nem mutatja láthatóan a kimenetet, ezért itt kiírjuk
        if result.stdout:
            print_info(f"Output: {result.stdout.strip()}")
        if result.stderr:
            print_error(f"Parancs hiba kimenete: {result.stderr.strip()}")
        raise subprocess.CalledProcessError(
            result.returncode, command, result.stdout, result.stderr
        )

    if _verbose and result.stdout:
        print_info(f"Output: {result.stdout.strip()}")
    if _verbose and result.stderr:
        print_info(f"Error: {result.stderr.strip()}")

    return result


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
        if _verbose:
            print_info("nvidia-smi nem elérhető")
        return False

    try:
        result = run_command("nvidia-smi --query-gpu=name --format=csv,noheader", check=False)

        if _verbose:
            print_info(f"Return code: {result.returncode}")
            print_info(f"Stdout: '{result.stdout}'")
            print_info(f"Stderr: '{result.stderr}'")

        gpu_detected = bool(
            result.returncode == 0 and result.stdout and result.stdout.strip() != ""
        )

        if _verbose:
            if gpu_detected:
                print_info(f"GPU detektálva: {result.stdout.strip()}")
            else:
                print_info(f"GPU nem található (returncode={result.returncode})")

        return gpu_detected
    except Exception as e:
        if _verbose:
            print_warning(f"Hiba a GPU detektálásakor: {e}")
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


def remove_conda_env() -> None:
    """Eltávolítja a neural-ai-next Conda környezetet, ha létezik."""
    print_info("Régi környezet ellenőrzése...")

    try:
        result = run_command(f"{get_conda_path()} env list | grep {CONDA_ENV_NAME}", check=False)

        # Check if result.stdout is not None before using 'in'
        if result.stdout and CONDA_ENV_NAME in result.stdout:
            print_info(f"A(z) '{CONDA_ENV_NAME}' környezet eltávolítása...")
            run_command(f"{get_conda_path()} env remove -n {CONDA_ENV_NAME} -y")
            print_success(f"A(z) '{CONDA_ENV_NAME}' környezet eltávolítva")
        else:
            print_info(f"A(z) '{CONDA_ENV_NAME}' környezet nem létezik")
    except Exception as e:
        print_warning(f"Hiba a környezet ellenőrzésekor: {e}")


def create_conda_env_with_packages(gpu_available: bool) -> None:
    """Létrehozza a neural-ai-next Conda környezetet az összes csomaggal együtt.

    Args:
        gpu_available: True, ha GPU elérhető
    """
    print_info(f"A(z) '{CONDA_ENV_NAME}' környezet létrehozása az összes csomaggal...")

    # Alap csomagok
    python = f"python={PYTHON_VERSION}"
    base_packages = "pandas numpy scikit-learn"

    # PyTorch csomagok
    # NOTE: --override-channels szükséges: a conda 26.x TOS-t kér a `defaults`
    # channel-hez (repo.anaconda.com/pkgs/*), ami meghiúsítaná a telepítést.
    # A projekt explicit channel-eket ad meg, azok elegendőek.
    if gpu_available:
        pytorch_packages = "pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 pytorch-cuda=12.1"
        channels = "-c pytorch -c nvidia -c conda-forge --override-channels"
    else:
        pytorch_packages = "pytorch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 cpuonly"
        channels = "-c pytorch -c conda-forge --override-channels"

    # Lightning
    lightning_package = "lightning=2.5.5"

    # Összes csomag együtt
    all_packages = f"{python} {pytorch_packages} {lightning_package} {base_packages}"

    # Környezet létrehozása az összes csomaggal
    run_command(f"{get_conda_path()} create -n {CONDA_ENV_NAME} {all_packages} {channels} -y")
    print_success(f"A(z) '{CONDA_ENV_NAME}' környezet létrejött az összes csomaggal")


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


def install_project_packages(extra_groups: list[str]) -> None:
    """Telepíti a projekt csomagjait a megadott opcionális függőséggel.

    Args:
        extra_groups: Az opcionális függőségi csoportok listája (pl: ['dev', 'trader'])
    """
    if not extra_groups:
        print_info("Projekt csomagok telepítése (csak alap csomagok)...")
        run_command(f"{get_conda_path()} run -n {CONDA_ENV_NAME} pip install -e .")
    else:
        groups_str = ",".join(extra_groups)
        print_info(f"Projekt csomagok telepítése ({groups_str})...")
        run_command(f"{get_conda_path()} run -n {CONDA_ENV_NAME} pip install -e .[{groups_str}]")

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
    gpu_available: bool = check_nvidia_gpu()
    if gpu_available:
        print_success("NVIDIA GPU észlelve")
    else:
        print_warning("NVIDIA GPU nem található, CPU mód használata")

    # AVX2 ellenőrzés
    avx2_supported: bool = check_avx2_support()
    if avx2_supported:
        print_success("AVX2 támogatott")
    else:
        print_warning("AVX2 nem támogatott, fastparquet fallback használata")

    print()
    return gpu_available, avx2_supported


def install_core_environment(
    gpu_available: bool, avx2_supported: bool, extra_groups: list[str]
) -> None:
    """Telepíti a core környezetet az új módszerrel (egyetlen conda create parancs).

    Args:
        gpu_available: True, ha GPU elérhető
        avx2_supported: True, ha AVX2 támogatott
        extra_groups: Az opcionális függőségi csoportok listája
    """
    print_info("Core környezet telepítése (új módszer)...")
    print()

    # Régi környezet eltávolítása
    remove_conda_env()
    print()

    # Környezet létrehozása az összes csomaggal együtt
    create_conda_env_with_packages(gpu_available)
    print()

    # Adatkezelő könyvtárak (ezeket pip-pel kell telepíteni)
    install_data_libraries(avx2_supported)
    print()

    # Projekt csomagok telepítése
    install_project_packages(extra_groups)
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


def collect_installed_versions() -> dict[str, str]:
    """Lekérdezi a legfontosabb telepített csomagok valós verzióit.

    A cél környezet `conda list` kimenetéből szűri ki a `VERSION_WHITELIST`
    csomagjait, hogy a befejezési üzenet valós képet adjon a verziókról
    (hiány / esetleges verzióütközés felderítéséhez).

    Returns:
        A whitelist szerinti csomagnév -> verzió szótár.
    """
    versions: dict[str, str] = {}
    try:
        result = run_command(
            f"{get_conda_path()} list -n {CONDA_ENV_NAME}",
            check=False,
        )
        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2 and parts[0] in VERSION_WHITELIST:
                versions[parts[0]] = parts[1]
    except Exception:
        # A kiértékelés nem kritikus: hiba esetén üres szótárt adunk vissza
        pass
    return versions


def print_completion_message(
    gpu_available: bool,
    avx2_supported: bool,
    extra_groups: list[str],
    brokers_installed: bool,
) -> None:
    """Kiírja a telepítés befejezési üzenetét a telepített verziókkal.

    Args:
        gpu_available: True, ha GPU elérhető
        avx2_supported: True, ha AVX2 támogatott
        extra_groups: A telepített csomagcsoportok listája
        brokers_installed: True, ha a bróker telepítők lefutottak
    """
    print(f"{Colors.GREEN}{'=' * 60}")
    print("✓ TELJES TELEPÍTÉS SIKERES!")
    print(f"{'=' * 60}{Colors.NC}")
    print()
    print("Telepített környezet összegzés:")
    print()

    # Hardver információk
    print("• Hardver:")
    print(f"  - GPU: {'✓ NVIDIA GPU észlelve' if gpu_available else '✗ CPU mód'}")
    print(f"  - AVX2: {'✓ Támogatott' if avx2_supported else '✗ Nem támogatott'}")
    print()

    # Telepített csomagok valós verziókkal (kiértékelés)
    versions = collect_installed_versions()
    print("• Telepített csomagok (valós verziók):")
    version_groups: list[tuple[str, list[str]]] = [
        ("Python / ML", [
            "python", "pytorch", "torchvision", "torchaudio",
            "pytorch-cuda", "lightning",
        ]),
        ("Adatfeldolgozás", [
            "polars", "pyarrow", "fastparquet", "pandas", "numpy",
            "scikit-learn",
        ]),
        ("Alkalmazás / Config", [
            "pydantic", "pydantic-settings", "sqlalchemy", "structlog",
            "fastapi", "streamlit",
        ]),
        ("Infrastruktúra / Utility", [
            "pyzmq", "psutil", "tenacity", "aiohttp", "requests", "vectorbt",
        ]),
    ]
    for group_name, names in version_groups:
        detail = ", ".join(f"{n}={versions.get(n, 'HIÁNYZIK')}" for n in names)
        print(f"  - {group_name}: {detail}")
    print()

    # Adatkezelő backend tény
    backend = "polars + pyarrow (AVX2)" if avx2_supported else "fastparquet (fallback)"
    print(f"• Adatkezelő backend: {backend}")
    print()

    # Telepített csomagcsoportok
    if extra_groups:
        groups_str = ", ".join(extra_groups)
        print(f"• Telepített csomagcsoportok: {groups_str}")
    else:
        print("• Telepített csomagcsoportok: alap csomagok")
    print()

    # Bróker információk (csak akkor, ha tényleg lefutott a bróker telepítés)
    print("• Bróker telepítők:")
    if brokers_installed:
        print("  - JForex4: Letöltve és elindítva")
        print("  - IBKR TWS: Letöltve és elindítva")
        print("  - MT5 (Dukascopy): Letöltve és elindítva (Wine)")
    else:
        print("  - Kihagyva (--no-brokers flag)")
    print()

    # Aktiválás
    print("Aktiválás:")
    print(f"  conda activate {CONDA_ENV_NAME}")
    print()

    # Ellenőrzés
    print("Ellenőrzés:")
    if gpu_available:
        print(
            "  python -c \"import torch; print(f'PyTorch: {torch.__version__}, "
            "CUDA: {torch.cuda.get_device_name(0)}')\""
        )
    else:
        print("  python -c \"import torch; print(f'PyTorch: {torch.__version__}')\"")
    print()

    print("További információ: docs/INSTALLATION_GUIDE.md")
    print()


def parse_arguments() -> argparse.Namespace:
    """Feldolgozza a parancssori argumentumokat.

    Returns:
        A feldolgozott argumentumok névtere
    """
    parser = argparse.ArgumentParser(
        description="Neural AI Next - Unified Zero-Touch Installer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Példák:
  python scripts/install.py                    # Alap telepítés (összes csoport)
  python scripts/install.py --no-brokers       # Csak környezet, brókerek nélkül
  python scripts/install.py --only dev         # Csak dev csomagok
  python scripts/install.py --only dev,trader  # Dev + trader csomagok
  python scripts/install.py -v                 # Verbose mód
  python scripts/install.py --only dev -v      # Dev csomagok verbose módban
        """,
    )

    parser.add_argument(
        "--only", type=str, help='Csak ezeket a függőségi csoportokat telepíti (pl: "dev,trader")'
    )

    parser.add_argument(
        "--no-brokers", action="store_true", help="Ne indítsa el a bróker telepítőket"
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Részletes kimenet (verbose mode)"
    )

    return parser.parse_args()


def main() -> None:
    """A fő telepítési folyamat."""
    try:
        # Argumentumok feldolgozása
        args = parse_arguments()

        # Globális verbose flag beállítása
        global _verbose
        _verbose = args.verbose

        # Függőségi csoportok meghatározása
        if args.only:
            extra_groups = [g.strip() for g in args.only.split(",")]
        else:
            # Alapértelmezett: minden csoport (UI is!)
            extra_groups = ["dev", "trader", "jupyter", "ui"]

        # Hardver detektálás
        gpu_available, avx2_supported = run_hardware_detection()

        # Core környezet telepítése
        install_core_environment(gpu_available, avx2_supported, extra_groups)

        # Bróker telepítés (ha nem letiltva)
        brokers_installed = not args.no_brokers
        if brokers_installed:
            install_brokers()
        else:
            print_info("Bróker telepítők kihagyása (--no-brokers flag)")

        # Befejezési üzenet
        print_completion_message(
            gpu_available, avx2_supported, extra_groups, brokers_installed
        )

    except KeyboardInterrupt:
        print()
        print_warning("Telepítés megszakítva a felhasználó által")
        sys.exit(1)
    except Exception as e:
        print_error(f"Váratlan hiba: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
