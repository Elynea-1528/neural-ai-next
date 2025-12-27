"""Tesztek a neural_ai.core.db.implementations.models modulhoz.

Ez a modul tartalmazza a DynamicConfig és LogEntry modellek tesztjeit,
100% kódfedettségi célkitűzéssel.
"""

from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from neural_ai.core.db.implementations.model_base import Base
from neural_ai.core.db.implementations.models import DynamicConfig, LogEntry


class TestDynamicConfig:
    """DynamicConfig modell tesztjei."""

    @pytest.fixture
    def engine(self):
        """In-memory SQLite engine létrehozása teszteléshez."""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        return engine

    @pytest.fixture
    def session(self, engine):
        """Adatbázis munkamenet létrehozása."""
        with Session(engine) as session:
            yield session

    def test_dynamic_config_creation(self, session: Session) -> None:
        """DynamicConfig létrehozásának tesztelése."""
        config = DynamicConfig(
            key="test_key",
            value={"nested": "value"},
            value_type="dict",
            category="test",
            description="Test configuration",
            is_active=True,
        )
        session.add(config)
        session.commit()

        assert config.id is not None
        assert config.key == "test_key"
        assert config.value == {"nested": "value"}
        assert config.value_type == "dict"
        assert config.category == "test"
        assert config.description == "Test configuration"
        assert config.is_active is True
        assert isinstance(config.created_at, datetime)
        assert isinstance(config.updated_at, datetime)

    def test_dynamic_config_default_values(self, session: Session) -> None:
        """DynamicConfig alapértelmezett értékeinek tesztelése."""
        config = DynamicConfig(
            key="test_key_default",
            value="default_value",
            value_type="str",
            category="test",
        )
        session.add(config)
        session.commit()

        assert config.is_active is True
        assert config.description is None

    def test_dynamic_config_repr(self, session: Session) -> None:
        """DynamicConfig __repr__ metódusának tesztelése."""
        config = DynamicConfig(
            key="test_repr",
            value=42,
            value_type="int",
            category="test",
        )
        session.add(config)
        session.commit()

        repr_str = repr(config)
        assert "DynamicConfig" in repr_str
        assert "test_repr" in repr_str
        assert "42" in repr_str
        assert "int" in repr_str

    def test_dynamic_config_to_dict(self, session: Session) -> None:
        """DynamicConfig to_dict metódusának tesztelése."""
        config = DynamicConfig(
            key="test_dict",
            value=[1, 2, 3],
            value_type="list",
            category="test",
        )
        session.add(config)
        session.commit()

        config_dict = config.to_dict()
        assert isinstance(config_dict, dict)
        assert config_dict["key"] == "test_dict"
        assert config_dict["value"] == [1, 2, 3]
        assert config_dict["value_type"] == "list"
        assert config_dict["category"] == "test"
        assert "created_at" in config_dict
        assert "updated_at" in config_dict
        assert isinstance(config_dict["created_at"], str)  # ISO format
        assert isinstance(config_dict["updated_at"], str)  # ISO format

    def test_dynamic_config_unique_key(self, session: Session) -> None:
        """DynamicConfig egyedi kulcsának tesztelése."""
        config1 = DynamicConfig(
            key="unique_key",
            value="value1",
            value_type="str",
            category="test",
        )
        session.add(config1)
        session.commit()

        config2 = DynamicConfig(
            key="unique_key",  # Ugyanaz a kulcs
            value="value2",
            value_type="str",
            category="test",
        )
        session.add(config2)

        with pytest.raises(Exception):  # Unique constraint violation
            session.commit()

    def test_dynamic_config_different_value_types(self, session: Session) -> None:
        """DynamicConfig különböző értéktípusokkal való tesztelése."""
        test_cases: list[tuple[str, object, str]] = [
            ("int_value", 42, "int"),
            ("float_value", 3.14, "float"),
            ("str_value", "hello", "str"),
            ("bool_value", True, "bool"),
            ("list_value", [1, 2, 3], "list"),
            ("dict_value", {"key": "value"}, "dict"),
        ]

        for key, value, value_type in test_cases:
            config = DynamicConfig(
                key=key,
                value=value,
                value_type=value_type,
                category="test",
            )
            session.add(config)
            session.commit()

            retrieved = session.get(DynamicConfig, config.id)
            assert retrieved.value == value
            assert retrieved.value_type == value_type

    def test_dynamic_config_json_serialization(self, session: Session) -> None:
        """DynamicConfig JSON értékének szerializálásának tesztelése."""
        complex_value: dict[str, object] = {
            "nested": {
                "level1": [1, 2, {"level2": "deep"}],
                "config": {"timeout": 30, "retries": 3},
            }
        }
        config = DynamicConfig(
            key="complex_json",
            value=complex_value,
            value_type="dict",
            category="test",
        )
        session.add(config)
        session.commit()

        retrieved = session.get(DynamicConfig, config.id)
        assert retrieved.value == complex_value
        # Ellenőrizzük, hogy a JSON mező helyesen tárolja a komplex struktúrát
        assert retrieved.value["nested"]["level1"][2]["level2"] == "deep"


