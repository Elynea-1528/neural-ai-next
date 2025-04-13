<!-- filepath: /home/elynea/Dokumentumok/neural-ai-next/docs/development/performance_optimization.md -->
# Teljesítmény Optimalizációs Útmutató

Ez az útmutató a Neural-AI-Next rendszer teljesítmény optimalizálási stratégiáit és technikáit tartalmazza.

## 1. Processzor Optimalizáció

### 1.1 Vectorizált műveletek

Mindig részesítsük előnyben a vektorizált műveleteket a ciklusok helyett.

```python
# Kerülendő:
result = []
for i in range(len(data)):
    result.append(data['close'][i] * 2)

# Javasolt:
result = data['close'] * 2
```

### 1.2 Pandas optimalizáció
```python
# Gyorsabb oszlop hozzáférés
close_col = data['close'].values  # NumPy array

# Aggregáló műveletek
data.groupby('symbol').agg({
    'close': ['mean', 'std', 'min', 'max']
})

# apply() helyett vectorizált műveletek
# Kerülendő:
data['result'] = data.apply(lambda row: complex_function(row), axis=1)

# Javasolt:
data['result'] = complex_vectorized_function(data)
```
### 1.3 NumPy hatékony használata
```python
# Broadcasting használata
ma_values = np.sum(prices * weights[:, np.newaxis], axis=0) / np.sum(weights)

# Felesleges másolatok elkerülése
# Kerülendő:
subset = data.copy()
subset['new_feature'] = calculation

# Javasolt:
data['new_feature'] = calculation  # Helyben módosítás
```
### 1.4 Típuskonverziók minimalizálása
```python
# Adattípusok beállítása előre
df = pd.DataFrame({
    'open': np.zeros(1000, dtype=np.float32),
    'high': np.zeros(1000, dtype=np.float32),
    'low': np.zeros(1000, dtype=np.float32),
    'close': np.zeros(1000, dtype=np.float32),
    'volume': np.zeros(1000, dtype=np.int32)
})

# Downcasting memória optimalizáláshoz
df['feature'] = df['calculation'].astype('float32')
```
## 2. Memória Optimalizáció

### 2.1 Memória-hatékony adatszerkezetek
```python
# DataFrame helyett NumPy array használata, ha lehetséges
prices = data[['open', 'high', 'low', 'close']].values

# Ritkás mátrixok használata nagy, ritka adathalmazoknál
from scipy.sparse import csr_matrix
sparse_matrix = csr_matrix(dense_matrix)
```
### 2.2 Hatalmas adathalmazok kezelése
```python
# Chunk-okban történő feldolgozás
def process_large_file(filename, chunk_size=100000):
    results = []
    for chunk in pd.read_csv(filename, chunksize=chunk_size):
        result = process_chunk(chunk)
        results.append(result)
    return pd.concat(results)

# Adatok szűrése betöltés előtt
query = "date >= '2023-01-01' and date <= '2023-01-31'"
filtered_data = pd.read_sql_query(f"SELECT * FROM data WHERE {query}", conn)
```
### 2.3 Memóriaszivárgások megelőzése
```python
# Nagy objektumok felszabadítása, ha már nincs rájuk szükség
import gc

def process_and_clean():
    large_df = load_large_dataset()
    result = process(large_df)

    # Explicit felszabadítás
    del large_df
    gc.collect()

    return result
```
## 3. Párhuzamos Feldolgozás

### 3.1 Többszálú feldolgozás
```python
from concurrent.futures import ThreadPoolExecutor

def process_symbols(symbols, timeframe):
    results = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_symbol, symbol, timeframe): symbol
                  for symbol in symbols}
        for future in as_completed(futures):
            symbol = futures[future]
            try:
                results[symbol] = future.result()
            except Exception as e:
                logger.error(f"Error processing {symbol}: {e}")
    return results
```
### 3.2 Többprocesszos feldolgozás
```python
from concurrent.futures import ProcessPoolExecutor

def train_models(configs):
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(train_model, configs))
    return results
```
### 3.3 Dask használata nagy adathalmazoknál
```python
import dask.dataframe as dd

# Dask DataFrame létrehozása
ddf = dd.read_csv('large_file.csv')

# Párhuzamos feldolgozás
result = ddf.map_partitions(process_partition).compute()
```
## 4. GPU Optimalizáció
### 4.1 CUDA használata számításigényes műveletekhez
```python
# PyTorch CUDA műveletek
if torch.cuda.is_available():
    tensor = tensor.to('cuda')
    result = model(tensor)  # GPU-n futó számítás
    result = result.to('cpu')  # Visszakonvertálás CPU-ra
```
### 4.2 Batch méret optimalizálása
```python
# Megfelelő batch méret keresése
# Túl kicsi: rossz GPU kihasználtság
# Túl nagy: memória problémák
optimal_batch_size = find_optimal_batch_size(
    model,
    start_size=32,
    max_size=1024,
    step=32
)
```
### 4.3 Mixed precision training
```python
# Float16 és Float32 kombinálása a sebességért
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for batch in dataloader:
    optimizer.zero_grad()

    # Automatikus vegyes pontosság
    with autocast():
        output = model(batch)
        loss = loss_fn(output, target)

    # Gradiens skálázás
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```
## 5. I/O Optimalizáció

