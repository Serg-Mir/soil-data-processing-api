from fastapi.testclient import TestClient
import app
import pytest
from unittest.mock import patch

client = TestClient(app)


@pytest.fixture
def mock_fetch_soil_data():
    with patch("app.services.soil_service.fetch_soil_data") as mock:
        yield mock


@pytest.fixture
def mock_analyze_soil_suitability():
    with patch("app.services.soil_service.analyze_soil_suitability") as mock:
        yield mock


def test_get_soil_info_success(mock_fetch_soil_data):
    mock_fetch_soil_data.return_value = {
        "clay_content": 16.1,
        "organic_carbon": 1.75,
        "pH": 8.1,
        "sand_content": 58.2,
        "silt_content": 25.7,
    }

    response = client.get("/soil-info?lat=25&lon=33")
    assert response.status_code == 200
    assert response.json() == mock_fetch_soil_data.return_value


def test_get_soil_info_invalid_coordinates():
    response = client.get("/soil-info?lat=91&lon=0")
    assert response.status_code == 422  # Unprocessable Entity


def test_get_soil_suitability_success(mock_analyze_soil_suitability):
    mock_analyze_soil_suitability.return_value = {
        "suitable": False,
        "criteria": {
            "pH": {"value": 8.1, "suitable": False},
            "organic_carbon": {"value": 1.75, "suitable": True},
            "texture": {"clay": 16.1, "silt": 25.7, "sand": 58.2, "suitable": False},
        },
    }

    response = client.get("/soil-suitability?lat=25&lon=33")
    assert response.status_code == 200
    assert response.json() == mock_analyze_soil_suitability.return_value


def test_get_soil_suitability_invalid_coordinates():
    response = client.get("/soil-suitability?lat=0&lon=181")
    assert response.status_code == 422  # Unprocessable Entity
