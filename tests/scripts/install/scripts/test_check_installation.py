#!/usr/bin/env python3
"""Tesztelő script a check_installation.py-hoz.

Ez egy egyszerű teszt, amely ellenőrzi a főbb funkciók működését.
A teljes teszteléshez manuális futtatás szükséges.
"""

import importlib.util
import sys
from pathlib import Path

# Hozzáadjuk a forrásfájl elérési útját
project_root = Path(__file__).parent.parent.parent.parent.parent
source_path = project_root / "scripts" / "install" / "scripts"

spec = importlib.util.spec_from_file_location(
    "check_installation", source_path / "check_installation.py"
)
if spec and spec.loader:
    check_installation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(check_installation)

    check_package = check_installation.check_package
    estimate_cuda_cores = check_installation.estimate_cuda_cores
else:
    raise ImportError("Could not load check_installation module")


def test_check_package_sys() -> None:
    """Teszteli a check_package függvényt Python verzióval."""
    ok, message = check_package("Python", "sys", "3.0")
    assert ok, f"Python check failed: {message}"
    assert "Python" in message
    print(f"✓ test_check_package_sys passed: {message}")


def test_check_package_nonexistent() -> None:
    """Teszteli a check_package függvényt nem létező csomaggal."""
    ok, message = check_package("NonexistentPackage12345", None, None)
    assert not ok, f"Should fail for non-existent package: {message}"
    assert "nincs telepítve" in message
    print(f"✓ test_check_package_nonexistent passed: {message}")


def test_estimate_cuda_cores() -> None:
    """Teszteli a CUDA core-ok becslését."""
    # Tesla V100 (7.0 compute capability)
    cores = estimate_cuda_cores(7, 0, 16.0)
    assert cores > 0, "Should return positive core count"
    print(f"✓ test_estimate_cuda_cores passed: {cores} cores estimated")

    # RTX 4090 (8.9 compute capability)
    cores_4090 = estimate_cuda_cores(8, 9, 24.0)
    assert cores_4090 == 10240, "Should return exact value for known GPU"
    print(f"✓ test_estimate_cuda_cores RTX 4090 passed: {cores_4090} cores")


def main() -> int:
    """Fő tesztfunkció."""
    print("=" * 60)
    print("check_installation.py - Egyszerű tesztek")
    print("=" * 60)

    try:
        test_check_package_sys()
        test_check_package_nonexistent()
        test_estimate_cuda_cores()

        print("=" * 60)
        print("✓ Összes teszt sikeres!")
        return 0
    except AssertionError as e:
        print(f"✗ Teszt sikertelen: {e}")
        return 1
    except Exception as e:
        print(f"✗ Váratlan hiba: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
