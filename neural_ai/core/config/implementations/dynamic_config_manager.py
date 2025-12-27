"""Dinamikus konfiguráció kezelő implementáció.

Ez a modul implementálja a DynamicConfigManager osztályt, amely a futás közben
módosítható konfigurációkat kezeli SQL adatbázisban tárolva, hot reload támogatással.
"""

import asyncio
from collections.abc import Awaitable, Callable
from contextlib import suppress
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from neural_ai.core.config.exceptions import ConfigError
from neural_ai.core.config.interfaces.async_config_interface import (
    AsyncConfigManagerInterface,
)
from neural_ai.core.db.implementations.models import DynamicConfig

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces import LoggerInterface

# Type alias a konfiguráció változásokat figyelő callback-ekhez
ConfigListener = Callable[[str, Any], Awaitable[None]]


class DynamicConfigManager(AsyncConfigManagerInterface):
    """Dinamikus konfiguráció kezelő SQL adatbázissal.

    Ez az osztály kezeli a futás közben módosítható konfigurációkat, amelyek
    hot reload támogatással rendelkeznek. A konfigurációk SQL adatbázisban
    tárolódnak, és változásukról a rendszer azonnal értesítést kap.

    Attributes:
        session: Az adatbázis session (Dependency Injection).
        logger: Logger interfész a naplózásra (opcionális).
        _cache: Konfigurációs értékek gyorsítótára.
        _listeners: Konfiguráció változásokat figyelő callback-ek listája.
        _last_update: Az utolsó frissítés időpontja.
        _hot_reload_task: A háttérben futó hot reload task referenciája.
        _stop_hot_reload: Esemény a hot reload leállításához.
    """

    def __init__(
        self,
        filename: str | None = None,
        session: AsyncSession | None = None,
        logger: "LoggerInterface | None" = None,
    ) -> None:
        """Inicializálja a DynamicConfigManager-t.

        Args:
            filename: Nincs használatban, csak a kompatibilitás miatt (deprecated).
            session: Az adatbázis session (kötelező a működéshez).
            logger: Logger interfész a naplózásra (opcionális).

        Raises:
            ValueError: Ha nincs megadva session.
        """
        if session is None:
            raise ValueError("Az adatbázis session megadása kötelező a DynamicConfigManager-hez")

        self.session: AsyncSession = session
        self._logger: LoggerInterface | None = logger
        self._cache: dict[str, Any] = {}
        self._listeners: list[ConfigListener] = []
        self._last_update: datetime | None = None
        self._hot_reload_task: asyncio.Task[None] | None = None
        self._stop_hot_reload = asyncio.Event()

    async def get(self, *keys: str, default: Any = None) -> Any:
        """Konfigurációs érték lekérdezése.

        Args:
            *keys: A konfigurációs kulcs(ok) hierarchiája. Csak egy kulcs támogatott.
            default: Alapértelmezett érték, ha a kulcs nem található.

        Returns:
            A konfigurációs érték vagy az alapértelmezett érték.

        Raises:
            ValueError: Ha több kulcsot adnak meg.
        """
        if len(keys) != 1:
            raise ValueError("A DynamicConfigManager csak egyetlen kulcsot támogat")

        key = keys[0]

        # Először cache-ből próbálkozunk
        if key in self._cache:
            return self._cache[key]

        # Adatbázisból olvasás
        try:
            stmt = (
                select(DynamicConfig)
                .where(DynamicConfig.key == key)
                .where(DynamicConfig.is_active == True)  # noqa: E712
            )
            result = await self.session.execute(stmt)
            config = result.scalar_one_or_none()

            if config is None:
                return default

            # Cache-be mentés
            self._cache[key] = config.value
            return config.value

        except Exception as e:
            if self._logger:
                self._logger.error(f"Hiba a konfiguráció lekérdezésekor ({key}): {e}")
            raise ConfigError(f"Konfiguráció lekérdezése sikertelen: {key}") from e

    async def set(self, *keys: str, value: Any) -> None:
        """Konfigurációs érték beállítása.

        Args:
            *keys: A konfigurációs kulcs(ok) hierarchiája. Csak egy kulcs támogatott.
            value: A beállítandó érték.

        Raises:
            ValueError: Ha több kulcsot adnak meg vagy érvénytelen az érték.
        """
        if len(keys) != 1:
            raise ValueError("A DynamicConfigManager csak egyetlen kulcsot támogat")

        key = keys[0]

        # Érték típusának meghatározása
        value_type = self._determine_value_type(value)

        try:
            # Létezik-e már a konfig?
            stmt = select(DynamicConfig).where(DynamicConfig.key == key)
            result = await self.session.execute(stmt)
            config = result.scalar_one_or_none()

            if config is None:
                # Új konfig létrehozása
                config = DynamicConfig(
                    key=key,
                    value=value,
                    value_type=value_type,
                    category="system",  # Alapértelmezett kategória
                    description=f"Automatikusan létrehozva: {key}",
                )
                self.session.add(config)
            else:
                # Meglévő konfig frissítése
                _ = config.value  # Nyomkövetéshez, de nem használjuk
                config.value = value
                config.value_type = value_type
                config.updated_at = datetime.now(UTC)

            await self.session.commit()

            # Cache frissítése
            self._cache[key] = value
            self._last_update = datetime.now(UTC)

            # Esemény küldése a listener-eknek
            await self._notify_listeners(key, value)

            if self._logger:
                self._logger.info(f"Konfiguráció frissítve: {key} = {value}")

        except Exception as e:
            await self.session.rollback()
            if self._logger:
                self._logger.error(f"Hiba a konfiguráció beállításakor ({key}): {e}")
            raise ConfigError(f"Konfiguráció beállítása sikertelen: {key}") from e

    async def get_section(self, section: str) -> dict[str, Any]:
        """Teljes konfigurációs szekció lekérése kategória alapján.

        Args:
            section: A konfigurációs kategória neve.

        Returns:
            A kategóriához tartozó összes konfigurációs érték.

        Raises:
            KeyError: Ha a kategória nem található vagy nincs aktív konfiguráció.
        """
        try:
            stmt = (
                select(DynamicConfig)
                .where(DynamicConfig.category == section)
                .where(DynamicConfig.is_active == True)  # noqa: E712
            )
            result = await self.session.execute(stmt)
            configs = result.scalars().all()

            if not configs:
                raise KeyError(f"Konfigurációs kategória nem található: {section}")

            return {config.key: config.value for config in configs}

        except KeyError:
            raise
        except Exception as e:
            if self._logger:
                self._logger.error(f"Hiba a konfigurációs szekció lekérdezésekor ({section}): {e}")
            raise ConfigError(f"Konfigurációs szekció lekérdezése sikertelen: {section}") from e

    async def save(self, filename: str | None = None) -> None:
        """Konfiguráció mentése (nincs értelmezve dinamikus konfigurációnál).

        A DynamicConfigManager nem támogatja a fájlba mentést, mivel az adatbázisban tárol.
        Ez a metódus csak a kompatibilitás miatt van jelen.

        Args:
            filename: Nincs használatban.

        Raises:
            NotImplementedError: Mindig, mivel nem támogatott művelet.
        """
        raise NotImplementedError(
            "A DynamicConfigManager nem támogatja a fájlba mentést. "
            "Használd a set() metódust az adatbázis frissítéséhez."
        )

    async def load(self, filename: str) -> None:
        """Konfiguráció betöltése (nincs értelmezve dinamikus konfigurációnál).

        A DynamicConfigManager nem támogatja a fájlból betöltést, mivel az adatbázisból olvas.
        Ez a metódus csak a kompatibilitás miatt van jelen.

        Args:
            filename: Nincs használatban.

        Raises:
            NotImplementedError: Mindig, mivel nem támogatott művelet.
        """
        raise NotImplementedError(
            "A DynamicConfigManager nem támogatja a fájlból betöltést. "
            "Használd a get() metódust az adatbázisból való olvasáshoz."
        )

    async def load_directory(self, path: str) -> None:
        """Konfigurációs mappa betöltése (nincs értelmezve dinamikus konfigurációnál).

        A DynamicConfigManager nem támogatja a mappából betöltést.
        Ez a metódus csak a kompatibilitás miatt van jelen.

        Args:
            path: Nincs használatban.

        Raises:
            NotImplementedError: Mindig, mivel nem támogatott művelet.
        """
        raise NotImplementedError(
            "A DynamicConfigManager nem támogatja a mappából betöltést. "
            "A konfigurációk az adatbázisban tárolódnak."
        )

    async def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]:
        """Konfiguráció validálása séma alapján.

        Args:
            schema: A validáláshoz használt séma.

        Returns:
            Tuple[bool, dict[str, str] | None]: (sikeres-e a validáció, hibák dictionary vagy None)

        Note:
            A validáció jelenleg csak a cache-ben lévő értékeket ellenőrzi.
        """
        errors: dict[str, str] = {}

        for key, expected_type in schema.items():
            value = self._cache.get(key)

            if value is None:
                errors[key] = "Kötelező mező hiányzik"
                continue

            if not isinstance(value, expected_type):
                errors[key] = f"Érvénytelen típus, várt: {expected_type.__name__}"

        return not bool(errors), errors if errors else None

    def add_listener(self, callback: ConfigListener) -> None:
        """Listener hozzáadása konfiguráció változásokhoz.

        Args:
            callback: A callback függvény, amelyet hívni kell a változás esetén.
                     A callbacknek két paramétert kell fogadnia: (key, value).
        """
        self._listeners.append(callback)

        if self._logger:
            self._logger.debug(f"Új konfiguráció listener hozzáadva: {callback.__name__}")

    def remove_listener(self, callback: ConfigListener) -> None:
        """Listener eltávolítása.

        Args:
            callback: Az eltávolítandó callback függvény.
        """
        with suppress(ValueError):
            self._listeners.remove(callback)

        if self._logger:
            self._logger.debug(f"Konfiguráció listener eltávolítva: {callback.__name__}")

    async def start_hot_reload(self, interval: float = 5.0) -> None:
        """Hot reload indítása (háttérben fut).

        A hot reload rendszeres időközönként ellenőrzi az adatbázist
        konfigurációs változásokért, és frissíti a cache-t.

        Args:
            interval: Az ellenőrzési időköz másodpercben (alapértelmezett: 5.0).

        Raises:
            RuntimeError: Ha a hot reload már fut.
        """
        if self._hot_reload_task is not None and not self._hot_reload_task.done():
            raise RuntimeError("A hot reload már fut")

        self._stop_hot_reload.clear()

        async def _hot_reload_loop() -> None:
            """A hot reload fő ciklusa."""
            if self._logger:
                self._logger.info(f"Konfiguráció hot reload elindítva ({interval}s intervallummal)")

            while not self._stop_hot_reload.is_set():
                try:
                    await self._check_for_updates()
                except Exception as e:
                    if self._logger:
                        self._logger.error(f"Hiba a hot reload során: {e}")

                try:
                    await asyncio.wait_for(self._stop_hot_reload.wait(), timeout=interval)
                except TimeoutError:
                    # Timeout lejárt, folytatjuk a következő iterációval
                    continue

            if self._logger:
                self._logger.info("Konfiguráció hot reload leállítva")

        self._hot_reload_task = asyncio.create_task(_hot_reload_loop())

    async def stop_hot_reload(self) -> None:
        """Hot reload leállítása."""
        if self._hot_reload_task is None or self._hot_reload_task.done():
            return

        self._stop_hot_reload.set()

        try:
            await asyncio.wait_for(self._hot_reload_task, timeout=10.0)
        except TimeoutError:
            if self._logger:
                self._logger.warning("Hot reload task nem állt le időben, megszakítva")
            self._hot_reload_task.cancel()

            with suppress(asyncio.CancelledError):
                await self._hot_reload_task

        self._hot_reload_task = None

    async def get_all(self, category: str | None = None) -> dict[str, Any]:
        """Összes konfiguráció lekérdezése.

        Args:
            category: Opcionális kategória szűréshez.

        Returns:
            Szótár az összes (vagy kategóriához tartozó) konfigurációval.
        """
        try:
            stmt = select(DynamicConfig).where(DynamicConfig.is_active == True)  # noqa: E712

            if category:
                stmt = stmt.where(DynamicConfig.category == category)

            result = await self.session.execute(stmt)
            configs = result.scalars().all()

            return {config.key: config.value for config in configs}

        except Exception as e:
            if self._logger:
                self._logger.error(f"Hiba az összes konfiguráció lekérdezésekor: {e}")
            raise ConfigError("Összes konfiguráció lekérdezése sikertelen") from e

    async def set_with_metadata(
        self,
        key: str,
        value: Any,
        category: str = "system",
        description: str | None = None,
        is_active: bool = True,
    ) -> None:
        """Konfiguráció beállítása metaadatokkal.

        Args:
            key: A konfigurációs kulcs.
            value: A konfigurációs érték.
            category: A konfiguráció kategóriája (alapértelmezett: "system").
            description: A konfiguráció leírása (opcionális).
            is_active: A konfiguráció aktív-e (alapértelmezett: True).
        """
        value_type = self._determine_value_type(value)

        try:
            # Létezik-e már a konfig?
            stmt = select(DynamicConfig).where(DynamicConfig.key == key)
            result = await self.session.execute(stmt)
            config = result.scalar_one_or_none()

            if config is None:
                # Új konfig létrehozása
                config = DynamicConfig(
                    key=key,
                    value=value,
                    value_type=value_type,
                    category=category,
                    description=description,
                    is_active=is_active,
                )
                self.session.add(config)
            else:
                # Meglévő konfig frissítése
                config.value = value
                config.value_type = value_type
                config.category = category
                config.description = description
                config.is_active = is_active
                config.updated_at = datetime.now(UTC)

            await self.session.commit()

            # Cache frissítése
            self._cache[key] = value
            self._last_update = datetime.now(UTC)

            # Esemény küldése a listener-eknek
            await self._notify_listeners(key, value)

            if self._logger:
                self._logger.info(
                    f"Konfiguráció frissítve (metaadatokkal): {key} = {value} "
                    f"(kategória: {category})"
                )

        except Exception as e:
            await self.session.rollback()
            if self._logger:
                self._logger.error(f"Hiba a konfiguráció beállításakor ({key}): {e}")
            raise ConfigError(f"Konfiguráció beállítása sikertelen: {key}") from e

    async def delete(self, key: str) -> bool:
        """Konfiguráció törlése (soft delete: is_active = False).

        Args:
            key: A törlendő konfigurációs kulcs.

        Returns:
            True ha a konfiguráció törölve lett, False ha nem található.

        Raises:
            ConfigError: Ha hiba történik a törlés során.
        """
        try:
            stmt = select(DynamicConfig).where(DynamicConfig.key == key)
            result = await self.session.execute(stmt)
            config = result.scalar_one_or_none()

            if config is None:
                return False

            # Soft delete: is_active = False
            config.is_active = False
            config.updated_at = datetime.now(UTC)

            await self.session.commit()

            # Cache-ből törlés
            self._cache.pop(key, None)
            self._last_update = datetime.now(UTC)

            if self._logger:
                self._logger.info(f"Konfiguráció törölve (deaktiválva): {key}")

            return True

        except Exception as e:
            await self.session.rollback()
            if self._logger:
                self._logger.error(f"Hiba a konfiguráció törlésekor ({key}): {e}")
            raise ConfigError(f"Konfiguráció törlése sikertelen: {key}") from e

    async def _notify_listeners(self, key: str, value: Any) -> None:
        """Listener-ek értesítése konfiguráció változásról.

        Args:
            key: A megváltozott konfigurációs kulcs.
            value: Az új konfigurációs érték.
        """
        for listener in self._listeners[:]:  # Másolat készítése a lista módosítása ellen
            try:
                await listener(key, value)
            except Exception as e:
                if self._logger:
                    self._logger.error(f"Konfiguráció listener hiba ({listener.__name__}): {e}")

    async def _check_for_updates(self) -> None:
        """Ellenőrzi, hogy történt-e változás az adatbázisban."""
        if self._last_update is None:
            # Első alkalommal betöltjük az összeset
            self._cache = await self.get_all()
            self._last_update = datetime.now(UTC)
            return

        try:
            # Utolsó frissítés időpontja után változott-e valami?
            stmt = select(DynamicConfig).where(DynamicConfig.updated_at > self._last_update)
            result = await self.session.execute(stmt)
            updated_configs = result.scalars().all()

            for config in updated_configs:
                old_value = self._cache.get(config.key)
                if old_value != config.value:
                    self._cache[config.key] = config.value
                    await self._notify_listeners(config.key, config.value)

            self._last_update = datetime.now(UTC)

        except Exception as e:
            if self._logger:
                self._logger.error(f"Hiba a változások ellenőrzésekor: {e}")

    @staticmethod
    def _determine_value_type(value: Any) -> str:
        """Érték típusának meghatározása.

        Args:
            value: Az ellenőrizendő érték.

        Returns:
            Az érték típusa string formátumban.
        """
        if isinstance(value, bool):
            return "bool"
        if isinstance(value, int):
            return "int"
        if isinstance(value, float):
            return "float"
        if isinstance(value, str):
            return "str"
        if isinstance(value, list):
            return "list"
        if isinstance(value, dict):
            return "dict"

        return "str"  # Alapértelmezett
