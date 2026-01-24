"""Teszt a pyproject.toml UI opcionális függőségeinek ellenőrzéséhez.

Ez a teszt ellenőrzi, hogy az ui opcionális függőségi csoport tartalmazza-e
az összes szükséges csomagot a megfelelő verziókkal.
"""

from pathlib import Path

import toml


def test_ui_optional_dependencies_exist() -> None:
    """Ellenőrzi, hogy az 'ui' opcionális függőségi csoport létezik.

    Raises:
        AssertionError: Ha az 'ui' csoport nem létezik vagy üres.
    """
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    with open(pyproject_path, encoding="utf-8") as f:
        config = toml.load(f)

    optional_deps = config.get("project", {}).get("optional-dependencies", {})

    assert "ui" in optional_deps, "Az 'ui' opcionális függőségi csoport nem létezik"
    assert len(optional_deps["ui"]) > 0, "Az 'ui' csoport üres"


def test_ui_dependencies_contain_required_packages() -> None:
    """Ellenőrzi, hogy az 'ui' csoport tartalmazza-e az összes szükséges csomagot.

    Raises:
        AssertionError: Ha bármelyik kötelező csomag hiányzik.
    """
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    with open(pyproject_path, encoding="utf-8") as f:
        config = toml.load(f)

    ui_deps = config["project"]["optional-dependencies"]["ui"]

    required_packages = [
        "streamlit>=",
        "plotly>=",
        "streamlit-aggrid",
        "watchdog",
        "tensorboard",
        "torchinfo",
    ]

    for package in required_packages:
        assert any(package in dep for dep in ui_deps), (
            f"A '{package}' csomag hiányzik az 'ui' függőségekből"
        )


def test_ui_dependencies_have_correct_versions() -> None:
    """Ellenőrzi a kritikus csomagok verziókövetelményeit.

    Raises:
        AssertionError: Ha a verziókövetelmények nem megfelelőek.
    """
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    with open(pyproject_path, encoding="utf-8") as f:
        config = toml.load(f)

    ui_deps = config["project"]["optional-dependencies"]["ui"]

    # Streamlit verzió ellenőrzése
    streamlit_dep = next((dep for dep in ui_deps if "streamlit" in dep), None)
    assert streamlit_dep is not None, "Streamlit dependency not found"
    assert ">=1.30.0" in streamlit_dep, f"Helytelen Streamlit verzió: {streamlit_dep}"

    # Plotly verzió ellenőrzése
    plotly_dep = next((dep for dep in ui_deps if "plotly" in dep), None)
    assert plotly_dep is not None, "Plotly dependency not found"
    assert ">=5.18.0" in plotly_dep, f"Helytelen Plotly verzió: {plotly_dep}"


def test_full_includes_ui() -> None:
    """Ellenőrzi, hogy a 'full' csoport tartalmazza-e az 'ui' csoportot.

    Raises:
        AssertionError: Ha a 'full' csoport nem tartalmazza az 'ui'-t.
    """
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    with open(pyproject_path, encoding="utf-8") as f:
        config = toml.load(f)

    full_deps = config["project"]["optional-dependencies"]["full"]

    assert any("ui" in dep for dep in full_deps), (
        "A 'full' opcionális függőségi csoport nem tartalmazza az 'ui'-t"
    )


def test_ui_dependencies_no_duplicates() -> None:
    """Ellenőrzi, hogy nincsenek-e duplikátumok az 'ui' csoportban.

    Raises:
        AssertionError: Ha duplikátumokat talál.
    """
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    with open(pyproject_path, encoding="utf-8") as f:
        config = toml.load(f)

    ui_deps = config["project"]["optional-dependencies"]["ui"]

    # Csomagnevek kinyerése (verzió spec nélkül)
    package_names: list[str] = []
    for dep in ui_deps:
        # Távolítsuk el a verzió specifikációt
        name = dep.split(">=")[0].split("==")[0].split("!=")[0].strip()
        package_names.append(name)

    assert len(package_names) == len(set(package_names)), (
        f"Duplikátumok találhatók az 'ui' függőségekben: {package_names}"
    )


def test_pyproject_toml_is_valid() -> None:
    """Ellenőrzi, hogy a pyproject.toml érvényes TOML formátumú.

    Raises:
        toml.TomlDecodeError: Ha a fájl nem érvényes TOML.
    """
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"

    # Ha a toml.load nem dob kivételt, a fájl érvényes
    with open(pyproject_path, encoding="utf-8") as f:
        toml.load(f)


if __name__ == "__main__":
    # Standalone futtatáshoz
    import pytest

    pytest.main([__file__, "-v"])
