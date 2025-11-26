from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    PROJECT_NAME: str = "Recommendation Service"
    MODEL_TYPE: Literal["dummy", "rule", "ml"] = "dummy"
    VERSION: str = "0.1.0"
    MODEL_PATH: str = "/app/models/v1.1.0_recommendation_model.h5"
    MODEL_VERSION: str = "v1.1.0"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
