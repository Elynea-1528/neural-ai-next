#!/usr/bin/env python3
"""Neural AI Next - Telepítési ellenőrző script.

Ellenőrzi, hogy minden szükséges csomag telepítve van-e és megfelelő verzióban.
"""

import sys

import torch
from packaging import version as pkg_version


def check_package(
    package_name: str,
    import_name: str | None = None,
    min_version: str | None = None,
) -> tuple[bool, str]:
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
                return (
                    False,
                    f"{package_name} {version} (minimum {min_version} szükséges)",
                )

        return True, f"{package_name} {version}"
    except ImportError:
        return False, f"{package_name} nincs telepítve"


def estimate_cuda_cores(major: int, minor: int, total_memory_gb: float) -> int:
    """Becsli a CUDA core-ok számát a compute capability és memória alapján.

    Args:
        major: Major compute capability verzió
        minor: Minor compute capability verzió
        total_memory_gb: Teljes GPU memória GB-ban

    Returns:
        Becsült CUDA core-ok száma
    """
    # CUDA core-ok becslése compute capability alapján
    # Forrás: NVIDIA architektúra dokumentációk
    cuda_cores_map = {
        (6, 1): 128,  # Pascal (GTX 1050 Ti)
        (7, 5): 1024,  # Turing (RTX 2060+)
        (8, 6): 2560,  # Ampere (RTX 3060+)
        (8, 9): 10240,  # Ada Lovelace (RTX 4090)
    }

    # Alapértelmezett becslés memória alapján
    base_cores = int(total_memory_gb * 64)  # ~64 core per GB

    # Compute capability alapú pontosítás
    return cuda_cores_map.get((major, minor), base_cores)


def check_cuda():
    """Ellenőrzi a CUDA és cuDNN telepítését."""
    try:
        if not torch.cuda.is_available():
            return False, "CUDA nem elérhető"

        device_name = torch.cuda.get_device_name(0)
        cuda_version = torch.version.cuda
        cudnn_version = torch.backends.cudnn.version()

        # GPU memória információk
        total_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # GB
        major = torch.cuda.get_device_properties(0).major
        minor = torch.cuda.get_device_properties(0).minor
        compute_capability = f"{major}.{minor}"

        # CUDA core-ok becslése
        cuda_cores = estimate_cuda_cores(major, minor, total_memory)

        # Ellenőrizzük, hogy a CUDA működik-e
        x = torch.randn(100, 100).cuda()
        y = torch.randn(100, 100).cuda()
        _ = torch.matmul(x, y)  # Teszteljük a CUDA működését

        return (
            True,
            f"CUDA: {device_name}, CUDA verzió: {cuda_version}, cuDNN: {cudnn_version}, Memória: {total_memory:.1f}GB, Compute: {compute_capability}, CUDA Cores: ~{cuda_cores}",
        )

    except Exception as e:
        return False, f"CUDA ellenőrzés sikertelen: {str(e)}"


def main():
    """Fő ellenőrzési funkció."""
    print("=" * 60)
    print("Neural AI Next - Telepítési Ellenőrzés")
    print("=" * 60)

    # Core csomagok
    core_packages = [
        ("Python", "sys", "3.12"),
        ("NumPy", "numpy", "1.24.3"),
        ("Pandas", "pandas", "2.0.3"),
        ("PyTorch", "torch", "2.5.0"),
        ("Lightning", "lightning", "2.5.0"),
        ("VectorBT", "vectorbt", "0.25.0"),
        ("Scikit-learn", "sklearn", "1.3.0"),
    ]

    all_ok = True

    print("\nCore csomagok:")
    for package, import_name, min_version in core_packages:
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

    # Fejlesztői eszközök
    dev_tools = [
        ("Pytest", "pytest", "8.0.0"),
        ("Black", "black", "24.1.0"),
        ("Flake8", "flake8", "7.0.0"),
        ("Mypy", "mypy", "1.8.0"),
        ("Pre-commit", "pre_commit", "3.5.0"),
        ("Ruff", "ruff", "0.1.0"),
    ]

    print("\nFejlesztői eszközök:")
    for package, import_name, min_version in dev_tools:
        ok, message = check_package(package, import_name, min_version)
        status = "✓" if ok else "✗"
        print(f"  {status} {message}")
        if not ok:
            all_ok = False

    # Adatkezelő eszközök
    data_tools = [
        ("Fastparquet", "fastparquet", "2023.4.0"),
    ]

    print("\nAdatkezelő eszközök:")
    for package, import_name, min_version in data_tools:
        ok, message = check_package(package, import_name, min_version)
        status = "✓" if ok else "✗"
        print(f"  {status} {message}")
        # Fastparquet opcionális, ne befolyásolja az összesített eredményt

    # Jupyter eszközök
    jupyter_tools = [
        ("JupyterLab", "jupyterlab", "4.0.0"),
        ("Notebook", "notebook", "7.0.0"),
        ("IPython", "IPython", "8.15.0"),
    ]

    print("\nJupyter eszközök:")
    for package, import_name, min_version in jupyter_tools:
        ok, message = check_package(package, import_name, min_version)
        status = "✓" if ok else "✗"
        print(f"  {status} {message}")
        if not ok:
            all_ok = False

    # Web framework eszközök
    web_tools = [
        ("FastAPI", "fastapi", "0.104.0"),
        ("Uvicorn", "uvicorn", "0.24.0"),
        ("WebSockets", "websockets", "12.0"),
        ("HTTPX", "httpx", "0.25.0"),
        ("Pydantic", "pydantic", "2.4.0"),
    ]

    print("\nWeb framework eszközök:")
    for package, import_name, min_version in web_tools:
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
