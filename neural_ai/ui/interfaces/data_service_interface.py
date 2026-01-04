"""
Data Service interfész definíciója.

Ez az interfész definiálja az adatkezelési szolgáltatás szerződését,
amely az adatok betöltését, szűrését és kezelését végzi.
"""

from typing import Protocol, runtime_checkable, Dict, Any, List, Optional, Generator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface


@runtime_checkable
class DataServiceInterface(Protocol):
    """
    Data Service interfész - Adatkezelésért felelős.
    
    Ez az interfész definiálja az adatok lekérdezését és kezelését
    végző metódusokat, Big Data támogatással.
    """

    def load_data(
        self,
        source: str,
        filters: Optional[Dict[str, Any]] = None,
        chunk_size: int = 10000
    ) -> Generator[List[Dict[str, Any]], None, None]:
        """
        Adatok aszinkron betöltése chunkokban.
        
        Args:
            source: Az adatforrás azonosítója
            filters: Szűrőfeltételek
            chunk_size: A chunkok mérete
            
        Yields:
            List[Dict[str, Any]]: Adat chunkok
        """
        ...

    def get_data_sources(self) -> List[Dict[str, str]]:
        """
        Elérhető adatforrások lekérdezése.
        
        Returns:
            List[Dict[str, str]]: Az adatforrások listája
        """
        ...

    def get_data_info(self, source: str) -> Dict[str, Any]:
        """
        Adatforrás információk lekérdezése.
        
        Args:
            source: Az adatforrás azonosítója
            
        Returns:
            Dict[str, Any]: Az adatforrás metaadatai
        """
        ...

    def apply_filters(
        self,
        data: List[Dict[str, Any]],
        filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Szűrők alkalmazása adatokra.
        
        Args:
            data: A szűrendő adatok
            filters: A alkalmazandó szűrők
            
        Returns:
            List[Dict[str, Any]]: A szűrt adatok
        """
        ...

    def export_data(
        self,
        data: List[Dict[str, Any]],
        format: str,
        destination: str
    ) -> bool:
        """
        Adatok exportálása különböző formátumokba.
        
        Args:
            data: Az exportálandó adatok
            format: A célformátum (parquet, csv, json)
            destination: A cél útvonal
            
        Returns:
            bool: True, ha sikeres az exportálás
        """
        ...