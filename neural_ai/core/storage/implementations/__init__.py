"""Storage komponens implementációk."""

from neural_ai.core.storage.implementations.file_storage import FileStorage
from neural_ai.core.storage.implementations.parquet_storage import ParquetStorageService

__all__ = [
    "FileStorage",
    "ParquetStorageService",
]
