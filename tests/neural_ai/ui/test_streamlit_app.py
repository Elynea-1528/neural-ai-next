"""Unit tesztek a streamlit_app modulhoz.

Ez a modul teszteli a Streamlit dashboard alkalmazás funkcióit.
"""

from unittest.mock import MagicMock, patch

import pytest

from neural_ai.ui.streamlit_app import (
    main,
    render_header,
    render_system_overview,
    setup_page_config,
)


class TestSetupPageConfig:
    """Tesztek a setup_page_config függvényhez."""

    @patch("neural_ai.ui.streamlit_app.st")
    def test_setup_page_config_calls_set_page_config(self, mock_st: MagicMock) -> None:
        """Ellenőrzi, hogy a setup_page_config meghívja a st.set_page_config-ot."""
        # Act
        setup_page_config()

        # Assert
        mock_st.set_page_config.assert_called_once_with(
            page_title="Neural AI Next - Dashboard",
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="expanded",
        )


class TestRenderHeader:
    """Tesztek a render_header függvényhez."""

    @patch("neural_ai.ui.streamlit_app.st")
    def test_render_header_displays_markdown(self, mock_st: MagicMock) -> None:
        """Ellenőrzi, hogy a render_header megjeleníti a fejléc markdown-t."""
        # Act
        render_header()

        # Assert
        mock_st.markdown.assert_called_once()
        call_args = mock_st.markdown.call_args
        assert "NEURAL AI NEXT" in call_args[0][0]
        assert "Hierarchical Trading System Dashboard" in call_args[0][0]
        assert call_args[1]["unsafe_allow_html"] is True


class TestRenderSystemOverview:
    """Tesztek a render_system_overview függvényhez."""

    @patch("neural_ai.ui.streamlit_app.st")
    def test_render_system_overview_displays_health_status(
        self, mock_st: MagicMock
    ) -> None:
        """Ellenőrzi, hogy a render_system_overview megjeleníti a rendszer állapotot."""
        # Arrange
        mock_app = MagicMock()
        mock_factory = MagicMock()
        mock_dashboard_service = MagicMock()

        mock_app.get_factory.return_value = mock_factory
        mock_factory.get_dashboard_service.return_value = mock_dashboard_service
        mock_dashboard_service.get_health_status.return_value = {
            "core": "OK",
            "database": "OK",
            "event_bus": "OK",
            "collectors": "OK",
        }

        mock_st.columns.return_value = [MagicMock() for _ in range(4)]

        # Act
        render_system_overview(mock_app)

        # Assert
        mock_st.header.assert_called_once_with("📊 Rendszer Áttekintés")
        mock_app.get_factory.assert_called_once()
        mock_factory.get_dashboard_service.assert_called_once()
        mock_dashboard_service.get_health_status.assert_called_once()
        mock_st.columns.assert_called_once_with(4)

    @patch("neural_ai.ui.streamlit_app.st")
    def test_render_system_overview_handles_warning_status(
        self, mock_st: MagicMock
    ) -> None:
        """Ellenőrzi, hogy a render_system_overview kezeli a WARNING státuszt."""
        # Arrange
        mock_app = MagicMock()
        mock_factory = MagicMock()
        mock_dashboard_service = MagicMock()

        mock_app.get_factory.return_value = mock_factory
        mock_factory.get_dashboard_service.return_value = mock_dashboard_service
        mock_dashboard_service.get_health_status.return_value = {
            "core": "WARNING",
            "database": "WARNING",
            "event_bus": "WARNING",
            "collectors": "WARNING",
        }

        mock_st.columns.return_value = [MagicMock() for _ in range(4)]

        # Act
        render_system_overview(mock_app)

        # Assert
        mock_dashboard_service.get_health_status.assert_called_once()
        mock_st.columns.assert_called_once_with(4)

    @patch("neural_ai.ui.streamlit_app.st")
    def test_render_system_overview_handles_error_status(
        self, mock_st: MagicMock
    ) -> None:
        """Ellenőrzi, hogy a render_system_overview kezeli az ERROR státuszt."""
        # Arrange
        mock_app = MagicMock()
        mock_factory = MagicMock()
        mock_dashboard_service = MagicMock()

        mock_app.get_factory.return_value = mock_factory
        mock_factory.get_dashboard_service.return_value = mock_dashboard_service
        mock_dashboard_service.get_health_status.return_value = {
            "core": "ERROR",
            "database": "ERROR",
            "event_bus": "ERROR",
            "collectors": "ERROR",
        }

        mock_st.columns.return_value = [MagicMock() for _ in range(4)]

        # Act
        render_system_overview(mock_app)

        # Assert
        mock_dashboard_service.get_health_status.assert_called_once()

    @patch("neural_ai.ui.streamlit_app.st")
    def test_render_system_overview_handles_exception(self, mock_st: MagicMock) -> None:
        """Ellenőrzi, hogy a render_system_overview kezeli a kivételeket."""
        # Arrange
        mock_app = MagicMock()
        mock_app.get_factory.side_effect = Exception("Test error")

        # Act & Assert - nem dob kivételt
        try:
            render_system_overview(mock_app)
        except Exception:
            pytest.fail("render_system_overview nem kezelte a kivételt")


class TestMain:
    """Tesztek a main függvényhez."""

    @patch("neural_ai.ui.streamlit_app.UIApplication")
    @patch("neural_ai.ui.streamlit_app.setup_page_config")
    @patch("neural_ai.ui.streamlit_app.render_header")
    @patch("neural_ai.ui.streamlit_app.render_system_overview")
    @patch("neural_ai.ui.streamlit_app.st")
    def test_main_initializes_and_renders(
        self,
        mock_st: MagicMock,
        mock_render_system_overview: MagicMock,
        mock_render_header: MagicMock,
        mock_setup_page_config: MagicMock,
        mock_ui_application: MagicMock,
    ) -> None:
        """Ellenőrzi, hogy a main inicializálja és rendereli az alkalmazást."""
        # Arrange
        mock_app = MagicMock()
        mock_ui_application.return_value = mock_app

        # Act
        main()

        # Assert
        mock_setup_page_config.assert_called_once()
        mock_render_header.assert_called_once()
        mock_ui_application.assert_called_once()
        mock_render_system_overview.assert_called_once_with(mock_app)

    @patch("neural_ai.ui.streamlit_app.UIApplication")
    @patch("neural_ai.ui.streamlit_app.setup_page_config")
    @patch("neural_ai.ui.streamlit_app.st")
    def test_main_handles_initialization_error(
        self,
        mock_st: MagicMock,
        mock_setup_page_config: MagicMock,
        mock_ui_application: MagicMock,
    ) -> None:
        """Ellenőrzi, hogy a main kezeli az inicializálási hibákat."""
        # Arrange
        mock_ui_application.side_effect = Exception("Initialization failed")

        # Act & Assert
        with pytest.raises(Exception, match="Initialization failed"):
            main()
