from abc import ABC, abstractmethod
from typing import List
from app.models.recommendation import RecommendationItem


class RecommendationStrategy(ABC):
    @abstractmethod
    def recommend(self, user_id: str, actions: List[str]) -> List[RecommendationItem]:
        pass
