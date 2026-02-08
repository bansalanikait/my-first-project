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
phishing_prob = proba[0][list(classes).index(-1)] * 100
legit_prob = proba[0][list(classes).index(1)] * 100

# Threshold-based decision
THRESHOLD = 60

# Manual risk score (URL-only boost)
risk_score = 0

suspicious_keywords = ["login", "verify", "secure", "account", "paypal"]
if any(k in url.lower() for k in suspicious_keywords):
    risk_score += 20

if url.startswith("http://"):
    risk_score += 15

if "-" in url:
    risk_score += 10

if ".xyz" in url:
    risk_score += 20

final_phishing_score = phishing_prob + risk_score

print(f"Adjusted Phishing Score: {final_phishing_score:.2f}%")

if final_phishing_score >= THRESHOLD:
    print("⚠️ Phishing Website Detected!")
else:
    print("✅ Legitimate Website")


print("Classes:", classes)
print("Raw probabilities:", proba)
print(f"Phishing prob: {phishing_prob:.2f}%")
print(f"Legit prob: {legit_prob:.2f}%")



