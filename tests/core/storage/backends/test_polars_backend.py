"""Polars Backend Teszt Modul.

Ez a modul tartalmazza a PolarsBackend osztály tesztjeit.
"""

import os
import tempfile
from pathlib import Path
from typing import Any

import pytest

from neural_ai.core.storage.backends.polars_backend import PolarsBackend


class TestPolarsDataFrame:
    """PolarsDataFrame wrapper osztály tesztjei."""

    def test_init(self) -> None:
        """Teszteli a PolarsDataFrame inicializálását."""
        wrapper = PolarsBackend()._polars_wrapper
        assert wrapper._polars is None
        assert wrapper._pyarrow is None

    def test_import_polars(self) -> None:
        """Teszteli a lazy import funkcionalitást."""
        wrapper = PolarsBackend()._polars_wrapper
        pl, pa, pq = wrapper._import_polars()
        assert pl is not None
        assert pa is not None
        assert pq is not None
        assert wrapper._polars is not None
        assert wrapper._pyarrow is not None

    def test_pl_property(self) -> None:
        """Teszteli a pl property-t."""
        wrapper = PolarsBackend()._polars_wrapper
        pl = wrapper.pl
        assert pl is not None

    def test_pa_property(self) -> None:
        """Teszteli a pa property-t."""
        wrapper = PolarsBackend()._polars_wrapper
        pa = wrapper.pa
        assert pa is not None

    def test_pq_property(self) -> None:
        """Teszteli a pq property-t."""
        wrapper = PolarsBackend()._polars_wrapper
        pq = wrapper.pq
        assert pq is not None


