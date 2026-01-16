"""Storage komponens implementációk."""

from neural_ai.data.storage.implementations.file_storage import FileStorage
from neural_ai.data.storage.implementations.parquet_storage import ParquetStorageService

__all__ = [
    "FileStorage",
    "ParquetStorageService",
]
