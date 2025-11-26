from typing import List
import logging
import numpy as np
from app.services.strategies.base import RecommendationStrategy
from app.models.recommendation import RecommendationItem
from app.services.model_loader import model_loader

logger = logging.getLogger(__name__)


class DummyRecommendationStrategy(RecommendationStrategy):
    def recommend(
        self, user_id: str, actions: List[str]
    ) -> List[RecommendationItem]:
        """
        Load and call the LSTM model with user data, but return dummy recommendations.
        This allows testing model loading without affecting API responses.
        """
        try:
            # Prepare dummy input data for the model (sequence of action IDs)
            # In a real scenario, you would encode the actions properly
            # Model expects vocab size of 100 (0-99)
            max_sequence_length = 10
            dummy_input = np.random.randint(0, 100, size=(1, max_sequence_length))

            # Call the model to ensure it's loaded and working
            logger.info(
                f"Calling LSTM model for user {user_id} with {len(actions)} actions"
            )
            predictions = model_loader.predict(dummy_input)
            logger.info(f"Model prediction shape: {predictions.shape}")

            # Log that we're using the model but returning dummy data
            logger.info(
                "Model called successfully, but returning dummy recommendations"
            )

        except Exception as e:
            logger.error(f"Error calling model: {e}")
            # Continue with dummy data even if model fails

        # Return dummy recommendations (unchanged)
        return [
            RecommendationItem(action="compose_gmail", score=0.92),
            RecommendationItem(action="create_event", score=0.82),
            RecommendationItem(action="attach_drive_file", score=0.61),
        ]
