#!/usr/bin/env python3
"""
JForex Live Probe - Reality Check Script
========================================
Manual test script to verify Bi5Downloader works with real Dukascopy server.

This script:
1. Bootstraps the core system
2. Creates a Bi5Downloader instance via factory
3. Downloads real tick data for EURUSD on 2024-06-01 10:00:00
4. Displays the first 5 TickData objects or error details
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from neural_ai.core.config.factory import ConfigManagerFactory
from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.core.events.factory import EventBusFactory
from neural_ai.collectors.jforex.factory import JForexFactory


async def main():
    """Main test function."""
    print("=" * 80)
    print("🚀 JFOREX LIVE PROBE - REALITY CHECK")
    print("=" * 80)
    print()
    
    try:
        # 1. Bootstrap Core System
        print("📦 Bootstrapping core system...")
        config = ConfigManagerFactory.get_manager("configs/system.yaml")
        logger = LoggerFactory.get_logger("jforex_live_probe")
        event_bus = EventBusFactory.create_from_config(config)
        
        print(f"   ✅ Config loaded: {type(config).__name__}")
        print(f"   ✅ Logger created: {type(logger).__name__}")
        print(f"   ✅ EventBus created: {type(event_bus).__name__}")
        print()
        
        # 2. Create Bi5Downloader via Factory
        print("🏭 Creating Bi5Downloader via JForexFactory...")
        downloader = JForexFactory.create_downloader(
            config=config,
            logger=logger,
            event_bus=event_bus
        )
        print(f"   ✅ Downloader created: {type(downloader).__name__}")
        print()
        
        # 3. Define Test Target
        symbol = "EURUSD"
        # Use a busy weekday afternoon (2024-05-02 14:00) for more reliable data
        target_date = datetime(2024, 5, 2, 14, 0, 0)
        print(f"🎯 Test Target:")
        print(f"   Symbol: {symbol}")
        print(f"   Date: {target_date} (Weekday afternoon - should have data)")
        print()
        
        # 4. Download Tick Data
        print("📥 Downloading tick data from Dukascopy...")
        print("   (This may take a moment, retrying up to 3 times...)")
        print()
        
        ticks = await downloader.download_tick_data(
            symbol=symbol,
            date=target_date
        )
        
        # 5. Display Results
        print("=" * 80)
        print("📊 DOWNLOAD RESULTS")
        print("=" * 80)
        print()
        
        if not ticks:
            print("⚠️  No tick data received (empty list)")
            print("   This could indicate:")
            print("   - Weekend/holiday (no trading)")
            print("   - Data not yet available for this date")
            print("   - Network issue (check logs above)")
            return
        
        print(f"✅ Successfully downloaded {len(ticks)} ticks")
        print()
        print("📋 First 5 TickData objects:")
        print("-" * 80)
        
        for i, tick in enumerate(ticks[:5], 1):
            print(f"{i}. {tick}")
        
        if len(ticks) > 5:
            print(f"... and {len(ticks) - 5} more ticks")
        
        print()
        print("🔍 Data Validation:")
        
        # Check for reasonable values
        first_tick = ticks[0]
        if first_tick.bid == 0.0 or first_tick.ask == 0.0:
            print("   ⚠️  WARNING: Bid/Ask prices are 0.0 - this may indicate a problem")
        elif first_tick.bid > 10.0 or first_tick.ask > 10.0:
            print("   ⚠️  WARNING: Bid/Ask prices seem unusually high for EURUSD")
        elif first_tick.ask <= first_tick.bid:
            print("   ⚠️  WARNING: Ask price should be higher than Bid price")
        else:
            print("   ✅ Prices look reasonable")
        
        print()
        print("=" * 80)
        print("✅ LIVE PROBE SUCCESSFUL")
        print("=" * 80)
        
    except Exception as e:
        print()
        print("=" * 80)
        print("❌ LIVE PROBE FAILED")
        print("=" * 80)
        print()
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}")
        print()
        print("🔍 Debug Information:")
        print(f"   Exception: {e}")
        print()
        
        # Print URL if available
        if hasattr(e, 'url'):
            print(f"   Generated URL: {e.url}")
        
        import traceback
        print("   Full Traceback:")
        traceback.print_exc()
        
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())