from flask_cors import CORS
from flask import Flask, request, jsonify
import joblib
import numpy as np
import random
import sqlite3

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
            risk_level TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

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

    # Simulated accumulated values
    rainfall = random.randint(0, 2)
    slope = random.randint(0, 2)
    soil = random.randint(0, 2)
    soil_flow = random.randint(0, 2)

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



if __name__ == "__main__":
    app.run(debug=True)

