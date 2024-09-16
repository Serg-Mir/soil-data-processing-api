from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")


class SoilDataSchema(BaseModel):
    clay_content: float
    organic_carbon: float
    pH: float
    sand_content: float
    silt_content: float


class SoilSuitabilityResponse(BaseModel):
    suitable: bool
    criteria: dict
