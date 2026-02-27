import joblib
import numpy as np

model = joblib.load("landslide_model.pkl")

# Example input (must match training feature order!)
# rainfall_level, slope_type, soil_type, crack_observed, soil_flow_observed
# Feature order:
# rainfall_level (0=Low, 1=Medium, 2=High)
# slope_type (0=Flat, 1=Moderate, 2=Steep)
# soil_type (0=Rock, 1=Clay, 2=Sand)
# crack_observed (0=None, 1=Moderate, 2=Severe)
# soil_flow_observed (0=None, 1=Moderate, 2=Severe)
new_data = np.array([[2, 1, 0, 1, 0]])
prediction = model.predict(new_data)
print("Predicted Risk Level:", prediction[0])
