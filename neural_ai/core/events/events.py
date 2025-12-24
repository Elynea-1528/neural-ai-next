"""Esemény modellek a Neural AI Next rendszerhez.

Ez a modul definiálja az összes eseménytípust, amelyek az EventBus-on keresztül
áramlanak a rendszerben. Minden esemény Pydantic BaseModel-ből származik,
biztosítva a típusbiztosságot és a validációt.

Author: Neural AI Next Team
Version: 1.0.0
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EventType(str, Enum):
    """Eseménytípusok enumerációja."""

    MARKET_DATA = "market_data"
    TRADE = "trade"
    SIGNAL = "signal"
    SYSTEM_LOG = "system_log"
    ORDER = "order"
    POSITION = "position"


class MarketDataEvent(BaseModel):
    """Piaci adat esemény.

    Ez az esemény akkor jön létre, amikor új piaci adat érkezik
    a collectoroktól (JForex, MT5, IBKR).

    Attributes:
        symbol: A pénzpár szimbóluma (pl. 'EURUSD')
        timestamp: Az esemény időbélyege
        bid: A bid ár
        ask: Az ask ár
        volume: A volumen (opcionális)
        source: Az adat forrása ('jforex', 'mt5', 'ibkr')
    """

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})

    symbol: str = Field(..., description="A pénzpár szimbóluma")
    timestamp: datetime = Field(..., description="Az esemény időbélyege")
    bid: float = Field(..., description="A bid ár", gt=0)
    ask: float = Field(..., description="Az ask ár", gt=0)
    volume: int | None = Field(None, description="A volumen", ge=0)
    source: str = Field(..., description="Az adat forrása")

    @field_validator("source")
    @classmethod
    def validate_source(cls, v: str) -> str:
        """Validálja a forrást."""
        valid_sources = {"jforex", "mt5", "ibkr"}
        if v not in valid_sources:
            raise ValueError(f"Érvénytelen forrás: {v}. Érvényes források: {valid_sources}")
        return v


class TradeEvent(BaseModel):
    """Kereskedési esemény.

    Ez az esemény akkor jön létre, amikor egy kereskedés végrehajtódik.

    Attributes:
        symbol: A pénzpár szimbóluma
        timestamp: A kereskedés időbélyege
        direction: A kereskedés iránya ('BUY' vagy 'SELL')
        price: A végrehajtási ár
        volume: A kereskedés volumene (lotban)
        order_id: A rendelés egyedi azonosítója
        strategy_id: A stratégiát azonosító ID (opcionális)
    """

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})

    symbol: str = Field(..., description="A pénzpár szimbóluma")
    timestamp: datetime = Field(..., description="A kereskedés időbélyege")
    direction: str = Field(..., description="A kereskedés iránya")
    price: float = Field(..., description="A végrehajtási ár", gt=0)
    volume: float = Field(..., description="A kereskedés volumene", gt=0)
    order_id: str = Field(..., description="A rendelés egyedi azonosítója")
    strategy_id: str | None = Field(None, description="A stratégiát azonosító ID")

    @field_validator("direction")
    @classmethod
    def validate_direction(cls, v: str) -> str:
        """Validálja a kereskedés irányát."""
        valid_directions = {"BUY", "SELL"}
        if v not in valid_directions:
            raise ValueError(f"Érvénytelen irány: {v}. Érvényes irányok: {valid_directions}")
        return v


class SignalEvent(BaseModel):
    """Jelzés esemény.

    Ez az esemény akkor jön létre, amikor a Strategy Engine jelzést generál.

    Attributes:
        symbol: A pénzpár szimbóluma
        timestamp: A jelzés időbélyege
        signal_type: A jelzés típusa (pl. 'ENTRY_LONG', 'EXIT_SHORT')
        confidence: A jelzés megbízhatósága (0.0 - 1.0)
        strategy_id: A stratégiát azonosító ID
        price: Az aktuális ár (opcionális)
        target_price: A célár (opcionális)
        stop_loss: Stop loss ár (opcionális)
    """

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})

    symbol: str = Field(..., description="A pénzpár szimbóluma")
    timestamp: datetime = Field(..., description="A jelzés időbélyege")
    signal_type: str = Field(..., description="A jelzés típusa")
    confidence: float = Field(..., description="A jelzés megbízhatósága", ge=0.0, le=1.0)
    strategy_id: str = Field(..., description="A stratégiát azonosító ID")
    price: float | None = Field(None, description="Az aktuális ár", gt=0)
    target_price: float | None = Field(None, description="A célár", gt=0)
    stop_loss: float | None = Field(None, description="Stop loss ár", gt=0)

    @field_validator("signal_type")
    @classmethod
    def validate_signal_type(cls, v: str) -> str:
        """Validálja a jelzés típusát."""
        valid_types = {
            "ENTRY_LONG",
            "ENTRY_SHORT",
            "EXIT_LONG",
            "EXIT_SHORT",
            "CLOSE_POSITION",
            "REVERSE_POSITION",
        }
        if v not in valid_types:
            raise ValueError(f"Érvénytelen jelzés típus: {v}")
        return v


class SystemLogEvent(BaseModel):
    """Rendszer log esemény.

    Ez az esemény a rendszer különböző komponenseinek log üzeneteit tartalmazza.

    Attributes:
        timestamp: A log időbélyege
        level: A log szintje ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        component: A komponens neve, amely generálta a logot
        message: A log üzenet
        extra_data: További adatok (opcionális)
    """

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})

    timestamp: datetime = Field(..., description="A log időbélyege")
    level: str = Field(..., description="A log szintje")
    component: str = Field(..., description="A komponens neve")
    message: str = Field(..., description="A log üzenet")
    extra_data: dict[str, Any] | None = Field(None, description="További adatok")

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        """Validálja a log szintjét."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v not in valid_levels:
            raise ValueError(f"Érvénytelen log szint: {v}")
        return v


