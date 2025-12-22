#!/usr/bin/env python3
"""Tesztek a jupyter_setup.py scripthez.

Ez a teszt modul ellenőrzi a Jupyter kernel konfiguráció és a Kaggle
template létrehozásának helyes működését.
"""

import json
import os
import shutil

# A tesztelendő modul importálása
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))
from scripts.install.scripts.jupyter_setup import (
    create_kaggle_template,
    create_kernel,
    main,
)


class TestJupyterSetup(unittest.TestCase):
    """Teszt osztály a Jupyter setup funkciókhoz."""

    def setUp(self) -> None:
        """Teszt előkészítés - ideiglenes könyvtár létrehozása."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_kernel_name = "neural-ai-next-test"

    def tearDown(self) -> None:
        """Teszt takarítás - ideiglenes könyvtár törlése."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        # Kaggle template törlése ha létezik
        template_path = Path("kaggle_template.ipynb")
        if template_path.exists():
            template_path.unlink()

    @patch("scripts.install.scripts.jupyter_setup.Path.home")
    def test_create_kernel_success(self, mock_home: Mock) -> None:
        """Teszteli a kernel létrehozását sikeres esetben."""
        # Mock-oljuk a home könyvtárat
        mock_home.return_value = Path(self.temp_dir)

        # Kernel könyvtár létrehozása
        kernel_base = Path(self.temp_dir) / ".local" / "share" / "jupyter" / "kernels"
        kernel_base.mkdir(parents=True, exist_ok=True)

        result = create_kernel()

        self.assertTrue(result, "A kernel létrehozásának sikeresnek kell lennie")

    @patch("scripts.install.scripts.jupyter_setup.Path.home")
    def test_create_kernel_directory_creation(self, mock_home: Mock) -> None:
        """Teszteli, hogy a kernel könyvtár létrejön-e."""
        mock_home.return_value = Path(self.temp_dir)

        # Először még ne legyen kernel könyvtár, de a szülő könyvtárnak léteznie kell
        kernel_base = Path(self.temp_dir) / ".local" / "share" / "jupyter" / "kernels"
        kernel_base.parent.mkdir(
            parents=True, exist_ok=True
        )  # A szülő könyvtár létezését biztosítjuk

        result = create_kernel()

        # Ellenőrizzük, hogy létrejött-e a könyvtár
        expected_kernel_dir = kernel_base / "neural-ai-next"
        self.assertTrue(expected_kernel_dir.exists(), "A kernel könyvtárnak léteznie kell")
        self.assertTrue(result, "A függvénynek True-t kell visszaadnia")

    @patch("scripts.install.scripts.jupyter_setup.Path.home")
    def test_create_kernel_json_content(self, mock_home: Mock) -> None:
        """Teszteli a kernel.json fájl tartalmát."""
        mock_home.return_value = Path(self.temp_dir)

        kernel_base = Path(self.temp_dir) / ".local" / "share" / "jupyter" / "kernels"
        kernel_base.mkdir(parents=True, exist_ok=True)

        create_kernel()

        # Ellenőrizzük a kernel.json tartalmát
        kernel_json = kernel_base / "neural-ai-next" / "kernel.json"
        self.assertTrue(kernel_json.exists(), "A kernel.json fájlnak léteznie kell")

        with open(kernel_json, encoding="utf-8") as f:
            kernel_spec = json.load(f)

        self.assertEqual(kernel_spec["display_name"], "Neural AI Next")
        self.assertEqual(kernel_spec["language"], "python")
        self.assertIn("argv", kernel_spec)
        self.assertIn("env", kernel_spec)
        self.assertIn("PYTHONPATH", kernel_spec["env"])
        self.assertIn("CUDA_VISIBLE_DEVICES", kernel_spec["env"])

    @patch("scripts.install.scripts.jupyter_setup.Path.home")
    def test_create_kernel_failure(self, mock_home: Mock) -> None:
        """Teszteli a kernel létrehozását sikertelen esetben."""
        # Olyan könyvtárat állítunk be, ahol nem lehet létrehozni
        mock_home.return_value = Path("/nonexistent")

        result = create_kernel()

        self.assertFalse(result, "A kernel létrehozásának sikertelennek kell lennie")

    def test_create_kaggle_template_success(self) -> None:
        """Teszteli a Kaggle template létrehozását."""
        # Változtassuk meg az aktuális könyvtárat az ideiglenes könyvtárra
        original_cwd = os.getcwd()
        try:
            os.chdir(self.temp_dir)

            result = create_kaggle_template()

            self.assertTrue(result, "A template létrehozásának sikeresnek kell lennie")

            # Ellenőrizzük, hogy a fájl létrejött-e
            template_path = Path("kaggle_template.ipynb")
            self.assertTrue(template_path.exists(), "A template fájlnak léteznie kell")

        finally:
            os.chdir(original_cwd)

    def test_create_kaggle_template_content(self) -> None:
        """Teszteli a Kaggle template tartalmát."""
        original_cwd = os.getcwd()
        try:
            os.chdir(self.temp_dir)

            create_kaggle_template()

            template_path = Path("kaggle_template.ipynb")
            with open(template_path, encoding="utf-8") as f:
                template = json.load(f)

            # Alapvető ellenőrzések
            self.assertIn("cells", template)
            self.assertIn("metadata", template)
            self.assertIn("nbformat", template)
            self.assertIn("nbformat_minor", template)

            # Első cella ellenőrzése
            self.assertGreater(len(template["cells"]), 0, "Legalább egy cellának kell lennie")
            first_cell = template["cells"][0]
            self.assertEqual(first_cell["cell_type"], "code")
            self.assertIn("source", first_cell)

            # Forráskód ellenőrzése
            source_code = "".join(first_cell["source"])
            self.assertIn("neural_ai", source_code)
            self.assertIn("torch", source_code)

        finally:
            os.chdir(original_cwd)

    @patch("scripts.install.scripts.jupyter_setup.create_kernel")
    @patch("scripts.install.scripts.jupyter_setup.create_kaggle_template")
    def test_main_success(self, mock_template: Mock, mock_kernel: Mock) -> None:
        """Teszteli a main függvényt sikeres futás esetén."""
        mock_kernel.return_value = True
        mock_template.return_value = True

        # A main függvény nem dob kivételt és nem lép ki
        try:
            main()
        except SystemExit as e:
            self.fail(f"main() nem szabad, hogy kilépjen, de kilépett: {e}")

    @patch("scripts.install.scripts.jupyter_setup.create_kernel")
    @patch("scripts.install.scripts.jupyter_setup.create_kaggle_template")
    @patch("scripts.install.scripts.jupyter_setup.sys.exit")
    def test_main_failure(self, mock_exit: Mock, mock_template: Mock, mock_kernel: Mock) -> None:
        """Teszteli a main függvényt sikertelen futás esetén."""
        mock_kernel.return_value = False
        mock_template.return_value = True

        main()

        # Ellenőrizzük, hogy meghívódott-e a sys.exit
        mock_exit.assert_called_once_with(1)

    def test_kaggle_template_structure(self) -> None:
        """Teszteli a Kaggle template szerkezetét."""
        original_cwd = os.getcwd()
        try:
            os.chdir(self.temp_dir)

            create_kaggle_template()

            template_path = Path("kaggle_template.ipynb")
            with open(template_path, encoding="utf-8") as f:
                template = json.load(f)

            # Metadata ellenőrzése
            self.assertIn("kernelspec", template["metadata"])
            kernelspec = template["metadata"]["kernelspec"]
            self.assertEqual(kernelspec["display_name"], "Python 3")
            self.assertEqual(kernelspec["language"], "python")
            self.assertEqual(kernelspec["name"], "python3")

            # Formátum ellenőrzése
            self.assertEqual(template["nbformat"], 4)
            self.assertEqual(template["nbformat_minor"], 4)

        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    unittest.main()
