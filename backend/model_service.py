import importlib
from typing import Dict, Any

from backend.adapters.base_adapter import BaseModelAdapter
from backend.adapters.v4_adapter import V4ModelAdapter
import backend.config as config

class ModelService:
    """
    Model Service Manager / Plug-and-Play Factory.
    Loads and manages the active model adapter dynamically based on ACTIVE_MODEL_VERSION.
    """

    def __init__(self):
        self.active_adapter: BaseModelAdapter = None
        self.load_active_model()

    def load_active_model(self) -> None:
        version = config.ACTIVE_MODEL_VERSION.upper()
        print(f"Initializing Model Service with Model Version: {version}")

        if version == "V4":
            self.active_adapter = V4ModelAdapter()
        else:
            # Dynamic loading mechanism for future models (V5, V6, etc.)
            try:
                module_name = f"backend.adapters.{version.lower()}_adapter"
                class_name = f"{version}ModelAdapter"
                module = importlib.import_module(module_name)
                adapter_cls = getattr(module, class_name)
                self.active_adapter = adapter_cls()
                print(f"Successfully loaded dynamic model adapter: {class_name}")
            except Exception as e:
                print(f"Could not load dynamic adapter for {version}: {e}. Falling back to V4.")
                self.active_adapter = V4ModelAdapter()

    def predict(self, raw_features: Dict[str, Any]) -> Dict[str, Any]:
        """Delegates prediction to the active model adapter."""
        if not self.active_adapter:
            self.load_active_model()
        return self.active_adapter.predict(raw_features)

    def get_metadata(self) -> Dict[str, Any]:
        """Returns metadata from the active model adapter."""
        if not self.active_adapter:
            self.load_active_model()
        return self.active_adapter.get_metadata()

# Singleton instance for Flask application
model_service = ModelService()
