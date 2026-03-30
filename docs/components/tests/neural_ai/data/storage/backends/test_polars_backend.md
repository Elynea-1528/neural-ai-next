# 🧪 Teszt: tests/neural_ai/data/storage/backends/test_polars_backend.py

**Tesztelt modul:** [`neural_ai/data/storage/backends/polars_backend.py`](../../neural_ai/data/storage/backends/polars_backend.py)

Polars Backend Teszt Modul.

# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false
# Polars DataFrame fixture type hibák.

Ez a modul tartalmazza a PolarsBackend osztály tesztjeit.

## Teszt Osztály: `TestPolarsDataFrame`

PolarsDataFrame wrapper osztály tesztjei.

### ✓ `test_init()`

Teszteli a PolarsDataFrame inicializálását.

### ✓ `test_import_polars()`

Teszteli a lazy import funkcionalitást.

### ✓ `test_pl_property()`

Teszteli a pl property-t.

### ✓ `test_pa_property()`

Teszteli a pa property-t.

### ✓ `test_pq_property()`

Teszteli a pq property-t.

## Teszt Osztály: `TestPolarsBackend`

PolarsBackend osztály tesztjei.

### ✓ `test_init()`

Teszteli a PolarsBackend inicializálását.

### ✓ `test_write_basic()`

Teszteli az alap write műveletet.

### ✓ `test_write_with_compression()`

Teszteli a write műveletet tömörítéssel.

### ✓ `test_write_invalid_data()`

Teszteli a write műveletet érvénytelen adatokkal.

### ✓ `test_write_invalid_path()`

Teszteli a write műveletet érvénytelen elérési úttal.

### ✓ `test_read_basic()`

Teszteli az alap read műveletet.

### ✓ `test_read_with_columns()`

Teszteli a read műveletet oszlopszűréssel.

### ✓ `test_read_file_not_found()`

Teszteli a read műveletet nem létező fájllal.

### ✓ `test_read_chunked()`

Teszteli a chunkolt olvasást.

### ✓ `test_append_to_new_file()`

Teszteli a hozzáfűzést új fájlhoz.

### ✓ `test_append_to_existing_file()`

Teszteli a hozzáfűzést meglévő fájlhoz.

### ✓ `test_append_with_schema_validation_valid()`

Teszteli a hozzáfűzést sémavizsgálattal - érvényes eset.

### ✓ `test_append_with_schema_validation_invalid()`

Teszteli a hozzáfűzést sémavizsgálattal - érvénytelen eset.

### ✓ `test_append_invalid_data()`

Teszteli a hozzáfűzést érvénytelen adatokkal.

### ✓ `test_supports_format()`

Teszteli a supports_format metódust.

### ✓ `test_get_info()`

Teszteli a get_info metódust.

### ✓ `test_get_info_file_not_found()`

Teszteli a get_info metódust nem létező fájllal.

### ✓ `test_validate_data()`

Teszteli a validate_data metódust.

### ✓ `test_repr()`

Teszteli a __repr__ metódust.

### ✓ `test_write_partitioned()`

Teszteli a particionált írást.

### ✓ `test_read_with_filters()`

Teszteli az olvasást szűrőkkel.

### ✓ `test_validate_schema_valid()`

Teszteli a _validate_schema metódust érvényes esetre.

### ✓ `test_validate_schema_invalid()`

Teszteli a _validate_schema metódust érvénytelen esetre.

### ✓ `test_validate_schema_exception()`

Teszteli a _validate_schema metódust kivétel esetén.

### ✓ `test_read_chunked_implementation()`

Teszteli a _read_chunked metódust.

---

**Teszt fájl:** [`tests/neural_ai/data/storage/backends/test_polars_backend.py`](../../tests/neural_ai/data/storage/backends/test_polars_backend.py)

**Tesztelt modul:** [`neural_ai/data/storage/backends/polars_backend.py`](../../neural_ai/data/storage/backends/polars_backend.py)
