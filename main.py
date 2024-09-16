from fastapi import FastAPI
from app.api import endpoints
from app.core.config import settings
import logging

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(title="Soil Data Processing API", version="1.0.0")

app.include_router(endpoints.router)
