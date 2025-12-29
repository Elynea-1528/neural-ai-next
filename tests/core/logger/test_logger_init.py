"""Logger modul inicializációjának tesztjei.

Ez a modul teszteli a neural_ai.core.logger.__init__ modul
verziókezelését és exportjait, beleértve a PackageNotFoundError
kezelését is.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

from neural_ai.core.logger import (
    __all__,
    __schema_version__,
    __version__,
)


class TestLoggerInitVersionFallback:
    """Teszteli a verzió fallback mechanizmust, ha a csomag nincs telepítve."""

    def test_version_fallback_on_package_not_found(self) -> None:
        """Teszteli, hogy a verzió fallback értéket vesz fel, ha a csomag nem található.
        
        Ez a teszt lefedi a 56-58. sorokat, ahol a PackageNotFoundError-t kezeljük.
        A teszt egy külön subprocess-ben futtatja a modult mockolt környezettel,
        és coverage-t is futtat a subprocess-ben.
        """
        # Create a temporary test script with coverage
        test_script = '''
import sys
from unittest.mock import patch
import importlib.metadata as metadata

# Start coverage tracking
import coverage
cov = coverage.Coverage(include=["neural_ai/core/logger/__init__.py"])
cov.start()

# Mock metadata.version to raise PackageNotFoundError
def mock_version(package_name: str) -> str:
    if package_name == "neural-ai-next":
        raise metadata.PackageNotFoundError("Package not found")
    return "1.0.0"

# Apply the mock
with patch.object(metadata, 'version', side_effect=mock_version):
    # Now import the module - it should use the fallback
    from neural_ai.core.logger import __version__
    print(f"Version: {__version__}")
    assert __version__ == "1.0.0", f"Expected '1.0.0', got '{__version__}'"
    print("SUCCESS: Fallback version works correctly")

# Stop coverage and save data
cov.stop()
cov.save()
print("COVERAGE_SAVED")
'''
        
        # Write test script to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_script)
            temp_file = Path(f.name)
        
        try:
            # Run the test script in a subprocess
            result = subprocess.run(
                [sys.executable, str(temp_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Check if the subprocess succeeded
            if result.returncode != 0:
                print(f"Subprocess stdout: {result.stdout}")
                print(f"Subprocess stderr: {result.stderr}")
                assert False, f"Subprocess failed with return code {result.returncode}"
            
            # Verify the output
            assert "SUCCESS" in result.stdout, f"Unexpected output: {result.stdout}"
            assert "COVERAGE_SAVED" in result.stdout, f"Coverage not saved: {result.stdout}"
            
        finally:
            # Clean up temporary file
            temp_file.unlink(missing_ok=True)


class TestLoggerInitExports:
    """Teszteli a modul exportjait."""

    def test_version_is_available(self) -> None:
        """Teszteli, hogy a __version__ elérhető-e."""
        assert isinstance(__version__, str)
        assert len(__version__) > 0

    def test_schema_version_is_available(self) -> None:
        """Teszteli, hogy a __schema_version__ elérhető-e."""
        assert isinstance(__schema_version__, str)
        assert len(__schema_version__) > 0

    def test_all_list_is_exported(self) -> None:
        """Teszteli, hogy az __all__ lista tartalmazza az összes exportálandó elemet."""
        expected_exports = [
            "__version__",
            "__schema_version__",
            "LoggerInterface",
            "LoggerFactoryInterface",
            "ColoredLogger",
            "DefaultLogger",
            "LoggerFactory",
            "RotatingFileLogger",
            "LoggerError",
            "LoggerConfigurationError",
            "LoggerInitializationError",
        ]
        assert len(__all__) == len(expected_exports)
        for export in expected_exports:
            assert export in __all__

    def test_all_imports_available(self) -> None:
        """Teszteli, hogy minden importálható elem elérhető-e."""
        from neural_ai.core.logger import (
            LoggerConfigurationError,
            LoggerError,
            LoggerFactory,
            LoggerFactoryInterface,
            LoggerInitializationError,
            LoggerInterface,
        )
        
        # Just check they can be imported without errors
        assert LoggerInterface is not None
        assert LoggerFactoryInterface is not None
        assert LoggerFactory is not None
        assert LoggerError is not None
        assert LoggerConfigurationError is not None
        assert LoggerInitializationError is not None