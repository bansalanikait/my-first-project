import numpy as np
import pickle
from feature_extraction import extract_features
import os

print("RUNNING FROM:", os.getcwd())

url = input("Enter website URL: ")

# Extract features
features = extract_features(url)
features = np.array(features).reshape(1, -1)

# Load model
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

# Get probabilities
proba = model.predict_proba(features)
classes = model.classes_

# Extract phishing & legit probabilities
class_map = dict(zip(model.classes_, proba[0]))

phishing_prob = class_map.get(-1, 0) * 100
legit_prob    = class_map.get(1, 0) * 100




if phishing_prob >= 80:
    print("🚨 Phishing Website")
elif phishing_prob >= 50:
    print("⚠️ Suspicious Website")
else:
    print("✅ Legitimate Website")






print("Classes:", classes)
print("Raw probabilities:", proba)
print(f"Phishing prob: {phishing_prob:.2f}%")
print(f"Legit prob: {legit_prob:.2f}%")





