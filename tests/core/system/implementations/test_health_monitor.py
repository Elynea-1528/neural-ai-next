"""HealthMonitor osztály tesztjei.

Ez a modul a `HealthMonitor` osztály egységtesztjeit tartalmazza,
amelyek ellenőrzik a komponens regisztrációt, egészségügyi ellenőrzést
és rendszer metrikák gyűjtését.
"""

import unittest
from datetime import datetime
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from neural_ai.core.system.implementations.health_monitor import (
    DefaultHealthCheck,
    HealthMonitor,
)
from neural_ai.core.system.interfaces.health_interface import (
    ComponentHealth,
    ComponentStatus,
    HealthStatus,
)


class TestDefaultHealthCheck(IsolatedAsyncioTestCase):
    """DefaultHealthCheck osztály tesztjei."""

    async def test_check_returns_healthy(self) -> None:
        """Teszteli, hogy a check metódus mindig HEALTHY státuszt ad vissza."""
        check = DefaultHealthCheck("test_component")
        result = await check.check()

        self.assertEqual(result.name, "test_component")
        self.assertEqual(result.status, ComponentStatus.HEALTHY)
        self.assertEqual(result.message, "Komponens egészséges")
        self.assertIsInstance(result.timestamp, datetime)

    def test_get_name_returns_component_name(self) -> None:
        """Teszteli, hogy a get_name metódus visszaadja a komponens nevét."""
        check = DefaultHealthCheck("test_component")
        self.assertEqual(check.get_name(), "test_component")


