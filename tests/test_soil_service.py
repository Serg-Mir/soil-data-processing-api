import pytest
from unittest.mock import Mock, patch
from app.services.soil_service import fetch_soil_data, analyze_soil_suitability
from app.core.schemas import SoilDataSchema
from app.core.exceptions import SoilDataFetchError


@pytest.fixture
def mock_soil_client():
    return Mock()


def test_fetch_soil_data_success(mock_soil_client):
    mock_response = Mock()
    mock_response.json.return_value = {
        "properties": {
            "layers": [
                {"name": "clay", "depths": [{"values": {"mean": 300}}]},
                {"name": "ocd", "depths": [{"values": {"mean": 500}}]},
                {"name": "phh2o", "depths": [{"values": {"mean": 65}}]},
                {"name": "sand", "depths": [{"values": {"mean": 400}}]},
                {"name": "silt", "depths": [{"values": {"mean": 300}}]},
            ]
        }
    }
    mock_soil_client.request.return_value = mock_response

    result = fetch_soil_data(0, 0, mock_soil_client)
    assert isinstance(result, SoilDataSchema)
    assert result.clay_content == 30
    assert result.organic_carbon == 5
    assert result.pH == 6.5
    assert result.sand_content == 40
    assert result.silt_content == 30


def test_fetch_soil_data_missing_data(mock_soil_client):
    mock_response = Mock()
    mock_response.json.return_value = {"properties": {"layers": []}}
    mock_soil_client.request.return_value = mock_response

    with pytest.raises(SoilDataFetchError):
        fetch_soil_data(0, 0, mock_soil_client)


def test_analyze_soil_suitability(mock_soil_client):
    with patch("app.services.soil_service.fetch_soil_data") as mock_fetch:
        mock_fetch.return_value = SoilDataSchema(
            clay_content=25, organic_carbon=2, pH=6.5, sand_content=35, silt_content=40
        )

        result = analyze_soil_suitability(0, 0, mock_soil_client)
        assert result["suitable"] is True
        assert all(
            result["criteria"][key]["suitable"]
            for key in ["pH", "organic_carbon", "texture"]
        )
