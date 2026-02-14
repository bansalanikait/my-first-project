import numpy as np
import pickle
from feature_extraction import extract_features
import os

print("RUNNING FROM:", os.getcwd())
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder='static', template_folder='templates')  # Add static and template folders
CORS(app)

print("RUNNING FROM BACKEND")

@app.route("/")
def home():
    return render_template('index.html')  # Serve the HTML page

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        url = data.get("url")
        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Extract features
        features = extract_features(url)
        if features is None:
            return jsonify({"error": "Failed to extract features from URL"}), 400

        # Load model (assuming it's in model/model.pkl)
        with open("model/model.pkl", "rb") as f:
            model = pickle.load(f)

        # Get probabilities
        proba = model.predict_proba([features])[0]  # Note: predict_proba expects a 2D array
        classes = model.classes_

        # Map classes to probabilities
        class_map = dict(zip(classes, proba))
        phishing_prob = class_map.get(-1, 0) * 100
        legit_prob = class_map.get(1, 0) * 100

        # Make prediction
        prediction = model.predict([features])[0]  # Note: predict expects a 2D array

        if prediction == -1:
            result = "Phishing"
            message = "⚠️ Phishing Website Detected!"
        else:
            result = "Legitimate"
            message = "✅ Legitimate Website"

        print(f"Prediction: {result}")
        print(f"Confidence → Phishing: {phishing_prob:.2f}% | Legit: {legit_prob:.2f}%")

        # Return JSON response
        return jsonify({
            "prediction": result,
            "phishing_prob": round(phishing_prob, 2),
            "legit_prob": round(legit_prob, 2),
            "message": message
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "An error occurred during prediction"}), 500

if __name__ == "__main__":
    app.run(debug=True)



