# Test Install Module

## Áttekintés

A `tests/scripts/test_install.py` modul unit és integrációs teszteket tartalmaz a [`scripts/install.py`](../scripts/install.md) telepítő szkript funkcióinak ellenőrzéséhez.

## Cél

A tesztek célja, hogy ellenőrizzék a telepítő szkript főbb komponenseit:
- Hardver detektálás (GPU, AVX2, Conda, Wine)
- Környezet létrehozás és konfiguráció
- Bróker telepítők indítása
- Parancssori argumentumok feldolgozása
- Kimeneti üzenetek formázása

## Teszt Struktúra

### 1. `TestColors` osztály
A konzol színező osztály tesztjei.

**Metódusok:**
- `test_colors_defined()`: Ellenőrzi, hogy minden szín definiálva van-e

### 2. `TestHelperFunctions` osztály
A segédfüggvények tesztjei.

**Metódusok:**
- `test_print_banner()`: Banner kiírás tesztelése
- `test_print_success()`: Sikeres üzenet kiírása
- `test_print_error()`: Hibaüzenet kiírása
- `test_print_warning()`: Figyelmeztető üzenet kiírása
- `test_print_info()`: Információs üzenet kiírása
- `test_command_exists_true()`: Parancs létezésének ellenőrzése (pozitív)
- `test_command_exists_false()`: Parancs létezésének ellenőrzése (negatív)
- `test_run_command_success()`: Sikeres parancs futtatás
- `test_run_command_failure()`: Sikertelen parancs futtatás
- `test_run_command_no_check()`: Parancs futtatás check=False esetén

### 3. `TestHardwareDetection` osztály
Hardver detektáló függvények tesztjei.

**Metódusok:**
- `test_check_conda_true()`: Conda jelenlétének ellenőrzése
- `test_check_conda_false()`: Conda hiányának ellenőrzése
- `test_check_nvidia_gpu_true()`: NVIDIA GPU jelenlétének ellenőrzése
- `test_check_nvidia_gpu_false_no_nvidia_smi()`: NVIDIA GPU hiánya (nvidia-smi nélkül)
- `test_check_nvidia_gpu_false_empty_output()`: NVIDIA GPU hiánya (üres output)
- `test_check_avx2_support_true()`: AVX2 támogatás ellenőrzése
- `test_check_avx2_support_false()`: AVX2 hiányának ellenőrzése
- `test_check_avx2_support_exception()`: AVX2 ellenőrzés kivétel esetén
- `test_check_wine_true()`: Wine jelenlétének ellenőrzése
- `test_check_wine_false()`: Wine hiányának ellenőrzése
- `test_get_conda_path()`: Conda elérési útjának ellenőrzése

### 4. `TestEnvironmentSetup` osztály
Környezet beállító függvények tesztjei.

**Metódusok:**
- `test_remove_conda_env_exists()`: Létező környezet eltávolítása
- `test_remove_conda_env_not_exists()`: Nem létező környezet ellenőrzése
- `test_create_conda_env_with_packages_gpu()`: Környezet létrehozása GPU-val
- `test_create_conda_env_with_packages_cpu()`: Környezet létrehozása CPU-val
- `test_install_data_libraries_avx2()`: Adatkönyvtárak telepítése AVX2-vel
- `test_install_data_libraries_no_avx2()`: Adatkönyvtárak telepítése AVX2 nélkül
- `test_install_project_packages_default()`: Projekt csomagok alapértelmezett telepítése
- `test_install_project_packages_with_groups()`: Projekt csomagok csoportokkal

### 5. `TestBrokerInstallation` osztály
Bróker telepítő függvények tesztjei.

**Metódusok:**
- `test_create_downloads_dir()`: Downloads mappa létrehozása
- `test_download_file()`: Fájl letöltés tesztelése
- `test_install_jforex4()`: JForex4 telepítés ellenőrzése
- `test_install_tws()`: TWS telepítés ellenőrzése
- `test_install_mt5_dukascopy_with_wine()`: MT5 telepítés Wine-el
- `test_install_mt5_dukascopy_no_wine()`: MT5 telepítés Wine nélkül

### 6. `TestMainFunctions` osztály
Fő függvények tesztjei.

**Metódusok:**
- `test_run_hardware_detection_success()`: Sikeres hardver detektálás
- `test_run_hardware_detection_no_conda()`: Hardver detektálás Conda hiányában
- `test_install_core_environment()`: Core környezet telepítésének ellenőrzése
- `test_install_brokers()`: Brókerek telepítésének ellenőrzése

### 7. `TestArgumentParsing` osztály
Parancssori argumentumok feldolgozásának tesztjei.

**Metódusok:**
- `test_parse_arguments_default()`: Alapértelmezett argumentumok
- `test_parse_arguments_only()`: --only argumentum ellenőrzése
- `test_parse_arguments_no_brokers()`: --no-brokers argumentum ellenőrzése
- `test_parse_arguments_verbose()`: --verbose argumentum ellenőrzése

### 8. `TestCompletionMessage` osztály
Befejezési üzenet tesztjei.

**Metódusok:**
- `test_print_completion_message_gpu_avx2()`: Üzenet GPU-val és AVX2-vel
- `test_print_completion_message_cpu_no_avx2()`: Üzenet CPU-val és AVX2 nélkül

## Teszt Futtatása

### Egyedi teszt futtatása
```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/scripts/test_install.py -v
```

### Konkrét teszt osztály futtatása
```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/scripts/test_install.py::TestColors -v
```

### Konkrét teszt metódus futtatása
```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/scripts/test_install.py::TestColors::test_colors_defined -v
```

### Coverage jelentés generálása
```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/scripts/test_install.py --cov=scripts.install --cov-report=html
```

## Mockolás és Izoláció

A tesztek során széles körben alkalmazunk mockolást, hogy:
- Ne futtassunk valódi shell parancsokat
- Ne hozzunk létre valódi Conda környezeteket
- Ne töltsünk le valódi fájlokat
- Előre definiált válaszokat kapjunk a hardver detektáló függvényektől

### Példa mock használatra

```python
@patch("install.command_exists")
def test_check_conda_true(self, mock_exists: MagicMock) -> None:
    mock_exists.return_value = True
    assert installer.check_conda() is True
```

## Függőségek

- `pytest`: A teszt keretrendszer
- `pytest-cov`: Code coverage támogatás
- `unittest.mock`: Mock objektumok létrehozásához
- `scripts/install.py`: A tesztelt modul

## Hibakeresés

Ha a tesztek nem futnak le sikeresen:

1. **Import hiba**: Ellenőrizd, hogy a `scripts` mappa szerepel-e a Python path-ban
2. **Mock hiba**: Ellenőrizd a mockolt függvények neveit és viselkedését
3. **Permission hiba**: Győződj meg róla, hogy a tesztfájl futtatható jogosultsággal rendelkezik

## Kapcsolódó Dokumentáció

- [`scripts/install.py`](../scripts/install.md): A tesztelt telepítő szkript dokumentációja
- [Telepítési útmutató](../../INSTALLATION_GUIDE.md): A teljes telepítési folyamat leírása
- [Tesztelési útmutató](../../development/testing_guide.md): Általános tesztelési irányelvek