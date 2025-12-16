import requests
from datetime import date
from typing import Dict


class WeatherClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def fetch_daily_weather(
        self, latitude: float, longitude: float, target_date: date
    ) -> Dict:
        url = (
            f"{self.base_url}/VisualCrossingWebServices/rest/services/timeline/"
            f"{latitude},{longitude}/{target_date.isoformat()}"
        )

        params = {
            "unitGroup": "us",
            "include": "days",
            "elements": "datetime,tempmax,tempmin,precip,snow",
            "key": self.api_key,
            "contentType": "json",
        }

        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()
        days = data.get("days", [])

        if not days:
            raise ValueError("No daily weather data returned from API")

        return days[0]
