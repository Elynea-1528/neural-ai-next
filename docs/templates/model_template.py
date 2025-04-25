"""Template for Neural-AI-Next models.

This template provides a base PyTorch model implementation with logging support.
"""

from typing import Any, Dict

import torch
import torch.nn as nn

from neural_ai.core.logger import LoggerInterface
from neural_ai.core.logger.implementations import LoggerFactory


class ModelTemplate(nn.Module):
    """Base model template with standard PyTorch architecture."""

    def __init__(self, config: Dict[str, Any], logger: LoggerInterface | None = None) -> None:
        """Initialize ModelTemplate.

        Args:
            config: Model configuration dictionary
            logger: Optional logger instance
        """
        super().__init__()
        self.config = config
        self.logger = logger or LoggerFactory.get_logger(__name__)
        self.logger.info("ModelTemplate initialized")

        # Define model layers
        self.fc1 = nn.Linear(config.get("input_size", 10), config.get("hidden_size", 20))
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(config.get("hidden_size", 20), config.get("output_size", 1))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Execute forward pass.

        Args:
            x: Input tensor

        Returns:
            torch.Tensor: Output tensor
        """
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

    def save(self, path: str) -> None:
        """Save model to file.

        Args:
            path: Path to save the model
        """
        self.logger.info(f"Saving model to: {path}")
        torch.save({"state_dict": self.state_dict(), "config": self.config}, path)

    def load(self, path: str) -> None:
        """Load model from file.

        Args:
            path: Path to load the model from
        """
        self.logger.info(f"Loading model from: {path}")
        checkpoint = torch.load(path)
        self.load_state_dict(checkpoint["state_dict"])

    def get_config(self) -> Dict[str, Any]:
        """Get model configuration.

        Returns:
            Dict[str, Any]: Model configuration dictionary
        """
        return self.config

    def get_parameters(self) -> Dict[str, Any]:
        """Get model parameters.

        Returns:
            Dict[str, Any]: Dictionary containing model parameters info
        """
        return {
            "input_size": self.fc1.in_features,
            "hidden_size": self.fc1.out_features,
            "output_size": self.fc2.out_features,
            "total_params": sum(p.numel() for p in self.parameters()),
        }