class TestLogEntry:
    """LogEntry modell tesztjei."""

    @pytest.fixture
    def engine(self):
        """In-memory SQLite engine létrehozása teszteléshez."""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        return engine

    @pytest.fixture
    def session(self, engine):
        """Adatbázis munkamenet létrehozása."""
        with Session(engine) as session:
            yield session

    def test_log_entry_creation(self, session: Session) -> None:
        """LogEntry létrehozásának tesztelése."""
        log_entry = LogEntry(
            level="INFO",
            logger_name="test.logger",
            message="Test log message",
            module="test_module",
            function="test_function",
            line_number=42,
            process_id=1234,
            thread_id=5678,
            exception_type="ValueError",
            exception_message="Test exception",
            traceback="Traceback details",
            extra_data={"key": "value"},
        )
        session.add(log_entry)
        session.commit()

        assert log_entry.id is not None
        assert log_entry.level == "INFO"
        assert log_entry.logger_name == "test.logger"
        assert log_entry.message == "Test log message"
        assert log_entry.module == "test_module"
        assert log_entry.function == "test_function"
        assert log_entry.line_number == 42
        assert log_entry.process_id == 1234
        assert log_entry.thread_id == 5678
        assert log_entry.exception_type == "ValueError"
        assert log_entry.exception_message == "Test exception"
        assert log_entry.traceback == "Traceback details"
        assert log_entry.extra_data == {"key": "value"}
        assert isinstance(log_entry.created_at, datetime)
        assert isinstance(log_entry.updated_at, datetime)

    def test_log_entry_optional_fields(self, session: Session) -> None:
        """LogEntry opcionális mezőinek tesztelése."""
        log_entry = LogEntry(
            level="DEBUG",
            logger_name="minimal.logger",
            message="Minimal log entry",
        )
        session.add(log_entry)
        session.commit()

        assert log_entry.module is None
        assert log_entry.function is None
        assert log_entry.line_number is None
        assert log_entry.process_id is None
        assert log_entry.thread_id is None
        assert log_entry.exception_type is None
        assert log_entry.exception_message is None
        assert log_entry.traceback is None
        assert log_entry.extra_data is None

    def test_log_entry_repr(self, session: Session) -> None:
        """LogEntry __repr__ metódusának tesztelése."""
        log_entry = LogEntry(
            level="ERROR",
            logger_name="test.repr",
            message="This is a very long message that should be truncated in the repr method",
        )
        session.add(log_entry)
        session.commit()

        repr_str = repr(log_entry)
        assert "LogEntry" in repr_str
        assert "ERROR" in repr_str
        assert "test.repr" in repr_str
        assert "This is a very long message that should be trunc" in repr_str
        # Ellenőrizzük, hogy a message le van vágva 50 karakterre
        assert len(repr_str.split("message='")[1].split("...")[0]) <= 50

    def test_log_entry_to_dict(self, session: Session) -> None:
        """LogEntry to_dict metódusának tesztelése."""
        log_entry = LogEntry(
            level="WARNING",
            logger_name="test.dict",
            message="Test warning message",
            module="test",
            line_number=100,
        )
        session.add(log_entry)
        session.commit()

        log_dict = log_entry.to_dict()
        assert isinstance(log_dict, dict)
        assert log_dict["level"] == "WARNING"
        assert log_dict["logger_name"] == "test.dict"
        assert log_dict["message"] == "Test warning message"
        assert log_dict["module"] == "test"
        assert log_dict["line_number"] == 100
        assert "created_at" in log_dict
        assert "updated_at" in log_dict
        assert isinstance(log_dict["created_at"], str)  # ISO format
        assert isinstance(log_dict["updated_at"], str)  # ISO format

    def test_log_entry_different_levels(self, session: Session) -> None:
        """LogEntry különböző naplózási szintek tesztelése."""
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        for level in levels:
            log_entry = LogEntry(
                level=level,
                logger_name=f"test.{level.lower()}",
                message=f"Test {level} message",
            )
            session.add(log_entry)
            session.commit()

            retrieved = session.get(LogEntry, log_entry.id)
            assert retrieved.level == level

    def test_log_entry_extra_data_types(self, session: Session) -> None:
        """LogEntry extra_data különböző típusainak tesztelése."""
        test_cases: list[dict[str, object] | None] = [
            {"simple": "value"},
            {"nested": {"level1": [1, 2, 3]}},
            {"complex": {"list": [{"dict": "value"}], "number": 42}},
            None,  # Üres extra_data
        ]

        for extra_data in test_cases:
            log_entry = LogEntry(
                level="INFO",
                logger_name="test.extra_data",
                message="Testing extra data",
                extra_data=extra_data,
            )
            session.add(log_entry)
            session.commit()

            retrieved = session.get(LogEntry, log_entry.id)
            assert retrieved.extra_data == extra_data

    def test_log_entry_long_message(self, session: Session) -> None:
        """LogEntry hosszú üzenetének tesztelése."""
        long_message = "A" * 1000
        log_entry = LogEntry(
            level="INFO",
            logger_name="test.long",
            message=long_message,
        )
        session.add(log_entry)
        session.commit()

        retrieved = session.get(LogEntry, log_entry.id)
        assert retrieved.message == long_message
        # A repr metódus levághatja, de az eredeti üzenet teljes marad
        assert len(retrieved.message) == 1000

    def test_log_entry_exception_data(self, session: Session) -> None:
        """LogEntry kivétel adatokkal való tesztelése."""
        log_entry = LogEntry(
            level="ERROR",
            logger_name="exception.handler",
            message="Exception occurred",
            exception_type="RuntimeError",
            exception_message="Something went wrong",
            traceback="File 'test.py', line 10, in main\n  raise RuntimeError('error')",
        )
        session.add(log_entry)
        session.commit()

        retrieved = session.get(LogEntry, log_entry.id)
        assert retrieved.exception_type == "RuntimeError"
        assert retrieved.exception_message == "Something went wrong"
        assert "File 'test.py'" in retrieved.traceback


