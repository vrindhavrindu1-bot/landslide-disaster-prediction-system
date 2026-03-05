from flask_cors import CORS
from flask import Flask, request, jsonify
import joblib
import numpy as np
import sqlite3
import requests

app = Flask(__name__)
CORS(app)
def init_db():
    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL,
            longitude REAL,
            crack_observed INTEGER,
            rainfall INTEGER,
            slope INTEGER,
            soil INTEGER,
            soil_flow INTEGER,
            risk_level TEXT,
            support_count INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")
    conn.commit()
    conn.close()

init_db()
def get_rainfall_level(lat, lon):
    

API_KEY = "b2a84e5e513605b4d8136a3245ef5a58"
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    rainfall = data.get("rain", {}).get("1h", 0)

    if rainfall < 2:
        return 0
    elif rainfall < 10:
        return 1
    else:
        return 2
def get_slope(lat, lon):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"

    response = requests.get(url)
    data = response.json()

    elevation = data["results"][0]["elevation"]

    if elevation < 100:
        return 0
    elif elevation < 500:
        return 1
    else:
        return 2
def get_soil_type(lat, lon):
    url = f"https://rest.isric.org/soilgrids/v2.0/properties/query?lon={lon}&lat={lat}"

    response = requests.get(url)
    data = response.json()

    if "properties" in data:
        return 1
    else:
        return 0
def get_soil_flow(rainfall):
    if rainfall == 2:
        return 2
    elif rainfall == 1:
        return 1
    else:
        return 0

# Load trained model
model = joblib.load("landslide_model.pkl")
@app.route("/")
def home():
    return "Backend is running!"
@app.route("/predict-risk", methods=["POST"])
def predict():
    
    data = request.json

    latitude = float(data.get("latitude", 0))
    longitude = float(data.get("longitude", 0))

    crack = int(data.get("crack_observed", 0))
    rainfall = get_rainfall_level(latitude, longitude)
    slope = get_slope(latitude, longitude)
    soil = get_soil_type(latitude, longitude)
    soil_flow = get_soil_flow(rainfall) 
    features = np.array([[rainfall, slope, soil, crack, soil_flow]])

    prediction = model.predict(features)[0]

    risk_map = {0: "Low", 1: "Medium", 2: "High"}
    risk = risk_map.get(prediction, "Low")

    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reports 
        (latitude, longitude, crack_observed, rainfall, slope, soil, soil_flow, risk_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (latitude, longitude, crack, rainfall, slope, soil, soil_flow, risk))

    conn.commit()
    conn.close()

    return jsonify({"risk_level": risk})
@app.route("/support/<int:report_id>", methods=["POST"])
def support_report(report_id):
    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE reports
        SET support_count = support_count + 1
        WHERE id = ?
    """, (report_id,))

    conn.commit()
    conn.close()

    return {"message": "Support added"}
@app.route("/get-reports")
def get_reports():
    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, latitude, longitude, risk_level, support_count
        FROM reports
    """)

    rows = cursor.fetchall()
    conn.close()

    reports = []
    for row in rows:
        reports.append({
            "id": row[0],
            "latitude": row[1],
            "longitude": row[2],
            "risk_level": row[3],
            "support_count": row[4]
        })

    return jsonify(reports)
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return {"message": "User registered"}
    except:
        return {"message": "Username already exists"}

    finally:
        conn.close()
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return {"message": "Login successful"}
    else:
        return {"message": "Invalid credentials"}
    



if __name__ == "__main__":
    app.run(debug=True)




