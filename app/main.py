import argparse
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import date, datetime

from app.config import Config
from app.weather_client import WeatherClient
from app.repository import WeatherRepository
from app.service import WeatherService


def parse_args():
    parser = argparse.ArgumentParser(description="Daily Weather Collector")
    parser.add_argument(
        "--date",
        help="Target date in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without calling the weather API",
    )
    return parser.parse_args()


def setup_logging(level: str, log_file: str):
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s - %(message)s"
    )

    root_logger = logging.getLogger()

    # Prevent duplicate handlers
    if root_logger.handlers:
        return

    root_logger.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


def main():
    args = parse_args()

    target_date = (
        datetime.strptime(args.date, "%Y-%m-%d").date()
        if args.date
        else date.today()
    )

    config = Config("config.yaml")

    setup_logging(config.log_level, config.log_file)

    logging.info("Weather collection job started for %s", target_date)

    client = WeatherClient(config.base_url, config.api_key)
    repository = WeatherRepository(config.database_path)

    service = WeatherService(
        client,
        repository,
        config.latitude,
        config.longitude,
    )

    try:
        service.collect_daily_weather(target_date, dry_run=args.dry_run)
    except Exception:
        logging.exception("Weather collection failed")
        raise

    logging.info("Weather collection job completed")


if __name__ == "__main__":
    main()