class TestModelRelationships:
    """Modellek közötti kapcsolatok tesztelése."""

    @pytest.fixture
    def engine(self):
        """In-memory SQLite engine létrehozása teszteléshez."""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        return engine

    @pytest.fixture
    def session(self, engine):
        """Adatbázis munkamenet létrehozása."""
        with Session(engine) as session:
            yield session

    def test_multiple_models_same_session(self, session: Session) -> None:
        """Több modell egy munkamenetben való használatának tesztelése."""
        # DynamicConfig létrehozása
        config = DynamicConfig(
            key="test_config",
            value="test_value",
            value_type="str",
            category="test",
        )
        session.add(config)

        # LogEntry létrehozása
        log_entry = LogEntry(
            level="INFO",
            logger_name="test.logger",
            message="Config created",
        )
        session.add(log_entry)

        session.commit()

        # Ellenőrzés
        assert config.id is not None
        assert log_entry.id is not None

        configs = session.query(DynamicConfig).all()
        logs = session.query(LogEntry).all()

        assert len(configs) == 1
        assert len(logs) == 1
        assert configs[0].key == "test_config"
        assert logs[0].message == "Config created"

    def test_model_timestamps(self, session: Session) -> None:
        """Modellek időbélyegeinek tesztelése."""
        config = DynamicConfig(
            key="timestamp_test",
            value="value",
            value_type="str",
            category="test",
        )
        session.add(config)
        session.commit()

        created_at_1 = config.created_at
        updated_at_1 = config.updated_at

        # Kis várakozás
        import time
        time.sleep(0.01)

        # Módosítás
        config.description = "Updated description"
        session.commit()

        created_at_2 = config.created_at
        updated_at_2 = config.updated_at

        # created_at nem változhat
        assert created_at_1 == created_at_2
        # updated_at-nek változnia kell
        assert updated_at_2 > updated_at_1

    def test_model_deletion(self, session: Session) -> None:
        """Modellek törlésének tesztelése."""
        config = DynamicConfig(
            key="delete_test",
            value="value",
            value_type="str",
            category="test",
        )
        session.add(config)
        session.commit()

        config_id = config.id
        assert session.get(DynamicConfig, config_id) is not None

        session.delete(config)
        session.commit()

        assert session.get(DynamicConfig, config_id) is None


