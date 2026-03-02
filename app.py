from flask_cors import CORS
from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# Load trained model
model = joblib.load("landslide_model.pkl")

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/predict-risk", methods=["POST"])
def predict():
    data = request.json

    rainfall = int(data.get("rainfall", 0))
    slope = int(data.get("slope", 0))
    soil = int(data.get("soil", 0))
    crack = int(data.get("crack", 0))
    soil_flow = int(data.get("soil_flow", 0))

    features = np.array([[rainfall, slope, soil, crack, soil_flow]])

    prediction = model.predict(features)[0]

    risk_map = {0: "Low", 1: "Medium", 2: "High"}
    risk = risk_map.get(prediction, "Low")

    return jsonify({"risk_level": risk})

if __name__ == "__main__":
    app.run(debug=True)
