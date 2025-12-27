"""Adatbázis modellek a Neural AI Next rendszerhez.

Ez a modul definiálja az összes adatbázis táblát és modellt a rendszerben,
beleértve a DynamicConfig és LogEntry modelleket.
"""

from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, Index, String, Text
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import Mapped, mapped_column

from .model_base import Base

if TYPE_CHECKING:
    from typing import Any


class DynamicConfig(Base):
    """Dinamikus konfigurációs értékek tárolására szolgáló modell.

    Ez a modell tárolja a futás közben módosítható konfigurációs értékeket,
    amelyek hot reload támogatással rendelkeznek.

    Attributes:
        key: A konfigurációs kulcs (egyedi).
        value: A konfigurációs érték (JSON formátumban).
        value_type: Az érték típusa (int, float, str, bool, list, dict).
        category: A konfiguráció kategóriája (risk, strategy, trading, system).
        description: A konfiguráció leírása.
        is_active: A konfiguráció aktív-e.
    """

    __tablename__ = "dynamic_configs"

    key: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True, doc="A konfigurációs kulcs (egyedi)"
    )

    value: Mapped[Any] = mapped_column(
        JSON, nullable=False, doc="A konfigurációs érték (JSON formátumban)"
    )

    value_type: Mapped[str] = mapped_column(
        String(50), nullable=False, doc="Az érték típusa (int, float, str, bool, list, dict)"
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="A konfiguráció kategóriája (risk, strategy, trading, system)",
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, doc="A konfiguráció részletes leírása"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, doc="A konfiguráció aktív-e"
    )

    # Indexek
    __table_args__ = (
        Index("idx_dynamic_config_category_active", "category", "is_active"),
        Index("idx_dynamic_config_key_active", "key", "is_active"),
    )

    def __repr__(self) -> str:
        """Modell string reprezentációja.

        Returns:
            A modell rövid string reprezentációja.
        """
        return f"<DynamicConfig(key='{self.key}', value={self.value}, type={self.value_type})>"


class LogEntry(Base):
    """Rendszer naplóbejegyzéseket tároló modell.

    Ez a modell tárolja a rendszer által generált naplóbejegyzéseket
    strukturált formában az adatbázisban.

    Attributes:
        level: A napló szintje (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        logger_name: A logger neve.
        message: A naplóüzenet.
        module: A modul neve, ahonnan a napló született.
        function: A függvény neve, ahonnan a napló született.
        line_number: A sor száma, ahonnan a napló született.
        process_id: A folyamat azonosítója.
        thread_id: A szál azonosítója.
        exception_type: A kivétel típusa (ha van).
        exception_message: A kivétel üzenete (ha van).
        traceback: A traceback információ (ha van).
        extra_data: További egyéni adatok (JSON formátumban).
    """

    __tablename__ = "log_entries"

    level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
        doc="A napló szintje (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    logger_name: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True, doc="A logger neve"
    )

    message: Mapped[str] = mapped_column(Text, nullable=False, doc="A naplóüzenet")

    module: Mapped[str | None] = mapped_column(
        String(255), nullable=True, doc="A modul neve, ahonnan a napló született"
    )

    function: Mapped[str | None] = mapped_column(
        String(255), nullable=True, doc="A függvény neve, ahonnan a napló született"
    )

    line_number: Mapped[int | None] = mapped_column(
        nullable=True, doc="A sor száma, ahonnan a napló született"
    )

    process_id: Mapped[int | None] = mapped_column(nullable=True, doc="A folyamat azonosítója")

    thread_id: Mapped[int | None] = mapped_column(nullable=True, doc="A szál azonosítója")

    exception_type: Mapped[str | None] = mapped_column(
        String(255), nullable=True, doc="A kivétel típusa (ha van)"
    )

    exception_message: Mapped[str | None] = mapped_column(
        Text, nullable=True, doc="A kivétel üzenete (ha van)"
    )

    traceback: Mapped[str | None] = mapped_column(
        Text, nullable=True, doc="A traceback információ (ha van)"
    )

    extra_data: Mapped[dict[str, Any] | None] = mapped_column(
        JSON, nullable=True, doc="További egyéni adatok (JSON formátumban)"
    )

    # Indexek
    __table_args__ = (
        Index("idx_log_entries_level_created", "level", "created_at"),
        Index("idx_log_entries_logger_created", "logger_name", "created_at"),
    )

    def __repr__(self) -> str:
        """Modell string reprezentációja.

        Returns:
            A modell rövid string reprezentációja.
        """
        msg = self.message[:50]
        return f"<LogEntry(level='{self.level}', logger='{self.logger_name}', message='{msg}...')>"
