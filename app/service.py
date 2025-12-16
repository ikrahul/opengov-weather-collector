import logging
from datetime import date
from app.weather_client import WeatherClient
from app.repository import WeatherRepository


class WeatherService:
    def __init__(
        self,
        client: WeatherClient,
        repository: WeatherRepository,
        latitude: float,
        longitude: float,
    ):
        self.client = client
        self.repository = repository
        self.latitude = latitude
        self.longitude = longitude

    def collect_daily_weather(self, target_date: date, dry_run: bool = False) -> None:
        date_str = target_date.isoformat()

        if self.repository.record_exists(date_str, self.latitude, self.longitude):
            logging.info("Weather record already exists for %s, skipping", date_str)
            return

        if dry_run:
            logging.info("Dry run enabled, skipping API call for %s", date_str)
            return

        logging.info("Fetching weather data for %s", date_str)
        weather = self.client.fetch_daily_weather(
            self.latitude, self.longitude, target_date
        )

        self.repository.insert_record(
            date_str, self.latitude, self.longitude, weather
        )

        logging.info("Weather data stored successfully for %s", date_str)
