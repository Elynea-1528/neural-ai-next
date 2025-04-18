"""Kivételek a konfigurációkezelő modulhoz."""


class ConfigError(Exception):
    """Alap kivétel a konfigurációkezelő hibákhoz."""


class ConfigLoadError(ConfigError):
    """Konfiguráció betöltési hiba."""


class ConfigSaveError(ConfigError):
    """Konfiguráció mentési hiba."""


class ConfigValidationError(ConfigError):
    """Konfiguráció validációs hiba."""


class ConfigTypeError(ConfigError):
    """Típus hiba a konfigurációban."""


class ConfigKeyError(ConfigError):
    """Kulcs hiba a konfigurációban."""
