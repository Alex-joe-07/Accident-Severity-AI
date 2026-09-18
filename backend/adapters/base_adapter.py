from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseModelAdapter(ABC):
    """
    Abstract Base Class for ML Model Adapters.
    Every model version (V4, V5, V6...) must implement this interface.
    This guarantees that the API and frontend remain stable regardless of model changes.
    """

    @abstractmethod
    def load_model(self) -> None:
        """Loads model artifacts from disk into memory."""
        pass

    @abstractmethod
    def predict(self, raw_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes a raw feature dictionary from the API request, performs model prediction
        and explanation, and returns a standardized response payload.
        
        Expected Return Structure:
        {
            "success": True,
            "prediction": {
                "class": "Minor",           # Capitalized label: Minor / Major / Fatal
                "class_id": 2,             # Numeric class index
                "probability": 0.64,       # Prediction confidence (0.0 to 1.0)
                "probabilities": {          # Class probability breakdown
                    "Minor": 0.64,
                    "Major": 0.21,
                    "Fatal": 0.15
                }
            },
            "explanation": [                # List of influential factors (SHAP / Feature Importance)
                {
                    "feature": "Vehicles Involved",
                    "value": "5",
                    "importance": 0.15,
                    "impact": "Increased risk"  # Optional directional descriptor
                }
            ],
            "model": {
                "version": "V4",
                "algorithm": "Optimized XGBoost",
                "accuracy": "68.90%"
            }
        }
        """
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Returns metadata about the currently loaded model."""
        pass
