#!/usr/bin/env python3
"""Rendszer állapot ellenőrző script
Ellenőrzi, hogy a kollektor és az MT5 EA megfelelően működik-e.
"""

import subprocess
import time

import requests


def check_collector_status():
    """Kollektor állapotának ellenőrzése."""
    print("=" * 80)
    print("KOLLEKTOR ÁLLAPOT ELLENŐRZÉSE")
    print("=" * 80)

    try:
        # Health check
        response = requests.get("http://localhost:8000/api/v1/health", timeout=5)
        if response.status_code == 200:
            print("✅ Kollektor szerver fut")
        else:
            print(f"❌ Kollektor szerver hibás állapot: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Kollektor szerver nem elérhető: {e}")
        return False

    # Pending jobs ellenőrzése
    try:
        response = requests.get("http://localhost:8000/api/v1/historical/pending", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Függőben lévő job-ok: {data.get('count', 0)}")

            if data.get("jobs"):
                for job in data["jobs"]:
                    print(
                        f"   - {job['symbol']}/{job['timeframe']}: {job['status']} ({job['progress']:.1%})"
                    )
        else:
            print(f"⚠️ Nem sikerült lekérdezni a job-okat: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Hiba a job lekérdezésekor: {e}")

    return True


def check_mt5_connection():
    """MT5 kapcsolat ellenőrzése."""
    print("\n" + "=" * 80)
    print("MT5 KAPCSOLAT ELLENŐRZÉSE")
    print("=" * 80)

    # Próbáljunk meg egy egyszerű ping-et küldeni
    try:
        response = requests.get("http://localhost:8000/api/v1/ping", timeout=5)
        if response.status_code == 200:
            print("✅ MT5 EA válaszol a ping-re")
            return True
        else:
            print(f"⚠️ MT5 EA nem válaszol megfelelően: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ MT5 EA nem elérhető: {e}")
        return False


def check_mt5_process():
    """MT5 folyamat ellenőrzése."""
    print("\n" + "=" * 80)
    print("MT5 FOLYAMAT ELLENŐRZÉSE")
    print("=" * 80)

    try:
        # Ellenőrizzük, hogy fut-e az MT5 folyamat
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=10)

        mt5_processes = []
        for line in result.stdout.split("\n"):
            if "terminal" in line.lower() or "metatrader" in line.lower():
                mt5_processes.append(line)

        if mt5_processes:
            print(f"✅ MT5 folyamatok találhatók: {len(mt5_processes)}")
            for proc in mt5_processes[:3]:  # Csak az első 3-at mutatjuk
                print(f"   {proc}")
        else:
            print("⚠️ Nem található MT5 folyamat")
            print("   Lehetséges, hogy az MT5 nincs elindítva")

    except Exception as e:
        print(f"⚠️ Hiba a folyamat ellenőrzésekor: {e}")


def main():
    """Főprogram."""
    print("\n" + "=" * 80)
    print("NEURAL AI NEXT - RENDSZER ÁLLAPOT ELLENŐRZŐ")
    print("=" * 80)
    print(f"Idő: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Kollektor ellenőrzése
    collector_ok = check_collector_status()

    if collector_ok:
        # MT5 kapcsolat ellenőrzése
        mt5_ok = check_mt5_connection()

        # MT5 folyamat ellenőrzése
        check_mt5_process()

        # Összefoglalás
        print("\n" + "=" * 80)
        print("ÖSSZEFOGLALÁS")
        print("=" * 80)

        if collector_ok:
            print("✅ Kollektor: OK")
        else:
            print("❌ Kollektor: HIBA")

        if mt5_ok:
            print("✅ MT5 EA: OK")
        else:
            print("❌ MT5 EA: NEM ELÉRHETŐ")
            print("\nJAVASLATOK:")
            print("1. Indítsd el az MT5-öt")
            print("2. Telepítsd az EA-t az MT5-be")
            print("3. Ellenőrizd, hogy az EA fut-e a charton")
            print("4. Ellenőrizd a Wine konfigurációt (ha Linuxon fut)")
    else:
        print("\n❌ A kollektor nem fut! Indítsd el:")
        print("   python scripts/run_collector.py")

    print("=" * 80)


if __name__ == "__main__":
    main()
