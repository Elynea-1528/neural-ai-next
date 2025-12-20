"""Unit tests for Collector Factory component.

Tests cover:
- Collector creation (MT5)
- Configuration validation
- Error handling for invalid configurations
- Factory registration and retrieval

Author: Neural AI Next Team
Date: 2025-12-17
"""

import unittest

from neural_ai.collectors.mt5.error_handler import ConfigurationError
from neural_ai.collectors.mt5.implementations.collector_factory import (
    CollectorFactory,
    MT5Collector,
)


class TestCollectorFactory(unittest.TestCase):
    """Test cases for CollectorFactory class."""

    def setUp(self):
        """Set up test fixtures."""
        # Test configuration
        self.test_config = {
            "collector_type": "mt5",
            "mt5": {"host": "127.0.0.1", "port": 8000},
        }

    def test_register_collector(self):
        """Test registering a collector."""

        # Create custom collector class
        class CustomCollector:
            def __init__(self, config):
                self.config = config

        # Register
        CollectorFactory.register_collector("custom", CustomCollector)

        # Verify
        available = CollectorFactory.get_available_collectors()
        self.assertIn("custom", available)
        self.assertIn("mt5", available)

    def test_get_collector_mt5(self):
        """Test getting MT5 collector."""
        config = {"host": "127.0.0.1", "port": 8000}
        collector = CollectorFactory.get_collector("mt5", config)
        self.assertIsInstance(collector, MT5Collector)

    def test_get_collector_invalid_type(self):
        """Test invalid collector type."""
        config = {"data_dir": "/tmp/test_data"}
        with self.assertRaises(ConfigurationError):
            CollectorFactory.get_collector("invalid", config)

    def test_get_available_collectors(self):
        """Test getting available collectors."""
        collectors = CollectorFactory.get_available_collectors()
        self.assertIsInstance(collectors, list)
        self.assertIn("mt5", collectors)

    def test_register_duplicate_collector(self):
        """Test registering duplicate collector."""

        class CustomCollector:
            def __init__(self, config):
                self.config = config

        # First registration should work
        CollectorFactory.register_collector("test", CustomCollector)

        # Second registration should raise error
        with self.assertRaises(ConfigurationError):
            CollectorFactory.register_collector("test", CustomCollector)


if __name__ == "__main__":
    unittest.main()
