"""
AI Service interfész definíciója.

Ez az interfész definiálja a mesterséges intelligencia szolgáltatás szerződését,
amely a modellek kezelését és futtatását végzi.
"""

from typing import Protocol, runtime_checkable, Dict, Any, List, Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface


@runtime_checkable
class AIServiceInterface(Protocol):
    """
    AI Service interfész - Mesterséges intelligencia kezeléséért felelős.
    
    Ez az interfész definiálja a modellek betöltését, konfigurálását és
    futtatását végző metódusokat.
    """

    def get_available_models(self) -> List[Dict[str, str]]:
        """
        Elérhető AI modellek lekérdezése.
        
        Returns:
            List[Dict[str, str]]: A modellek listája
        """
        ...

    def load_model(self, model_id: str, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        AI modell betöltése.
        
        Args:
            model_id: A modell azonosítója
            config: A modell konfigurációja
            
        Returns:
            bool: True, ha sikeres a betöltés
        """
        ...

    def run_inference(
        self,
        model_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Inferencia futtatása a modellen.
        
        Args:
            model_id: A modell azonosítója
            input_data: A bemeneti adatok
            
        Returns:
            Dict[str, Any]: Az inferencia eredménye
        """
        ...

    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """
        Modell információk lekérdezése.
        
        Args:
            model_id: A modell azonosítója
            
        Returns:
            Dict[str, Any]: A modell metaadatai
        """
        ...

    def train_model(
        self,
        model_id: str,
        training_data: List[Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Modell betanítása.
        
        Args:
            model_id: A modell azonosítója
            training_data: A tanítóadatok
            config: A tanítás konfigurációja
            
        Returns:
            Dict[str, Any]: A tanítás eredménye
        """
        ...

    def get_training_status(self, training_id: str) -> Dict[str, Any]:
        """
        Tanítás állapotának lekérdezése.
        
        Args:
            training_id: A tanítás azonosítója
            
        Returns:
            Dict[str, Any]: A tanítás állapota
        """
        ...