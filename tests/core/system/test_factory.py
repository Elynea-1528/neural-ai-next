"""SystemComponentFactory tesztelése.

Ez a modul a SystemComponentFactory osztályt teszteli, amely felelős
a rendszer komponensek (pl. HealthMonitor) létrehozásáért és kezeléséért.
"""

import unittest
from unittest.mock import MagicMock, patch

from neural_ai.core.system.factory import SystemComponentFactory
from neural_ai.core.system.interfaces.health_interface import (
    ComponentHealth,
    ComponentStatus,
    HealthCheckInterface,
    HealthMonitorInterface,
    HealthStatus,
)


class TestSystemComponentFactory(unittest.TestCase):
    """SystemComponentFactory osztály tesztjei."""

    def setUp(self) -> None:
        """Tesztelés előtti beállítások."""
        # Töröljük a gyorsítótárban lévő monitorokat
        SystemComponentFactory.clear_monitors()

    def tearDown(self) -> None:
        """Tesztelés utáni takarítás."""
        # Töröljük a gyorsítótárban lévő monitorokat
        SystemComponentFactory.clear_monitors()

    def test_create_health_monitor_default(self) -> None:
        """Alapértelmezett HealthMonitor létrehozásának tesztelése."""
        monitor = SystemComponentFactory.create_health_monitor()

        self.assertIsInstance(monitor, HealthMonitorInterface)
        self.assertEqual(monitor.get_registered_components(), [])

    def test_create_health_monitor_with_name(self) -> None:
        """HealthMonitor létrehozása névvel."""
        monitor = SystemComponentFactory.create_health_monitor(name="test_monitor")

        self.assertIsInstance(monitor, HealthMonitorInterface)
        self.assertIn("test_monitor", SystemComponentFactory.get_registered_monitors())

    def test_create_health_monitor_with_logger(self) -> None:
        """HealthMonitor létrehozása loggerrel."""
        mock_logger = MagicMock()
        monitor = SystemComponentFactory.create_health_monitor(
            name="logger_test", logger=mock_logger
        )

        self.assertIsInstance(monitor, HealthMonitorInterface)
        # Ellenőrizzük, hogy a monitor rendelkezik-e loggerrel
        self.assertTrue(hasattr(monitor, "_logger"))

    def test_create_health_monitor_caching(self) -> None:
        """HealthMonitor gyorsítótár tesztelése."""
        monitor1 = SystemComponentFactory.create_health_monitor(name="cached")
        monitor2 = SystemComponentFactory.create_health_monitor(name="cached")

        self.assertIs(monitor1, monitor2)

    def test_create_health_check_default(self) -> None:
        """Alapértelmezett HealthCheck létrehozásának tesztelése."""
        check = SystemComponentFactory.create_health_check(
            component_name="test_component"
        )

        self.assertIsInstance(check, HealthCheckInterface)
        self.assertEqual(check.get_name(), "test_component")

        # Teszteljük az ellenőrzés végrehajtását
        health = check.check()
        self.assertIsInstance(health, ComponentHealth)
        self.assertEqual(health.status, ComponentStatus.HEALTHY)

    def test_create_health_check_with_logger(self) -> None:
        """HealthCheck létrehozása loggerrel."""
        mock_logger = MagicMock()
        check = SystemComponentFactory.create_health_check(
            component_name="logger_test", logger=mock_logger
        )

        self.assertIsInstance(check, HealthCheckInterface)
        self.assertTrue(hasattr(check, "_logger"))

    def test_create_health_check_invalid_type(self) -> None:
        """Érvénytelen HealthCheck típus tesztelése."""
        with self.assertRaises(ValueError) as context:
            SystemComponentFactory.create_health_check(
                component_name="test", health_check_type="invalid"
            )

        self.assertIn("Ismeretlen health check típus", str(context.exception))

    def test_register_component(self) -> None:
        """Komponens regisztrálásának tesztelése."""
        monitor = SystemComponentFactory.create_health_monitor(name="register_test")
        SystemComponentFactory.register_component(
            monitor_name="register_test", component_name="database"
        )

        components = monitor.get_registered_components()
        self.assertIn("database", components)

    def test_register_component_with_custom_check(self) -> None:
        """Komponens regisztrálása egyedi ellenőrzéssel."""
        mock_check = MagicMock(spec=HealthCheckInterface)
        mock_check.check.return_value = ComponentHealth(
            name="custom_test",
            status=ComponentStatus.HEALTHY,
            message="Custom check passed",
            timestamp=None,  # type: ignore
        )

        monitor = SystemComponentFactory.create_health_monitor(name="custom_test")
        SystemComponentFactory.register_component(
            monitor_name="custom_test",
            component_name="storage",
            health_check=mock_check,
        )

        components = monitor.get_registered_components()
        self.assertIn("storage", components)

    def test_register_component_nonexistent_monitor(self) -> None:
        """Komponens regisztrálása nem létező monitorhoz."""
        with self.assertRaises(ValueError) as context:
            SystemComponentFactory.register_component(
                monitor_name="nonexistent", component_name="test"
            )

        self.assertIn("nem létezik", str(context.exception))

    def test_unregister_component(self) -> None:
        """Komponens eltávolításának tesztelése."""
        monitor = SystemComponentFactory.create_health_monitor(name="unregister_test")
        SystemComponentFactory.register_component(
            monitor_name="unregister_test", component_name="database"
        )

        # Ellenőrizzük, hogy a komponens regisztrálva van
        components = monitor.get_registered_components()
        self.assertIn("database", components)

        # Távolítsuk el a komponenst
        SystemComponentFactory.unregister_component(
            monitor_name="unregister_test", component_name="database"
        )

        # Ellenőrizzük, hogy a komponens eltávolításra került
        components = monitor.get_registered_components()
        self.assertNotIn("database", components)

    def test_unregister_component_nonexistent_monitor(self) -> None:
        """Komponens eltávolítása nem létező monitorból."""
        with self.assertRaises(ValueError) as context:
            SystemComponentFactory.unregister_component(
                monitor_name="nonexistent", component_name="test"
            )

        self.assertIn("nem létezik", str(context.exception))

    def test_get_health_monitor(self) -> None:
        """HealthMonitor lekérdezésének tesztelése."""
        monitor = SystemComponentFactory.create_health_monitor(name="get_test")

        retrieved = SystemComponentFactory.get_health_monitor("get_test")
        self.assertIs(monitor, retrieved)

    def test_get_health_monitor_nonexistent(self) -> None:
        """Nem létező HealthMonitor lekérdezésének tesztelése."""
        retrieved = SystemComponentFactory.get_health_monitor("nonexistent")
        self.assertIsNone(retrieved)

    def test_get_registered_monitors(self) -> None:
        """Regisztrált monitorok listázásának tesztelése."""
        # Kezdetben üres a lista
        monitors = SystemComponentFactory.get_registered_monitors()
        self.assertEqual(monitors, [])

        # Hozzunk létre néhány monitort
        SystemComponentFactory.create_health_monitor(name="monitor1")
        SystemComponentFactory.create_health_monitor(name="monitor2")

        monitors = SystemComponentFactory.get_registered_monitors()
        self.assertEqual(len(monitors), 2)
        self.assertIn("monitor1", monitors)
        self.assertIn("monitor2", monitors)

    def test_clear_monitors(self) -> None:
        """Monitorok törlésének tesztelése."""
        # Hozzunk létre néhány monitort
        SystemComponentFactory.create_health_monitor(name="monitor1")
        SystemComponentFactory.create_health_monitor(name="monitor2")

        monitors = SystemComponentFactory.get_registered_monitors()
        self.assertEqual(len(monitors), 2)

        # Töröljük a monitorokat
        SystemComponentFactory.clear_monitors()

        monitors = SystemComponentFactory.get_registered_monitors()
        self.assertEqual(monitors, [])

    def test_health_monitor_integration(self) -> None:
        """HealthMonitor integrációs teszt."""
        # Hozzuk létre a monitort
        monitor = SystemComponentFactory.create_health_monitor(name="integration_test")

        # Regisztráljunk néhány komponenst
        SystemComponentFactory.register_component(
            monitor_name="integration_test", component_name="database"
        )
        SystemComponentFactory.register_component(
            monitor_name="integration_test", component_name="storage"
        )

        # Ellenőrizzük a komponensek regisztrációját
        components = monitor.get_registered_components()
        self.assertEqual(len(components), 2)
        self.assertIn("database", components)
        self.assertIn("storage", components)

        # Ellenőrizzük az egészségügyi állapotot
        health = monitor.check_health()
        self.assertIsInstance(health.overall_status, HealthStatus)
        self.assertEqual(len(health.components), 2)

        # Ellenőrizzük az egyes komponenseket
        db_health = monitor.check_component("database")
        self.assertIsInstance(db_health, ComponentHealth)
        self.assertEqual(db_health.status, ComponentStatus.HEALTHY)

    def test_health_monitor_with_system_metrics(self) -> None:
        """HealthMonitor rendszer metrikák gyűjtésének tesztelése."""
        monitor = SystemComponentFactory.create_health_monitor(name="metrics_test")
        SystemComponentFactory.register_component(
            monitor_name="metrics_test", component_name="test_component"
        )

        health = monitor.check_health()

        # Ellenőrizzük, hogy vannak-e rendszer metrikák
        self.assertIsNotNone(health.system_metrics)

        # Ellenőrizzük a metrikák tartalmát
        if health.system_metrics:
            self.assertIn("cpu_percent", health.system_metrics)
            self.assertIn("memory_percent", health.system_metrics)
            # A metrikáknak float típusúnak kell lenniük
            self.assertIsInstance(health.system_metrics["cpu_percent"], float)
            self.assertIsInstance(health.system_metrics["memory_percent"], float)


if __name__ == "__main__":
    unittest.main()