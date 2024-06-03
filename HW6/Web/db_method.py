import sqlite3
from datetime import datetime
from flask import Flask, jsonify

DB_NAME = "temp_data.sqlite"
# Initialize SQLite database
def initdb(db_name=DB_NAME):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(
        """CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY,
        temperature REAL NOT NULL,
        humidity REAL NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
        )
        conn.commit()
        conn.close()
        print("(initdb) Database initialized successfully.")
    except sqlite3.Error as e:
        print("(initdb) Error occurred:", e)
initdb(db_name=DB_NAME) 

def insert_sensor_data(temperature, humidity, timestamp=None,
db_name=DB_NAME):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if timestamp is None:
            timestamp = datetime.now().replace(microsecond=0)
        cursor.execute("""INSERT INTO sensor_data (temperature, humidity,
timestamp) VALUES (?, ?, ?)""", (temperature, humidity, timestamp), 
        ) 
        conn.commit()
        conn.close()
        print("(insert_sensor_data) Sensor data inserted successfully.")
    except sqlite3.Error as e:
        print("(insert_sensor_data) Error occurred:", e)
