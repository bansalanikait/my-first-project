import argparse
import pickle

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score

from feature_extraction import extract_features


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='dataset/urls.csv')
    parser.add_argument('--model', default='model/model.pkl')
    parser.add_argument('--sample-size', type=int, default=300)
    parser.add_argument('--random-state', type=int, default=42)
    parser.add_argument('--threshold', type=float, default=60.0)
    return parser.parse_args()


def heuristic_score(url):
    url = (url or '').lower()
    score = 0

    if url.startswith('http://'):
        score += 15
    if '@' in url:
        score += 20
    if any(k in url for k in ['login', 'verify', 'secure', 'account', 'signin', 'update']):
        score += 20
    if any(tld in url for tld in ['.xyz', '.tk', '.ml', '.ga', '.cf', '.top']):
        score += 20
    if '-' in url:
        score += 10
    if len(url) > 100:
        score += 15

    return min(100, score)


def report(name, y_true, y_pred):
    print(f'\n=== {name} ===')
    print('Accuracy:', round(accuracy_score(y_true, y_pred), 4))
    print('Phishing precision:', round(precision_score(y_true, y_pred, pos_label=-1, zero_division=0), 4))
    print('Phishing recall:', round(recall_score(y_true, y_pred, pos_label=-1, zero_division=0), 4))
    print('Phishing F1:', round(f1_score(y_true, y_pred, pos_label=-1, zero_division=0), 4))
    print('Confusion matrix [rows=true(-1,1), cols=pred(-1,1)]:')
    print(confusion_matrix(y_true, y_pred, labels=[-1, 1]))
    print('Classification report:')
    print(classification_report(y_true, y_pred, labels=[-1, 1], target_names=['Phishing', 'Legitimate'], zero_division=0))


def main():
    args = parse_args()

    data = pd.read_csv(args.dataset)
    if args.sample_size and args.sample_size > 0 and args.sample_size < len(data):
        data = data.sample(n=args.sample_size, random_state=args.random_state)

    urls = data['url'].astype(str).tolist()
    y_true = data['label'].astype(int).to_numpy()

    with open(args.model, 'rb') as f:
        model = pickle.load(f)

    # Model predictions
    model_preds = []
    for url in urls:
        feats = np.array(extract_features(url)).reshape(1, -1)
        proba = model.predict_proba(feats)[0]
        class_map = dict(zip(model.classes_, proba))
        phishing_prob = class_map.get(-1, 0.0) * 100.0
        pred = -1 if phishing_prob >= args.threshold else 1
        model_preds.append(pred)

    # Heuristic predictions
    heur_preds = [(-1 if heuristic_score(url) >= args.threshold else 1) for url in urls]

    report('Model', y_true, np.array(model_preds))
    report('Heuristic baseline', y_true, np.array(heur_preds))


if __name__ == '__main__':
    main()
