from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return "Backend is running!"

@app.route("/predict-risk", methods=["POST"])
def predict():
    data = request.json
    rainfall = data.get("rainfall", 0)
    slope = data.get("slope", 0)

    if rainfall > 80 and slope > 30:
        risk = "High"
    elif rainfall > 50:
        risk = "Medium"
    else:
        risk = "Low"

    return jsonify({"risk_level": risk})

if __name__ == "__main__":
    app.run(debug=True)