import os
import pickle

import numpy as np

from feature_extraction import extract_features


def main():
    print('RUNNING FROM:', os.getcwd())
    url = input('Enter website URL: ').strip()

    features = np.array(extract_features(url)).reshape(1, -1)

    with open('model/model.pkl', 'rb') as f:
        model = pickle.load(f)

    proba = model.predict_proba(features)[0]
    classes = list(model.classes_)
    class_map = dict(zip(classes, proba))

    phishing_prob = class_map.get(-1, 0.0) * 100.0
    legit_prob = class_map.get(1, 0.0) * 100.0

    prediction = model.predict(features)[0]
    if prediction == -1:
        print('Phishing Website Detected!')
    else:
        print('Legitimate Website')

    print(f'Confidence -> Phishing: {phishing_prob:.2f}% | Legit: {legit_prob:.2f}%')
    print('Classes:', classes)
    print('Raw probabilities:', proba)


if __name__ == '__main__':
    main()
