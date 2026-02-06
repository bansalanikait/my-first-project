import pandas as pd

data = pd.read_csv("dataset/phishing.csv")
print(data.head())
print(data.shape)

from sklearn.model_selection import train_test_split

X = data.drop("Result", axis=1)
y = data["Result"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

from sklearn.metrics import accuracy_score

y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))


import pickle

with open("model/model.pkl", "wb") as f:
    pickle.dump(model, f)