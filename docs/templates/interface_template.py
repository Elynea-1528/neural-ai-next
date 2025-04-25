"""Template for Neural-AI-Next interfaces.

This file contains a general interface template that can be used
as a base for defining new component interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

from neural_ai.core.logger import LoggerInterface


class ComponentInterface(ABC):
    """Description of component interface.

    This interface defines the basic functionality and API
    provided by a component.
    """

    @abstractmethod
    def main_operation(self, input_data: Any) -> Any:
        """Execute main operation.

        Args:
            input_data: Input data for processing

        Returns:
            Processed output data

        Raises:
            ComponentException: When processing fails
        """
        pass

    @abstractmethod
    def get_configuration(self) -> Dict[str, Any]:
        """Get component configuration.

        Returns:
            Current component configuration
        """
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get component status.

        Returns:
            Current component status
        """
        pass


class ComponentFactoryInterface(ABC):
    """Component factory interface.

    This interface defines the common API for factory objects
    that create component instances.
    """

    @staticmethod
    @abstractmethod
    def create_component(
        config: Dict[str, Any],
        logger: LoggerInterface | None = None,
    ) -> "ComponentInterface":
        """Create component instance.

        Args:
            config: Component configuration
            logger: Optional logger instance

        Returns:
            ComponentInterface: New component instance

        Raises:
            ValueError: If configuration is invalid
        """
        pass

    @staticmethod
    @abstractmethod
    def get_component_types() -> list[str]:
        """Get available component types.

        Returns:
            List of component types supported by the factory
        """
        pass


class ComponentException(Exception):
    """Component specific exception.

    Exception raised by components implementing the interface.
    """


class InterfaceTemplate(ABC):
    """Base interface template."""

    @abstractmethod
    def method1(self) -> None:
        """Execute first abstract method."""
        pass

    @abstractmethod
    def method2(self, param1: str) -> Dict[str, Any]:
        """Execute second abstract method.

        Args:
            param1: First parameter

        Returns:
            Dict[str, Any]: Return value
        """
        pass
