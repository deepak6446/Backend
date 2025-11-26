from fastapi import APIRouter, Header, HTTPException, Depends
from typing import Annotated
from app.models.recommendation import RecommendationRequest, RecommendationResponse
from app.services.recommender import recommender_service
from app.core.config import settings

router = APIRouter()


async def verify_api_version(x_api_version: Annotated[str, Header()] = "v1"):
    if x_api_version != "v1":
        raise HTTPException(status_code=400, detail="Invalid API version")


@router.post(
    "/recommendations",
    response_model=RecommendationResponse,
    dependencies=[Depends(verify_api_version)],
)
async def get_recommendations(request: RecommendationRequest):
    recommendations = recommender_service.get_recommendations(
        request.user_id, request.actions
    )
    return RecommendationResponse(
        recommendations=recommendations, modelVersion=settings.MODEL_TYPE
    )
