"""Tesztek az adatbázis modellekhez.

Ez a modul tartalmazza az összes tesztet a DynamicConfig és LogEntry
modellek CRUD műveleteihez.
"""

import asyncio
from datetime import datetime

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from neural_ai.core.db.implementations.model_base import Base
from neural_ai.core.db.implementations.models import DynamicConfig, LogEntry


@pytest.fixture
async def async_engine():
    """Aszinkron engine létrehozása in-memory SQLite adatbázishoz."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        poolclass=None,
    )

    # Táblák létrehozása
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture
async def async_session(async_engine):
    """Aszinkron session létrehozása."""
    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        yield session




class TestDynamicConfig:
    """Tesztek a DynamicConfig modellhez."""

    @pytest.mark.asyncio
    async def test_create_dynamic_config(self, async_session: AsyncSession):
        """Teszteli a DynamicConfig létrehozását."""
        config = DynamicConfig(
            key="test.key",
            value=2.5,
            value_type="float",
            category="risk",
            description="Teszt konfiguráció",
        )

        async_session.add(config)
        await async_session.commit()

        assert config.id is not None
        assert config.key == "test.key"
        assert config.value == 2.5
        assert config.value_type == "float"
        assert config.category == "risk"
        assert config.is_active is True
        assert isinstance(config.created_at, datetime)
        assert isinstance(config.updated_at, datetime)

    async def test_read_dynamic_config(self, async_session: AsyncSession):
        """Teszteli a DynamicConfig olvasását."""
        # Létrehozás
        config = DynamicConfig(
            key="test.read", value="test_value", value_type="str", category="system"
        )
        async_session.add(config)
        await async_session.commit()

        # Olvasás
        stmt = select(DynamicConfig).where(DynamicConfig.key == "test.read")
        result = await async_session.execute(stmt)
        fetched_config = result.scalar_one()

        assert fetched_config.key == "test.read"
        assert fetched_config.value == "test_value"
        assert fetched_config.value_type == "str"

    async def test_update_dynamic_config(self, async_session: AsyncSession):
        """Teszteli a DynamicConfig frissítését."""
        # Létrehozás
        config = DynamicConfig(key="test.update", value=10, value_type="int", category="trading")
        async_session.add(config)
        await async_session.commit()

        # Frissítés
        config.value = 20
        config.value_type = "int"
        await async_session.commit()

        # Ellenőrzés
        stmt = select(DynamicConfig).where(DynamicConfig.key == "test.update")
        result = await async_session.execute(stmt)
        updated_config = result.scalar_one()

        assert updated_config.value == 20
        assert updated_config.updated_at >= config.created_at

    async def test_delete_dynamic_config(self, async_session: AsyncSession):
        """Teszteli a DynamicConfig törlését."""
        # Létrehozás
        config = DynamicConfig(
            key="test.delete", value=True, value_type="bool", category="strategy"
        )
        async_session.add(config)
        await async_session.commit()

        # Törlés
        await async_session.delete(config)
        await async_session.commit()

        # Ellenőrzés
        stmt = select(DynamicConfig).where(DynamicConfig.key == "test.delete")
        result = await async_session.execute(stmt)
        deleted_config = result.scalar_one_or_none()

        assert deleted_config is None

    async def test_dynamic_config_unique_key(self, async_session: AsyncSession):
        """Teszteli a unique key constraint-et."""
        config1 = DynamicConfig(
            key="unique.key", value="value1", value_type="str", category="system"
        )
        async_session.add(config1)
        await async_session.commit()

        # Ugyanazzal a kulccsal nem lehet új konfigot létrehozni
        config2 = DynamicConfig(
            key="unique.key", value="value2", value_type="str", category="system"
        )
        async_session.add(config2)

        with pytest.raises(Exception):  # IntegrityError
            await async_session.commit()

    async def test_dynamic_config_to_dict(self, async_session: AsyncSession):
        """Teszteli a to_dict metódust."""
        config = DynamicConfig(
            key="test.dict", value={"nested": "value"}, value_type="dict", category="system"
        )
        async_session.add(config)
        await async_session.commit()

        result = config.to_dict()

        assert isinstance(result, dict)
        assert result["key"] == "test.dict"
        assert result["value"] == {"nested": "value"}
        assert "created_at" in result
        assert "updated_at" in result

    async def test_dynamic_config_repr(self, async_session: AsyncSession):
        """Teszteli a __repr__ metódust."""
        config = DynamicConfig(key="test.repr", value=42, value_type="int", category="system")

        repr_str = repr(config)

        assert "DynamicConfig" in repr_str
        assert "test.repr" in repr_str
        assert "42" in repr_str


class TestLogEntry:
    """Tesztek a LogEntry modellhez."""

    async def test_create_log_entry(self, async_session: AsyncSession):
        """Teszteli a LogEntry létrehozását."""
        log_entry = LogEntry(
            level="INFO",
            logger_name="test.logger",
            message="Teszt naplóüzenet",
            module="test_module.py",
            function="test_function",
            line_number=42,
            process_id=1234,
            thread_id=5678,
        )

        async_session.add(log_entry)
        await async_session.commit()

        assert log_entry.id is not None
        assert log_entry.level == "INFO"
        assert log_entry.logger_name == "test.logger"
        assert log_entry.message == "Teszt naplóüzenet"
        assert log_entry.module == "test_module.py"
        assert log_entry.function == "test_function"
        assert log_entry.line_number == 42
        assert log_entry.process_id == 1234
        assert log_entry.thread_id == 5678
        assert log_entry.exception_type is None
        assert log_entry.exception_message is None
        assert log_entry.traceback is None
        assert isinstance(log_entry.created_at, datetime)

    async def test_create_log_entry_with_exception(self, async_session: AsyncSession):
        """Teszteli a LogEntry létrehozását kivétel információkkal."""
        log_entry = LogEntry(
            level="ERROR",
            logger_name="error.logger",
            message="Hiba történt",
            exception_type="ValueError",
            exception_message="Érvénytelen érték",
            traceback="Traceback (most recent call last)...",
            extra_data={"user_id": 123, "request_id": "abc-def"},
        )

        async_session.add(log_entry)
        await async_session.commit()

        assert log_entry.exception_type == "ValueError"
        assert log_entry.exception_message == "Érvénytelen érték"
        assert log_entry.traceback.startswith("Traceback")
        assert log_entry.extra_data["user_id"] == 123
        assert log_entry.extra_data["request_id"] == "abc-def"

    async def test_read_log_entry(self, async_session: AsyncSession):
        """Teszteli a LogEntry olvasását."""
        # Létrehozás
        log_entry = LogEntry(level="WARNING", logger_name="read.logger", message="Figyelmeztetés")
        async_session.add(log_entry)
        await async_session.commit()

        # Olvasás
        stmt = select(LogEntry).where(LogEntry.logger_name == "read.logger")
        result = await async_session.execute(stmt)
        fetched_log = result.scalar_one()

        assert fetched_log.level == "WARNING"
        assert fetched_log.message == "Figyelmeztetés"

    async def test_update_log_entry(self, async_session: AsyncSession):
        """Teszteli a LogEntry frissítését."""
        # Létrehozás
        log_entry = LogEntry(level="DEBUG", logger_name="update.logger", message="Debug üzenet")
        async_session.add(log_entry)
        await async_session.commit()

        # Frissítés
        log_entry.level = "INFO"
        log_entry.message = "Frissített üzenet"
        await async_session.commit()

        # Ellenőrzés
        stmt = select(LogEntry).where(LogEntry.logger_name == "update.logger")
        result = await async_session.execute(stmt)
        updated_log = result.scalar_one()

        assert updated_log.level == "INFO"
        assert updated_log.message == "Frissített üzenet"

    async def test_delete_log_entry(self, async_session: AsyncSession):
        """Teszteli a LogEntry törlését."""
        # Létrehozás
        log_entry = LogEntry(level="ERROR", logger_name="delete.logger", message="Törlendő üzenet")
        async_session.add(log_entry)
        await async_session.commit()

        # Törlés
        await async_session.delete(log_entry)
        await async_session.commit()

        # Ellenőrzés
        stmt = select(LogEntry).where(LogEntry.logger_name == "delete.logger")
        result = await async_session.execute(stmt)
        deleted_log = result.scalar_one_or_none()

        assert deleted_log is None

    async def test_log_entry_to_dict(self, async_session: AsyncSession):
        """Teszteli a to_dict metódust."""
        log_entry = LogEntry(level="INFO", logger_name="dict.logger", message="Dict teszt")
        async_session.add(log_entry)
        await async_session.commit()

        result = log_entry.to_dict()

        assert isinstance(result, dict)
        assert result["level"] == "INFO"
        assert result["logger_name"] == "dict.logger"
        assert result["message"] == "Dict teszt"
        assert "created_at" in result
        assert "updated_at" in result

    async def test_log_entry_repr(self, async_session: AsyncSession):
        """Teszteli a __repr__ metódust."""
        log_entry = LogEntry(
            level="ERROR",
            logger_name="repr.logger",
            message="Hosszú hibaüzenet, amit a repr metódus le fog rövidíteni",
        )

        repr_str = repr(log_entry)

        assert "LogEntry" in repr_str
        assert "ERROR" in repr_str
        assert "repr.logger" in repr_str
        assert len(repr_str) < 120  # Rövid legyen


class TestDynamicConfigCRUDOperations:
    """Komplex CRUD műveletek tesztelése a DynamicConfig-hez."""

    async def test_bulk_create_and_query(self, async_session: AsyncSession):
        """Tömeges létrehozás és lekérdezés tesztelése."""
        # Tömeges létrehozás
        configs = [
            DynamicConfig(key=f"config.{i}", value=i * 10, value_type="int", category="test")
            for i in range(10)
        ]

        async_session.add_all(configs)
        await async_session.commit()

        # Lekérdezés kategória alapján
        stmt = select(DynamicConfig).where(DynamicConfig.category == "test")
        result = await async_session.execute(stmt)
        fetched_configs = result.scalars().all()

        assert len(fetched_configs) == 10
        assert all(c.category == "test" for c in fetched_configs)

    async def test_filter_by_is_active(self, async_session: AsyncSession):
        """Szűrés is_active mező alapján."""
        # Aktív konfigok
        active_configs = [
            DynamicConfig(
                key=f"active.{i}", value=i, value_type="int", category="active_test", is_active=True
            )
            for i in range(5)
        ]

        # Inaktív konfigok
        inactive_configs = [
            DynamicConfig(
                key=f"inactive.{i}",
                value=i,
                value_type="int",
                category="inactive_test",
                is_active=False,
            )
            for i in range(3)
        ]

        async_session.add_all(active_configs + inactive_configs)
        await async_session.commit()

        # Csak aktívak lekérdezése
        stmt = select(DynamicConfig).where(DynamicConfig.is_active == True)
        result = await async_session.execute(stmt)
        active_only = result.scalars().all()

        assert len(active_only) == 5
        assert all(c.is_active for c in active_only)

    async def test_value_type_filtering(self, async_session: AsyncSession):
        """Szűrés value_type alapján."""
        configs = [
            DynamicConfig(key=f"str.{i}", value=f"value{i}", value_type="str", category="type_test")
            for i in range(3)
        ] + [
            DynamicConfig(key=f"bool.{i}", value=True, value_type="bool", category="type_test")
            for i in range(2)
        ]

        async_session.add_all(configs)
        await async_session.commit()

        # Csak string típusúak
        stmt = select(DynamicConfig).where(
            DynamicConfig.category == "type_test", DynamicConfig.value_type == "str"
        )
        result = await async_session.execute(stmt)
        str_configs = result.scalars().all()

        assert len(str_configs) == 3
        assert all(c.value_type == "str" for c in str_configs)


class TestLogEntryCRUDOperations:
    """Komplex CRUD műveletek tesztelése a LogEntry-hez."""

    async def test_bulk_create_logs(self, async_session: AsyncSession):
        """Tömeges naplóbejegyzés létrehozás."""
        logs = [
            LogEntry(level="INFO", logger_name=f"logger.{i}", message=f"Message {i}")
            for i in range(20)
        ]

        async_session.add_all(logs)
        await async_session.commit()

        # Összes napló lekérdezése
        stmt = select(LogEntry)
        result = await async_session.execute(stmt)
        all_logs = result.scalars().all()

        assert len(all_logs) == 20

    async def test_filter_by_level(self, async_session: AsyncSession):
        """Szűrés log level alapján."""
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        logs = []

        for level in levels:
            for i in range(2):
                logs.append(
                    LogEntry(
                        level=level,
                        logger_name=f"{level.lower()}.logger",
                        message=f"{level} message {i}",
                    )
                )

        async_session.add_all(logs)
        await async_session.commit()

        # Csak ERROR szintű naplók
        stmt = select(LogEntry).where(LogEntry.level == "ERROR")
        result = await async_session.execute(stmt)
        error_logs = result.scalars().all()

        assert len(error_logs) == 2
        assert all(log.level == "ERROR" for log in error_logs)

    async def test_log_ordering_by_created_at(self, async_session: AsyncSession):
        """Naplók rendezése created_at szerint."""
        logs = []
        for i in range(5):
            logs.append(LogEntry(level="INFO", logger_name="order.logger", message=f"Message {i}"))
            await asyncio.sleep(0.01)  # Kis késleltetés a timestamp különbséghez

        async_session.add_all(logs)
        await async_session.commit()

        # Rendezés created_at szerint csökkenőben
        stmt = select(LogEntry).order_by(LogEntry.created_at.desc())
        result = await async_session.execute(stmt)
        ordered_logs = result.scalars().all()

        assert len(ordered_logs) == 5
        # Ellenőrizzük, hogy csökkenő sorrendben vannak
        for i in range(len(ordered_logs) - 1):
            assert ordered_logs[i].created_at >= ordered_logs[i + 1].created_at
