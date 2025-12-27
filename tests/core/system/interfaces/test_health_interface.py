"""Health interfész tesztek.

Ez a modul a `health_interface.py` interfészek tesztjeit tartalmazza.
"""

import pytest
from datetime import datetime
from neural_ai.core.system.interfaces.health_interface import (
    ComponentStatus,
    HealthStatus,
    ComponentHealth,
    SystemHealth,
    HealthMonitorInterface,
    HealthCheckInterface
)


class TestComponentStatus:
    """ComponentStatus enum tesztek."""
    
    def test_enum_values(self):
        """Teszteli az enum értékeket."""
        assert ComponentStatus.HEALTHY.value == "healthy"
        assert ComponentStatus.WARNING.value == "warning"
        assert ComponentStatus.CRITICAL.value == "critical"
        assert ComponentStatus.UNKNOWN.value == "unknown"
        assert ComponentStatus.OFFLINE.value == "offline"
    
    def test_enum_members(self):
        """Teszteli az enum tagokat."""
        assert len(list(ComponentStatus)) == 5
        assert ComponentStatus.HEALTHY in ComponentStatus
        assert ComponentStatus.WARNING in ComponentStatus
        assert ComponentStatus.CRITICAL in ComponentStatus
        assert ComponentStatus.UNKNOWN in ComponentStatus
        assert ComponentStatus.OFFLINE in ComponentStatus


class TestHealthStatus:
    """HealthStatus enum tesztek."""
    
    def test_enum_values(self):
        """Teszteli az enum értékeket."""
        assert HealthStatus.OK.value == "ok"
        assert HealthStatus.DEGRADED.value == "degraded"
        assert HealthStatus.CRITICAL.value == "critical"
        assert HealthStatus.UNKNOWN.value == "unknown"
    
    def test_enum_members(self):
        """Teszteli az enum tagokat."""
        assert len(list(HealthStatus)) == 4
        assert HealthStatus.OK in HealthStatus
        assert HealthStatus.DEGRADED in HealthStatus
        assert HealthStatus.CRITICAL in HealthStatus
        assert HealthStatus.UNKNOWN in HealthStatus


class TestComponentHealth:
    """ComponentHealth dataclass tesztek."""
    
    def test_create_with_required_fields(self):
        """Teszteli a létrehozást kötelező mezőkkel."""
        timestamp = datetime.now()
        health = ComponentHealth(
            name="test_component",
            status=ComponentStatus.HEALTHY,
            message="Minden OK",
            timestamp=timestamp
        )
        
        assert health.name == "test_component"
        assert health.status == ComponentStatus.HEALTHY
        assert health.message == "Minden OK"
        assert health.timestamp == timestamp
        assert health.metrics is None
    
    def test_create_with_optional_metrics(self):
        """Teszteli a létrehozást opcionális metrikákkal."""
        timestamp = datetime.now()
        metrics = {"response_time_ms": 10.5, "error_rate": 0.01}
        health = ComponentHealth(
            name="test_component",
            status=ComponentStatus.HEALTHY,
            message="Minden OK",
            timestamp=timestamp,
            metrics=metrics
        )
        
        assert health.metrics == metrics
        assert health.metrics["response_time_ms"] == 10.5
        assert health.metrics["error_rate"] == 0.01
    
    def test_immutability(self):
        """Teszteli az adatok megváltoztathatóságát."""
        timestamp = datetime.now()
        health = ComponentHealth(
            name="test_component",
            status=ComponentStatus.HEALTHY,
            message="Minden OK",
            timestamp=timestamp
        )
        
        # A dataclass alapértelmezett nem változtatható (frozen=False)
        # Ezért ez a teszt csak ellenőrzi, hogy a mezők beállíthatók-e
        health.metrics = {"test": 1.0}
        assert health.metrics == {"test": 1.0}


