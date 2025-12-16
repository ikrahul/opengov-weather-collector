import sqlite3

conn = sqlite3.connect("data/weather.db")
cursor = conn.cursor()

for row in cursor.execute("SELECT * FROM daily_weather"):
    print(row)

conn.close()
