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

proba = model.predict_proba(features)[0]
classes = model.classes_

class_map = dict(zip(classes, proba))

phishing_prob = class_map.get(-1, 0) * 100
legit_prob = class_map.get(1, 0) * 100

prediction = model.predict(features)[0]

if prediction == -1:
    print("⚠️ Phishing Website Detected!")
else:
    print("✅ Legitimate Website")

print(f"Confidence → Phishing: {phishing_prob:.2f}% | Legit: {legit_prob:.2f}%")


print("Classes:", classes)
print("Raw probabilities:", proba)
print(f"Phishing prob: {phishing_prob:.2f}%")
print(f"Legit prob: {legit_prob:.2f}%")





