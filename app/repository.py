import sqlite3
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime


class WeatherRepository:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS daily_weather (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    temp_max_f REAL,
                    temp_min_f REAL,
                    rainfall_in REAL,
                    snowfall_in REAL,
                    source TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(date, latitude, longitude)
                )
                """
            )

    def record_exists(self, date: str, latitude: float, longitude: float) -> bool:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT 1 FROM daily_weather
                WHERE date = ? AND latitude = ? AND longitude = ?
                """,
                (date, latitude, longitude),
            )
            return cursor.fetchone() is not None

    def insert_record(
        self,
        date: str,
        latitude: float,
        longitude: float,
        weather: Dict,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO daily_weather (
                    date,
                    latitude,
                    longitude,
                    temp_max_f,
                    temp_min_f,
                    rainfall_in,
                    snowfall_in,
                    source,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    date,
                    latitude,
                    longitude,
                    weather.get("tempmax"),
                    weather.get("tempmin"),
                    weather.get("precip"),
                    weather.get("snow"),
                    "visualcrossing",
                    datetime.utcnow().isoformat(),
                ),
            )
