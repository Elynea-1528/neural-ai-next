"""Processors konfigurációs teszt.

A processors.yaml konfigurációs fájl betöltésének és használatának tesztjei.
"""

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface


class TestProcessorsConfig:
    """Processors konfigurációs osztály tesztjei."""

    @pytest.fixture
    def config_manager(self) -> "ConfigManagerInterface":
        """Konfiguráció kezelő példány létrehozása."""
        from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager

        manager = YAMLConfigManager(filename="configs/processors.yaml")
        return manager

    def test_processors_config_loaded(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli, hogy a processors konfiguráció sikeresen betöltődött."""
        # Ellenőrizzük, hogy a processors szekció létezik
        processors = config_manager.get("processors")
        assert processors is not None
        assert isinstance(processors, dict)

    def test_d01_processor_config_exists(self, config_manager):
        """Teszteli, hogy a d01 processor konfigurációja létezik."""
        d01_config = config_manager.get("processors", "d01")
        assert d01_config is not None
        assert isinstance(d01_config, dict)

    def test_required_timeframes_config(self, config_manager):
        """Teszteli a required_timeframes konfigurációt."""
        required_timeframes = config_manager.get("processors", "d01", "required_timeframes")
        assert required_timeframes is not None
        assert isinstance(required_timeframes, list)
        assert len(required_timeframes) == 7

        expected_timeframes = ["tick", "1m", "5m", "15m", "1h", "4h", "1d"]
        assert required_timeframes == expected_timeframes

    def test_timeframe_configs_structure(self, config_manager):
        """Teszteli a timeframe_configs struktúrát."""
        timeframe_configs = config_manager.get("processors", "d01", "timeframe_configs")
        assert timeframe_configs is not None
        assert isinstance(timeframe_configs, dict)

    def test_tick_timeframe_config(self, config_manager):
        """Teszteli a tick timeframe konfigurációt."""
        tick_config = config_manager.get("processors", "d01", "timeframe_configs", "tick")
        assert tick_config is not None
        assert isinstance(tick_config, dict)
        assert tick_config["z_score_window"] == 2000

    def test_1m_timeframe_config(self, config_manager):
        """Teszteli az 1m timeframe konfigurációt."""
        m1_config = config_manager.get("processors", "d01", "timeframe_configs", "1m")
        assert m1_config is not None
        assert isinstance(m1_config, dict)
        assert m1_config["z_score_window"] == 60

    def test_general_z_score_window_config(self, config_manager):
        """Teszteli az általános z_score_window konfigurációt."""
        z_score_window = config_manager.get("processors", "d01", "z_score_window")
        assert z_score_window == 60
        assert isinstance(z_score_window, int)

    def test_calc_shadows_config(self, config_manager):
        """Teszteli a calc_shadows konfigurációt."""
        calc_shadows = config_manager.get("processors", "d01", "calc_shadows")
        assert calc_shadows is True
        assert isinstance(calc_shadows, bool)

    def test_timeframe_configs_keys_exist(self, config_manager):
        """Teszteli, hogy a timeframe_configs-ban a megfelelő kulcsok léteznek."""
        timeframe_configs = config_manager.get("processors", "d01", "timeframe_configs")
        assert "tick" in timeframe_configs
        assert "1m" in timeframe_configs

    def test_timeframe_configs_z_score_window_type(self, config_manager):
        """Teszteli, hogy a timeframe-specifikus z_score_window értékek helyes típusúak."""
        tick_window = config_manager.get(
            "processors", "d01", "timeframe_configs", "tick", "z_score_window"
        )
        m1_window = config_manager.get(
            "processors", "d01", "timeframe_configs", "1m", "z_score_window"
        )

        assert isinstance(tick_window, int)
        assert isinstance(m1_window, int)

    def test_config_section_accessible_via_get_section(self, config_manager):
        """Teszteli a konfigurációs szekció lekérését get_section metódussal."""
        processors_section = config_manager.get_section("processors")
        assert "d01" in processors_section

        d01_section = processors_section["d01"]
        assert "required_timeframes" in d01_section
        assert "timeframe_configs" in d01_section
        assert "z_score_window" in d01_section
        assert "calc_shadows" in d01_section
