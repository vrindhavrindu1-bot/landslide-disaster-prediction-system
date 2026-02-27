import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
data = pd.read_csv("landslide_dataset.csv")
print(data.columns)

# Define features and target
# -------------------------------------------------
# Environmental Feature Encoding Explanation
# -------------------------------------------------

# Rainfall Level Encoding:
# 0 → Low (0–50 mm/day)
# 1 → Moderate (51–100 mm/day)
# 2 → Heavy (>100 mm/day)

# Slope Type Encoding:
# 0 → Gentle (0–15 degrees)
# 1 → Moderate (16–30 degrees)
# 2 → Steep (>30 degrees)

# Soil Stability Encoding:
# 0 → Stable
# 1 → Moderately Stable
# 2 → Loose / Unstable
# Crack Observed:
# 0 → None
# 1 - Moderate
# 2 → Severe

# Soil Flow Observed:
# 0 → None
# 1 → Moderate
# 2 - Severe
X = data[["rainfall_level",  "slope_type",  "soil_type",  "crack_observed",  "soil_flow_observed"]]
y = data["risk_level"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)

# Save trained model for backend use
joblib.dump(model, "landslide_model.pkl")
print("Model saved as landslide_model.pkl")
