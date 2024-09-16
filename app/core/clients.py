import logging
from requests import Session
from app.core.config import settings

logger = logging.getLogger(__name__)


class SoilClient:
    def __init__(self):
        self.url = settings.SOILGRIDS_API_URL
        self.session = Session()

    def request(self, method: str, params: dict, data: dict = None):
        """
        Make a request to the SoilGrids API.

        :param method: HTTP method (e.g., 'get', 'post')
        :param params: Query parameters
        :param data: Request body data (optional)
        :return: Response object
        """
        try:
            with self.session:
                response = self.session.request(
                    method, self.url, params=params, data=data
                )
                response.raise_for_status()
                logger.debug(f"Successfully retrieved soil data: {str(response.text)}")
                return response
        except Exception as e:
            logger.error(f"Error making request to SoilGrids API: {str(e)}")
            raise
