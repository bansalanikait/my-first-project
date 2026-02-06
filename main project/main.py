import os
print("RUNNING FROM:", os.getcwd())
import pandas as pd
data = pd.read_csv("dataset/phishing.csv")
print(len(data.columns) - 1)
print(data.columns)


import numpy as np
import pickle
from feature_extraction import extract_features

url = input("Enter website URL: ")

features = extract_features(url)
features = np.array(features).reshape(1, -1)

with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

prediction = model.predict(features)

if prediction[0] == -1:
    print("⚠️ Phishing Website Detected!")
else:
    print("✅ Legitimate Website")



