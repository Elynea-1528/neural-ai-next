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
        # Ellenőrizzük, hogy a d01 szekció létezik (nincs 'processors' gyökér kulcs)
        d01 = config_manager.get("d01")
        assert d01 is not None
        assert isinstance(d01, dict)

    def test_d01_processor_config_exists(self, config_manager):
        """Teszteli, hogy a d01 processor konfigurációja létezik."""
        d01_config = config_manager.get("d01")
        assert d01_config is not None
        assert isinstance(d01_config, dict)

    def test_required_timeframes_config(self, config_manager):
        """Teszteli a required_timeframes konfigurációt."""
        required_timeframes = config_manager.get("d01", "required_timeframes")
        assert required_timeframes is not None
        assert isinstance(required_timeframes, list)
        assert len(required_timeframes) == 7

        expected_timeframes = ["tick", "1m", "5m", "15m", "1h", "4h", "1d"]
        assert required_timeframes == expected_timeframes

    def test_timeframe_configs_structure(self, config_manager):
        """Teszteli a timeframe_configs struktúrát."""
        timeframe_configs = config_manager.get("d01", "timeframe_configs")
        assert timeframe_configs is not None
        assert isinstance(timeframe_configs, dict)

    def test_tick_timeframe_config(self, config_manager):
        """Teszteli a tick timeframe konfigurációt."""
        tick_config = config_manager.get("d01", "timeframe_configs", "tick")
        assert tick_config is not None
        assert isinstance(tick_config, dict)
        assert tick_config["z_score_window"] == 2000

    def test_1m_timeframe_config(self, config_manager):
        """Teszteli az 1m timeframe konfigurációt."""
        m1_config = config_manager.get("d01", "timeframe_configs", "1m")
        assert m1_config is not None
        assert isinstance(m1_config, dict)
        assert m1_config["z_score_window"] == 60

    def test_general_z_score_window_config(self, config_manager):
        """Teszteli az általános z_score_window konfigurációt."""
        z_score_window = config_manager.get("d01", "z_score_window")
        assert z_score_window == 60
        assert isinstance(z_score_window, int)

    def test_calc_shadows_config(self, config_manager):
        """Teszteli a calc_shadows konfigurációt."""
        calc_shadows = config_manager.get("d01", "calc_shadows")
        assert calc_shadows is True
        assert isinstance(calc_shadows, bool)

    def test_timeframe_configs_keys_exist(self, config_manager):
        """Teszteli, hogy a timeframe_configs-ban a megfelelő kulcsok léteznek."""
        timeframe_configs = config_manager.get("d01", "timeframe_configs")
        assert "tick" in timeframe_configs
        assert "1m" in timeframe_configs

    def test_timeframe_configs_z_score_window_type(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli, hogy a timeframe-specifikus z_score_window értékek helyes típusúak."""
        tick_window = config_manager.get(
            "d01", "timeframe_configs", "tick", "z_score_window"
        )
        m1_window = config_manager.get(
            "d01", "timeframe_configs", "1m", "z_score_window"
        )

        assert isinstance(tick_window, int)
        assert isinstance(m1_window, int)

    def test_config_section_accessible_via_get_section(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli a konfigurációs szekció lekérését get_section metódussal."""
        d01_section = config_manager.get_section("d01")
        assert "required_timeframes" in d01_section
        assert "timeframe_configs" in d01_section
        assert "z_score_window" in d01_section
        assert "calc_shadows" in d01_section

    def test_d02_processor_config_exists(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli, hogy a d02 processor konfigurációja létezik."""
        d02_config = config_manager.get("d02")
        assert d02_config is not None
        assert isinstance(d02_config, dict)

    def test_d02_swing_window_config(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli a d02 swing_window konfigurációt."""
        swing_window = config_manager.get("d02", "swing_window")
        assert swing_window == 5
        assert isinstance(swing_window, int)

    def test_d02_min_distance_config(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli a d02 min_distance konfigurációt."""
        min_distance = config_manager.get("d02", "min_distance")
        assert min_distance == 10
        assert isinstance(min_distance, int)

    def test_d02_use_close_open_config(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli a d02 use_close_open konfigurációt."""
        use_close_open = config_manager.get("d02", "use_close_open")
        assert use_close_open is True
        assert isinstance(use_close_open, bool)

    def test_d02_use_high_low_config(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli a d02 use_high_low konfigurációt."""
        use_high_low = config_manager.get("d02", "use_high_low")
        assert use_high_low is True
        assert isinstance(use_high_low, bool)

    def test_d02_primary_weight_config(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli a d02 primary_weight konfigurációt."""
        primary_weight = config_manager.get("d02", "primary_weight")
        assert primary_weight == 0.7
        assert isinstance(primary_weight, float)

    def test_d02_secondary_weight_config(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli a d02 secondary_weight konfigurációt."""
        secondary_weight = config_manager.get("d02", "secondary_weight")
        assert secondary_weight == 0.3
        assert isinstance(secondary_weight, float)

    def test_d02_level_merge_config(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli a d02 level_merge konfigurációt."""
        level_merge = config_manager.get("d02", "level_merge")
        assert level_merge == 0.0005
        assert isinstance(level_merge, float)

    def test_d02_min_touches_config(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli a d02 min_touches konfigurációt."""
        min_touches = config_manager.get("d02", "min_touches")
        assert min_touches == 2
        assert isinstance(min_touches, int)

    def test_d02_volume_confirmation_config(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli a d02 volume_confirmation konfigurációt."""
        volume_confirmation = config_manager.get("d02", "volume_confirmation")
        assert volume_confirmation is True
        assert isinstance(volume_confirmation, bool)

    def test_d02_strength_window_config(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli a d02 strength_window konfigurációt."""
        strength_window = config_manager.get("d02", "strength_window")
        assert strength_window == 100
        assert isinstance(strength_window, int)

    def test_d02_timeframe_configs_structure(
        self, config_manager: "ConfigManagerInterface"
    ) -> None:
        """Teszteli a d02 timeframe_configs struktúrát."""
        timeframe_configs = config_manager.get("d02", "timeframe_configs")
        assert timeframe_configs is not None
        assert isinstance(timeframe_configs, dict)
        assert "M1" in timeframe_configs
        assert "H1" in timeframe_configs
        assert "D1" in timeframe_configs

    def test_d02_m1_timeframe_config(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli a d02 M1 timeframe konfigurációt."""
        m1_config = config_manager.get("d02", "timeframe_configs", "M1")
        assert m1_config is not None
        assert isinstance(m1_config, dict)
        assert m1_config["swing_window"] == 5

    def test_d02_h1_timeframe_config(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli a d02 H1 timeframe konfigurációt."""
        h1_config = config_manager.get("d02", "timeframe_configs", "H1")
        assert h1_config is not None
        assert isinstance(h1_config, dict)
        assert h1_config["swing_window"] == 5

    def test_d02_d1_timeframe_config(self, config_manager: "ConfigManagerInterface") -> None:
        """Teszteli a d02 D1 timeframe konfigurációt."""
        d1_config = config_manager.get("d02", "timeframe_configs", "D1")
        assert d1_config is not None
        assert isinstance(d1_config, dict)
        assert d1_config["swing_window"] == 3
