"""
NEURAL AI NEXT - LIVE SYSTEM VISUAL CHECK
Ez a script demonstrálja, hogy a Core komponensek (EventBus, Storage, DB, Config)
valóban működnek és beszélgetnek egymással.
"""

import asyncio
import sys
import os
import shutil
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path.cwd()))

# Színek a menő kimenethez
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(message):
    print(f"\n{Colors.CYAN}{Colors.BOLD}>>> {message}{Colors.ENDC}")

def print_success(message):
    print(f"{Colors.GREEN}  ✅ {message}{Colors.ENDC}")

def print_fail(message):
    print(f"{Colors.FAIL}  ❌ {message}{Colors.ENDC}")

def print_info(key, value):
    print(f"  ℹ️  {key}: {Colors.BLUE}{value}{Colors.ENDC}")

# ---------------------------------------------------------

async def run_live_test():
    print(f"{Colors.HEADER}{Colors.BOLD}=== NEURAL AI NEXT | SYSTEM INTEGRATION CHECK ==={Colors.ENDC}")
    
    # 1. BOOTSTRAP
    print_step("1. RENDSZER INDÍTÁSA (BOOTSTRAP)")
    try:
        from neural_ai.core import bootstrap_core
        from neural_ai.core.events.interfaces.event_models import SystemLogEvent
        
        # Ez a sor mindent beindít: Config, Logger, DB, EventBus, Storage
        components = bootstrap_core()
        
        print_success("Bootstrap sikeresen lefutott")
        print_info("Logger", "Aktív (Színes/JSON)")
        print_info("Config", "Betöltve a configs/ mappából")
        
        if components.logger:
            components.logger.info("LIVE_TEST_STARTED", user="admin")
            print_success("Logger teszt üzenet elküldve")
            
    except Exception as e:
        print_fail(f"Bootstrap hiba: {e}")
        return

    # 2. EVENT BUS TESZT
    print_step("2. EVENT BUS TESZT (Ping-Pong)")
    try:
        if not components.event_bus:
            raise RuntimeError("EventBus nincs inicializálva!")

        await components.event_bus.start()
        print_success("EventBus elindult (ZeroMQ)")

        # Callback definíció
        received_event = asyncio.Event()
        
        async def on_test_event(event):
            print(f"     {Colors.WARNING}[EventBus] Üzenet megérkezett: {event.message}{Colors.ENDC}")
            received_event.set()

        # Feliratkozás
        components.event_bus.subscribe("system_log", on_test_event)
        print("     ⏳ ZMQ kapcsolódás...")
        await asyncio.sleep(2.0) # <--- Növelt timeout a lassú ZMQ indításhoz
        
        # Küldés
        test_msg = SystemLogEvent(
            timestamp=datetime.now(),
            level="INFO",
            component="LiveTest",
            message="Hello EventBus!"
        )
        await components.event_bus.publish("system_log", test_msg)
        print_info("Publish", "Üzenet elküldve...")

        # Várakozás
        try:
            await asyncio.wait_for(received_event.wait(), timeout=2.0)
            print_success("EventBus működik: Üzenet megérkezett és feldolgozva")
        except asyncio.TimeoutError:
            print_fail("EventBus Timeout: Az üzenet nem érkezett meg!")

    except Exception as e:
        print_fail(f"EventBus hiba: {e}")

    # 3. STORAGE TESZT (Parquet írás/olvasás)
    print_step("3. STORAGE & BIG DATA TESZT")
    try:
        if not components.storage:
            raise RuntimeError("Storage nincs inicializálva!")

        # Importok (hardver függő)
        try:
            import polars as pl
            print_info("Engine", "Polars (Fast & Modern)")
            df = pl.DataFrame({
                "timestamp": [datetime.now()],
                "bid": [1.12345],
                "ask": [1.12350],
                "source": ["TEST"]
            })
        except ImportError:
            import pandas as pd
            print_info("Engine", "Pandas (Legacy Compatibility)")
            df = pd.DataFrame({
                "timestamp": [datetime.now()],
                "bid": [1.12345],
                "ask": [1.12350],
                "source": ["TEST"]
            })

        symbol = "TEST_PAIR"
        date = datetime.now()
        
        # Írás
        await components.storage.store_tick_data(symbol, df, date)
        print_success("Parquet fájl sikeresen kiírva")
        
        # Ellenőrzés
        # (Itt egy kis hack, hogy megtudjuk az útvonalat a loghoz, de a storage elfedi)
        print_info("Path", f"data/tick/{symbol}/...")

        # Olvasás (Validáció) - Bővített ablakkal!
        from datetime import timedelta
        # Olvassunk egy teljes napot, hogy biztosan benne legyen
        start_read = date - timedelta(hours=1)
        end_read = date + timedelta(hours=1)
        
        data_back = await components.storage.read_tick_data(symbol, start_read, end_read)
        if len(data_back) > 0:
            print_success(f"Adat sikeresen visszaolvasva ({len(data_back)} sor)")
        else:
            print_fail("Visszaolvasott adat üres!")

    except Exception as e:
        print_fail(f"Storage hiba: {e}")

    # 4. HEALTH CHECK
    print_step("4. SYSTEM HEALTH CHECK (Szívverés)")
    try:
        # Ha van health monitor a komponensekben (márpedig kéne lennie a factoryból)
        # Ha nincs közvetlen hozzáférés, lekérjük a factory-tól
        from neural_ai.core.system.factory import SystemComponentFactory
        
        monitor = SystemComponentFactory.get_health_monitor("core")
        if monitor:
            status = monitor.check_health()
            
            color = Colors.GREEN if status.overall_status.value == "ok" else Colors.FAIL
            print_info("Status", f"{color}{status.overall_status.value.upper()}{Colors.ENDC}")
            
            for comp in status.components:
                print(f"     - {comp.name}: {comp.status.value}")
            
            print_success("Health Monitor aktív és jelent")
        else:
            print_fail("Health Monitor nem található")

    except Exception as e:
        print_fail(f"Health Check hiba: {e}")

    # CLEANUP
    print_step("5. CLEANUP")
    # Töröljük a teszt adatokat
    test_path = Path("data/tick/TEST_PAIR")
    if test_path.exists():
        shutil.rmtree(test_path)
        print_success("Teszt adatok törölve")
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== TEST COMPLETE ==={Colors.ENDC}\n")

if __name__ == "__main__":
    try:
        asyncio.run(run_live_test())
    except KeyboardInterrupt:
        pass