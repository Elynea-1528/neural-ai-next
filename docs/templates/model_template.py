"""Template a Neural-AI-Next modellekhez."""

import logging
from typing import Any, Dict, List, Optional  # noqa: F401 - Sablon részeként szerepel

import numpy as np  # noqa: F401 - Sablon részeként szerepel
import torch
import torch.nn as nn
from torch.utils.data import DataLoader  # noqa: F401 - Sablon részeként szerepel

from neural_ai.core.logger import LoggerInterface


class ModelTemplate(nn.Module):
    """Alap modell template."""

    def __init__(self, config: Dict[str, Any], logger: LoggerInterface = None):
        """
        ModelTemplate inicializálása.

        Args:
            config: Modell konfiguráció
            logger: Logger példány
        """
        super().__init__()
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("ModelTemplate inicializálva")

        # Modell rétegek definiálása
        self.fc1 = nn.Linear(config.get("input_size", 10), config.get("hidden_size", 20))
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(config.get("hidden_size", 20), config.get("output_size", 1))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.

        Args:
            x: Bemeneti tenzor

        Returns:
            torch.Tensor: Kimeneti tenzor
        """
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

    def save(self, path: str) -> None:
        """
        Modell mentése.

        Args:
            path: Mentési útvonal
        """
        self.logger.info(f"Modell mentése: {path}")
        torch.save({"state_dict": self.state_dict(), "config": self.config}, path)

    def load(self, path: str) -> None:
        """
        Modell betöltése.

        Args:
            path: Betöltési útvonal
        """
        self.logger.info(f"Modell betöltése: {path}")
        checkpoint = torch.load(path)
        self.load_state_dict(checkpoint["state_dict"])
