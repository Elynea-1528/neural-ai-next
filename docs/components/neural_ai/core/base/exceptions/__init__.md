# Base Kivételek Modul

## Áttekintés

Kivételek modul a Neural AI Next projektben.

Ez a modul exportálja az összes alap és specifikus kivétel osztályt, amelyeket a rendszer különböző komponensei használnak.

## Exportált Kivétel Osztályok

- [`NeuralAIException`](base_error.md#neuralaiexception): Alap kivétel az összes Neural AI Next kivételhez
- [`StorageException`](base_error.md#storageexception): Alap kivétel a tárolással kapcsolatos hibákhoz
- [`StorageWriteError`](base_error.md#storagewriteerror): Fájlírási művelet sikertelenségére
- [`StorageReadError`](base_error.md#storagereaderror): Fájlolvasási művelet sikertelenségére
- [`StoragePermissionError`](base_error.md#storagepermissionerror): Jogosultsági problémákra
- [`ConfigurationError`](base_error.md#configurationerror): Érvénytelen vagy hiányos konfigurációra
- [`DependencyError`](base_error.md#dependencyerror): Hiányzó függőségekre
- [`SingletonViolationError`](base_error.md#singletonviolationerror): Singleton minta megsértésére
- [`ComponentNotFoundError`](base_error.md#componentnotfounderror): Komponens nem találhatóra
- [`NetworkException`](base_error.md#networkexception): Alap kivétel hálózati hibákhoz
- [`TimeoutError`](base_error.md#timeouterror): Időtúllépésre
- [`ConnectionError`](base_error.md#connectionerror): Kapcsolódási hibákra
- [`InsufficientDiskSpaceError`](base_error.md#insufficientdiskspaceerror): Elégtelen lemezterületre
- [`PermissionDeniedError`](base_error.md#permissiondeniederror): Jogosultság megtagadására

## Kapcsolódó Dokumentáció

- [Base Error](base_error.md): Az összes kivétel osztály részletes leírása