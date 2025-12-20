"""Template for components in the Neural-AI-Next project.

This file contains a general component implementation template
that can be used as a base when creating new components.
"""

import logging
from typing import Any

from neural_ai.core.logger import LoggerInterface
from neural_ai.core.logger.implementations import LoggerFactory


class ComponentTemplate:
    """Base template component class."""

    def __init__(self, config: dict[str, Any], logger: LoggerInterface | None = None) -> None:
        """Initialize ComponentTemplate.

        Args:
            config: Component configuration
            logger: Logger instance
        """
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("ComponentTemplate initialized")

    def run(self) -> dict[str, Any]:
        """Run the component.

        Returns:
            Dict[str, Any]: Component output
        """
        self.logger.info("Running ComponentTemplate")
        return {"status": "success"}


class ComponentName:
    """Component description.

    Detailed explanation of the component's responsibility. Write here the
    general description of the component's functions, purpose and usage.

    Attributes:
        config: The component's configuration
        logger: Logger instance
        dependencies: Description of other dependencies
    """

    def __init__(self, config: dict[str, Any], logger: LoggerInterface | None = None) -> None:
        """Initialize the component.

        Args:
            config: Component configuration
            logger: Logger instance or None (default logger will be created)
        """
        self.config = config
        self.logger = logger or LoggerFactory.get_logger(__name__)

        # Read configuration values
        self.parameter1 = config.get("parameter1", "default_value")
        self.parameter2 = config.get("parameter2", 100)

        # Initialize dependencies
        self._init_dependencies()

        self.logger.info(
            f"{self.__class__.__name__} initialized with "
            f"parameter1={self.parameter1}, parameter2={self.parameter2}"
        )

    def _init_dependencies(self) -> None:
        """Initialize internal dependencies."""
        # Example: initialize storage
        # storage_config = self.config.get("storage", {})
        # self.storage = StorageFactory.get_storage(storage_config)
        pass

    def main_method(self, input_data: Any) -> Any:
        """Process the input data.

        Args:
            input_data: Input data to process

        Returns:
            Processed output data

        Raises:
            ComponentException: When processing fails
        """
        self.logger.debug(f"Processing input data: {input_data}")

        try:
            # Implement processing
            result = self._process(input_data)

            self.logger.info(f"Successfully processed data, result shape: {len(result)}")
            return result

        except Exception as e:
            self.logger.error(f"Error processing data: {str(e)}")
            raise ComponentException(f"Processing failed: {str(e)}") from e

    def _process(self, data: Any) -> Any:
        """Process the data internally.

        Args:
            data: Data to process

        Returns:
            Processed data
        """
        # Implementation...
        return data


class ComponentException(Exception):
    """Component specific exception."""


# Factory example
class ComponentNameFactory:
    """Factory class for creating component instances."""

    @staticmethod
    def create_component(
        config: dict[str, Any], logger: LoggerInterface | None = None
    ) -> "ComponentName":
        """Create a new component instance.

        Args:
            config: Component configuration
            logger: Optional logger instance

        Returns:
            ComponentName: New component instance
        """
        return ComponentName(config, logger)
