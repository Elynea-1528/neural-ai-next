#!/usr/bin/env python3
"""Simple script to run the MT5 Collector.

Usage:
    python scripts/run_collector.py
"""

import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from neural_ai.collectors.mt5 import CollectorFactory
from neural_ai.core.config import ConfigManagerFactory


def main():
    """Run the MT5 Collector."""
    print("=" * 50)
    print("MT5 Collector - Starting...")
    print("=" * 50)

    try:
        # Create collector using Factory pattern
        config_path = project_root / "configs" / "collector_config.yaml"
        config_manager = ConfigManagerFactory.get_manager(filename=str(config_path))

        # Get collector configuration
        try:
            collector_config = config_manager.get_section("collector")
        except KeyError:
            collector_config = {}
        collector_config["config_path"] = str(config_path)

        # Create collector using Factory
        collector = CollectorFactory.get_collector("mt5", collector_config)

        # Run the server
        collector.run(host="0.0.0.0", port=8000)

    except KeyboardInterrupt:
        print("\n\nMT5 Collector stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError starting MT5 Collector: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
