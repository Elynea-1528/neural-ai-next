#!/usr/bin/env python3
"""Streamlit Dashboard Application.

Ez a modul implementálja a Neural AI Next Streamlit dashboardját,
ami a rendszer állapotát és teljesítményét jeleníti meg.
"""

import sys
from pathlib import Path
from typing import TYPE_CHECKING

import streamlit as st

# Hozzáadjuk a neural_ai könyvtárat a Python path-hoz
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from neural_ai.ui.app import UIApplication

if TYPE_CHECKING:
    pass


def setup_page_config() -> None:
    """Oldal konfiguráció beállítása."""
    st.set_page_config(
        page_title="Neural AI Next - Dashboard",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_header() -> None:
    """Fejléc renderelése."""
    st.markdown(
        """
        <div style='text-align: center; padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='color: white; margin: 0;'>🧠 NEURAL AI NEXT</h1>
            <p style='color: white; margin: 0.5rem 0 0 0;'>
                Hierarchical Trading System Dashboard
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_system_overview(app: UIApplication) -> None:
    """Rendszer áttekintő megjelenítése.

    A valós rendszerállapotot jeleníti meg a DashboardService.get_health_status()
    metódusból lekért adatok alapján.

    Args:
        app: A UI alkalmazás példány
    """
    st.header("📊 Rendszer Áttekintés")

    try:
        factory = app.get_factory()
        dashboard_service = factory.get_dashboard_service()

        # Rendszer egészségügyi állapot lekérdezése
        health_status = dashboard_service.get_health_status()

        # Kártyák létrehozása a valós állapotok alapján
        col1, col2, col3, col4 = st.columns(4)

        # Core státusz
        core_status = health_status.get("core", "UNKNOWN")
        core_icon = "✅" if core_status == "OK" else "⚠️" if core_status == "WARNING" else "❌"
        with col1:
            st.metric(label="Core", value=core_icon, delta=core_status)

        # Database státusz
        db_status = health_status.get("database", "UNKNOWN")
        db_icon = "✅" if db_status == "OK" else "⚠️" if db_status == "WARNING" else "❌"
        with col2:
            st.metric(label="Database", value=db_icon, delta=db_status)

        # Event Bus státusz
        event_status = health_status.get("event_bus", "UNKNOWN")
        event_icon = "✅" if event_status == "OK" else "⚠️" if event_status == "WARNING" else "❌"
        with col3:
            st.metric(label="Event Bus", value=event_icon, delta=event_status)

        # Collectors státusz
        collector_status = health_status.get("collectors", "UNKNOWN")
        collector_icon = (
            "✅" if collector_status == "OK" else "⚠️" if collector_status == "WARNING" else "❌"
        )
        with col4:
            st.metric(label="Collectors", value=collector_icon, delta=collector_status)

        # Részletes információk
        with st.expander("Részletes információk", expanded=False):
            st.json(health_status)

    except Exception as e:
        st.error(f"Hiba a rendszer információk lekérdezésekor: {e}")


def render_health_status(app: UIApplication) -> None:
    """Egészségügyi állapot megjelenítése.

    Args:
        app: A UI alkalmazás példány
    """
    st.header("❤️ Egészségügyi Állapot")

    try:
        factory = app.get_factory()
        dashboard_service = factory.get_dashboard_service()

        health_status = dashboard_service.get_health_status()

        # Állapot kártyák
        for component, status in health_status.items():
            col1, col2 = st.columns([1, 3])

            with col1:
                if status == "OK":
                    st.success(f"✅ {component.upper()}")
                elif status == "WARNING":
                    st.warning(f"⚠️ {component.upper()}")
                else:
                    st.error(f"❌ {component.upper()}")

            with col2:
                st.progress(100 if status == "OK" else 50 if status == "WARNING" else 0)

    except Exception as e:
        st.error(f"Hiba az egészségügyi állapot lekérdezésekor: {e}")


def render_performance_metrics(app: UIApplication) -> None:
    """Teljesítmény metrikák megjelenítése.

    Args:
        app: A UI alkalmazás példány
    """
    st.header("⚡ Teljesítmény Metrikák")

    try:
        factory = app.get_factory()
        dashboard_service = factory.get_dashboard_service()

        metrics = dashboard_service.get_performance_metrics()

        # CPU és Memória metrikák
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🖥️ CPU Használat")
            cpu_usage = metrics.get("cpu_usage", 0.0)
            st.metric(label="CPU %", value=f"{cpu_usage:.1f}%")
            st.progress(cpu_usage / 100)

        with col2:
            st.subheader("💾 Memória Használat")
            memory_usage = metrics.get("memory_usage", 0.0)
            st.metric(label="Memória %", value=f"{memory_usage:.1f}%")
            st.progress(memory_usage / 100)

        # Egyéb metrikák
        col3, col4 = st.columns(2)

        with col3:
            st.subheader("💿 Disk Használat")
            disk_usage = metrics.get("disk_usage", 0.0)
            st.metric(label="Disk %", value=f"{disk_usage:.1f}%")
            st.progress(disk_usage / 100)

        with col4:
            st.subheader("⏱️ Válaszidő")
            response_time = metrics.get("response_time", 0.0)
            st.metric(label="ms", value=f"{response_time:.1f}")

    except Exception as e:
        st.error(f"Hiba a teljesítmény metrikák lekérdezésekor: {e}")


def render_recent_activities(app: UIApplication) -> None:
    """Legutóbbi tevékenységek megjelenítése.

    Args:
        app: A UI alkalmazás példány
    """
    st.header("📋 Legutóbbi Tevékenységek")

    try:
        factory = app.get_factory()
        dashboard_service = factory.get_dashboard_service()

        activities = dashboard_service.get_recent_activities()

        # Tevékenységek listázása
        for activity in activities:
            timestamp = activity.get("timestamp", "")
            activity_type = activity.get("type", "INFO")
            message = activity.get("message", "")
            component = activity.get("component", "")

            # Típus alapján ikon kiválasztása
            icon = {
                "INFO": "ℹ️",
                "SUCCESS": "✅",
                "WARNING": "⚠️",
                "ERROR": "❌",
            }.get(activity_type, "ℹ️")

            # Tevékenység kártya
            with st.container():
                col1, col2 = st.columns([1, 4])

                with col1:
                    st.write(f"{icon} **{activity_type}**")
                    st.caption(component)

                with col2:
                    st.write(message)
                    st.caption(timestamp)

                st.divider()

    except Exception as e:
        st.error(f"Hiba a tevékenységek lekérdezésekor: {e}")


def render_sidebar(app: UIApplication) -> None:
    """Oldalsáv renderelése.

    Args:
        app: A UI alkalmazás példány
    """
    with st.sidebar:
        st.header("🧠 Neural AI Next")

        # Frissítés gomb
        if st.button("🔄 Adatok Frissítése", type="primary"):
            try:
                factory = app.get_factory()
                dashboard_service = factory.get_dashboard_service()
                dashboard_service.refresh_data()
                st.success("Adatok frissítve!")
            except Exception as e:
                st.error(f"Hiba a frissítéskor: {e}")

        st.divider()

        # Navigáció
        st.subheader("Navigáció")
        st.page_link("streamlit_app.py", label="🏠 Főoldal", icon="🏠")

        st.divider()

        # Információk
        st.subheader("Információ")
        st.write("Verzió: 0.5.0")
        st.write(f"Státusz: {'✅ Fut' if app.is_running else '❌ Leállítva'}")


def main() -> None:
    """Fő alkalmazás."""
    # Oldal konfiguráció
    setup_page_config()

    # Fejléc
    render_header()

    # UI alkalmazás inicializálása
    app = UIApplication()

    try:
        # Inicializálás
        if not app.initialize():
            st.error("Hiba az alkalmazás inicializálásakor!")
            if app.init_error:
                st.exception(app.init_error)
            st.stop()

        # Alkalmazás indítása
        app.run()

        # Oldalsáv
        render_sidebar(app)

        # Fő tartalom
        render_system_overview(app)
        render_health_status(app)
        render_performance_metrics(app)
        render_recent_activities(app)

    except Exception as e:
        st.error(f"Váratlan hiba: {e}")
        st.exception(e)

    finally:
        # Alkalmazás leállítása
        app.stop()


if __name__ == "__main__":
    main()
