"""Adatbázis modellek alaposztályai.

Ez a modul definiálja az összes adatbázis modell által használt alaposztályokat
és segédosztályokat a Neural AI Next rendszerben.
"""

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

if TYPE_CHECKING:
    pass


class Base(DeclarativeBase):
    """SQLAlchemy deklaratív alaposztály a modellekhez.

    Ez az osztály biztosítja a standardizált mezőket és metódusokat
    az összes adatbázis modell számára.

    Attributes:
        id: Elsődleges kulcs minden modellhez.
        created_at: A rekord létrehozásának időpontja.
        updated_at: A rekord utolsó módosításának időpontja.
    """

    type_annotation_map = {
        datetime: DateTime(timezone=True),
    }

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        doc="Rekord elsődleges kulcsa",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
        doc="A rekord létrehozásának időpontja (UTC)",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
        doc="A rekord utolsó módosításának időpontja (UTC)",
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        """Automatikus táblanév generálás a class névből.

        A class nevet snake_case formátumba konvertálja és hozzáadja egy 's' végződést.
        Például: DynamicConfig -> dynamic_configs

        Returns:
            A generált táblanév string formátumban.
        """
        return cls.__name__.lower().replace("config", "").replace("entry", "") + "s"

    def to_dict(self) -> dict[str, Any]:
        """Modell átalakítása dictionary formátumba.

        Az összes oszlop értékét dictionary formátumba konvertálja,
        datetime objektumokat ISO formátumú stringgé alakítja.

        Returns:
            A modell adatait tartalmazó dictionary.
        """
        result: dict[str, Any] = {}
        for column in self.__table__.columns:  # type: ignore
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result

    def __repr__(self) -> str:
        """Modell string reprezentációja.

        Returns:
            A modell rövid string reprezentációja.
        """
        class_name = self.__class__.__name__
        return f"<{class_name}(id={self.id})>"
