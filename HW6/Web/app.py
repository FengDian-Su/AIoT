import sqlite3
from flask import Flask, jsonify, render_template, request
from db_method import DB_NAME, insert_sensor_data, initdb
import datetime

DB_NAME = "temp_data.sqlite"

app = Flask(__name__)
data = {"temperature": [], "humidity": []}

@app.post("/post_data")
def receive_data():
    try:
        content = request.get_json()
        temperature = content["temperature"]
        humidity = content["humidity"]
        data["temperature"].append(temperature)
        data["humidity"].append(humidity)
        # Call function to insert sensor data into the database
        insert_sensor_data(temperature, humidity)
        print(f"Received data: temperature={temperature},humidity={humidity}")
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error receiving data: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/data')
def get_data():
    start = request.args.get('start')
    end = request.args.get('end')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if start and end:
        cursor.execute("SELECT timestamp, temperature, humidity FROM sensor_data WHERE timestamp BETWEEN ? AND ?", (start, end))
    else:
        cursor.execute("SELECT timestamp, temperature, humidity FROM sensor_data")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/time_ranges')
def get_time_ranges():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM sensor_data")
    min_timestamp, max_timestamp = cursor.fetchone()
    conn.close()

    if not min_timestamp or not max_timestamp:
        return jsonify([])

    min_time = datetime.datetime.strptime(min_timestamp, "%Y-%m-%d %H:%M:%S")
    max_time = datetime.datetime.strptime(max_timestamp, "%Y-%m-%d %H:%M:%S")

    time_ranges = []
    while min_time < max_time:
        end_time = min_time + datetime.timedelta(seconds=30)
        time_ranges.append({
            "start": min_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end": end_time.strftime("%Y-%m-%d %H:%M:%S")
        })
        min_time = end_time

    # 只返回最新的10個區間
    return jsonify(time_ranges[-10:])

if __name__ == "__main__":
    initdb(DB_NAME)
    app.run(host="0.0.0.0", port=5500, debug=True)