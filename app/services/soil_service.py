from app.core.schemas import SoilDataSchema
from app.core.clients import SoilClient
from app.core.exceptions import SoilDataFetchError, SoilDataProcessingError


class SoilData:
    def __init__(self, clay_content, organic_carbon, pH, sand_content, silt_content):
        self.clay_content = clay_content
        self.organic_carbon = organic_carbon
        self.pH = pH
        self.sand_content = sand_content
        self.silt_content = silt_content


def api_parameters(lat: float, lon: float) -> dict:
    return {
        "lon": lon,
        "lat": lat,
        "property": ["phh2o", "clay", "ocd", "sand", "silt", "soc"],
        "depth": ["0-5cm"],
        "value": ["Q0.05", "Q0.5", "Q0.95", "mean", "uncertainty"],
    }


def fetch_data(client: SoilClient, params: dict) -> dict:
    response = client.request(method="get", params=params)
    return response.json()


def extract_soil_properties(data: dict) -> dict:
    properties = {
        "clay_content": None,
        "organic_carbon": None,
        "pH": None,
        "sand_content": None,
        "silt_content": None,
    }

    for layer in data["properties"]["layers"]:
        if layer["depths"][0]["values"]["mean"]:
            name = layer["name"]
            mean_value = layer["depths"][0]["values"]["mean"]
            if name == "clay":
                properties["clay_content"] = mean_value / 10  # Convert to percentage
            elif name == "ocd":
                properties["organic_carbon"] = (
                    mean_value / 100
                )  # Convert to g/cm3 or percentage equivalent
            elif name == "phh2o":
                properties["pH"] = mean_value / 10  # Convert from pH*10
            elif name == "sand":
                properties["sand_content"] = mean_value / 10  # Convert to percentage
            elif name == "silt":
                properties["silt_content"] = mean_value / 10  # Convert to percentage

    return properties


def validate_soil_properties(properties: dict):
    if not all(properties.values()):
        raise SoilDataProcessingError(
            "Missing essential soil data from the API response."
        )


def fetch_soil_data(lat: float, lon: float, client: SoilClient) -> SoilDataSchema:
    """
    Fetch soil data for given coordinates.

    :param lat: Latitude
    :param lon: Longitude
    :param client: SoilClient instance
    :return: SoilDataSchema object
    :raises SoilDataFetchError: If there's an error fetching or processing soil data
    """
    try:
        params = api_parameters(lat, lon)
        data = fetch_data(client, params)
        properties = extract_soil_properties(data)
        validate_soil_properties(properties)
        return SoilDataSchema(**properties)
    except Exception as e:
        raise SoilDataFetchError(f"Error fetching soil data: {str(e)}")


def analyze_soil_suitability(lat: float, lon: float, client: SoilClient) -> dict:
    """
    Analyze soil suitability for given coordinates.

    :param lat: Latitude
    :param lon: Longitude
    :param client: SoilClient instance
    :return: Dictionary with suitability analysis
    """
    try:
        soil_data = fetch_soil_data(lat, lon, client)

        # Enhanced suitability criteria
        ph_suitable = 5.5 < soil_data.pH < 7.5
        organic_carbon_suitable = soil_data.organic_carbon > 1.5
        texture_suitable = 20 < soil_data.clay_content < 30 < soil_data.silt_content

        suitability_score = sum(
            [ph_suitable, organic_carbon_suitable, texture_suitable]
        )
        return {
            "suitable": suitability_score >= 2,  # At least 2 out of 3 criteria met
            "criteria": {
                "pH": {"value": soil_data.pH, "suitable": ph_suitable},
                "organic_carbon": {
                    "value": soil_data.organic_carbon,
                    "suitable": organic_carbon_suitable,
                },
                "texture": {
                    "clay": soil_data.clay_content,
                    "silt": soil_data.silt_content,
                    "sand": soil_data.sand_content,
                    "suitable": texture_suitable,
                },
            },
        }
    except SoilDataFetchError as e:
        raise
    except Exception as e:
        raise SoilDataProcessingError(f"Error analyzing soil suitability: {str(e)}")
