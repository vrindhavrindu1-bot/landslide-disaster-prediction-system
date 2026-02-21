import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
data = pd.read_csv("landslide_dataset.csv")
print(data.columns)

# Define features and target
X = data[["rainfall_level",  "slope_type",  "soil_type",  "crack_observed",  "soil_flow_observed"]]
y = data["risk_level"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)

# Save trained model for backend use
joblib.dump(model, "landslide_model.pkl")
print("Model saved as landslide_model.pkl")