class TestHealthMonitor(IsolatedAsyncioTestCase):
    """HealthMonitor osztály tesztjei."""

    def setUp(self) -> None:
        """Teszt előkészítése."""
        self.monitor = HealthMonitor()

    def test_initial_state(self) -> None:
        """Teszteli a kezdeti állapotot."""
        self.assertEqual(self.monitor.get_registered_components(), [])
        self.assertIsNone(self.monitor._logger)

    def test_register_component(self) -> None:
        """Teszteli a komponens regisztrációt."""
        self.monitor.register_component("test_component")
        components = self.monitor.get_registered_components()

        self.assertIn("test_component", components)
        self.assertEqual(len(components), 1)

    async def test_register_component_with_custom_check(self) -> None:
        """Teszteli a komponens regisztrációt egyedi ellenőrzéssel."""
        mock_check: MagicMock = MagicMock()
        mock_check.check = AsyncMock(return_value=ComponentHealth(
            name="test_component",
            status=ComponentStatus.HEALTHY,
            message="Test message",
            timestamp=datetime.now(),
        ))

        self.monitor.register_component("test_component", mock_check)
        health = await self.monitor.check_component("test_component")

        self.assertEqual(health.name, "test_component")
        self.assertEqual(health.status, ComponentStatus.HEALTHY)
        mock_check.check.assert_called_once()

    def test_unregister_component(self) -> None:
        """Teszteli a komponens eltávolítását."""
        self.monitor.register_component("test_component")
        self.monitor.unregister_component("test_component")

        components = self.monitor.get_registered_components()
        self.assertNotIn("test_component", components)

    def test_unregister_nonexistent_component(self) -> None:
        """Teszteli a nem létező komponens eltávolítását."""
        # Nem szabad hibát dobnia
        self.monitor.unregister_component("nonexistent_component")

    async def test_check_component_success(self) -> None:
        """Teszteli a komponens ellenőrzését sikeres esetben."""
        self.monitor.register_component("test_component")
        health = await self.monitor.check_component("test_component")

        self.assertEqual(health.name, "test_component")
        self.assertEqual(health.status, ComponentStatus.HEALTHY)
        self.assertIsInstance(health.timestamp, datetime)

    async def test_check_component_nonexistent(self) -> None:
        """Teszteli a nem létező komponens ellenőrzését."""
        with self.assertRaises(ValueError) as context:
            await self.monitor.check_component("nonexistent_component")

        self.assertIn("nincs regisztrálva", str(context.exception))

    async def test_check_component_with_exception(self) -> None:
        """Teszteli a komponens ellenőrzését kivétel esetén."""
        mock_check: MagicMock = MagicMock()
        mock_check.check.side_effect = Exception("Test exception")

        self.monitor.register_component("test_component", mock_check)
        health = await self.monitor.check_component("test_component")

        self.assertEqual(health.status, ComponentStatus.CRITICAL)
        self.assertIn("Hiba", health.message)

    async def test_check_health_no_components(self) -> None:
        """Teszteli a rendszer egészségügyi állapotát komponensek nélkül."""
        health = await self.monitor.check_health()

        self.assertEqual(health.overall_status, HealthStatus.OK)
        self.assertEqual(len(health.components), 0)
        self.assertIsInstance(health.system_metrics, dict)

    async def test_check_health_with_healthy_components(self) -> None:
        """Teszteli a rendszer egészségügyi állapotát egészséges komponensekkel."""
        self.monitor.register_component("component1")
        self.monitor.register_component("component2")

        health = await self.monitor.check_health()

        self.assertEqual(health.overall_status, HealthStatus.OK)
        self.assertEqual(len(health.components), 2)
        self.assertTrue(
            all(c.status == ComponentStatus.HEALTHY for c in health.components)
        )

    async def test_check_health_with_warning_component(self) -> None:
        """Teszteli a rendszer egészségügyi állapotát figyelmeztető komponenssel."""
        mock_check: MagicMock = MagicMock()
        mock_check.check = AsyncMock(return_value=ComponentHealth(
            name="warning_component",
            status=ComponentStatus.WARNING,
            message="High memory usage",
            timestamp=datetime.now(),
        ))

        self.monitor.register_component("warning_component", mock_check)
        health = await self.monitor.check_health()

        self.assertEqual(health.overall_status, HealthStatus.DEGRADED)
        self.assertIn("figyelmeztetés", health.message.lower())

    async def test_check_health_with_critical_component(self) -> None:
        """Teszteli a rendszer egészségügyi állapotát kritikus komponenssel."""
        mock_check: MagicMock = MagicMock()
        mock_check.check = AsyncMock(return_value=ComponentHealth(
            name="critical_component",
            status=ComponentStatus.CRITICAL,
            message="Database connection failed",
            timestamp=datetime.now(),
        ))

        self.monitor.register_component("critical_component", mock_check)
        health = await self.monitor.check_health()

        self.assertEqual(health.overall_status, HealthStatus.CRITICAL)
        self.assertIn("kritikus", health.message.lower())

    async def test_check_health_mixed_components(self) -> None:
        """Teszteli a rendszer egészségügyi állapotát vegyes komponensekkel."""
        # Egészséges komponens
        self.monitor.register_component("healthy_component")

        # Figyelmeztető komponens
        warning_check: MagicMock = MagicMock()
        warning_check.check.return_value = ComponentHealth(
            name="warning_component",
            status=ComponentStatus.WARNING,
            message="High CPU usage",
            timestamp=datetime.now(),
        )
        self.monitor.register_component("warning_component", warning_check)

        health = await self.monitor.check_health()

        self.assertEqual(health.overall_status, HealthStatus.DEGRADED)
        self.assertEqual(len(health.components), 2)

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    @patch("psutil.disk_usage")
    @patch("psutil.net_io_counters")
    async def test_collect_system_metrics_success(
        self,
        mock_net_io: MagicMock,
        mock_disk: MagicMock,
        mock_memory: MagicMock,
        mock_cpu: MagicMock,
    ) -> None:
        """Teszteli a rendszer metrikák gyűjtését sikeres esetben."""
        # Mock adatok beállítása
        mock_cpu.return_value = 45.5
        mock_memory.return_value = MagicMock(
            percent=65.3, used=8 * 1024**3, total=16 * 1024**3
        )
        mock_disk.return_value = MagicMock(
            used=100 * 1024**3, total=500 * 1024**3
        )
        mock_net_io.return_value = MagicMock(bytes_sent=1024**2, bytes_recv=2 * 1024**2)

        health = await self.monitor.check_health()
        metrics = health.system_metrics

        self.assertIsNotNone(metrics)
        assert metrics is not None  # Type narrowing
        self.assertIn("cpu_percent", metrics)
        self.assertIn("memory_percent", metrics)
        self.assertIn("memory_used_gb", metrics)
        self.assertIn("memory_total_gb", metrics)
        self.assertIn("disk_percent", metrics)
        self.assertIn("disk_used_gb", metrics)
        self.assertIn("disk_total_gb", metrics)
        self.assertIn("net_bytes_sent_mb", metrics)
        self.assertIn("net_bytes_recv_mb", metrics)

        # Értékek ellenőrzése
        self.assertEqual(metrics["cpu_percent"], 45.5)
        self.assertEqual(metrics["memory_percent"], 65.3)
        self.assertEqual(metrics["memory_used_gb"], 8.0)
        self.assertEqual(metrics["memory_total_gb"], 16.0)

    @patch("psutil.cpu_percent")
    async def test_collect_system_metrics_with_exception(self, mock_cpu: MagicMock) -> None:
        """Teszteli a rendszer metrikák gyűjtését kivétel esetén."""
        mock_cpu.side_effect = Exception("CPU error")

        health = await self.monitor.check_health()
        metrics = health.system_metrics

        # Üres metrikákat kell kapnunk hiba esetén
        self.assertEqual(metrics, {})

    def test_register_component_with_logger(self) -> None:
        """Teszteli a komponens regisztrációt naplózóval."""
        mock_logger: MagicMock = MagicMock()
        monitor = HealthMonitor(logger=mock_logger)

        monitor.register_component("test_component")

        # Ellenőrizzük, hogy a logger info metódusa meghívásra került-e
        mock_logger.info.assert_called_once()

    def test_unregister_component_with_logger(self) -> None:
        """Teszteli a komponens eltávolítását naplózóval."""
        mock_logger: MagicMock = MagicMock()
        monitor = HealthMonitor(logger=mock_logger)

        monitor.register_component("test_component")
        monitor.unregister_component("test_component")

        # Ellenőrizzük, hogy a logger info metódusa meghívásra került-e
        self.assertEqual(mock_logger.info.call_count, 2)

    def test_register_duplicate_component(self) -> None:
        """Teszteli a duplikált komponens regisztrációját."""
        mock_logger: MagicMock = MagicMock()
        monitor = HealthMonitor(logger=mock_logger)

        monitor.register_component("test_component")
        monitor.register_component("test_component")  # Duplikált regisztráció

        # Ellenőrizzük, hogy a második regisztráció felülírja az elsőt
        components = monitor.get_registered_components()
        self.assertEqual(len(components), 1)
        # A warning hívás ellenőrzése
        mock_logger.warning.assert_called_once()

    async def test_check_health_with_exception_in_component_check(self) -> None:
        """Teszteli a check_health-t, ha egy komponens ellenőrzése kivételt dob."""
        mock_check: MagicMock = MagicMock()
        mock_check.check.side_effect = Exception("Komponens hiba")

        self.monitor.register_component("faulty_component", mock_check)
        health = await self.monitor.check_health()

        # A hibás komponensnek CRITICAL státuszúnak kell lennie
        self.assertEqual(health.overall_status, HealthStatus.CRITICAL)
        self.assertEqual(len(health.components), 1)
        self.assertEqual(health.components[0].status, ComponentStatus.CRITICAL)
        self.assertIn("Hiba", health.components[0].message)

    async def test_check_health_with_unknown_status_components(self) -> None:
        """Teszteli a check_health-t UNKNOWN státuszú komponensekkel."""
        mock_check: MagicMock = MagicMock()
        mock_check.check.return_value = ComponentHealth(
            name="unknown_component",
            status=ComponentStatus.UNKNOWN,
            message="Ismeretlen állapot",
            timestamp=datetime.now(),
        )

        self.monitor.register_component("unknown_component", mock_check)
        health = await self.monitor.check_health()

        self.assertEqual(health.overall_status, HealthStatus.UNKNOWN)
        self.assertIn("Ismeretlen", health.message)

    async def test_collect_system_metrics_with_disk_error(self) -> None:
        """Teszteli a rendszer metrikák gyűjtését lemez hiba esetén."""
        with patch("psutil.cpu_percent", return_value=50.0):
            with patch("psutil.virtual_memory") as mock_memory:
                mock_memory.return_value = MagicMock(
                    percent=65.3, used=8 * 1024**3, total=16 * 1024**3
                )
                with patch(
                    "psutil.disk_usage",
                    side_effect=PermissionError("Hozzáférés megtagadva")
                ):
                    with patch("psutil.net_io_counters") as mock_net:
                        mock_net.return_value = MagicMock(
                            bytes_sent=1024**2, bytes_recv=2 * 1024**2
                        )

                        health = await self.monitor.check_health()
                        metrics = health.system_metrics

                        # A lemez metrikák nem szerepelhetnek
                        assert metrics is not None
                        self.assertNotIn("disk_percent", metrics)
                        self.assertIn("cpu_percent", metrics)
                        self.assertIn("memory_percent", metrics)

    async def test_collect_system_metrics_with_net_error(self) -> None:
        """Teszteli a rendszer metrikák gyűjtését hálózat hiba esetén."""
        with patch("psutil.cpu_percent", return_value=50.0):
            with patch("psutil.virtual_memory") as mock_memory:
                mock_memory.return_value = MagicMock(
                    percent=65.3, used=8 * 1024**3, total=16 * 1024**3
                )
                with patch("psutil.disk_usage") as mock_disk:
                    mock_disk.return_value = MagicMock(
                        used=100 * 1024**3, total=500 * 1024**3
                    )
                    with patch("psutil.net_io_counters", side_effect=OSError("Hálózat hiba")):
                        health = await self.monitor.check_health()
                        metrics = health.system_metrics

                        # A hálózati metrikák nem szerepelhetnek
                        assert metrics is not None
                        self.assertNotIn("net_bytes_sent_mb", metrics)
                        self.assertIn("cpu_percent", metrics)
                        self.assertIn("disk_percent", metrics)

    async def test_default_health_check_with_logger(self) -> None:
        """Teszteli a DefaultHealthCheck loggerrel való használatát."""
        mock_logger: MagicMock = MagicMock()
        check = DefaultHealthCheck("test_component", mock_logger)

        self.assertEqual(check.get_name(), "test_component")
        health = await check.check()

        self.assertEqual(health.name, "test_component")
        self.assertEqual(health.status, ComponentStatus.HEALTHY)
        self.assertEqual(health.message, "Komponens egészséges")

    def test_unregister_component_logs_warning_when_not_registered(self) -> None:
        """Teszteli, hogy a nem regisztrált komponens eltávolítása warningot logol."""
        mock_logger: MagicMock = MagicMock()
        monitor = HealthMonitor(logger=mock_logger)

        monitor.unregister_component("nonexistent")

        # Ellenőrizzük, hogy a warning metódus meghívásra került-e
        mock_logger.warning.assert_called_once()

    async def test_collect_system_metrics_logs_error_on_exception(self) -> None:
        """Teszteli, hogy a rendszer metrikák gyűjtése error-t logol kivétel esetén."""
        mock_logger: MagicMock = MagicMock()
        monitor = HealthMonitor(logger=mock_logger)

        with patch("psutil.cpu_percent", side_effect=Exception("Általános hiba")):
            health = await monitor.check_health()
            metrics = health.system_metrics

            # Üres metrikákat kell kapnunk
            self.assertEqual(metrics, {})
            # Error log ellenőrzése
            mock_logger.error.assert_called_once()

    async def test_check_health_exception_in_for_loop_coverage(self) -> None:
        """Teszteli a check_health 77-87 sorainak kivételkezelését.

        Ez a teszt specifikusan a 77-87 sorok kivételkezelő blokkját fedi le.
        A kivételnek a check_health for ciklusában kell keletkeznie.
        """
        # Mockoljuk a check_component metódust, hogy kivételt dobjon
        with patch.object(self.monitor, 'check_component') as mock_check_component:
            mock_check_component.side_effect = RuntimeError("For loop exception")

            # Regisztrálunk egy komponenst
            self.monitor.register_component("test_component")

            # Ellenőrizzük az egészségügyi állapotot
            health = await self.monitor.check_health()

            # A rendszernek CRITICAL állapotúnak kell lennie
            self.assertEqual(health.overall_status, HealthStatus.CRITICAL)
            self.assertEqual(len(health.components), 1)

            # Ellenőrizzük a hibás komponenst
            error_component = health.components[0]
            self.assertEqual(error_component.name, "test_component")
            self.assertEqual(error_component.status, ComponentStatus.CRITICAL)
            self.assertIn("Hiba", error_component.message)
            self.assertIn("For loop exception", error_component.message)


    if __name__ == "__main__":
        unittest.main()
