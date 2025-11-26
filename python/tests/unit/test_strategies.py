from app.services.strategies.dummy import DummyRecommendationStrategy


def test_dummy_strategy_returns_recommendations():
    strategy = DummyRecommendationStrategy()
    recommendations = strategy.recommend("user1", ["a", "b", "c"])

    assert len(recommendations) == 3
    assert recommendations[0].action == "compose_gmail"
    assert recommendations[0].score == 0.92
