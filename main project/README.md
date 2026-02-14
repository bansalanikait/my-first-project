# Phishing URL Detection (Model + Extractor)

## Setup

1. Install dependencies:

```bash
pip install pandas numpy scikit-learn whois tqdm joblib
```

2. Ensure dataset exists at `dataset/urls.csv` with columns:
- `url`
- `label` (`-1` phishing, `1` legitimate)

## Train

```bash
python train_with_extractor.py --sample-size 5000 --random-state 42
```

Outputs model to `model/model.pkl`.

## Predict (CLI)

```bash
python main.py
```

## Compare Model vs Heuristic

```bash
python compare_model_vs_heuristic.py --sample-size 300 --threshold 60
```

This reports accuracy plus phishing precision/recall/F1 for both methods.

## Notes

- Network features (DNS/WHOIS/SSL) can vary by environment and time.
- If those checks fail, extractor returns neutral values so inference can continue.
- For reproducibility, use fixed `--random-state` and keep feature extraction logic consistent between training and inference.
