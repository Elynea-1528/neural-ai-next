# core/storage/services/resampler_service/factory.py

ResamplerService Factory - A ResamplerService létrehozásáért felelős.

## Osztályok

### `ResamplerServiceFactory`

Factory osztály a ResamplerService létrehozásához és kezeléséhez.


## Függvények

### `create`

ResamplerService példány létrehozása.

        Args:
            storage: A tárolási interfész példány

        Returns:
            ResamplerInterface: A létrehozott ResamplerService példány

### `get_instance`

ResamplerService példány lekérdezése a DI konténerből.

        Returns:
            ResamplerInterface: A ResamplerService példány

        Raises:
            ComponentNotFoundError: Ha a komponens nem található a konténerben


---

**Forrásfájl:** [`core/storage/services/resampler_service/factory.py`](../../../neural_ai/core/storage/services/resampler_service/factory.py)
