import numpy as np
import pickle
from feature_extraction import extract_features
import os

# Show working directory (debug)
print("RUNNING FROM:", os.getcwd())

url = input("Enter website URL: ")

# Extract features
features = extract_features(url)
features = np.array(features).reshape(1, -1)

# Load model
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

# Prediction
prediction = model.predict(features)
probability = model.predict_proba(features)

# Get confidence
phishing_prob = probability[0][list(model.classes_).index(-1)] * 100
legit_prob = probability[0][list(model.classes_).index(1)] * 100

# Output
if prediction[0] == -1:
    print("⚠️ Phishing Website Detected!")
    print(f"Confidence: {phishing_prob:.2f}%")
else:
    print("✅ Legitimate Website")
    print(f"Confidence: {legit_prob:.2f}%")