### 5.1 Aszinkron I/O műveletek
```python
import asyncio
import aiofiles

async def async_read_files(filenames):
    results = []
    for filename in filenames:
        async with aiofiles.open(filename, 'r') as f:
            content = await f.read()
            results.append(process_content(content))
    return results
```
### 5.2 I/O műveletek bufferelése
```python
# Nagy fájlok hatékony írása
with open(large_file_path, 'w', buffering=1024*1024) as f:
    for chunk in large_chunks:
        f.write(chunk)
```
### 5.3 Adatbázis optimalizáció
```python
# Kötegelt beszúrások
with conn.cursor() as cursor:
    cursor.executemany(
        "INSERT INTO data (time, price, volume) VALUES (%s, %s, %s)",
        batch_of_records
    )
    conn.commit()
```
## 6. Profilozás és teljesítménymérés

### 6.1 Kód profilozása
```python
import cProfile
import pstats

def profile_function(func, *args, **kwargs):
    profiler = cProfile.Profile()
    profiler.enable()

    result = func(*args, **kwargs)

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 időigényes függvény

    return result
```
### 6.2 Időmérés
```python
import time

def measure_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - start_time

    print(f"{func.__name__} végrehajtási ideje: {elapsed:.4f} másodperc")
    return result
```
### 6.3 Memóriahasználat mérése
```python
import psutil
import os

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB-ban

def measure_memory(func, *args, **kwargs):
    mem_before = get_memory_usage()
    result = func(*args, **kwargs)
    mem_after = get_memory_usage()

    print(f"{func.__name__} memóriahasználata: {mem_after - mem_before:.2f} MB")
    return result
```
## 7. Teljesítmény benchmarkok

### 7.1 Benchmarkok készítése és futtatása
```python
import pytest
import numpy as np

@pytest.mark.benchmark
def test_feature_extraction_performance(benchmark):
    # Teszt adat előkészítése
    data = generate_test_data(size=10000)

    # Teljesítmény mérése
    result = benchmark(extract_features, data)

    # Eredmény validálása
    assert result.shape[0] == data.shape[0]
    assert "feature1" in result.columns
```
### 7.2 Alternatív megvalósítások összehasonlítása
```python
def test_compare_implementations(benchmark):
    data = generate_test_data(size=10000)

    # Első implementáció
    result1 = benchmark.pedantic(
        implementation1,
        args=(data,),
        iterations=5,
        rounds=100
    )

    # Második implementáció
    result2 = benchmark.pedantic(
        implementation2,
        args=(data,),
        iterations=5,
        rounds=100
    )

    # Eredmények összehasonlítása
    assert np.allclose(result1, result2)
    print(f"Sebesség különbség: {benchmark.stats1.mean / benchmark.stats2.mean:.2f}x")
```
## 8. Best Practices
### 8.1 Fejlesztési tanácsok
- Kerüld a ciklusokat: használj vektorizált műveleteket NumPy/pandas/torch eszközökkel
- Használj megfelelő adattípusokat: float32 elegendő legtöbbször float64 helyett
- Kerüld a szükségtelen másolásokat: használj view-kat és referenciákat
- Dolgozz batch-eken: ne egy-egy példányt dolgozz fel, hanem nagyobb egységeket
### 8.2 Teljesítmény optimalizálási folyamat
1. Mérd meg az aktuális teljesítményt (benchmark)
2. Azonosítsd a szűk keresztmetszeteket (profiling)
3. Optimalizáld a kritikus részeket
4. Mérd meg újra a teljesítményt
5. Ismételd, amíg szükséges
### 8.3 Rendszeres teljesítménytesztek
- Építs be automatikus teljesítményteszteket a CI/CD folyamatba
- Monitorozd a rendszer teljesítményét hosszú távon
- Állíts fel teljesítmény célokat és figyeld a regressziókat
