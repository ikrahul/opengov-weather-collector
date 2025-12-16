import yaml
from pathlib import Path


class Config:
    def __init__(self, path: str):
        self.path = Path(path)
        self._data = self._load()

    def _load(self) -> dict:
        if not self.path.exists():
            raise FileNotFoundError(f"Config file not found: {self.path}")

        with open(self.path, "r") as f:
            return yaml.safe_load(f)

    @property
    def api_key(self) -> str:
        return self._data["weather_api"]["api_key"]

    @property
    def base_url(self) -> str:
        return self._data["weather_api"]["base_url"]

    @property
    def latitude(self) -> float:
        return self._data["location"]["latitude"]

    @property
    def longitude(self) -> float:
        return self._data["location"]["longitude"]

    @property
    def database_path(self) -> str:
        return self._data["storage"]["database_path"]

    @property
    def log_level(self) -> str:
        return self._data["logging"].get("level", "INFO")

    @property
    def log_file(self) -> str:
        return self._data["logging"]["file"]
