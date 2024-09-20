# Soil Data Processing API
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/serg-mir/soil-data-processing-api/ci.yml?branch=main&style=for-the-badge)

This project processes soil data using the SoilGrids API and provides insights into soil suitability for agriculture.

## Features
- Fetch soil data by coordinates (latitude, longitude)
- Analyze soil suitability based on various soil properties (e.g., pH, organic carbon)
- Exposed via REST API using FastAPI
- Fully containerized with Docker

## Endpoints
- `/soil-info`: Get soil data for a specific location
- `/soil-suitability`: Determine if soil is suitable for farming

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Serg-Mir/soil-data-processing-api.git
   cd soil-data-processing-api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m <project_name> .virtualenvs/soil-data-processing-api
   source .virtualenvs/soil-data-processing-api/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

* Start the FastAPI server locally:
   ```uvicorn main:app --reload```
* Build and run docker container:
   ```
   docker-compose up --build
   docker run -p 8000:8000 soil-data-processing-api
   ```

## Additional information
#### Soil Suitability Analysis
Soil_suitability endpoint evaluates soil quality based on key factors such as pH, organic carbon content, and soil texture.
It uses data retrieved from the SoilGrids API to assess whether the soil at specific coordinates is suitable for agriculture.
Implemented function considers the optimal ranges for these parameters, assigning a suitability score based on how many criteria are met.
At least two out of three criteria must be satisfied for the soil to be considered suitable.

These criteria are inspired by agricultural research and environmental science standards, like soil management guides or the [USDA Soil Texture Classification](https://www.vdh.virginia.gov/content/uploads/sites/20/2016/05/Appendix-F.pdf).
