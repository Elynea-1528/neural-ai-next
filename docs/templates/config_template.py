"""Template for Neural-AI-Next configuration manager.

This template provides a base implementation for configuration management
with YAML support and dependency injection.
"""

import os
from typing import Any, Dict, Protocol

import yaml

from neural_ai.core.logger import LoggerInterface
from neural_ai.core.logger.implementations import LoggerFactory


class ConfigManagerInterface(Protocol):
    """Interface for configuration managers."""

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.

        Args:
            key: Configuration key (e.g. "app.debug")
            default: Default value if key not found

        Returns:
            Any: Configuration value or default
        """
        ...

    def get_section(self, section: str, default: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Get configuration section.

        Args:
            section: Section name
            default: Default section if not found

        Returns:
            Dict[str, Any]: Configuration section or default

        Raises:
            ConfigSectionNotFoundError: If section not found and no default provided
        """
        ...

    def get_all(self) -> Dict[str, Any]:
        """Get complete configuration.

        Returns:
            Dict[str, Any]: Complete configuration object
        """
        ...


class ConfigError(Exception):
    """Base exception for configuration errors."""


class ConfigNotFoundException(ConfigError):
    """Exception raised when configuration file is not found."""


class ConfigParseError(ConfigError):
    """Exception raised when configuration parsing fails."""


class ConfigSectionNotFoundError(ConfigError):
    """Exception raised when a configuration section is not found."""


class YAMLConfigManager:
    """YAML based configuration manager implementation."""

    def __init__(self, config_path: str, logger: LoggerInterface | None = None) -> None:
        """Initialize YAML configuration manager.

        Args:
            config_path: Path to the configuration file
            logger: Optional logger instance

        Raises:
            ConfigNotFoundException: If configuration file not found
            ConfigParseError: If configuration file is not valid YAML
        """
        self.config_path = config_path
        self.logger = logger or LoggerFactory.get_logger(__name__)
        self.config_data: Dict[str, Any] = {}

        # Load configuration file
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration file.

        Raises:
            ConfigNotFoundException: If configuration file not found
            ConfigParseError: If configuration file is not valid YAML
        """
        if not os.path.exists(self.config_path):
            raise ConfigNotFoundException(f"Configuration not found: {self.config_path}")

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config_data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ConfigParseError(f"Error parsing configuration: {str(e)}")
        except Exception as e:
            raise ConfigParseError(f"Unexpected error loading configuration: {str(e)}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.

        Args:
            key: Configuration key (e.g. "app.debug")
            default: Default value if key not found

        Returns:
            Any: Configuration value or default
        """
        # Handle nested keys (e.g. "app.debug")
        parts = key.split(".")
        value = self.config_data

        try:
            for part in parts:
                value = value.get(part, {})

            # If value is empty dict and this was the last key part, config doesn't exist
            if value == {} and parts[-1] in self.config_data:
                return default

            return value if value != {} else default
        except (AttributeError, KeyError):
            return default

    def get_section(self, section: str, default: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Get configuration section.

        Args:
            section: Section name
            default: Default section if not found

        Returns:
            Dict[str, Any]: Configuration section or default

        Raises:
            ConfigSectionNotFoundError: If section not found and no default provided
        """
        section_value = self.config_data.get(section, None)

        if section_value is None:
            if default is not None:
                return default
            raise ConfigSectionNotFoundError(f"Configuration section not found: {section}")

        return section_value

    def get_all(self) -> Dict[str, Any]:
        """Get complete configuration.

        Returns:
            Dict[str, Any]: Complete configuration object
        """
        return self.config_data


class ConfigManagerFactory:
    """Factory class for creating configuration managers."""

    @staticmethod
    def get_manager(
        config_path: str,
        format_type: str | None = None,
        create_if_not_exists: bool = False,
        logger: LoggerInterface | None = None,
    ) -> YAMLConfigManager:
        """Create configuration manager instance.

        Args:
            config_path: Path to configuration file
            format_type: Configuration format (yaml, json, ini, etc.)
            create_if_not_exists: Create config file if it doesn't exist
            logger: Optional logger instance

        Returns:
            YAMLConfigManager: Configuration manager instance

        Raises:
            ValueError: If format type not supported
        """
        log = logger or LoggerFactory.get_logger(__name__)

        # Try to determine format type from extension if not provided
        if format_type is None:
            _, ext = os.path.splitext(config_path)
            format_type = ext.lstrip(".").lower()

        # Create file if requested and doesn't exist
        if create_if_not_exists and not os.path.exists(config_path):
            log.info(f"Creating default config file: {config_path}")
            return ConfigManagerFactory.create_default_config(config_path, format_type, logger)

        # Handle supported formats
        if format_type in ["yaml", "yml"]:
            return YAMLConfigManager(config_path, logger)
        # Add support for other formats here...
        else:
            log.error(f"Unsupported config format: {format_type}")
            raise ValueError(f"Unsupported config format: {format_type}")

    @staticmethod
    def create_default_config(
        config_path: str,
        format_type: str,
        logger: LoggerInterface | None = None,
    ) -> YAMLConfigManager:
        """Create default configuration.

        Args:
            config_path: Path to configuration file
            format_type: Configuration format
            logger: Optional logger instance

        Returns:
            YAMLConfigManager: Configuration manager with default config

        Raises:
            ValueError: If format type not supported
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(config_path), exist_ok=True)

        # Default configuration
        default_config = {
            "app": {"name": "neural-ai-next", "version": "1.0.0", "environment": "development"},
            "logging": {
                "level": "INFO",
                "file": "logs/app.log",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
            "storage": {"path": "data/", "format": "parquet"},
        }

        # Save configuration in appropriate format
        if format_type in ["yaml", "yml"]:
            with open(config_path, "w", encoding="utf-8") as f:
                yaml.dump(default_config, f, default_flow_style=False)
            return YAMLConfigManager(config_path, logger)
        # Add support for other formats here...
        else:
            raise ValueError(f"Unsupported config format: {format_type}")
