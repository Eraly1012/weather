import requests
import sqlite3
import time
from datetime import datetime

CITY = "Uralsk"
DB_NAME = "weather.db"
INTERVAL = 1800


def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            temperature REAL
        )
    """)
    conn.commit()
    conn.close()


def get_temperature():
    url = f"https://wttr.in/{CITY}?format=3"
    response = requests.get(url, timeout=10)
    text = response.text

    # оставляем только цифры и знак минус
    temp_str = ""
    for ch in text:
        if ch.isdigit() or ch == "-" :
            temp_str += ch

    return float(temp_str)



def save_to_db(temp):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO weather (datetime, temperature) VALUES (?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), temp)
    )
    conn.commit()
    conn.close()


def main():
    create_db()
    print("Программа запущена. Ctrl+C — остановка.")

    try:
        while True:
            temperature = get_temperature()
            save_to_db(temperature)
            print(f"{datetime.now()} | Температура: {temperature}°C")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("Остановлено пользователем.")


if __name__ == "__main__":
    main()
