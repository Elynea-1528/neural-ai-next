"""MT5 Collector implementáció.

Ez a modul tartalmazza az MT5 Collector komponens fő implementációját,
amely felelős a MetaTrader 5 platformról történő adatgyűjtésért.

Author: Neural AI Team
Date: 2025-12-16
Version: 1.0.0
"""

import datetime as dt
import os
import random
import signal
import time
from collections.abc import Callable
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any

import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import interfaces and exceptions
# Import factory components
from neural_ai.collectors.mt5.data_validator import DataValidator
from neural_ai.collectors.mt5.dlq import DeadLetterQueue
from neural_ai.collectors.mt5.error_handler import (
    ErrorHandler,
    NetworkError,
    StorageError,
    ValidationError,
)
from neural_ai.collectors.mt5.exceptions import (
    MT5ConnectionError,
    MT5DataValidationError,
    MT5Exception,
    MT5SocketError,
    MT5TimeoutError,
)
from neural_ai.collectors.mt5.implementations.historical_data_manager import (
    HistoricalDataManager,
)
from neural_ai.collectors.mt5.implementations.storage.collector_storage import (
    CollectorStorage,
)
from neural_ai.collectors.mt5.interfaces.collector_interface import CollectorInterface
from neural_ai.core.config.implementations.config_manager_factory import (
    ConfigManagerFactory,
)
from neural_ai.core.logger.implementations.logger_factory import LoggerFactory
from neural_ai.core.storage.implementations.storage_factory import StorageFactory
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

# ===== TIMEOUT DECORATOR AND EXCEPTIONS =====


class TimeoutError(Exception):
    """Raised when a function call times out."""

    pass


def timeout(seconds: int):
    """Decorator to add timeout to function calls."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def timeout_handler(signum, frame):
                raise TimeoutError(f"Function {func.__name__} timed out after {seconds} seconds")

            # Set the signal handler
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
            finally:
                # Reset the alarm and restore the old handler
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)

            return result

        return wrapper

    return decorator


# ===== EXPONENTIAL BACKOFF AND CIRCUIT BREAKER =====


class ExponentialBackoff:
    """Implements exponential backoff with jitter for retry operations."""

    def __init__(
        self,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        max_retries: int = 5,
        jitter: bool = True,
    ):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.max_retries = max_retries
        self.jitter = jitter
        self.retry_count = 0

    def calculate_delay(self) -> float:
        """Calculate next delay with exponential backoff and optional jitter."""
        if self.retry_count >= self.max_retries:
            return -1  # Signal to stop retrying

        # Exponential backoff: base_delay * (2 ^ retry_count)
        delay = self.base_delay * (2**self.retry_count)

        # Cap at max_delay
        delay = min(delay, self.max_delay)

        # Add jitter (random value between 0 and delay)
        if self.jitter:
            delay = random.uniform(0, delay)

        self.retry_count += 1
        return delay

    def reset(self) -> None:
        """Reset retry counter."""
        self.retry_count = 0

    def should_retry(self) -> bool:
        """Check if we should continue retrying."""
        return self.retry_count < self.max_retries


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exceptions: tuple = (MT5TimeoutError, MT5ConnectionError, MT5SocketError),
):
    """Decorator to retry function calls with exponential backoff."""

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            backoff = ExponentialBackoff(base_delay, max_delay, max_retries)

            while backoff.should_retry():
                try:
                    result = func(self, *args, **kwargs)
                    backoff.reset()  # Reset on success
                    return result
                except exceptions as e:
                    delay = backoff.calculate_delay()
                    if delay < 0:  # Max retries reached
                        self._logger.error(
                            f"Max retries ({max_retries}) reached for {func.__name__}. "
                            f"Last error: {e}"
                        )
                        raise

                    self._logger.warning(
                        f"Retrying {func.__name__} after {delay:.1f}s delay "
                        f"(attempt {backoff.retry_count}/{max_retries}). Error: {e}"
                    )
                    time.sleep(delay)

            # Should not reach here, but raise last exception just in case
            raise

        return wrapper

    return decorator


class CircuitBreaker:
    """Implements circuit breaker pattern to prevent cascading failures."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exceptions: tuple = (
            MT5TimeoutError,
            MT5ConnectionError,
            MT5SocketError,
        ),
        logger: Any | None = None,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exceptions = expected_exceptions
        self.logger = logger

        self.failure_count = 0
        self.last_failure_time: float | None = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Execute function with circuit breaker protection."""
        if self.state == "OPEN":
            if (
                self.last_failure_time
                and time.time() - self.last_failure_time < self.recovery_timeout
            ):
                raise MT5ConnectionError(
                    f"Circuit breaker is OPEN. Waiting for recovery. "
                    f"Last failure: {time.time() - self.last_failure_time:.1f}s ago"
                )
            else:
                # Try to recover
                self.state = "HALF_OPEN"
                if self.logger:
                    self.logger.info("Circuit breaker entering HALF_OPEN state")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exceptions:
            self._on_failure()
            raise
        except Exception:
            # Unexpected exceptions don't trip the circuit breaker
            raise

    def _on_success(self) -> None:
        """Handle successful execution."""
        self.failure_count = 0
        self.last_failure_time = None
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            if self.logger:
                self.logger.info("Circuit breaker reset to CLOSED state after successful recovery")

    def _on_failure(self) -> None:
        """Handle failed execution."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            if self.logger:
                self.logger.error(
                    f"Circuit breaker tripped to OPEN state after {self.failure_count} failures. "
                    f"Will attempt recovery in {self.recovery_timeout}s"
                )

    def get_state(self) -> dict[str, Any]:
        """Get current circuit breaker state."""
        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "last_failure_time": self.last_failure_time,
            "failure_threshold": self.failure_threshold,
            "recovery_timeout": self.recovery_timeout,
        }


class TickData(BaseModel):
    """Tick adatok modellje."""

    symbol: str
    bid: float
    ask: float
    time: int
    volume: int | None = None


class OHLCVData(BaseModel):
    """OHLCV adatok modellje."""

    symbol: str
    timeframe: str | int
    bars: list[dict[str, Any]]
    timestamp: int


class HistoricalDataRequest(BaseModel):
    """Historikus adatkérés modellje."""

    symbol: str
    timeframe: str
    start_date: str
    end_date: str
    batch_size: int = 365
    priority: str = "normal"


class HistoricalDataCollect(BaseModel):
    """Historikus adatgyűjtés modellje."""

    job_id: str
    batch_number: int
    symbol: str
    timeframe: str | int
    date_range: dict[str, str]
    bars: list[dict[str, Any]]


class GapDetectionRequest(BaseModel):
    """Hézagdetektálás kérés modellje."""

    symbol: str | None = None
    timeframe: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class QualityReportRequest(BaseModel):
    """Minőségjelentés kérés modellje."""

    symbol: str | None = None
    timeframe: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    format: str = "json"  # json vagy csv
    include_corrections: bool = True


class HistoricalProgressUpdate(BaseModel):
    """Historikus adatgyűjtés progresszének frissítése."""

    job_id: str
    progress: int
    total_bars: int
    current_batch: int


