# core/db/implementations/model_base.py

Adatbázis modellek alaposztályai.

Ez a modul definiálja az összes adatbázis modell által használt alaposztályokat
és segédosztályokat a Neural AI Next rendszerben.

## Osztályok

### `Base`

SQLAlchemy deklaratív alaposztály a modellekhez.

    Ez az osztály biztosítja a standardizált mezőket és metódusokat
    az összes adatbázis modell számára.

    Attributes:
        id: Elsődleges kulcs minden modellhez.
        created_at: A rekord létrehozásának időpontja.
        updated_at: A rekord utolsó módosításának időpontja.


## Függvények

### `__tablename__`

Automatikus táblanév generálás a class névből.

        A class nevet snake_case formátumba konvertálja és hozzáadja egy 's' végződést.
        Például: DynamicConfig -> dynamic_configs

        Returns:
            A generált táblanév string formátumban.

### `to_dict`

Modell átalakítása dictionary formátumba.

        Az összes oszlop értékét dictionary formátumba konvertálja,
        datetime objektumokat ISO formátumú stringgé alakítja.

        Returns:
            A modell adatait tartalmazó dictionary.

### `__repr__`

Modell string reprezentációja.

        Returns:
            A modell rövid string reprezentációja.


---

**Forrásfájl:** [`core/db/implementations/model_base.py`](../../../neural_ai/core/db/implementations/model_base.py)
