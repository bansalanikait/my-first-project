import pandas as pd
import pickle
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("dataset/phishing.csv")

print("Dataset loaded:", data.shape)

# Split features & label
X = data.drop("Result", axis=1)
y = data["Result"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Check accuracy (IMPORTANT)
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Model Accuracy:", acc)

# Create model folder
os.makedirs("model", exist_ok=True)

# Save model
with open("model/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ model.pkl saved successfully")