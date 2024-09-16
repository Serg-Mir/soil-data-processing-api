from fastapi import APIRouter, HTTPException, Depends
from app.core.schemas import Coordinates, SoilSuitabilityResponse, SoilDataSchema
from app.services.soil_service import (
    fetch_soil_data,
    analyze_soil_suitability,
    SoilClient,
)
from app.core.exceptions import SoilDataFetchError
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


def get_soil_client():
    return SoilClient()


@router.get("/soil-info", response_model=SoilDataSchema)
async def get_soil_info(
    coords: Coordinates = Depends(), client: SoilClient = Depends(get_soil_client)
):
    try:
        soil_data = fetch_soil_data(coords.lat, coords.lon, client)
        return soil_data
    except SoilDataFetchError as e:
        logger.error(f"Error fetching soil data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_soil_info: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/soil-suitability", response_model=SoilSuitabilityResponse)
async def get_soil_suitability(
    coords: Coordinates = Depends(), client: SoilClient = Depends(get_soil_client)
):
    try:
        suitability = analyze_soil_suitability(coords.lat, coords.lon, client)
        return SoilSuitabilityResponse(**suitability)
    except SoilDataFetchError as e:
        logger.error(f"Error analyzing soil suitability: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_soil_suitability: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