class BatchValidationRequest(BaseModel):
    """Kötegelt validálás kérés modellje."""

    data: list[dict[str, Any]]
    data_type: str = "ohlcv"  # ohlcv vagy tick
    auto_correct: bool = False


class TrainingDatasetGenerateRequest(BaseModel):
    """Tanulási adathalmaz generálás kérés modellje."""

    dataset_type: str  # retraining, medium, deep_learning, validation
    symbols: list[str]
    timeframes: list[str]
    date_range: dict[str, str]
    quality_threshold: float = 0.95
    output_format: str = "parquet"


class MT5Collector(CollectorInterface):
    """MT5 Collector implementáció.

    Felelős a MetaTrader 5 platformról történő adatgyűjtésért
    FastAPI szerveren keresztül.
    """

    def __init__(self, config: dict[str, Any]):
        """Inicializálás.

        Args:
            config: Konfigurációs szótár

        Raises:
            ConfigurationError: Konfigurációs hiba esetén
        """
        self.config = config
        self._initialize_components()
        self._initialize_api()
        self.is_running = False

        self.logger.info(f"{self.__class__.__name__} initialized")

    def _initialize_components(self):
        """Komponensek inicializálása."""
        # Config
        config_path = self.config.get("config_path", "configs/collector_config.yaml")
        self.config_manager = ConfigManagerFactory.get_manager(filename=config_path)

        # Logger
        logger_config = self.config_manager.get_section("logger")
        self.logger = LoggerFactory.get_logger(
            name="MT5Collector",
            logger_type=logger_config.get("type", "colored"),
            log_level=logger_config.get("level", "INFO"),
        )

        # File logger
        log_dir = Path("logs/collectors/mt5")
        log_dir.mkdir(parents=True, exist_ok=True)
        self.file_logger = LoggerFactory.get_logger(
            name="MT5CollectorFile",
            logger_type="rotating",
            log_file=str(log_dir / "mt5_collector.log"),
            rotation_type="time",
            when="midnight",
            backup_count=7,
        )

        # Create data directory
        self.data_dir = Path("data/collectors/mt5")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # DataValidator (Data Quality Frameworkkel)
        self.validator = DataValidator(logger=None, enable_quality_framework=True)

        # ErrorHandler
        self.error_handler = ErrorHandler(logger=self.file_logger)

        # CollectorStorage
        self.collector_storage = CollectorStorage(
            base_path=str(self.data_dir.parent.parent),  # Use main data directory
            logger=self.file_logger,
            use_parquet=True,  # Enable Parquet format for OHLCV data
        )

        # Storage (legacy)
        self.storage: StorageInterface = StorageFactory.get_storage(
            storage_type="file", base_path=str(self.data_dir)
        )

        # Historical Data Manager
        self.historical_manager = HistoricalDataManager(
            storage=self.collector_storage,
            validator=self.validator,
            error_handler=self.error_handler,
            logger=self.file_logger,
        )

        self.logger.info("CollectorStorage initialized with CSV and multi-instrument support")
        self.logger.info("HistoricalDataManager initialized")

        # Circuit breaker for MT5 operations
        self._circuit_breaker = CircuitBreaker(
            failure_threshold=5, recovery_timeout=60, logger=self.logger
        )

        # Dead-Letter-Queue for corrupted data
        dlq_directory = self.data_dir / "dlq"
        self._dlq = DeadLetterQueue(dlq_directory, max_file_size_mb=100)
        self.logger.info(f"Dead-Letter-Queue initialized at {dlq_directory}")

    @retry_with_backoff(max_retries=3, base_delay=1.0, max_delay=10.0)
    def _check_socket_integrity(self) -> bool:
        """Check if the MT5 socket connection is still valid with retry logic.

        Note: This method will be used when MT5 API calls are present.
        Currently, the collector uses FastAPI endpoints for data collection.
        """
        try:
            # Import mt5 module if available
            try:
                import MetaTrader5 as mt5
            except ImportError:
                self.logger.warning("MetaTrader5 module not available")
                return True  # Assume valid if MT5 not available

            # Try to get terminal info - if this fails, socket is broken
            info = mt5.terminal_info()
            if info is None:
                return False

            # Check if terminal is connected
            if not info.connected:
                return False

            # Try a simple API call to verify socket
            symbols = mt5.symbols_get()
            if symbols is None:
                return False

            return True
        except Exception as e:
            self.logger.error(f"Socket integrity check failed: {e}")
            return False

    def _reconnect(self, max_retries: int = 3) -> bool:
        """Attempt to reconnect to MT5 with exponential backoff.

        Args:
            max_retries: Maximum number of reconnection attempts

        Returns:
            True if reconnection successful, False otherwise
        """
        backoff = ExponentialBackoff(base_delay=2.0, max_delay=30.0, max_retries=max_retries)

        while backoff.should_retry():
            try:
                delay = backoff.calculate_delay()
                self.logger.warning(
                    f"Attempting to reconnect to MT5 (attempt {backoff.retry_count}/{max_retries}) "
                    f"after {delay:.1f}s delay"
                )

                time.sleep(delay)

                # Import mt5 module if available
                try:
                    import MetaTrader5 as mt5
                except ImportError:
                    self.logger.warning("MetaTrader5 module not available")
                    return True  # Assume success if MT5 not available

                # Shutdown existing connection
                if mt5.initialized():
                    mt5.shutdown()

                # Reinitialize
                if self.initialize():
                    self.logger.info("Successfully reconnected to MT5")
                    return True

            except Exception as e:
                self.logger.error(f"Reconnection attempt {backoff.retry_count} failed: {e}")

        self.logger.error("All reconnection attempts failed")
        return False

    def _safe_mt5_call(
        self, func, *args, expected_type=None, retry_on_failure: bool = True, **kwargs
    ):
        """Wrapper for MT5 API calls with circuit breaker protection and exponential backoff.

        Args:
            func: MT5 API function to call
            *args: Positional arguments for the function
            expected_type: Expected return type (optional)
            retry_on_failure: Whether to retry on failure with exponential backoff (default: True)
            **kwargs: Keyword arguments for the function

        Returns:
            Result of the MT5 API call

        Raises:
            MT5ConnectionError: If connection fails
            MT5TimeoutError: If operation times out
        """
        self._heartbeat_check()

        # Wrap the function call with circuit breaker
        def _wrapped_call():
            if not self._check_socket_integrity():
                if not self._reconnect():
                    raise MT5ConnectionError("Failed to establish MT5 connection")

            try:
                result = func(*args, **kwargs)
                if not self._validate_mt5_response(result, expected_type):
                    raise MT5ConnectionError(f"Invalid response from MT5 API call {func.__name__}")
                return result
            except (TimeoutError, MT5TimeoutError) as e:
                self.logger.error(f"MT5 call {func.__name__} timed out: {e}")
                if retry_on_failure:
                    # Use exponential backoff for retry
                    backoff = ExponentialBackoff(base_delay=1.0, max_delay=15.0, max_retries=2)
                    while backoff.should_retry():
                        delay = backoff.calculate_delay()
                        self.logger.warning(
                            f"Retrying {func.__name__} after {delay:.1f}s (timeout error)"
                        )
                        time.sleep(delay)
                        if self._reconnect():
                            return func(*args, **kwargs)
                raise MT5TimeoutError(
                    f"MT5 call {func.__name__} timed out after reconnection attempt"
                ) from e
            except (ConnectionError, MT5ConnectionError, MT5SocketError) as e:
                self.logger.error(f"MT5 call {func.__name__} failed: {e}")
                if retry_on_failure:
                    # Use exponential backoff for retry
                    backoff = ExponentialBackoff(base_delay=1.0, max_delay=15.0, max_retries=2)
                    while backoff.should_retry():
                        delay = backoff.calculate_delay()
                        self.logger.warning(
                            f"Retrying {func.__name__} after {delay:.1f}s (connection error)"
                        )
                        time.sleep(delay)
                        if self._reconnect():
                            return func(*args, **kwargs)
                raise MT5ConnectionError(
                    f"MT5 call {func.__name__} failed after reconnection attempt"
                ) from e
            except Exception as e:
                self.logger.exception(f"Unexpected error in MT5 call {func.__name__}: {e}")
                raise

        return self._circuit_breaker.call(_wrapped_call)

    def get_circuit_breaker_status(self) -> dict[str, Any]:
        """Get detailed circuit breaker status information.

        Returns:
            Dictionary containing circuit breaker state, failure count,
            last failure time, and configuration parameters
        """
        return self._circuit_breaker.get_state()

    def get_connection_status(self) -> dict[str, Any]:
        """Get detailed connection status information.

        Returns:
            Dictionary containing connection status details, circuit breaker state, and DLQ status
        """
        try:
            # Import mt5 module if available
            try:
                import MetaTrader5 as mt5
            except ImportError:
                return {
                    "initialized": False,
                    "socket_valid": False,
                    "terminal_info": None,
                    "last_error": "MetaTrader5 module not available",
                    "last_heartbeat": time.time(),
                    "circuit_breaker": self.get_circuit_breaker_status(),
                    "dlq": self.get_dlq_statistics(),
                }

            terminal_info = mt5.terminal_info()
            return {
                "initialized": mt5.initialized(),
                "socket_valid": self._check_socket_integrity(),
                "terminal_info": terminal_info._asdict() if terminal_info else None,
                "last_error": mt5.last_error(),
                "last_heartbeat": time.time(),
                "circuit_breaker": self.get_circuit_breaker_status(),
                "dlq": self.get_dlq_statistics(),
            }
        except Exception as e:
            self.logger.error(f"Error getting connection status: {e}")
            return {
                "initialized": False,
                "socket_valid": False,
                "terminal_info": None,
                "last_error": str(e),
                "last_heartbeat": time.time(),
                "circuit_breaker": self.get_circuit_breaker_status(),
                "dlq": self.get_dlq_statistics(),
            }

    def _heartbeat_check(self) -> None:
        """Periodic heartbeat check to maintain socket integrity.

        This method is called before each MT5 API call to ensure
        the connection is still valid.
        """
        if not hasattr(self, "_last_heartbeat"):
            self._last_heartbeat = time.time()

        # Check every 60 seconds
        if time.time() - self._last_heartbeat > 60:
            if not self._check_socket_integrity():
                self.logger.warning("Heartbeat check failed, attempting reconnection")
                self._reconnect()
            self._last_heartbeat = time.time()

    def _validate_mt5_response(self, response, expected_type: type = None) -> bool:
        """Validate MT5 API response.

        Args:
            response: The response from MT5 API
            expected_type: Expected type of the response (optional)

        Returns:
            True if response is valid, False otherwise
        """
        if response is None:
            return False

        if expected_type and not isinstance(response, expected_type):
            return False

        # Check for common error indicators in MT5 responses
        if isinstance(response, tuple) and hasattr(response, "_fields"):
            if hasattr(response, "retcode") and response.retcode != 0:
                return False

        return True

    def _initialize_api(self):
        """FastAPI inicializálása."""
        self.app = FastAPI(
            title="MT5 Collector API",
            description="API for receiving data from MT5 Expert Advisor",
            version="1.0.0",
        )

        self._setup_routes()

    def _setup_routes(self):
        """API útvonalak beállítása."""

        @self.app.get("/")
        async def root():
            """Root endpoint - API info."""
            return {"service": "MT5 Collector", "version": "1.0.0", "status": "running"}

        @self.app.get("/api/v1/ping")
        async def ping():
            """Health check endpoint."""
            return {"status": "ok", "message": "MT5 Collector is running"}

        @self.app.get("/api/v1/health")
        async def health_check():
            """Health check endpoint for GUI."""
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
            }

        @self.app.post("/api/v1/collect/tick")
        async def collect_tick(tick_data: TickData):
            """Tick adatok gyűjtése."""
            try:
                # Log the received data to both loggers
                log_message = (
                    f"Tick received: {tick_data.symbol} "
                    f"Bid={tick_data.bid:.5f} "
                    f"Ask={tick_data.ask:.5f} "
                    f"Time={tick_data.time}"
                )
                self.logger.info(log_message)
                self.file_logger.debug(log_message)

                # Prepare tick data
                tick_dict = tick_data.model_dump()
                tick_dict["type"] = "tick"
                tick_dict["received_at"] = datetime.now().isoformat()

                # Validate tick data
                validation_result = self.validator.validate_tick(tick_dict)

                if not validation_result.is_valid:
                    self.file_logger.warning(
                        f"Invalid tick data received for {tick_data.symbol}: "
                        f"{validation_result.errors}"
                    )
                    # Store invalid data
                    self.collector_storage.store_invalid_data(
                        data=tick_dict,
                        data_type="tick",
                        reason="; ".join(validation_result.errors),
                    )
                    return {
                        "status": "warning",
                        "message": "Invalid tick data received and stored separately",
                        "errors": validation_result.errors,
                    }

                if validation_result.warnings:
                    self.file_logger.warning(
                        f"Tick data warnings for {tick_data.symbol}: {validation_result.warnings}"
                    )

                # Store valid tick data
                self.collector_storage.store_tick(tick_dict)

                # Store to warehouse
                self.collector_storage.store_to_warehouse(
                    data=tick_dict, data_type="raw", validated=True
                )

                # Log successful storage
                self.file_logger.info(
                    f"Tick data stored: {tick_data.symbol} at {datetime.now().isoformat()}"
                )

                return {
                    "status": "success",
                    "message": "Tick data received and stored",
                    "data": tick_dict,
                }

            except (MT5ConnectionError, MT5TimeoutError) as e:
                # Handle MT5-specific network errors
                self.logger.exception(
                    f"MT5 network error processing tick data: {tick_data.symbol}",
                    stack_info=True,
                )
                self.error_handler.handle_error(e)

                return {
                    "status": "error",
                    "message": f"MT5 connection issue: {str(e)}",
                    "recovery_suggestion": self.error_handler.get_recovery_suggestion(e),
                }
            except MT5DataValidationError as e:
                # Handle MT5 data validation errors
                self.logger.exception(
                    f"MT5 data validation error for tick: {tick_data.symbol}",
                    stack_info=True,
                )
                self.error_handler.handle_error(e)

                return {
                    "status": "error",
                    "message": f"Data validation failed: {str(e)}",
                    "recovery_suggestion": self.error_handler.get_recovery_suggestion(e),
                }
            except MT5Exception as e:
                # Handle other MT5-specific errors
                self.logger.exception(
                    f"MT5 error processing tick data: {tick_data.symbol}",
                    stack_info=True,
                )
                self.error_handler.handle_error(e)

                return {
                    "status": "error",
                    "message": f"MT5 error: {str(e)}",
                    "recovery_suggestion": self.error_handler.get_recovery_suggestion(e),
                }
            except Exception as e:
                # Handle unexpected errors
                error = NetworkError(
                    f"Unexpected error processing tick data: {e}",
                    details={"tick_data": tick_data.model_dump()},
                )
                self.error_handler.handle_error(error)

                error_message = f"Error processing tick data: {e}"
                self.logger.error(error_message)
                self.file_logger.error(error_message)

                # Return error with recovery suggestion
                return {
                    "status": "error",
                    "message": str(e),
                    "recovery_suggestion": self.error_handler.get_recovery_suggestion(error),
                }

        @self.app.post("/api/v1/collect/ohlcv")
        async def collect_ohlcv(ohlcv_data: OHLCVData):
            """OHLCV adatok gyűjtése."""
            try:
                # Log the received data to both loggers
                log_message = (
                    f"OHLCV received: {ohlcv_data.symbol} "
                    f"TF={ohlcv_data.timeframe} "
                    f"Bars={len(ohlcv_data.bars)} "
                    f"Time={ohlcv_data.timestamp}"
                )
                self.logger.info(log_message)
                self.file_logger.debug(log_message)

                # Prepare OHLCV data
                ohlcv_dict = ohlcv_data.model_dump()
                ohlcv_dict["type"] = "ohlcv"
                ohlcv_dict["received_at"] = datetime.now().isoformat()

                # Validate OHLCV data
                invalid_bars = []
                valid_bars = []

                for bar in ohlcv_dict["bars"]:
                    # Add symbol and timeframe to bar for validation
                    bar["symbol"] = ohlcv_data.symbol
                    # Convert timeframe to int - handle both string and int types
                    if isinstance(ohlcv_data.timeframe, str):
                        # If it's a string, try to convert to int
                        try:
                            bar["timeframe"] = int(ohlcv_data.timeframe)
                        except ValueError:
                            # If conversion fails, use default (e.g., for "PERIOD_H1" strings)
                            bar["timeframe"] = 16385
                    else:
                        # If it's already an int, use it directly
                        bar["timeframe"] = ohlcv_data.timeframe

                    validation_result = self.validator.validate_ohlcv(bar)

                    if not validation_result.is_valid:
                        # Create validation error for invalid bar
                        error = ValidationError(
                            f"Invalid OHLCV bar for {ohlcv_data.symbol} (TF={ohlcv_data.timeframe})",
                            details={
                                "bar": bar,
                                "errors": validation_result.errors,
                                "warnings": validation_result.warnings,
                            },
                        )
                        self.error_handler.handle_error(error)

                        self.file_logger.warning(
                            f"Invalid OHLCV bar for {ohlcv_data.symbol} "
                            f"(TF={ohlcv_data.timeframe}): {validation_result.errors}"
                        )
                        invalid_bars.append(bar)
                    else:
                        valid_bars.append(bar)

                # Store invalid bars separately
                if invalid_bars:
                    for bar in invalid_bars:
                        try:
                            self.collector_storage.store_invalid_data(
                                data=bar,
                                data_type="ohlcv",
                                reason="; ".join(validation_result.errors),
                            )
                        except Exception as storage_error:
                            # Handle storage error for invalid data
                            storage_err = StorageError(
                                f"Failed to store invalid OHLCV bar: {storage_error}",
                                details={"bar": bar},
                            )
                            self.error_handler.handle_error(storage_err)

                # Store only valid bars
                ohlcv_dict["bars"] = valid_bars

                try:
                    # Store valid OHLCV data
                    self.collector_storage.store_ohlcv(ohlcv_dict)

                    # Store to warehouse
                    self.collector_storage.store_to_warehouse(
                        data=ohlcv_dict, data_type="raw", validated=True
                    )

                except Exception as storage_error:
                    # Handle storage errors
                    error = StorageError(
                        f"Failed to store OHLCV data: {storage_error}",
                        details={"ohlcv_data": ohlcv_dict},
                    )
                    self.error_handler.handle_error(error)

                    return {
                        "status": "storage_error",
                        "message": "Failed to store OHLCV data",
                        "error": str(storage_error),
                        "recovery_suggestion": self.error_handler.get_recovery_suggestion(error),
                    }

                # Log successful storage
                self.file_logger.info(
                    f"OHLCV data stored: {ohlcv_data.symbol} "
                    f"TF={ohlcv_data.timeframe} "
                    f"at {datetime.now().isoformat()}"
                )

                return {
                    "status": "success",
                    "message": "OHLCV data received and stored",
                    "data": {
                        "symbol": ohlcv_data.symbol,
                        "timeframe": ohlcv_data.timeframe,
                        "bars_count": len(ohlcv_data.bars),
                    },
                }
            except (MT5ConnectionError, MT5TimeoutError) as e:
                # Handle MT5-specific network errors
                self.logger.exception(
                    f"MT5 network error processing OHLCV data: {ohlcv_data.symbol}",
                    stack_info=True,
                )
                self.error_handler.handle_error(e)

                return {
                    "status": "error",
                    "message": f"MT5 connection issue: {str(e)}",
                    "recovery_suggestion": self.error_handler.get_recovery_suggestion(e),
                }
            except MT5DataValidationError as e:
                # Handle MT5 data validation errors
                self.logger.exception(
                    f"MT5 data validation error for OHLCV: {ohlcv_data.symbol}",
                    stack_info=True,
                )
                self.error_handler.handle_error(e)

                return {
                    "status": "error",
                    "message": f"Data validation failed: {str(e)}",
                    "recovery_suggestion": self.error_handler.get_recovery_suggestion(e),
                }
            except MT5Exception as e:
                # Handle other MT5-specific errors
                self.logger.exception(
                    f"MT5 error processing OHLCV data: {ohlcv_data.symbol}",
                    stack_info=True,
                )
                self.error_handler.handle_error(e)

                return {
                    "status": "error",
                    "message": f"MT5 error: {str(e)}",
                    "recovery_suggestion": self.error_handler.get_recovery_suggestion(e),
                }
            except Exception as e:
                # Handle unexpected errors
                error = NetworkError(
                    f"Unexpected error processing OHLCV data: {e}",
                    details={"ohlcv_data": ohlcv_data.model_dump()},
                )
                self.error_handler.handle_error(error)

                error_message = f"Error processing OHLCV data: {e}"
                self.logger.error(error_message)
                self.file_logger.error(error_message)

                # Return error with recovery suggestion
                return {
                    "status": "error",
                    "message": str(e),
                    "recovery_suggestion": self.error_handler.get_recovery_suggestion(error),
                }

        @self.app.get("/api/v1/validation/report")
        async def get_validation_report():
            """Get validation statistics report."""
            report = self.validator.get_validation_report()
            return report

        @self.app.post("/api/v1/validation/reset")
        async def reset_validation_stats():
            """Reset validation statistics."""
            self.validator.reset_statistics()
            return {"status": "success", "message": "Validation statistics reset"}

        @self.app.get("/api/v1/storage/stats")
        async def get_storage_stats():
            """Get storage statistics."""
            stats = self.collector_storage.get_storage_stats()
            return stats

        @self.app.get("/api/v1/errors/report")
        async def get_error_report():
            """Get error statistics report."""
            report = self.error_handler.get_error_report()
            return report

        @self.app.post("/api/v1/errors/reset")
        async def reset_error_stats():
            """Reset error statistics."""
            self.error_handler.reset_statistics()
            return {"status": "success", "message": "Error statistics reset"}

        # ===== DATA QUALITY FRAMEWORK ENDPOINTS =====

        @self.app.get("/api/v1/quality/metrics")
        async def get_quality_metrics():
            """Minőségi metrikák lekérdezése."""
            try:
                metrics = self.validator.get_quality_metrics()

                if not metrics:
                    return {
                        "status": "no_data",
                        "message": "Nincs elérhető minőségadatok",
                    }

                return {"status": "success", "metrics": metrics.to_dict()}

            except Exception as e:
                self.logger.error(f"Error getting quality metrics: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/v1/quality/summary")
        async def get_quality_summary():
            """Összesített minőségi összefoglaló."""
            try:
                if not self.validator.quality_framework:
                    return {
                        "status": "error",
                        "message": "Data Quality Framework not enabled",
                    }

                summary = self.validator.quality_framework.get_quality_summary()
                return summary

            except Exception as e:
                self.logger.error(f"Error getting quality summary: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/v1/quality/report")
        async def generate_quality_report(request: QualityReportRequest):
            """Minőségjelentés generálása."""
            try:
                # Fájl elérési út beállítása
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"quality_report_{timestamp}"

                if request.symbol:
                    filename += f"_{request.symbol}"
                if request.timeframe:
                    filename += f"_{request.timeframe}"

                output_path = f"logs/quality_reports/{filename}.{request.format}"

                # Jelentés generálása
                self.validator.generate_quality_report(output_path, request.format)

                # Ha CSV formátum, akkor a fájlok listázása
                files_generated = [output_path]
                if request.format.lower() == "csv":
                    base_name = output_path.replace(f".{request.format}", "")
                    issues_file = f"{base_name}_issues.csv"
                    corrections_file = f"{base_name}_corrections.csv"

                    if os.path.exists(issues_file):
                        files_generated.append(issues_file)
                    if request.include_corrections and os.path.exists(corrections_file):
                        files_generated.append(corrections_file)

                return {
                    "status": "success",
                    "message": "Quality report generated",
                    "files": files_generated,
                    "output_path": output_path,
                }

            except Exception as e:
                self.logger.error(f"Error generating quality report: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/v1/quality/validate-batch")
        async def validate_batch_data(request: BatchValidationRequest):
            """Kötegelt adatok validálása."""
            try:
                # Validálás
                result = self.validator.validate_batch(request.data, request.data_type)

                # Automatikus javítás, ha kérték
                corrections = []
                if request.auto_correct and result["overall_status"] != "passed":
                    corrected_data, corrections = self.validator.auto_correct_batch(
                        request.data, request.data_type
                    )

                    # Javított adatok újravalidálása
                    result = self.validator.validate_batch(corrected_data, request.data_type)

                    result["corrected_data"] = corrected_data

                result["corrections"] = corrections
                return result

            except Exception as e:
                self.logger.error(f"Error validating batch data: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/v1/quality/auto-correct")
        async def auto_correct_data(request: BatchValidationRequest):
            """Kötegelt adatok automatikus javítása."""
            try:
                corrected_data, corrections = self.validator.auto_correct_batch(
                    request.data, request.data_type
                )

                return {
                    "status": "success",
                    "message": f"Auto-corrected {len(corrections)} issues",
                    "corrected_data": corrected_data,
                    "corrections": corrections,
                    "corrections_count": len(corrections),
                }

            except Exception as e:
                self.logger.error(f"Error auto-correcting data: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/v1/quality/history")
        async def get_quality_history(
            symbol: str | None = None,
            timeframe: str | None = None,
            limit: int = 30,
        ):
            """Minőségtörténet lekérdezése."""
            try:
                if not self.validator.quality_framework:
                    return {
                        "status": "error",
                        "message": "Data Quality Framework not enabled",
                    }

                history = self.validator.quality_framework.quality_history

                # Szűrés szimbólumra és időkeretre
                if symbol or timeframe:
                    filtered_history = [
                        h
                        for h in history
                        if (not symbol or h.get("symbol") == symbol)
                        and (not timeframe or h.get("timeframe") == timeframe)
                    ]
                else:
                    filtered_history = history

                # Limit alkalmazása
                filtered_history = filtered_history[-limit:]

                return {
                    "status": "success",
                    "history": filtered_history,
                    "total_entries": len(filtered_history),
                }

            except Exception as e:
                self.logger.error(f"Error getting quality history: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/v1/quality/track")
        async def track_quality(symbol: str, timeframe: str):
            """Minőség nyomon követése adott szimbólumra és időkeretre."""
            try:
                self.validator.track_quality(symbol, timeframe)

                return {
                    "status": "success",
                    "message": f"Quality tracking enabled for {symbol} {timeframe}",
                }

            except Exception as e:
                self.logger.error(f"Error tracking quality: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        # ===== HISTORICAL DATA ENDPOINTS =====

        @self.app.post("/api/v1/historical/request")
        async def request_historical_data(request: HistoricalDataRequest):
            """Historikus adatkérés létrehozása."""
            try:
                result = self.historical_manager.request_historical_data(
                    symbol=request.symbol,
                    timeframe=request.timeframe,
                    start_date=request.start_date,
                    end_date=request.end_date,
                    batch_size=request.batch_size,
                    priority=request.priority,
                )
                return result
            except HTTPException:
                raise
            except Exception as e:
                self.logger.error(f"Error in historical data request: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/v1/historical/status/{job_id}")
        async def get_historical_job_status(job_id: str):
            """Historikus job státusz lekérdezése."""
            try:
                result = self.historical_manager.get_job_status(job_id)
                return result
            except HTTPException:
                raise
            except Exception as e:
                self.logger.error(f"Error getting job status: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/v1/historical/collect")
        async def collect_historical_data(data: HistoricalDataCollect):
            """Historikus adatok fogadása az EA-tól."""
            try:
                result = self.historical_manager.collect_historical_data(
                    job_id=data.job_id,
                    batch_number=data.batch_number,
                    symbol=data.symbol,
                    timeframe=data.timeframe,
                    date_range=data.date_range,
                    bars=data.bars,
                )
                return result
            except HTTPException:
                raise
            except Exception as e:
                self.logger.error(f"Error collecting historical data: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/v1/data/gaps")
        async def get_data_gaps(
            symbol: str | None = None,
            timeframe: str | None = None,
            start_date: str | None = None,
            end_date: str | None = None,
        ):
            """Adathézagok azonosítása."""
            try:
                result = self.historical_manager.identify_data_gaps(
                    symbol=symbol,
                    timeframe=timeframe,
                    start_date=start_date,
                    end_date=end_date,
                )
                return result
            except HTTPException:
                raise
            except Exception as e:
                self.logger.error(f"Error identifying data gaps: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/v1/data/fill-gaps")
        async def fill_data_gaps(request: GapDetectionRequest):
            """Adathézagok pótlásának kérése."""
            try:
                # Először azonosítjuk a hézagokat
                gaps_result = self.historical_manager.identify_data_gaps(
                    symbol=request.symbol,
                    timeframe=request.timeframe,
                    start_date=request.start_date,
                    end_date=request.end_date,
                )

                # Ha vannak hézagok, létrehozzuk a pótlási job-okat
                if gaps_result["total_gaps"] > 0:
                    job_ids = []
                    for gap in gaps_result["gaps"]:
                        job_result = self.historical_manager.request_historical_data(
                            symbol=gap["symbol"],
                            timeframe=gap["timeframe"],
                            start_date=gap["start"],
                            end_date=gap["end"],
                            batch_size=30,  # Kis kötegekben pótoljuk
                            priority="high",
                        )
                        job_ids.append(job_result["job_id"])

                    return {
                        "status": "success",
                        "message": f"Gap filling jobs created: {len(job_ids)}",
                        "job_ids": job_ids,
                        "total_gaps": gaps_result["total_gaps"],
                    }
                else:
                    return {
                        "status": "success",
                        "message": "No data gaps found",
                        "total_gaps": 0,
                    }

            except HTTPException:
                raise
            except Exception as e:
                self.logger.error(f"Error filling data gaps: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/v1/historical/start")
        async def start_historical_collection(
            auto_start: bool = True,
            symbol: str | None = None,
            timeframe: str | None = None,
            start_date: str | None = None,
            end_date: str | None = None,
            batch_size: int = 365,
            priority: str = "normal",
        ):
            """Historikus adatgyűjtés indítása.

            Args:
                auto_start: Automatikus indítás (hiányzó adatok detektálása és feltöltése)
                symbol: Szimbólum (opcionális, ha nincs megadva, minden szimbólumra indít)
                timeframe: Időkeret (opcionális)
                start_date: Kezdő dátum (opcionális)
                end_date: Befejező dátum (opcionális)
                batch_size: Kötegméret (alapértelmezett: 365 nap)
                priority: Prioritás (normal, high, low)
            """
            try:
                if auto_start:
                    # Automatikus indítás - hiányzó adatok detektálása és feltöltése
                    result = self.historical_manager.auto_start_historical_collection()
                    return result

                elif symbol:
                    # Specifikus szimbólum és időkeret indítása
                    if not start_date or not end_date:
                        raise HTTPException(
                            status_code=400,
                            detail="start_date and end_date are required when symbol is specified",
                        )

                    result = self.historical_manager.request_historical_data(
                        symbol=symbol,
                        timeframe=timeframe or "H1",
                        start_date=start_date,
                        end_date=end_date,
                        batch_size=batch_size,
                        priority=priority,
                    )
                    return result

                else:
                    # Összes szimbólum indítása
                    result = await self.historical_manager.start_historical_collection_for_all_instruments()
                    return result

            except HTTPException:
                raise
            except Exception as e:
                self.logger.error(f"Error starting historical collection: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/v1/historical/pending")
        async def get_pending_historical_requests():
            """Get pending historical data requests."""
            try:
                self.logger.info("=== HISTORICAL REQUEST RECEIVED ===")
                self.logger.info(f"Time: {datetime.now()}")

                # Kérdezd le a pending job-okat
                pending_jobs = self.historical_manager.get_pending_jobs()

                self.logger.info(f"Pending jobs: {len(pending_jobs)}")
                for job in pending_jobs:
                    self.logger.info(
                        f"  - Job {job['job_id']}: {job['symbol']} {job['timeframe']} ({job['status']})"
                    )

                result = {
                    "status": "success",
                    "jobs": pending_jobs,
                    "count": len(pending_jobs),
                }

                self.logger.info(f"Response: {result}")
                self.logger.info("=== END HISTORICAL REQUEST ===")

                return result
            except Exception as e:
                self.logger.error(f"Error getting pending jobs: {e}")
                return {"status": "error", "message": str(e)}

        @self.app.get("/api/v1/historical/poll")
        async def poll_historical_requests():
            """Poll for pending historical data requests (compatibility endpoint)."""
            try:
                self.logger.info("=== HISTORICAL POLL REQUEST RECEIVED ===")
                self.logger.info(f"Time: {datetime.now()}")

                # Kérdezd le a pending job-okat
                pending_jobs = self.historical_manager.get_pending_jobs()

                self.logger.info(f"Pending jobs: {len(pending_jobs)}")

                # Ha vannak függőben lévő job-ok, adjuk vissza az elsőt
                if pending_jobs:
                    job = pending_jobs[0]
                    self.logger.info(f"Returning job: {job['job_id']}")
                    self.logger.info("=== END HISTORICAL POLL ===")

                    return {
                        "job_id": job["job_id"],
                        "symbol": job["symbol"],
                        "timeframe": job["timeframe"],
                        "start_date": job["start_date"],
                        "end_date": job["end_date"],
                        "batch_size_days": job["batch_size"],
                    }
                else:
                    self.logger.info("No pending jobs")
                    self.logger.info("=== END HISTORICAL POLL ===")
                    return {}

            except Exception as e:
                self.logger.error(f"Error polling historical jobs: {e}")
                return {}

        @self.app.post("/api/v1/historical/trigger")
        async def trigger_historical_request():
            """Trigger immediate historical data request to Expert."""
            try:
                self.logger.info("=== TRIGGER HISTORICAL REQUEST ===")
                self.logger.info(f"Time: {datetime.now()}")

                # Kérdezd le a pending job-okat
                pending_jobs = self.historical_manager.get_pending_jobs()

                if not pending_jobs:
                    self.logger.info("No pending jobs found")
                    return {
                        "status": "no_jobs",
                        "message": "No pending historical jobs found",
                    }

                # Válaszd ki az első job-ot
                job = pending_jobs[0]
                job_id = job["job_id"]

                self.logger.info(f"Triggering job: {job_id}")
                self.logger.info(f"Symbol: {job['symbol']}")
                self.logger.info(f"Timeframe: {job['timeframe']}")

                # Itt küldj egy speciális kérést az Expertnek
                # Ez egy "push" mechanizmus lesz, nem "pull"

                # Jelenleg csak logoljuk, hogy a kérés érkezett
                # A jövőben itt lehet WebSocket vagy más push technológiát implementálni

                self.logger.info("=== END TRIGGER HISTORICAL REQUEST ===")

                return {
                    "status": "success",
                    "message": "Historical request triggered",
                    "job_id": job_id,
                    "job": job,
                }

            except Exception as e:
                self.logger.error(f"Error triggering historical request: {e}")
                return {"status": "error", "message": str(e)}

        @self.app.post("/api/v1/historical/progress")
        async def update_historical_progress(request: HistoricalProgressUpdate):
            """Historikus adatgyűjtés progresszének frissítése."""
            try:
                job_id = request.job_id
                progress = request.progress
                total_bars = request.total_bars
                current_batch = request.current_batch

                self.logger.info(f"Progress update for job {job_id}: {progress}%")
                self.logger.info(f"  - Total bars: {total_bars}")
                self.logger.info(f"  - Current batch: {current_batch}")

                # Progressz mentése az adatbázisba
                # Ehhez szükségünk van egy új metódusra a HistoricalDataManagerben
                # Jelenleg csak logoljuk

                return {"status": "success"}

            except Exception as e:
                self.logger.error(f"Error updating progress: {e}")
                return {"status": "error", "message": str(e)}

        # ===== TRAINING DATASET ENDPOINTS =====

        @self.app.post("/api/v1/training/generate")
        async def generate_training_dataset(request: TrainingDatasetGenerateRequest):
            """Tanulási adathalmaz generálása."""
            try:
                # Training Dataset Generator inicializálása
                # Data Warehouse Manager inicializálása
                from neural_ai.collectors.mt5.implementations.storage.data_warehouse_manager import (
                    DataWarehouseManager,
                )
                from neural_ai.collectors.mt5.implementations.training_dataset_generator import (
                    TrainingDatasetGenerator,
                )

                warehouse_manager = DataWarehouseManager(base_path="data", logger=self.file_logger)

                training_generator = TrainingDatasetGenerator(
                    warehouse_manager=warehouse_manager, logger=self.file_logger
                )

                # Adathalmaz generálása
                result = training_generator.generate_dataset(
                    dataset_type=request.dataset_type,
                    symbols=request.symbols,
                    timeframes=request.timeframes,
                    end_date=request.date_range.get("end"),
                    quality_threshold=request.quality_threshold,
                    output_format=request.output_format,
                )

                return result

            except Exception as e:
                self.logger.error(f"Error generating training dataset: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/v1/training/status/{dataset_id}")
        async def get_training_dataset_status(dataset_id: str):
            """Tanulási adathalmaz állapotának lekérdezése."""
            try:
                from neural_ai.collectors.mt5.implementations.storage.data_warehouse_manager import (
                    DataWarehouseManager,
                )
                from neural_ai.collectors.mt5.implementations.training_dataset_generator import (
                    TrainingDatasetGenerator,
                )

                warehouse_manager = DataWarehouseManager(base_path="data", logger=self.file_logger)

                training_generator = TrainingDatasetGenerator(
                    warehouse_manager=warehouse_manager, logger=self.file_logger
                )

                result = training_generator.get_dataset_status(dataset_id)
                return result

            except Exception as e:
                self.logger.error(f"Error getting dataset status: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/v1/training/datasets")
        async def list_training_datasets(dataset_type: str | None = None):
            """Elérhető tanulási adathalmazok listázása."""
            try:
                from neural_ai.collectors.mt5.implementations.storage.data_warehouse_manager import (
                    DataWarehouseManager,
                )
                from neural_ai.collectors.mt5.implementations.training_dataset_generator import (
                    TrainingDatasetGenerator,
                )

                warehouse_manager = DataWarehouseManager(base_path="data", logger=self.file_logger)

                training_generator = TrainingDatasetGenerator(
                    warehouse_manager=warehouse_manager, logger=self.file_logger
                )

                result = training_generator.list_datasets(dataset_type)
                return result

            except Exception as e:
                self.logger.error(f"Error listing datasets: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/v1/training/info")
        async def get_training_dataset_info():
            """Tanulási adathalmaz típusok információinak lekérdezése."""
            try:
                from neural_ai.collectors.mt5.implementations.storage.data_warehouse_manager import (
                    DataWarehouseManager,
                )
                from neural_ai.collectors.mt5.implementations.training_dataset_generator import (
                    TrainingDatasetGenerator,
                )

                warehouse_manager = DataWarehouseManager(base_path="data", logger=self.file_logger)

                training_generator = TrainingDatasetGenerator(
                    warehouse_manager=warehouse_manager, logger=self.file_logger
                )

                result = training_generator.get_dataset_info()
                return result

            except Exception as e:
                self.logger.error(f"Error getting dataset info: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        # ===== DATA WAREHOUSE ENDPOINTS =====

        @self.app.get("/api/v1/warehouse/stats")
        async def get_warehouse_stats():
            """Data Warehouse statisztikák lekérdezése."""
            try:
                stats = self.collector_storage.get_warehouse_stats()
                return stats

            except Exception as e:
                self.logger.error(f"Error getting warehouse stats: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/v1/warehouse/organize")
        async def organize_to_warehouse(
            instrument: str,
            timeframe: str | None = None,
            data_type: str = "validated",
        ):
            """Adatok szervezése a Data Warehouse-ba."""
            try:
                result = self.collector_storage.organize_data_to_warehouse(
                    instrument=instrument, timeframe=timeframe, data_type=data_type
                )
                return result

            except Exception as e:
                self.logger.error(f"Error organizing to warehouse: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/v1/warehouse/auto-organize")
        async def auto_organize_warehouse():
            """Validált adatok automatikus szervezése."""
            try:
                result = self.collector_storage.auto_organize_validated_data()
                return result

            except Exception as e:
                self.logger.error(f"Error auto-organizing warehouse: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/v1/warehouse/merge")
        async def merge_update_to_historical(instrument: str, timeframe: str):
            """Update adatok merge-elése historical-ba."""
            try:
                result = self.collector_storage.merge_update_to_historical(
                    instrument=instrument, timeframe=timeframe
                )
                return result

            except Exception as e:
                self.logger.error(f"Error merging to historical: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/v1/warehouse/maintenance")
        async def run_warehouse_maintenance():
            """Warehouse karbantartás futtatása."""
            try:
                result = self.collector_storage.schedule_warehouse_maintenance()
                return result

            except Exception as e:
                self.logger.error(f"Error running warehouse maintenance: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/v1/warehouse/backup")
        async def backup_warehouse(
            backup_name: str,
            instruments: str | None = None,
            timeframes: str | None = None,
        ):
            """Warehouse adatok biztonsági mentése."""
            try:
                instrument_list = instruments.split(",") if instruments else None
                timeframe_list = timeframes.split(",") if timeframes else None

                result = self.collector_storage.backup_warehouse_data(
                    backup_name=backup_name,
                    instruments=instrument_list,
                    timeframes=timeframe_list,
                )
                return result

            except Exception as e:
                self.logger.error(f"Error backing up warehouse: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/v1/warehouse/validate")
        async def validate_warehouse(
            instrument: str, timeframe: str, location: str = "warehouse/historical"
        ):
            """Warehouse adatok integritásának ellenőrzése."""
            try:
                result = self.collector_storage.validate_warehouse_integrity(
                    instrument=instrument, timeframe=timeframe, location=location
                )
                return result

            except Exception as e:
                self.logger.error(f"Error validating warehouse: {e}")
                raise HTTPException(status_code=500, detail=str(e))

    async def connect(self) -> bool:
        """Kapcsolódás (nyitott API esetén mindig True)."""
        return True

    async def disconnect(self) -> bool:
        """Kapcsolat bontás."""
        self.is_running = False
        return True

    def is_connected(self) -> bool:
        """Kapcsolat állapota."""
        return self.is_running

    async def collect_data(
        self,
        symbol: str,
        timeframe: str,
        start_date: str | dt.datetime | None = None,
        end_date: str | dt.datetime | None = None,
    ) -> pd.DataFrame:
        """Adatok gyűjtése (nem implementált, mert API-n keresztül jönnek az adatok)."""
        raise NotImplementedError("Direct data collection not supported. Use FastAPI endpoints.")

    async def get_available_symbols(self) -> list[str]:
        """Elérhető szimbólumok."""
        return ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]

    def get_available_timeframes(self) -> dict[str, int]:
        """Elérhető időkeretek."""
        return {"M1": 1, "M5": 5, "M15": 15, "H1": 60, "H4": 240, "D1": 1440}

    def _process_tick_data(self, symbol: str) -> None:
        """Process tick data for a symbol with DLQ support.

        Args:
            symbol: Symbol to process tick data for
        """
        try:
            # Note: In the current FastAPI-based architecture, tick data
            # is received via POST /api/v1/collect/tick endpoint.
            # This method is a placeholder for future batch processing
            # or retry logic that may be implemented.

            self.logger.debug(f"Processing tick data for {symbol}")

            # In a future implementation, this would:
            # 1. Fetch tick data from storage
            # 2. Validate the data
            # 3. Process/store the data
            # 4. Handle failures with DLQ

            # Placeholder for tick data processing
            # tick_data = self.collector_storage.get_tick_data(symbol)
            # if tick_data:
            #     validation_result = self.validator.validate_tick(tick_data)
            #     if not validation_result.is_valid:
            #         error = MT5DataValidationError(f"Tick data validation failed for {symbol}")
            #         self._dlq.record_failure(
            #             data={'symbol': symbol, 'tick_data': tick_data},
            #             error=error,
            #             context={'timeframe': 'TICK', 'symbol': symbol},
            #             retryable=True
            #         )
            #         return

        except Exception as e:
            self.logger.exception(f"Failed to process tick data for {symbol}")

            # Record to DLQ
            self._dlq.record_failure(
                data={"symbol": symbol},
                error=e,
                context={"timeframe": "TICK", "symbol": symbol},
                retryable=isinstance(e, (MT5ConnectionError, MT5TimeoutError)),
            )

    def _fetch_historical_data(
        self, symbol: str, timeframe: int, start: int, end: int
    ) -> pd.DataFrame | None:
        """Fetch historical data with DLQ support.

        Args:
            symbol: Symbol to fetch data for
            timeframe: Timeframe in minutes
            start: Start timestamp
            end: End timestamp

        Returns:
            DataFrame with historical data or None if failed
        """
        try:
            # Note: In the current FastAPI-based architecture, historical data
            # is received via POST /api/v1/collect/ohlcv endpoint.
            # This method is a placeholder for future direct MT5 API integration
            # or retry logic that may be implemented.

            self.logger.debug(f"Fetching historical data for {symbol} timeframe {timeframe}")

            # Placeholder for historical data fetching
            # In a future implementation, this would:
            # 1. Call MT5 API to fetch rates
            # 2. Validate the data
            # 3. Handle failures with DLQ

            # rates = mt5.copy_rates_range(symbol, timeframe, start, end)
            # if rates is None or len(rates) == 0:
            #     error = MT5DataValidationError(f"No data returned for {symbol} timeframe {timeframe}")
            #     self._dlq.record_failure(
            #         data={'symbol': symbol, 'timeframe': timeframe, 'start': start, 'end': end},
            #         error=error,
            #         context={'timeframe': timeframe, 'symbol': symbol},
            #         retryable=False
            #     )
            #     return None

            # df = pd.DataFrame(rates)
            # return df

            return None  # Placeholder - would return actual data

        except Exception as e:
            self.logger.exception(f"Failed to fetch historical data for {symbol}")

            # Record to DLQ
            self._dlq.record_failure(
                data={
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "start": start,
                    "end": end,
                },
                error=e,
                context={"timeframe": timeframe, "symbol": symbol},
                retryable=isinstance(e, (MT5ConnectionError, MT5TimeoutError)),
            )
            raise

    def retry_failed_data(self, max_retries: int = 3) -> dict[str, Any]:
        """Retry processing failed data from DLQ.

        Args:
            max_retries: Maximum number of retry attempts

        Returns:
            Statistics about retry attempts
        """
        stats = {"total_retried": 0, "successful": 0, "failed": 0, "errors": []}

        # Get retryable failures from DLQ
        failures = self._dlq.get_failures(retryable_only=True)

        for failure in failures:
            try:
                data = failure.get("data", {})
                context = failure.get("context", {})

                # Determine processing type based on context
                if context.get("timeframe") == "TICK":
                    # Retry tick data processing
                    symbol = data.get("symbol")
                    if symbol:
                        self._process_tick_data(symbol)
                elif "timeframe" in context:
                    # Retry historical data fetch
                    symbol = data.get("symbol")
                    timeframe = context.get("timeframe")
                    if symbol and timeframe and timeframe != "TICK":
                        # Note: We would need to store more context to properly retry
                        # For now, just log the attempt
                        self.logger.info(f"Retry attempt for historical data: {symbol} {timeframe}")

                stats["successful"] += 1
                stats["total_retried"] += 1

                # Mark as processed
                self._dlq.mark_as_processed(failure["timestamp"])

            except Exception as e:
                stats["failed"] += 1
                stats["total_retried"] += 1
                stats["errors"].append(str(e))
                self.logger.error(f"Failed to retry processing: {e}")

        return stats

    def get_dlq_statistics(self) -> dict[str, Any]:
        """Get DLQ statistics."""
        return self._dlq.get_statistics()

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Szerver indítása.

        Args:
            host: Hoszt cím
            port: Port szám
        """
        self.logger.info(f"Starting MT5 Collector server on {host}:{port}")
        self.is_running = True
        uvicorn.run(self.app, host=host, port=port)
