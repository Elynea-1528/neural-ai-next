"""Dinamikus konfiguráció kezelő átfogó tesztek a hiányzó sorok lefedésére."""
import asyncio
import datetime
from contextlib import suppress
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from neural_ai.core.config.exceptions import ConfigError
from neural_ai.core.config.implementations.dynamic_config_manager import DynamicConfigManager


class TestDynamicConfigManagerComprehensive:
    """Dinamikus konfiguráció kezelő hiányzó sorok lefedésére szolgáló tesztek."""

    @pytest.mark.asyncio
    async def test_get_logs_error_on_exception(self) -> None:
        """Teszteli a hiba logolását a get metódusban (114. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_session.execute.side_effect = Exception("Adatbázis hiba")
        
        mock_logger = MagicMock()
        
        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        
        with pytest.raises(ConfigError, match="Konfiguráció lekérdezése sikertelen"):
            await manager.get("test_key")
        
        # Ellenőrizzük, hogy a logger error metódusa meghívódott-e
        mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_logs_info_on_success(self) -> None:
        """Teszteli az info logolást a set metódusban (168. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_logger = MagicMock()
        
        # Mockoljuk, hogy nem létezik a konfig
        stmt_result = MagicMock()
        stmt_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = stmt_result
        
        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        await manager.set("test_key", value="test_value")
        
        # Ellenőrizzük, hogy a logger info metódusa meghívódott-e
        mock_logger.info.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_logs_error_on_exception(self) -> None:
        """Teszteli a hiba logolását a set metódusban (173. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_session.execute.side_effect = Exception("Adatbázis hiba")
        mock_logger = MagicMock()
        
        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        
        with pytest.raises(ConfigError, match="Konfiguráció beállítása sikertelen"):
            await manager.set("test_key", value="test_value")
        
        # Ellenőrizzük, hogy a logger error metódusa meghívódott-e
        mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_section_logs_error_on_exception(self) -> None:
        """Teszteli a hiba logolását a get_section metódusban (206. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_session.execute.side_effect = Exception("Adatbázis hiba")
        mock_logger = MagicMock()
        
        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        
        with pytest.raises(ConfigError, match="Konfigurációs szekció lekérdezése sikertelen"):
            await manager.get_section("test_section")
        
        # Ellenőrizzük, hogy a logger error metódusa meghívódott-e
        mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_hot_reload_logs_info_and_error(self) -> None:
        """Teszteli az info és error logolást a start_hot_reload metódusban (330, 337. sorok)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_logger = MagicMock()
        
        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        
        # Mockoljuk a _check_for_updates-t, hogy dobjon egy kivételt
        with patch.object(manager, '_check_for_updates', side_effect=Exception("Hiba")):
            await manager.start_hot_reload(interval=0.1)
            
            # Várunk egy kicsit, hogy a task futni kezdjen
            await asyncio.sleep(0.2)
            
            # Leállítjuk a taskot
            await manager.stop_hot_reload()
            
            # Ellenőrizzük, hogy a logger metódusai meghívást kaptak-e
            mock_logger.info.assert_called()
            mock_logger.error.assert_called()

    @pytest.mark.asyncio
    async def test_stop_hot_reload_logs_warning_on_timeout(self) -> None:
        """Teszteli a warning logolást a stop_hot_reload metódusban timeout esetén (361. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_logger = MagicMock()
        
        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        
        # Létrehozunk egy valódi taskot, ami nem áll le időben
        async def slow_task():
            await asyncio.sleep(20)  # Nem fog leállni 10 másodpercen belül
        
        # Mockoljuk az asyncio.wait_for-t, hogy timeout-ot okozzon
        with patch('asyncio.wait_for', side_effect=asyncio.TimeoutError):
            # Beállítjuk a taskot
            manager._hot_reload_task = asyncio.create_task(slow_task())
            manager._stop_hot_reload.set()  # Beállítjuk, hogy a stop event is aktív legyen
            
            # Leállítjuk a hot reload-ot
            await manager.stop_hot_reload()
            
            # Ellenőrizzük, hogy a logger warning metódusa meghívódott-e
            mock_logger.warning.assert_called_once()
            
            # Takarítás
            if manager._hot_reload_task and not manager._hot_reload_task.done():
                manager._hot_reload_task.cancel()
                with suppress(asyncio.CancelledError):
                    await manager._hot_reload_task

    @pytest.mark.asyncio
    async def test_stop_hot_reload_logs_info_on_successful_stop(self) -> None:
        """Teszteli az info logolást a stop_hot_reload metódusban sikeres leállásnál (346. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_logger = MagicMock()
        
        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        
        # Elindítjuk a hot reload-ot
        await manager.start_hot_reload(interval=0.1)
        
        # Leállítjuk a hot reload-ot
        await manager.stop_hot_reload()
        
        # Ellenőrizzük, hogy a logger info metódusa meghívódott-e (346. sor)
        mock_logger.info.assert_called()
        
        # Ellenőrizzük, hogy a warning NEM lett meghívva
        mock_logger.warning.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_logs_error_on_exception(self) -> None:
        """Teszteli a hiba logolását a get_all metódusban (391. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_session.execute.side_effect = Exception("Adatbázis hiba")
        mock_logger = MagicMock()
        
        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        
        with pytest.raises(ConfigError, match="Összes konfiguráció lekérdezése sikertelen"):
            await manager.get_all()
        
        # Ellenőrizzük, hogy a logger error metódusa meghívódott-e
        mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_with_metadata_logs_info_and_error(self) -> None:
        """Teszteli az info és error logolást a set_with_metadata metódusban (449-458. sorok)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_logger = MagicMock()
        
        # Mockoljuk, hogy nem létezik a konfig
        stmt_result = MagicMock()
        stmt_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = stmt_result
        
        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        await manager.set_with_metadata("test_key", "test_value", category="test_category")
        
        # Ellenőrizzük, hogy a logger info metódusa meghívódott-e
        mock_logger.info.assert_called_once()
        
        # Teszteljük a hiba esetét is
        mock_session.execute.side_effect = Exception("Adatbázis hiba")
        
        with pytest.raises(ConfigError, match="Konfiguráció beállítása sikertelen"):
            await manager.set_with_metadata("test_key", "test_value")
        
        # Ellenőrizzük, hogy a logger error metódusa meghívódott-e
        assert mock_logger.error.call_count >= 1

    @pytest.mark.asyncio
    async def test_delete_logs_info_and_error(self) -> None:
        """Teszteli az info és error logolást a delete metódusban (491, 498. sorok)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_logger = MagicMock()
        
        # Mockoljuk, hogy létezik a konfig
        mock_config = MagicMock()
        mock_config.is_active = True
        stmt_result = MagicMock()
        stmt_result.scalar_one_or_none.return_value = mock_config
        mock_session.execute.return_value = stmt_result
        
        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        result = await manager.delete("test_key")
        
        assert result is True
        # Ellenőrizzük, hogy a logger info metódusa meghívódott-e
        mock_logger.info.assert_called_once()
        
        # Teszteljük a hiba esetét is
        mock_session.execute.side_effect = Exception("Adatbázis hiba")
        
        with pytest.raises(ConfigError, match="Konfiguráció törlése sikertelen"):
            await manager.delete("test_key")
        
        # Ellenőrizzük, hogy a logger error metódusa meghívódott-e
        assert mock_logger.error.call_count >= 1

    @pytest.mark.asyncio
    async def test_notify_listeners_logs_error(self) -> None:
        """Teszteli a hiba logolást a _notify_listeners metódusban (513. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_logger = MagicMock()
        
        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        
        # Mockoljuk a listener-t, hogy dobjon egy kivételt
        async def failing_listener(key: str, value: Any) -> None:
            raise Exception("Listener hiba")
        
        manager.add_listener(failing_listener)
        
        # Értesítjük a listener-t
        await manager._notify_listeners("test_key", "test_value")
        
        # Ellenőrizzük, hogy a logger error metódusa meghívódott-e
        mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_check_for_updates_logs_error(self) -> None:
        """Teszteli a hiba logolást a _check_for_updates metódusban (539. sor)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_session.execute.side_effect = Exception("Adatbázis hiba")
        mock_logger = MagicMock()
        
        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        # Beállítjuk, hogy legyen last_update, így a _check_for_updates a változásokat ellenőrzi
        manager._last_update = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)
        
        # Ellenőrizzük a változásokat, a kivételt elkapjuk
        try:
            await manager._check_for_updates()
        except ConfigError:
            pass  # A kivétel várható
        
        # Ellenőrizzük, hogy a logger error metódusa meghívódott-e
        mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_and_remove_listener_logging(self) -> None:
        """Teszteli a debug logolást az add_listener és remove_listener metódusokban (296, 308. sorok)."""
        mock_session = MagicMock(spec=AsyncSession)
        mock_logger = MagicMock()
        
        manager = DynamicConfigManager(session=mock_session, logger=mock_logger)
        
        # Listener hozzáadása
        async def test_listener(key: str, value: Any) -> None:
            pass
        
        manager.add_listener(test_listener)
        mock_logger.debug.assert_called_once()
        
        # Listener eltávolítása
        manager.remove_listener(test_listener)
        assert mock_logger.debug.call_count == 2