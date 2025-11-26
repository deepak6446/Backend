from typing import List
from app.models.recommendation import RecommendationItem
from app.services.strategies.base import RecommendationStrategy
from app.services.strategies.dummy import DummyRecommendationStrategy
from app.core.config import settings


class RecommenderService:
    def __init__(self):
        self.strategy: RecommendationStrategy = self._get_strategy()

    def _get_strategy(self) -> RecommendationStrategy:
        if settings.MODEL_TYPE == "dummy":
            return DummyRecommendationStrategy()
        # Add other strategies here
        return DummyRecommendationStrategy()

    def get_recommendations(
        self, user_id: str, actions: List[str]
    ) -> List[RecommendationItem]:
        return self.strategy.recommend(user_id, actions)


recommender_service = RecommenderService()
