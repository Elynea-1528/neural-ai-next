#!/usr/bin/env python3
"""Jupyter kernel konfiguráció Neural AI Next-hez.

Ez a script létrehozza a Jupyter kernel konfigurációt,
ami Kaggle GPU használatához is alkalmas.
"""

import json
import subprocess
import sys
from pathlib import Path


def create_kernel():
    """Létrehozza a Neural AI Next Jupyter kernel-t."""
    kernel_name = "neural-ai-next"

    # Kernel könyvtár meghatározása
    kernel_dirs = [
        Path.home() / ".local" / "share" / "jupyter" / "kernels",
        Path.home() / ".jupyter" / "kernels",
    ]

    kernel_dir = None
    for kd in kernel_dirs:
        if kd.exists() or kd.parent.exists():
            kd.mkdir(parents=True, exist_ok=True)
            kernel_dir = kd / kernel_name
            kernel_dir.mkdir(parents=True, exist_ok=True)
            break

    if kernel_dir is None:
        print("✗ Nem található Jupyter kernel könyvtár")
        return False

    # Kernel specifikáció
    kernel_spec = {
        "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
        "display_name": "Neural AI Next",
        "language": "python",
        "env": {"PYTHONPATH": str(Path.cwd()), "CUDA_VISIBLE_DEVICES": "0"},
        "metadata": {"debugger": True},
    }

    # Kernel spec fájl írása
    kernel_json = kernel_dir / "kernel.json"
    with open(kernel_json, "w", encoding="utf-8") as f:
        json.dump(kernel_spec, f, indent=2, ensure_ascii=False)

    print(f"✓ Jupyter kernel létrehozva: {kernel_name}")
    print(f"  Hely: {kernel_json}")

    # Kernel telepítése
    try:
        subprocess.run(
            ["python", "-m", "ipykernel", "install", "--user", "--name", kernel_name],
            check=True,
        )
        print(f"✓ Kernel telepítve: {kernel_name}")
    except subprocess.CalledProcessError:
        print("⚠️  Kernel telepítése nem sikerült, de a konfiguráció létrejött")

    return True


def create_kaggle_template():
    """Létrehozza a Kaggle notebook template-et."""
    template = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Neural AI Next - Kaggle Setup\n",
                    "import sys\n",
                    "sys.path.append('/kaggle/working/neural-ai-next')\n",
                    "\n",
                    "from neural_ai.core.base import CoreComponentFactory\n",
                    "from neural_ai.collectors.mt5 import MT5Collector\n",
                    "import torch\n",
                    "\n",
                    "print(f'PyTorch: {torch.__version__}')\n",
                    "print(f'CUDA available: {torch.cuda.is_available()}')\n",
                    "if torch.cuda.is_available():\n",
                    "    print(f'CUDA device: {torch.cuda.get_device_name(0)}')\n",
                    "print('✓ Neural AI Next loaded')",
                ],
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4,
    }

    template_path = Path("kaggle_template.ipynb")
    with open(template_path, "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)

    print(f"✓ Kaggle template létrehozva: {template_path}")
    return True


def main():
    """Fő belépési pont."""
    print("=" * 60)
    print("Jupyter Kernel Konfiguráció")
    print("=" * 60)

    success = True

    # Kernel létrehozása
    if not create_kernel():
        success = False

    # Template létrehozása
    if not create_kaggle_template():
        success = False

    if success:
        print("\n" + "=" * 60)
        print("✓ Jupyter konfiguráció sikeres!")
        print("=" * 60)
        print("\nHasználat:")
        print("1. JupyterLab indítása:")
        print("   jupyter lab")
        print("\n2. Kernel kiválasztása:")
        print("   Kernel -> Change Kernel -> Neural AI Next")
        print("\n3. Kaggle használata:")
        print("   Töltsd fel a kaggle_template.ipynb fájlt")
    else:
        print("\n✗ Jupyter konfiguráció sikertelen!")
        sys.exit(1)


if __name__ == "__main__":
    main()