class OrderEvent(BaseModel):
    """Rendelés esemény.

    Ez az esemény akkor jön létre, amikor új rendelést helyezünk vagy
    egy létező rendelés állapota megváltozik.

    Attributes:
        order_id: A rendelés egyedi azonosítója
        timestamp: Az esemény időbélyege
        symbol: A pénzpár szimbóluma
        order_type: A rendelés típusa ('MARKET', 'LIMIT', 'STOP')
        direction: A rendelés iránya ('BUY' vagy 'SELL')
        volume: A rendelés volumene
        price: A rendelés ára (opcionális limit/stop rendeléseknél)
        status: A rendelés állapota ('PENDING', 'FILLED', 'CANCELLED', 'REJECTED')
    """

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})

    order_id: str = Field(..., description="A rendelés egyedi azonosítója")
    timestamp: datetime = Field(..., description="Az esemény időbélyege")
    symbol: str = Field(..., description="A pénzpár szimbóluma")
    order_type: str = Field(..., description="A rendelés típusa")
    direction: str = Field(..., description="A rendelés iránya")
    volume: float = Field(..., description="A rendelés volumene", gt=0)
    price: float | None = Field(None, description="A rendelés ára", gt=0)
    status: str = Field(..., description="A rendelés állapota")

    @field_validator("order_type")
    @classmethod
    def validate_order_type(cls, v: str) -> str:
        """Validálja a rendelés típusát."""
        valid_types = {"MARKET", "LIMIT", "STOP"}
        if v not in valid_types:
            raise ValueError(f"Érvénytelen rendelés típus: {v}")
        return v

    @field_validator("direction")
    @classmethod
    def validate_direction(cls, v: str) -> str:
        """Validálja a rendelés irányát."""
        valid_directions = {"BUY", "SELL"}
        if v not in valid_directions:
            raise ValueError(f"Érvénytelen irány: {v}")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validálja a rendelés állapotát."""
        valid_statuses = {"PENDING", "FILLED", "CANCELLED", "REJECTED"}
        if v not in valid_statuses:
            raise ValueError(f"Érvénytelen állapot: {v}")
        return v


class PositionEvent(BaseModel):
    """Pozíció esemény.

    Ez az esemény akkor jön létre, amikor pozíció nyílik vagy zárul.

    Attributes:
        position_id: A pozíció egyedi azonosítója
        timestamp: Az esemény időbélyege
        symbol: A pénzpár szimbóluma
        direction: A pozíció iránya ('LONG' vagy 'SHORT')
        volume: A pozíció volumene
        entry_price: A belépési ár
        current_price: Az aktuális ár
        profit_loss: A nyereség/veszteség (opcionális)
        status: A pozíció állapota ('OPEN', 'CLOSED')
    """

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})

    position_id: str = Field(..., description="A pozíció egyedi azonosítója")
    timestamp: datetime = Field(..., description="Az esemény időbélyege")
    symbol: str = Field(..., description="A pénzpár szimbóluma")
    direction: str = Field(..., description="A pozíció iránya")
    volume: float = Field(..., description="A pozíció volumene", gt=0)
    entry_price: float = Field(..., description="A belépési ár", gt=0)
    current_price: float = Field(..., description="Az aktuális ár", gt=0)
    profit_loss: float | None = Field(None, description="A nyereség/veszteség")
    status: str = Field(..., description="A pozíció állapota")

    @field_validator("direction")
    @classmethod
    def validate_direction(cls, v: str) -> str:
        """Validálja a pozíció irányát."""
        valid_directions = {"LONG", "SHORT"}
        if v not in valid_directions:
            raise ValueError(f"Érvénytelen irány: {v}")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validálja a pozíció állapotát."""
        valid_statuses = {"OPEN", "CLOSED"}
        if v not in valid_statuses:
            raise ValueError(f"Érvénytelen állapot: {v}")
        return v