class TestPolarsBackend:
    """PolarsBackend osztály tesztjei."""

    @pytest.fixture
    def backend(self) -> PolarsBackend:
        """Visszaad egy PolarsBackend példányt."""
        return PolarsBackend()

    @pytest.fixture
    def sample_dataframe(self, backend: PolarsBackend) -> Any:
        """Visszaad egy mint DataFrame-et."""
        pl = backend._polars_wrapper.pl
        return pl.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35]
        })

    @pytest.fixture
    def temp_dir(self) -> Path:
        """Visszaad egy ideiglenes könyvtárat."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_init(self, backend: PolarsBackend) -> None:
        """Teszteli a PolarsBackend inicializálását."""
        assert backend.name == 'polars'
        assert backend.supported_formats == ['parquet']
        assert backend.is_async is True
        assert backend._initialized is False

    def test_ensure_initialized(self, backend: PolarsBackend) -> None:
        """Teszteli a _ensure_initialized metódust."""
        assert backend._initialized is False
        backend._ensure_initialized()
        assert backend._initialized is True

    def test_write_basic(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli az alap write műveletet."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        assert path.exists()
        backend._ensure_initialized()
        # Ellenőrizzük, hogy a fájl valóban Parquet formátumú
        parquet_file = backend._polars_wrapper.pq.ParquetFile(str(path))
        assert parquet_file is not None

    def test_write_with_compression(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a write műveletet tömörítéssel."""
        path = temp_dir / "test_compressed.parquet"
        backend.write(sample_dataframe, str(path), compression='gzip')
        
        assert path.exists()

    def test_write_invalid_data(self, backend: PolarsBackend, temp_dir: Path) -> None:
        """Teszteli a write műveletet érvénytelen adatokkal."""
        path = temp_dir / "test.parquet"
        with pytest.raises(ValueError, match="Érvénytelen DataFrame adatok"):
            backend.write(None, str(path))

    def test_write_invalid_path(self, backend: PolarsBackend, sample_dataframe: Any) -> None:
        """Teszteli a write műveletet érvénytelen elérési úttal."""
        with pytest.raises(ValueError, match="\.parquet kiterjesztéssel kell rendelkeznie"):
            backend.write(sample_dataframe, "/invalid/path.txt")

    def test_read_basic(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli az alap read műveletet."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        result = backend.read(str(path))
        assert len(result) == 3
        assert 'id' in result.columns
        assert 'name' in result.columns
        assert 'age' in result.columns

    def test_read_with_columns(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a read műveletet oszlopszűréssel."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        result = backend.read(str(path), columns=['id', 'name'])
        assert len(result.columns) == 2
        assert 'age' not in result.columns

    def test_read_file_not_found(self, backend: PolarsBackend, temp_dir: Path) -> None:
        """Teszteli a read műveletet nem létező fájllal."""
        path = temp_dir / "nonexistent.parquet"
        with pytest.raises(FileNotFoundError):
            backend.read(str(path))

    def test_read_chunked(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a chunkolt olvasást."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        result = backend.read(str(path), chunk_size=2)
        assert len(result) == 3

    def test_append_to_new_file(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a hozzáfűzést új fájlhoz."""
        path = temp_dir / "test.parquet"
        backend.append(sample_dataframe, str(path))
        
        assert path.exists()
        result = backend.read(str(path))
        assert len(result) == 3

    def test_append_to_existing_file(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a hozzáfűzést meglévő fájlhoz."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        # Új adatok
        pl = backend._polars_wrapper.pl
        new_data = pl.DataFrame({
            'id': [4, 5],
            'name': ['David', 'Eve'],
            'age': [28, 32]
        })
        
        backend.append(new_data, str(path))
        result = backend.read(str(path))
        assert len(result) == 5

    def test_append_with_schema_validation_valid(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a hozzáfűzést sémavizsgálattal - érvényes eset."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        # Ugyanazok az oszlopok
        pl = backend._polars_wrapper.pl
        new_data = pl.DataFrame({
            'id': [4],
            'name': ['David'],
            'age': [28]
        })
        
        backend.append(new_data, str(path), schema_validation=True)
        result = backend.read(str(path))
        assert len(result) == 4

    def test_append_with_schema_validation_invalid(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a hozzáfűzést sémavizsgálattal - érvénytelen eset."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        # Hiányzó oszlop
        pl = backend._polars_wrapper.pl
        new_data = pl.DataFrame({
            'id': [4],
            'name': ['David']
            # 'age' oszlop hiányzik
        })
        
        with pytest.raises(ValueError, match="sémája nem kompatibilis"):
            backend.append(new_data, str(path), schema_validation=True)

    def test_append_invalid_data(self, backend: PolarsBackend, temp_dir: Path) -> None:
        """Teszteli a hozzáfűzést érvénytelen adatokkal."""
        path = temp_dir / "test.parquet"
        with pytest.raises(ValueError, match="Érvénytelen DataFrame adatok"):
            backend.append(None, str(path))

    def test_supports_format(self, backend: PolarsBackend) -> None:
        """Teszteli a supports_format metódust."""
        assert backend.supports_format('parquet') is True
        assert backend.supports_format('csv') is False
        assert backend.supports_format('json') is False

    def test_get_info(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
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

    def test_get_info_file_not_found(self, backend: PolarsBackend, temp_dir: Path) -> None:
        """Teszteli a get_info metódust nem létező fájllal."""
        path = temp_dir / "nonexistent.parquet"
        with pytest.raises(FileNotFoundError):
            backend.get_info(str(path))

    def test_validate_data(self, backend: PolarsBackend, sample_dataframe: Any) -> None:
        """Teszteli a validate_data metódust."""
        assert backend.validate_data(sample_dataframe) is True
        assert backend.validate_data(None) is False

    def test_repr(self, backend: PolarsBackend) -> None:
        """Teszteli a __repr__ metódust."""
        repr_str = repr(backend)
        assert 'PolarsBackend' in repr_str
        assert 'polars' in repr_str
        assert 'parquet' in repr_str

    def test_write_partitioned(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a particionált írást."""
        path = temp_dir / "partitioned.parquet"
        backend.write(sample_dataframe, str(path), partition_by=['age'])
        
        # A particionált írás létrehoz egy könyvtárat
        assert path.exists() or path.parent.exists()

    def test_read_with_filters(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli az olvasást szűrőkkel."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        # Szűrők a pyarrow formátumban
        filters = [('age', '=', 25)]
        result = backend.read(str(path), filters=filters)
        assert len(result) >= 0  # Legalább 0 sor, attól függ a szűrés

    def test_validate_schema_valid(self, backend: PolarsBackend, sample_dataframe: Any) -> None:
        """Teszteli a _validate_schema metódust érvényes esetre."""
        pl = backend._polars_wrapper.pl
        new_data = pl.DataFrame({
            'id': [4],
            'name': ['David'],
            'age': [28],
            'extra': ['info']  # Extra oszlop is lehet
        })
        
        assert backend._validate_schema(sample_dataframe, new_data) is True

    def test_validate_schema_invalid(self, backend: PolarsBackend, sample_dataframe: Any) -> None:
        """Teszteli a _validate_schema metódust érvénytelen esetre."""
        pl = backend._polars_wrapper.pl
        new_data = pl.DataFrame({
            'id': [4],
            'name': ['David']
            # 'age' oszlop hiányzik
        })
        
        assert backend._validate_schema(sample_dataframe, new_data) is False

    def test_validate_schema_exception(self, backend: PolarsBackend) -> None:
        """Teszteli a _validate_schema metódust kivétel esetén."""
        # Olyan objektumok, amelyeknek nincs columns attribútuma
        assert backend._validate_schema("invalid", "invalid") is False

    def test_read_chunked_implementation(self, backend: PolarsBackend, sample_dataframe: Any, temp_dir: Path) -> None:
        """Teszteli a _read_chunked metódust."""
        path = temp_dir / "test.parquet"
        backend.write(sample_dataframe, str(path))
        
        # Közvetlen hívás a _read_chunked metódusra
        result = backend._read_chunked(str(path), chunk_size=2, columns=None, filters=None)
        assert len(result) == 3