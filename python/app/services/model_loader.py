"""
Model loader service for loading and managing the LSTM recommendation model.
"""
import logging
from typing import Optional
import numpy as np
from tensorflow import keras
from app.core.config import settings

logger = logging.getLogger(__name__)


class ModelLoader:
    """Singleton class to load and manage the LSTM model."""

    _instance: Optional["ModelLoader"] = None
    _model: Optional[keras.Model] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_model(self) -> keras.Model:
        """Load the LSTM model from the configured path."""
        if self._model is None:
            try:
                logger.info(f"Loading model from {settings.MODEL_PATH}")
                self._model = keras.models.load_model(settings.MODEL_PATH)
                logger.info(
                    f"Model loaded successfully. Version: {settings.MODEL_VERSION}"
                )
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                raise

        return self._model

    def predict(self, input_data: np.ndarray) -> np.ndarray:
        """
        Make predictions using the loaded model.

        Args:
            input_data: Input data for the model (preprocessed)

        Returns:
            Model predictions
        """
        model = self.load_model()
        predictions = model.predict(input_data, verbose=0)
        return predictions


# Global model loader instance
model_loader = ModelLoader()
