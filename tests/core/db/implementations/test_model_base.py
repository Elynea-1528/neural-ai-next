"""Tesztek a model_base modulhoz.

Ez a modul tartalmazza a Base osztály és annak metódusainak tesztjeit.
"""

from collections.abc import Generator
from datetime import datetime
from typing import Any

import pytest
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, sessionmaker

from neural_ai.core.db.implementations.model_base import Base


class DummyModel(Base):
    """Teszt modell a Base osztály teszteléséhez."""

    name: str = Column(String(50), nullable=False)  # type: ignore
    value: int = Column(Integer, nullable=False)  # type: ignore


@pytest.fixture
def engine() -> Any:
    """In-memory SQLite engine létrehozása teszteléshez."""
    return create_engine("sqlite:///:memory:")


@pytest.fixture
def session(engine: Any) -> Generator[Session, None, None]:
    """Teszt session létrehozása és törlése."""
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


class TestBase:
    """A Base osztály tesztjei."""

    def test_base_initialization(self):
        """Teszteli a Base osztály inicializálását."""
        assert hasattr(Base, "id")
        assert hasattr(Base, "created_at")
        assert hasattr(Base, "updated_at")

    def test_id_column_properties(self):
        """Teszteli az id oszlop tulajdonságait."""
        id_column = DummyModel.__table__.columns["id"]  # type: ignore
        assert id_column.primary_key
        assert id_column.autoincrement
        assert not id_column.nullable

    def test_created_at_column_properties(self):
        """Teszteli a created_at oszlop tulajdonságait."""
        created_at_column = DummyModel.__table__.columns["created_at"]  # type: ignore
        assert not created_at_column.nullable
        assert created_at_column.type.__class__.__name__ == "DateTime"

    def test_updated_at_column_properties(self):
        """Teszteli az updated_at oszlop tulajdonságait."""
        updated_at_column = DummyModel.__table__.columns["updated_at"]  # type: ignore
        assert not updated_at_column.nullable
        assert updated_at_column.type.__class__.__name__ == "DateTime"
        assert updated_at_column.onupdate is not None

    def test_automatic_tablename_generation(self):
        """Teszteli az automatikus táblanév generálást."""
        assert DummyModel.__tablename__ == "dummymodels"

    def test_model_creation_with_defaults(self, session: Session):
        """Teszteli a modell létrehozását alapértelmezett értékekkel."""
        dummy_model = DummyModel(name="Test", value=42)
        session.add(dummy_model)
        session.commit()

        assert dummy_model.id is not None
        assert isinstance(dummy_model.created_at, datetime)
        assert isinstance(dummy_model.updated_at, datetime)
        # SQLite nem támogatja a timezone-t, ezért csak a típus ellenőrzés
        # A lambda default működik, de SQLite eltávolítja a timezone infót
        assert dummy_model.created_at is not None
        assert dummy_model.updated_at is not None

    def test_to_dict_method(self, session: Session):
        """Teszteli a to_dict metódust."""
        dummy_model = DummyModel(name="Test", value=42)
        session.add(dummy_model)
        session.commit()

        result = dummy_model.to_dict()

        assert isinstance(result, dict)
        assert "id" in result
        assert "name" in result
        assert "value" in result
        assert "created_at" in result
        assert "updated_at" in result
        assert result["name"] == "Test"
        assert result["value"] == 42
        assert isinstance(result["created_at"], str)
        assert isinstance(result["updated_at"], str)

    def test_to_dict_datetime_isoformat(self, session: Session):
        """Teszteli, hogy a datetime értékek ISO formátumban vannak-e."""
        dummy_model = DummyModel(name="Test", value=42)
        session.add(dummy_model)
        session.commit()

        result = dummy_model.to_dict()

        # Ellenőrizzük, hogy ISO formátumú string-e
        datetime.fromisoformat(result["created_at"])
        datetime.fromisoformat(result["updated_at"])

    def test_repr_method(self, session: Session):
        """Teszteli a __repr__ metódust."""
        dummy_model = DummyModel(name="Test", value=42)
        session.add(dummy_model)
        session.commit()

        repr_str = repr(dummy_model)

        assert "DummyModel" in repr_str
        assert f"id={dummy_model.id}" in repr_str

    def test_updated_at_changes_on_update(self, session: Session):
        """Teszteli, hogy az updated_at módosul-e frissítéskor."""
        dummy_model = DummyModel(name="Test", value=42)
        session.add(dummy_model)
        session.commit()

        original_updated_at = dummy_model.updated_at

        # Várunk egy kicsit, hogy a timestamp biztosan változzon
        import time

        time.sleep(0.001)

        dummy_model.value = 100
        session.commit()

        assert dummy_model.updated_at > original_updated_at

    def test_created_at_does_not_change_on_update(self, session: Session):
        """Teszteli, hogy a created_at ne változzon frissítéskor."""
        dummy_model = DummyModel(name="Test", value=42)
        session.add(dummy_model)
        session.commit()

        original_created_at = dummy_model.created_at

        import time

        time.sleep(0.001)

        dummy_model.value = 100
        session.commit()

        assert dummy_model.created_at == original_created_at

    def test_multiple_models_have_different_ids(self, session: Session):
        """Teszteli, hogy különböző modelleknek különböző id-ja van."""
        model1 = DummyModel(name="Test1", value=1)
        model2 = DummyModel(name="Test2", value=2)

        session.add_all([model1, model2])
        session.commit()

        assert model1.id != model2.id
        assert model1.id is not None
        assert model2.id is not None
