from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):
    SOILGRIDS_API_URL: HttpUrl = (
        "https://rest.isric.org/soilgrids/v2.0/properties/query"
    )
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