class TestModelValidation:
    """Modell validáció tesztelése."""

    @pytest.fixture
    def engine(self):
        """In-memory SQLite engine létrehozása teszteléshez."""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        return engine

    @pytest.fixture
    def session(self, engine):
        """Adatbázis munkamenet létrehozása."""
        with Session(engine) as session:
            yield session

    def test_dynamic_config_nullable_fields(self, session: Session) -> None:
        """DynamicConfig nem nullázható mezőinek tesztelése."""
        # Kötelező mezők hiánya hibát okoz
        with pytest.raises(Exception):
            config = DynamicConfig()  # Hiányzik minden kötelező mező
            session.add(config)
            session.commit()

    def test_log_entry_nullable_fields(self, session: Session) -> None:
        """LogEntry nem nullázható mezőinek tesztelése."""
        # Kötelező mezők hiánya hibát okoz
        with pytest.raises(Exception):
            log_entry = LogEntry()  # Hiányzik minden kötelező mező
            session.add(log_entry)
            session.commit()

    def test_dynamic_config_string_length_limits(self, session: Session) -> None:
        """DynamicConfig string mezőinek hosszkorlátainak tesztelése."""
        # Túl hosszú kulcs - SQLite nem érvényesíti a String hosszkorlátot,
        # ezért ez a teszt csak dokumentációs célokat szolgál
        config = DynamicConfig(
            key="x" * 256,  # Túl hosszú lenne (limit: 255), de SQLite engedélyezi
            value="value",
            value_type="str",
            category="test",
        )
        session.add(config)
        session.commit()  # SQLite nem dob kivételt, csak levágja vagy engedélyezi
        # Ellenőrizzük, hogy a rekord létrejött (SQLite viselkedése)
        assert config.id is not None

    def test_log_entry_string_length_limits(self, session: Session) -> None:
        """LogEntry string mezőinek hosszkorlátainak tesztelése."""
        # Túl hosszú logger név - SQLite nem érvényesíti a String hosszkorlátot,
        # ezért ez a teszt csak dokumentációs célokat szolgál
        log_entry = LogEntry(
            level="INFO",
            logger_name="x" * 256,  # Túl hosszú lenne (limit: 255), de SQLite engedélyezi
            message="Test message",
        )
        session.add(log_entry)
        session.commit()  # SQLite nem dob kivételt, csak levágja vagy engedélyezi
        # Ellenőrizzük, hogy a rekord létrejött (SQLite viselkedése)
        assert log_entry.id is not None