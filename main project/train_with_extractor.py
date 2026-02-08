import pandas as pd
import numpy as np
import pickle
import os

from feature_extraction import extract_features
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load URL dataset
data = pd.read_csv("dataset/urls.csv")

X = []
y = []

for _, row in data.iterrows():
    url = row["url"]
    label = row["label"]

    try:
        features = extract_features(url)
    except Exception as e:
        print(f"Feature extraction failed for {url}: {e}")
        continue

    X.append(features)
    y.append(label)

X = np.array(X)
y = np.array(y)

print("Feature shape:", X.shape)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save model
os.makedirs("model", exist_ok=True)
with open("model/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model retrained using extractor")