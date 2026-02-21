import joblib
import numpy as np

model = joblib.load("landslide_model.pkl")

# example input
sample = np.array([[2, 0, 0, 0, 0]])  

prediction = model.predict(sample)

print("Predicted Risk Level:", prediction[0])
