#!/usr/bin/env python3
"""
Neural AI Next - Telepítési ellenőrző script

Ellenőrzi, hogy minden szükséges csomag telepítve van-e és megfelelő verzióban.
"""

import sys
from typing import Tuple

import torch
from packaging import version as pkg_version


def check_package(
    package_name: str, import_name: str = None, min_version: str = None
) -> Tuple[bool, str]:
    """Ellenőrzi egy csomag telepítését és verzióját."""
    try:
        module = __import__(import_name or package_name)

        # Speciális eset: Python verzió
        if import_name == "sys":
            version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        else:
            version = getattr(module, "__version__", "unknown")

        if min_version and version != "unknown":
            if pkg_version.parse(version) < pkg_version.parse(min_version):
                return False, f"{package_name} {version} (minimum {min_version} szükséges)"

        return True, f"{package_name} {version}"
    except ImportError:
        return False, f"{package_name} nincs telepítve"


def check_cuda():
    """Ellenőrzi a CUDA és cuDNN telepítését."""
    try:

        if not torch.cuda.is_available():
            return False, "CUDA nem elérhető"

        device_name = torch.cuda.get_device_name(0)
        cuda_version = torch.version.cuda
        cudnn_version = torch.backends.cudnn.version()

        # Ellenőrizzük, hogy a CUDA működik-e
        x = torch.randn(100, 100).cuda()
        y = torch.randn(100, 100).cuda()
        z = torch.matmul(x, y)

        return True, f"CUDA: {device_name}, CUDA verzió: {cuda_version}, cuDNN: {cudnn_version}"

    except Exception as e:
        return False, f"CUDA ellenőrzés sikertelen: {str(e)}"


def main():
    """Fő ellenőrzési funkció."""
    print("=" * 60)
    print("Neural AI Next - Telepítési Ellenőrzés")
    print("=" * 60)

    checks = [
        ("Python", "sys", "3.12"),
        ("NumPy", "numpy", "1.26.0"),
        ("Pandas", "pandas", "2.2.0"),
        ("PyTorch", "torch", "2.5.0"),
        ("Lightning", "lightning", "2.5.0"),
        ("VectorBT", "vectorbt", "0.25.0"),
        ("Scikit-learn", "sklearn", "1.4.0"),
        ("Matplotlib", "matplotlib", "3.8.0"),
        ("JupyterLab", "jupyterlab", "4.1.0"),
    ]

    all_ok = True

    # Csomagok ellenőrzése
    for package, import_name, min_version in checks:
        ok, message = check_package(package, import_name, min_version)
        status = "✓" if ok else "✗"
        print(f"{status} {message}")
        if not ok:
            all_ok = False

    # CUDA ellenőrzés
    cuda_ok, cuda_message = check_cuda()
    status = "✓" if cuda_ok else "✗"
    print(f"{status} {cuda_message}")
    if not cuda_ok:
        all_ok = False

    # Fejlesztői eszközök ellenőrzése
    dev_tools = [
        ("Pytest", "pytest", "8.0.0"),
        ("Black", "black", "24.1.0"),
        ("Flake8", "flake8", "7.0.0"),
        ("Mypy", "mypy", "1.8.0"),
        ("Pre-commit", "pre_commit", "3.5.0"),
    ]

    print("\nFejlesztői eszközök:")
    for package, import_name, min_version in dev_tools:
        ok, message = check_package(package, import_name, min_version)
        status = "✓" if ok else "✗"
        print(f"  {status} {message}")
        if not ok:
            all_ok = False

    print("=" * 60)

    if all_ok:
        print("✓ Minden ellenőrzés sikeres!")
        print("\nA környezet készen áll a fejlesztésre!")
        return 0
    else:
        print("✗ Néhány ellenőrzés sikertelen!")
        print("\nKérlek telepítsd a hiányzó csomagokat:")
        print("conda activate neural-ai-next")
        print("python install_environment.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())
