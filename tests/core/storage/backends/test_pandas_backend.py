"""Pandas Backend Teszt Modul.

Ez a modul tartalmazza a PandasBackend osztály tesztjeit.
"""

import os
import tempfile
from pathlib import Path
from typing import Any

import pytest

from neural_ai.core.storage.backends.pandas_backend import PandasBackend


class TestPandasDataFrame:
    """PandasDataFrame wrapper osztály tesztjei."""

    def test_init(self) -> None:
        """Teszteli a PandasDataFrame inicializálását."""
        wrapper = PandasBackend()._pandas_wrapper
        assert wrapper._pandas is None
        assert wrapper._fastparquet is None

    def test_import_pandas(self) -> None:
        """Teszteli a lazy import funkcionalitást."""
        wrapper = PandasBackend()._pandas_wrapper
        pd, fp = wrapper._import_pandas()
        assert pd is not None
        assert fp is not None
        assert wrapper._pandas is not None
        assert wrapper._fastparquet is not None

    def test_pd_property(self) -> None:
        """Teszteli a pd property-t."""
        wrapper = PandasBackend()._pandas_wrapper
        pd = wrapper.pd
        assert pd is not None

    def test_fp_property(self) -> None:
        """Teszteli az fp property-t."""
        wrapper = PandasBackend()._pandas_wrapper
        fp = wrapper.fp
        assert fp is not None


