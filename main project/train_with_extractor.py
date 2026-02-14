import argparse
import os
import pickle

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from DNS_LOOKUP import stats
from feature_extraction import extract_features


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='dataset/urls.csv')
    parser.add_argument('--sample-size', type=int, default=5000)
    parser.add_argument('--random-state', type=int, default=42)
    parser.add_argument('--n-jobs', type=int, default=-1)
    return parser.parse_args()


def process_row(row):
    url = row['url']
    label = row['label']
    try:
        return extract_features(url), label
    except Exception as exc:
        print(f'Feature extraction failed for: {url}')
        print(f'Error: {exc}')
        return None


def main():
    args = parse_args()

    data = pd.read_csv(args.dataset)
    if args.sample_size and args.sample_size > 0 and args.sample_size < len(data):
        data = data.sample(n=args.sample_size, random_state=args.random_state)

    results = Parallel(n_jobs=args.n_jobs, backend='loky')(
        delayed(process_row)(row)
        for _, row in tqdm(data.iterrows(), total=len(data), desc='Extracting features')
    )

    X = []
    y = []
    for result in results:
        if result is not None:
            features, label = result
            X.append(features)
            y.append(label)

    X = np.array(X)
    y = np.array(y)

    print('Feature shape:', X.shape)
    print('Final dataset size:', len(X))
    print('Labels distribution:', np.unique(y, return_counts=True))

    if len(X) == 0:
        raise RuntimeError('No features extracted. Dataset empty.')

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=args.random_state,
        stratify=y
    )

    base_model = RandomForestClassifier(
        n_estimators=200,
        random_state=args.random_state,
        n_jobs=-1,
        class_weight='balanced'
    )

    model = CalibratedClassifierCV(base_model, method='isotonic', cv=5)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print('Accuracy:', accuracy_score(y_test, y_pred))

    os.makedirs('model', exist_ok=True)
    with open('model/model.pkl', 'wb') as f:
        pickle.dump(model, f)

    print('Model retrained using extractor and saved to model/model.pkl')

    print('\nFeature extraction summary:')
    print(f"DNS failures handled: {stats['dns_fail']}")
    print(f"WHOIS failures handled: {stats['whois_fail']}")
    print(f"SSL failures handled: {stats['ssl_fail']}")

    print('\nConfusion Matrix:')
    print(confusion_matrix(y_test, y_pred))

    print('\nClassification Report:')
    print(classification_report(y_test, y_pred, target_names=['Phishing', 'Legitimate']))

    print('\nFeature importances: unavailable for CalibratedClassifierCV wrapper.')


if __name__ == '__main__':
    main()