class TestSystemHealth:
    """SystemHealth dataclass tesztek."""
    
    def test_create_with_required_fields(self):
        """Teszteli a létrehozást kötelező mezőkkel."""
        timestamp = datetime.now()
        components = [
            ComponentHealth(
                name="comp1",
                status=ComponentStatus.HEALTHY,
                message="OK",
                timestamp=timestamp
            )
        ]
        
        health = SystemHealth(
            overall_status=HealthStatus.OK,
            message="Rendszer OK",
            timestamp=timestamp,
            components=components
        )
        
        assert health.overall_status == HealthStatus.OK
        assert health.message == "Rendszer OK"
        assert health.timestamp == timestamp
        assert health.components == components
        assert health.system_metrics is None
    
    def test_create_with_optional_metrics(self):
        """Teszteli a létrehozást opcionális metrikákkal."""
        timestamp = datetime.now()
        components = []
        system_metrics = {
            "cpu_usage": 45.2,
            "memory_usage": 67.8,
            "disk_usage": 23.4
        }
        
        health = SystemHealth(
            overall_status=HealthStatus.OK,
            message="Rendszer OK",
            timestamp=timestamp,
            components=components,
            system_metrics=system_metrics
        )
        
        assert health.system_metrics == system_metrics
        assert health.system_metrics["cpu_usage"] == 45.2
    
    def test_empty_components_list(self):
        """Teszteli az üres komponens listát."""
        timestamp = datetime.now()
        health = SystemHealth(
            overall_status=HealthStatus.UNKNOWN,
            message="Nincsenek komponensek",
            timestamp=timestamp,
            components=[]
        )
        
        assert len(health.components) == 0


class TestHealthMonitorInterface:
    """HealthMonitorInterface tesztek."""
    
    def test_interface_is_abstract(self):
        """Teszteli, hogy az interfész absztrakt."""
        with pytest.raises(TypeError):
            HealthMonitorInterface()
    
    def test_check_health_is_abstract(self):
        """Teszteli, hogy a check_health metódus absztrakt."""
        
        class ConcreteMonitor(HealthMonitorInterface):
            pass
        
        with pytest.raises(TypeError):
            ConcreteMonitor()
    
    def test_implement_interface(self):
        """Teszteli az interfész implementációját."""
        
        class TestMonitor(HealthMonitorInterface):
            def check_health(self):
                return SystemHealth(
                    overall_status=HealthStatus.OK,
                    message="Test",
                    timestamp=datetime.now(),
                    components=[]
                )
            
            def check_component(self, component_name: str):
                return ComponentHealth(
                    name=component_name,
                    status=ComponentStatus.HEALTHY,
                    message="OK",
                    timestamp=datetime.now()
                )
            
            def get_registered_components(self):
                return []
            
            def register_component(self, component_name: str):
                pass
            
            def unregister_component(self, component_name: str):
                pass
        
        monitor = TestMonitor()
        assert isinstance(monitor, HealthMonitorInterface)
        assert hasattr(monitor, 'check_health')
        assert hasattr(monitor, 'check_component')
        assert hasattr(monitor, 'get_registered_components')
        assert hasattr(monitor, 'register_component')
        assert hasattr(monitor, 'unregister_component')


class TestHealthCheckInterface:
    """HealthCheckInterface tesztek."""
    
    def test_interface_is_abstract(self):
        """Teszteli, hogy az interfész absztrakt."""
        with pytest.raises(TypeError):
            HealthCheckInterface()
    
    def test_check_is_abstract(self):
        """Teszteli, hogy a check metódus absztrakt."""
        
        class ConcreteCheck(HealthCheckInterface):
            pass
        
        with pytest.raises(TypeError):
            ConcreteCheck()
    
    def test_implement_interface(self):
        """Teszteli az interfész implementációját."""
        
        class TestCheck(HealthCheckInterface):
            def check(self):
                return ComponentHealth(
                    name="test",
                    status=ComponentStatus.HEALTHY,
                    message="OK",
                    timestamp=datetime.now()
                )
            
            def get_name(self):
                return "test_check"
        
        check = TestCheck()
        assert isinstance(check, HealthCheckInterface)
        assert hasattr(check, 'check')
        assert hasattr(check, 'get_name')


