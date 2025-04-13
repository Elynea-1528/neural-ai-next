# Telepítési útmutató - Neural-AI-Next

Ez a dokumentum részletes útmutatót biztosít a Neural-AI-Next fejlesztői és futtatási környezetének telepítéséhez.

Utolsó frissítés: 2025. március 30.

## Rendszerkövetelmények

- **Python**: 3.12
- **CUDA**: 12.1 (NVIDIA GPU használatához)
- **Operációs rendszer**: Linux (Ubuntu 22.04+ ajánlott), Windows 10/11
- **RAM**: Minimum 16GB javasolt
- **Tárhely**: Minimum 20GB szabad hely javasolt

## Conda környezet telepítése

### 1. Conda telepítése (ha még nincs)

Látogass el a [Miniconda weboldalára](https://docs.conda.io/en/latest/miniconda.html) és kövesd a telepítési útmutatót.

### 2. Környezet létrehozása és aktiválása

```bash
# Korábbi környezet eltávolítása (ha létezik)
conda remove -n neural-ai-next --all -y

# Új környezet létrehozása Python 3.12-vel
conda create -n neural-ai-next python=3.12 -y

# Környezet aktiválása
conda activate neural-ai-next
```

### 3. Függőségek telepítése

#### PyTorch és Lightning telepítése

```bash
# PyTorch telepítése CUDA 12.1 támogatással
pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu121

# Lightning telepítése
pip install lightning==2.4.0
```

#### Projekt telepítése fejlesztői módban

```bash
# Navigálj a projekt gyökérkönyvtárába
cd /path/to/neural-ai-next

# Telepítés fejlesztői módban
pip install -e .
```

## Használat VS Code-ban

A Visual Studio Code-hoz néhány beállítást javaslunk a jobb fejlesztői élmény érdekében:

1. Telepítsd a [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) és [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) bővítményeket
2. Nyisd meg a projekt mappáját VS Code-ban
3. Válaszd ki a Python interpretert (F1 -> "Python: Select Interpreter" -> válaszd a neural-ai-next környezetet)
4. A terminálban aktiváld a környezetet: `conda activate neural-ai-next`

## Tesztelés

A tesztek futtatásához:

```bash
# A pytest telepítése (ha még nincs)
pip install pytest pytest-cov

# Összes teszt futtatása
pytest

# Tesztek futtatása lefedettség méréssel
pytest --cov=neural_ai tests/
```

## Hibaelhárítás

### CUDA problémák

Ha problémád van a CUDA-val, ellenőrizd:

```bash
python -c "import torch; print('CUDA elérhető:', torch.cuda.is_available())"
```

Ha a CUDA nem érhető el:
1. Ellenőrizd, hogy az NVIDIA illesztőprogramok telepítve vannak-e
2. Ellenőrizd, hogy a CUDA 12.1 telepítve van-e
3. Ellenőrizd, hogy a megfelelő PyTorch verziót telepítetted-e

### Egyéb problémák

Ha további problémákba ütközöl, nyiss egy [issue-t](https://github.com/your-organization/neural-ai-next/issues) a GitHub oldalon.
