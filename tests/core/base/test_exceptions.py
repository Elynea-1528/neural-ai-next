"""Tesztek a neural_ai.core.base.exceptions modulhoz.

Ez a tesztfájl ellenőrzi az összes alap kivétel osztályt.
"""

import unittest
from typing import List, Type

from neural_ai.core.base import exceptions


class TestExceptions(unittest.TestCase):
    """Tesztosztály az összes kivételhez."""

    def test_neural_ai_exception(self) -> None:
        """NeuralAIException alap kivétel tesztelése."""
        with self.assertRaises(exceptions.NeuralAIException):
            raise exceptions.NeuralAIException("Alap hiba")

    def test_storage_exception_hierarchy(self) -> None:
        """Storage kivétel hierarchia tesztelése."""
        # StorageException örökli NeuralAIException-t
        assert issubclass(exceptions.StorageException, exceptions.NeuralAIException)
        
        # StorageWriteError örökli StorageException-t
        assert issubclass(exceptions.StorageWriteError, exceptions.StorageException)
        
        # StorageReadError örökli StorageException-t
        assert issubclass(exceptions.StorageReadError, exceptions.StorageException)
        
        # StoragePermissionError örökli StorageException-t
        assert issubclass(exceptions.StoragePermissionError, exceptions.StorageException)
        
        # InsufficientDiskSpaceError örökli StorageException-t
        assert issubclass(exceptions.InsufficientDiskSpaceError, exceptions.StorageException)
        
        # PermissionDeniedError örökli StorageException-t
        assert issubclass(exceptions.PermissionDeniedError, exceptions.StorageException)

    def test_storage_write_error(self) -> None:
        """StorageWriteError kivétel tesztelése."""
        with self.assertRaises(exceptions.StorageWriteError):
            raise exceptions.StorageWriteError("Írási hiba")

    def test_storage_read_error(self) -> None:
        """StorageReadError kivétel tesztelése."""
        with self.assertRaises(exceptions.StorageReadError):
            raise exceptions.StorageReadError("Olvasási hiba")

    def test_storage_permission_error(self) -> None:
        """StoragePermissionError kivétel tesztelése."""
        with self.assertRaises(exceptions.StoragePermissionError):
            raise exceptions.StoragePermissionError("Jogosultsági hiba")

    def test_insufficient_disk_space_error(self) -> None:
        """InsufficientDiskSpaceError kivétel tesztelése."""
        with self.assertRaises(exceptions.InsufficientDiskSpaceError):
            raise exceptions.InsufficientDiskSpaceError("Nincs elég hely")

    def test_permission_denied_error(self) -> None:
        """PermissionDeniedError kivétel tesztelése."""
        with self.assertRaises(exceptions.PermissionDeniedError):
            raise exceptions.PermissionDeniedError("Hozzáférés megtagadva")

    def test_configuration_error(self) -> None:
        """ConfigurationError kivétel tesztelése."""
        with self.assertRaises(exceptions.ConfigurationError):
            raise exceptions.ConfigurationError("Érvénytelen konfiguráció")

    def test_dependency_error(self) -> None:
        """DependencyError kivétel tesztelése."""
        with self.assertRaises(exceptions.DependencyError):
            raise exceptions.DependencyError("Hiányzó függőség")

    def test_singleton_violation_error(self) -> None:
        """SingletonViolationError kivétel tesztelése."""
        with self.assertRaises(exceptions.SingletonViolationError):
            raise exceptions.SingletonViolationError("Singleton megsértve")

    def test_component_not_found_error(self) -> None:
        """ComponentNotFoundError kivétel tesztelése."""
        with self.assertRaises(exceptions.ComponentNotFoundError):
            raise exceptions.ComponentNotFoundError("Komponens nem található")

    def test_network_exception_hierarchy(self) -> None:
        """Network kivétel hierarchia tesztelése."""
        # NetworkException örökli NeuralAIException-t
        assert issubclass(exceptions.NetworkException, exceptions.NeuralAIException)
        
        # TimeoutError örökli NetworkException-t
        assert issubclass(exceptions.TimeoutError, exceptions.NetworkException)
        
        # ConnectionError örökli NetworkException-t
        assert issubclass(exceptions.ConnectionError, exceptions.NetworkException)

    def test_timeout_error(self) -> None:
        """TimeoutError kivétel tesztelése."""
        with self.assertRaises(exceptions.TimeoutError):
            raise exceptions.TimeoutError("Időtúllépés")

    def test_connection_error(self) -> None:
        """ConnectionError kivétel tesztelése."""
        with self.assertRaises(exceptions.ConnectionError):
            raise exceptions.ConnectionError("Kapcsolódási hiba")

    def test_exception_message_propagation(self) -> None:
        """Kivétel üzenet továbbadásának tesztelése."""
        message = "Test error message"
        
        try:
            raise exceptions.NeuralAIException(message)
        except exceptions.NeuralAIException as e:
            self.assertEqual(str(e), message)

    def test_exception_inheritance_chain(self) -> None:
        """Kivétel öröklési lánc ellenőrzése."""
        # Minden kivételnek Exception az ősosztálya
        all_exceptions: List[Type[Exception]] = [
            exceptions.NeuralAIException,
            exceptions.StorageException,
            exceptions.StorageWriteError,
            exceptions.StorageReadError,
            exceptions.StoragePermissionError,
            exceptions.InsufficientDiskSpaceError,
            exceptions.PermissionDeniedError,
            exceptions.ConfigurationError,
            exceptions.DependencyError,
            exceptions.SingletonViolationError,
            exceptions.ComponentNotFoundError,
            exceptions.NetworkException,
            exceptions.TimeoutError,
            exceptions.ConnectionError,
        ]
        
        for exc_class in all_exceptions:
            with self.subTest(exception=exc_class):
                self.assertTrue(issubclass(exc_class, Exception))


if __name__ == '__main__':
    unittest.main()