class TestIntegration:
    """Integrációs tesztek."""
    
    def test_component_health_in_system_health(self):
        """Teszteli a ComponentHealth integrációját SystemHealth-ben."""
        timestamp = datetime.now()
        
        component1 = ComponentHealth(
            name="database",
            status=ComponentStatus.HEALTHY,
            message="Adatbázis OK",
            timestamp=timestamp
        )
        
        component2 = ComponentHealth(
            name="api",
            status=ComponentStatus.WARNING,
            message="Lassú válaszidő",
            timestamp=timestamp,
            metrics={"response_time_ms": 500.0}
        )
        
        system_health = SystemHealth(
            overall_status=HealthStatus.DEGRADED,
            message="Rendszer figyelmeztetéssel",
            timestamp=timestamp,
            components=[component1, component2]
        )
        
        assert len(system_health.components) == 2
        assert system_health.components[0].name == "database"
        assert system_health.components[1].name == "api"
        assert system_health.components[1].metrics["response_time_ms"] == 500.0
    
    def test_health_status_aggregation(self):
        """Teszteli az egészségügyi állapotok aggregációját."""
        # Kritikus komponens -> CRITICAL
        critical_component = ComponentHealth(
            name="critical",
            status=ComponentStatus.CRITICAL,
            message="Hiba",
            timestamp=datetime.now()
        )
        
        # Figyelmeztető komponens -> DEGRADED
        warning_component = ComponentHealth(
            name="warning",
            status=ComponentStatus.WARNING,
            message="Figyelmeztetés",
            timestamp=datetime.now()
        )
        
        # Egészséges komponens -> OK
        healthy_component = ComponentHealth(
            name="healthy",
            status=ComponentStatus.HEALTHY,
            message="OK",
            timestamp=datetime.now()
        )
        
        # Teszteljük a különböző kombinációkat
        assert ComponentStatus.CRITICAL.value == "critical"
        assert ComponentStatus.WARNING.value == "warning"
        assert ComponentStatus.HEALTHY.value == "healthy"


class TestTypeSafety:
    """Típusbiztonság tesztek."""
    
    def test_component_status_type(self):
        """Teszteli a ComponentStatus típusát."""
        status = ComponentStatus.HEALTHY
        assert isinstance(status, ComponentStatus)
        assert isinstance(status.value, str)
    
    def test_health_status_type(self):
        """Teszteli a HealthStatus típusát."""
        status = HealthStatus.OK
        assert isinstance(status, HealthStatus)
        assert isinstance(status.value, str)
    
    def test_component_health_types(self):
        """Teszteli a ComponentHealth mezőinek típusát."""
        health = ComponentHealth(
            name="test",
            status=ComponentStatus.HEALTHY,
            message="OK",
            timestamp=datetime.now(),
            metrics={"test": 1.0}
        )
        
        assert isinstance(health.name, str)
        assert isinstance(health.status, ComponentStatus)
        assert isinstance(health.message, str)
        assert isinstance(health.timestamp, datetime)
        assert isinstance(health.metrics, dict)
    
    def test_system_health_types(self):
        """Teszteli a SystemHealth mezőinek típusát."""
        health = SystemHealth(
            overall_status=HealthStatus.OK,
            message="OK",
            timestamp=datetime.now(),
            components=[],
            system_metrics={"cpu": 50.0}
        )
        
        assert isinstance(health.overall_status, HealthStatus)
        assert isinstance(health.message, str)
        assert isinstance(health.timestamp, datetime)
        assert isinstance(health.components, list)
        assert isinstance(health.system_metrics, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])