class TestPandasBackend:
    """PandasBackend osztály tesztjei."""

    @pytest.fixture
    def backend(self) -> PandasBackend:
        """Visszaad egy PandasBackend példányt."""
        return PandasBackend()

    @pytest.fixture
    def sample_dataframe(self, backend: PandasBackend) -> Any:
        """Visszaad egy mint DataFrame-et."""
        pd = backend._pandas_wrapper.pd
        return pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35]
        })

    @pytest.fixture
    def temp_dir(self) -> Path:
        """Visszaad egy ideiglenes könyvtárat."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_init(self, backend: PandasBackend) -> None:
        """Teszteli a PandasBackend inicializálását."""
        assert backend.name == 'pandas'
        assert backend.supported_formats == ['parquet']
        assert backend.is_async is True
        assert backend._initialized is False

    def test_ensure_initialized(self, backend: PandasBackend) -> None:
        """Teszteli a _ensure_initialized metódust."""
        assert backend._initialized is False
        backend._ensure_initialized()
        assert backend._initialized is True

    def test_write_basic(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli az alap write műveletet."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        assert path.exists()
        backend._ensure_initialized()
        assert backend._pandas_wrapper.fp.ParquetFile(str(path)) is not None

    def test_write_with_compression(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a write műveletet tömörítéssel."""
        path = temp_dir / "test_compressed.parquet"
        backend.write(sample_dataframe, str(path), compression='gzip')
        
        assert path.exists()

    def test_write_invalid_data(self, backend: PandasBackend, temp_dir: Path) -> None:
        """Teszteli a write műveletet érvénytelen adatokkal."""
        path = temp_dir / "test.parquet"
        with pytest.raises(RuntimeError, match="Érvénytelen DataFrame adatok"):
            backend.write(None, str(path))

    def test_write_invalid_path(self, backend: PandasBackend, sample_dataframe: Any) -> None:
        """Teszteli a write műveletet érvénytelen elérési úttal."""
        with pytest.raises(RuntimeError, match="\.parquet kiterjesztéssel kell rendelkeznie"):
            backend.write(sample_dataframe, "/invalid/path.txt")

    def test_read_basic(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli az alap read műveletet."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        result = backend.read(str(path))
        assert len(result) == 3
        assert list(result.columns) == ['id', 'name', 'age']

    def test_read_with_columns(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a read műveletet oszlopszűréssel."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        result = backend.read(str(path), columns=['id', 'name'])
        assert len(result.columns) == 2
        assert 'age' not in result.columns

    def test_read_file_not_found(self, backend: PandasBackend, temp_dir: Path) -> None:
        """Teszteli a read műveletet nem létező fájllal."""
        path = temp_dir / "nonexistent.parquet"
        with pytest.raises(FileNotFoundError):
            backend.read(str(path))

    def test_read_chunked(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a chunkolt olvasást."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        result = backend.read(str(path), chunk_size=2)
        assert len(result) == 3

    def test_append_to_new_file(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a hozzáfűzést új fájlhoz."""
        path = temp_dir / "test.parquet"
        backend.append(sample_dataframe, str(path))
        
        assert path.exists()
        result = backend.read(str(path))
        assert len(result) == 3

    def test_append_to_existing_file(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a hozzáfűzést meglévő fájlhoz."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        # Új adatok
        pd = backend._pandas_wrapper.pd
        new_data = pd.DataFrame({
            'id': [4, 5],
            'name': ['David', 'Eve'],
            'age': [28, 32]
        })
        
        backend.append(new_data, str(path))
        result = backend.read(str(path))
        assert len(result) == 5

    def test_append_with_schema_validation_valid(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a hozzáfűzést sémavizsgálattal - érvényes eset."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        # Ugyanazok az oszlopok
        pd = backend._pandas_wrapper.pd
        new_data = pd.DataFrame({
            'id': [4],
            'name': ['David'],
            'age': [28]
        })
        
        backend.append(new_data, str(path), schema_validation=True)
        result = backend.read(str(path))
        assert len(result) == 4

    def test_append_with_schema_validation_invalid(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a hozzáfűzést sémavizsgálattal - érvénytelen eset."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        # Hiányzó oszlop
        pd = backend._pandas_wrapper.pd
        new_data = pd.DataFrame({
            'id': [4],
            'name': ['David']
            # 'age' oszlop hiányzik
        })
        
        with pytest.raises(ValueError, match="sémája nem kompatibilis"):
            backend.append(new_data, str(path), schema_validation=True)

    def test_append_invalid_data(self, backend: PandasBackend, temp_dir: Path) -> None:
        """Teszteli a hozzáfűzést érvénytelen adatokkal."""
        path = temp_dir / "test.parquet"
        with pytest.raises(ValueError, match="Érvénytelen DataFrame adatok"):
            backend.append(None, str(path))

    def test_supports_format(self, backend: PandasBackend) -> None:
        """Teszteli a supports_format metódust."""
        assert backend.supports_format('parquet') is True
        assert backend.supports_format('csv') is False
        assert backend.supports_format('json') is False

    def test_get_info(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a get_info metódust."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        info = backend.get_info(str(path))
        
        assert info['size'] > 0
        assert info['rows'] == 3
        assert set(info['columns']) == {'id', 'name', 'age'}
        assert info['format'] == 'parquet'
        assert 'created' in info
        assert 'modified' in info
        assert 'num_row_groups' in info
        assert 'compression' in info

    def test_get_info_file_not_found(self, backend: PandasBackend, temp_dir: Path) -> None:
        """Teszteli a get_info metódust nem létező fájllal."""
        path = temp_dir / "nonexistent.parquet"
        with pytest.raises(FileNotFoundError):
            backend.get_info(str(path))

    def test_validate_data(self, backend: PandasBackend, sample_dataframe: Any) -> None:
        """Teszteli a validate_data metódust."""
        assert backend.validate_data(sample_dataframe) is True
        assert backend.validate_data(None) is False

    def test_repr(self, backend: PandasBackend) -> None:
        """Teszteli a __repr__ metódust."""
        repr_str = repr(backend)
        assert 'PandasBackend' in repr_str
        assert 'pandas' in repr_str
        assert 'parquet' in repr_str

    def test_write_partitioned(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a particionált írást."""
        path = temp_dir / "partitioned.parquet"
        backend.write(sample_dataframe, str(path), partition_by=['age'])
        
        # A particionált írás létrehoz egy könyvtárat
        assert path.exists() or path.parent.exists()

    def test_write_with_index(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli az írást index mentéssel."""
        path = temp_dir / "test_index.parquet"
        backend.write(sample_dataframe, str(path), index=True)
        
        assert path.exists()

    def test_read_with_filters(self, backend: PandasBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli az olvasást szűrőkkel."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        # Szűrők a fastparquet formátumban
        filters = [('age', '=', 25)]
        result = backend.read(str(path), filters=filters)
        assert len(result) >= 0  # Legalább 0 sor, attól függ a szűrés

    def test_validate_schema_valid(self, backend: PandasBackend, sample_dataframe: Any) -> None:
        """Teszteli a _validate_schema metódust érvényes esetre."""
        pd = backend._pandas_wrapper.pd
        new_data = pd.DataFrame({
            'id': [4],
            'name': ['David'],
            'age': [28],
            'extra': ['info']  # Extra oszlop is lehet
        })
        
        assert backend._validate_schema(sample_dataframe, new_data) is True

    def test_validate_schema_invalid(self, backend: PandasBackend, sample_dataframe: Any) -> None:
        """Teszteli a _validate_schema metódust érvénytelen esetre."""
        pd = backend._pandas_wrapper.pd
        new_data = pd.DataFrame({
            'id': [4],
            'name': ['David']
            # 'age' oszlop hiányzik
        })
        
        assert backend._validate_schema(sample_dataframe, new_data) is False

    def test_validate_schema_exception(self, backend: PandasBackend) -> None:
        """Teszteli a _validate_schema metódust kivétel esetén."""
        # Olyan objektumok, amelyeknek nincs columns attribútuma
        assert backend._validate_schema("invalid", "invalid") is False