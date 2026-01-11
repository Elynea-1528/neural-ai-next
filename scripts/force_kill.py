#!/usr/bin/env python3
"""Folyamat erőszakos leállító szkript a projekt folyamatainak tisztítására.

Ez a szkript psutil használatával azonosítja és leállítja azokat a folyamatokat,
amelyek foglalják a projekt kritikus portjait (8501, 5555-5558) vagy
tartalmazzák a "streamlit" vagy "neural_ai" neveket a parancsorban.

Használat:
    python scripts/force_kill.py

Author: Neural AI Next Team
Version: 1.0.0
"""

import sys

try:
    import psutil
except ImportError:
    print("❌ psutil modul nincs telepítve. Telepítés: pip install psutil")
    sys.exit(1)


def force_kill_processes() -> None:
    """Folyamatok erőszakos leállítása.

    Iterál az összes futó folyamaton keresztül és leállítja azokat,
    amelyek egyeznek a kritériumokkal.
    """
    killed_processes: list[str] = []

    # Projekt portjai
    project_ports = [8501, 5555, 5556, 5557, 5558]

    # Név kulcsszavak
    name_keywords = ["streamlit", "neural_ai"]

    for proc in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
        try:
            pid = proc.info["pid"]
            name = proc.info["name"] or ""
            cmdline = proc.info["cmdline"] or []

            # Skip saját folyamat
            if pid == psutil.Process().pid:
                continue

            kill_reason = None

            # Ellenőrizzük a portokat
            try:
                connections = proc.net_connections(kind="inet")
                for conn in connections:
                    if hasattr(conn, "laddr") and conn.laddr:
                        port = conn.laddr.port
                        if port in project_ports:
                            kill_reason = f"port használat: {port}"
                            break
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue

            # Ha még nem találtunk okot, ellenőrizzük a nevet és cmdline-t
            if not kill_reason:
                cmdline_str = " ".join(cmdline).lower()
                name_lower = name.lower()

                for keyword in name_keywords:
                    if keyword in name_lower or keyword in cmdline_str:
                        kill_reason = f"név egyezés: {keyword}"
                        break

            # Leállítjuk, ha találtunk okot
            if kill_reason:
                try:
                    proc.kill()
                    killed_processes.append(f"PID {pid} ({name}) - {kill_reason}")
                    print(f"✅ Leállítva: PID {pid} ({name}) - {kill_reason}")
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    print(f"⚠️ Nem sikerült leállítani PID {pid}: {e}")

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if killed_processes:
        print(f"\n📊 Összesen {len(killed_processes)} folyamat leállítva.")
    else:
        print("ℹ️ Nincs leállítandó folyamat.")


if __name__ == "__main__":
    print("🔪 Folyamat erőszakos leállító indítása...")
    force_kill_processes()
    print("✅ Folyamat tisztítás befejezve.")
