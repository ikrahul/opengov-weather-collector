# OpenGov Weather Collector

A small background service that collects daily weather data to help City Public Works teams make safe crew deployment decisions.

---

## 1. Overview

Public Works teams often need to decide whether crews can be sent out to maintain storm drains. Weather conditions like heavy rain, snowfall, or extreme temperatures directly affect those decisions.

This project is a simple background program that collects daily weather data for a specific location and stores it for later reference. The focus is on reliability, simplicity, and collecting only the data that is actually needed.

The goal was to build something realistic, easy to run, and easy to reason about—without adding unnecessary complexity.

---

## 2. User Story Alignment

**User Story**

> As a City Public Works Department Supervisor, I want to know the actual weather conditions for a given location as latitude and longitude so that I can decide if I can deploy my work crews.

**How this solution addresses it**

- Uses latitude and longitude as the source of truth for location
- Collects daily weather aggregates relevant to operational decisions
- Stores historical data so past conditions can be reviewed if needed
- Runs as a background job that can be scheduled once per day

---

## 3. Data Collected

For each configured location and date, the application stores:

| Field | Description |
|-----|------------|
| Date | Date of the weather observation |
| Max Temperature (°F) | Daily maximum temperature |
| Min Temperature (°F) | Daily minimum temperature |
| Rainfall (inches) | Total daily rainfall |
| Snowfall (inches) | Total daily snowfall |
| Source | Weather data provider |
| Created At | Timestamp when the record was stored |

Only daily summary data is collected, since that is what the user story requires.

---

## 4. Architecture Overview

```

OS Scheduler (cron / Task Scheduler)
↓
Weather Service
↓
Visual Crossing API
↓
SQLite Database
↓
Logs

````

### Design principles

- Each component has a single, clear responsibility
- The job can be run repeatedly without creating duplicate data
- API usage is kept intentionally low
- Failures are visible through logs, not hidden

---

## 5. Technology Choices

| Area | Choice | Reasoning |
|----|------|----------|
| Language | Python | Quick to develop, readable, and well-suited for data tasks |
| Weather API | Visual Crossing | Required by the assignment |
| Database | SQLite | Simple, portable, and sufficient for the scope |
| Configuration | YAML | Easy to read and modify without touching code |
| Scheduling | OS-level scheduler | Reliable and commonly used in production |

The structure is intentionally straightforward and could be translated to C# if needed.

---

## 6. Configuration

All configuration lives in a single file: `config.yaml`.

```yaml
weather_api:
  base_url: https://weather.visualcrossing.com
  api_key: YOUR_API_KEY

location:
  latitude: 18.5204
  longitude: 73.8567

storage:
  database_path: data/weather.db

logging:
  level: INFO
````

Changing the location or credentials does not require any code changes.

---

## 7. How to Run

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run for today

```bash
python -m app.main
```

### Run for a specific date

```bash
python -m app.main --date 2025-12-15
```

### Dry-run mode (no API call)

```bash
python -m app.main --dry-run
```

Dry-run mode is useful during development to validate behavior without consuming API quota.

---

## 8. Scheduling

The program is designed to be run once per day using an OS scheduler.

### Example cron job

```bash
0 6 * * * python -m app.main
```

This example runs the job every day at 6:00 AM local time.

---

## 9. Data Storage

Weather data is stored in a local SQLite database:

```
data/weather.db
```

### Schema highlights

* A unique constraint on `(date, latitude, longitude)`
* Prevents duplicate inserts if the job is re-run
* Safe to execute multiple times without side effects

### Reading the database

```bash
sqlite3 data/weather.db
SELECT * FROM daily_weather;
```

---

## 10. Error Handling and Logging

The application logs both operational events and errors to ensure issues can be reviewed after execution.

- Logs are written to the console for interactive runs
- Logs are also persisted to a rotating log file
- Errors and exceptions include stack traces
- Log files are automatically rotated to prevent uncontrolled growth

By default, logs are written to:

logs/weather_collector.log

This approach keeps logging simple while ensuring failures are traceable in a production-like environment.

---

## 11. Rate Limit and Safety Considerations

* Only one API call is made per day per location
* The request includes only the fields required by the user story
* Dry-run support helps avoid accidental API usage during development
* Dates can be explicitly specified for controlled backfills

These measures are intended to stay well within Visual Crossing free-tier limits.

---

## 12. Assumptions and Trade-offs

* SQLite was chosen to keep setup simple and portable
* The solution supports a single location, matching the user story
* No UI was added to keep the scope focused
* The implementation avoids over-engineering by design

---

## 13. Future Improvements (that can be added)

* Support multiple configured locations
* Add unit and integration tests
* Move to a managed database if usage grows
* Add monitoring or alerting if required
* Expose the data through an internal API

---

## 14. Summary

This project delivers a focused solution for the stated problem:

* Collects accurate daily weather data
* Stores it reliably for later use
* Is easy to configure and run
* Avoids unnecessary complexity

The result is a small, maintainable service that fits the scope of the assignment.