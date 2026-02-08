import pandas as pd
import numpy as np
import pickle
import os

from sklearn.metrics import (
    confusion_matrix,
    classification_report
)

from feature_extraction import extract_features
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load URL dataset
data = pd.read_csv("dataset/urls.csv").sample(5000)

X = []
y = []

from tqdm import tqdm

from joblib import Parallel, delayed
import numpy as np

def process_row(row):
    url = row["url"]
    label = row["label"]
    try:
        features = extract_features(url)
        return features, label
    except Exception:
        return None

results = Parallel(
    n_jobs=-1,          # use all CPU cores
    backend="loky"      # best for network / I/O
)(
    delayed(process_row)(row)
    for _, row in tqdm(
        data.iterrows(),
        total=len(data),
        desc="Extracting features"
    )
)

# Collect results
X = []
y = []

for result in results:
    if result is not None:
        features, label = result
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
    random_state=42,
    verbose=1,
    n_jobs=-1
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

# Detects how many times the error came due to non rechable sites
from DNS_LOOKUP import stats

print("\nFeature extraction summary:")
print(f"DNS failures handled: {stats['dns_fail']}")
print(f"WHOIS failures handled: {stats['whois_fail']}")
print(f"SSL failures handled: {stats['ssl_fail']}")


print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Phishing", "Legitimate"]
))
