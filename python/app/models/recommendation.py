from pydantic import BaseModel, Field, ConfigDict
from typing import List
import uuid


class RecommendationRequest(BaseModel):
    user_id: str = Field(..., alias="userId")
    actions: List[str] = Field(..., min_length=3)


class RecommendationItem(BaseModel):
    action: str
    score: float = Field(..., ge=0.0, le=1.0)


class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationItem]
    model_version: str = Field(..., alias="modelVersion")
    request_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), alias="requestId"
    )

    model_config = ConfigDict(populate_by_name=True)
