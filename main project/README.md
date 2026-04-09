# Phishing URL Detection (Model + Extractor)

An advanced phishing URL detection system that combines machine learning with heuristic-based feature extraction. This project extracts network and URL features (DNS, WHOIS, SSL) to train a classifier for distinguishing phishing URLs from legitimate ones.

## Setup

1. Install dependencies:

```bash
pip install pandas numpy scikit-learn whois tqdm joblib
```

2. Ensure dataset exists at `dataset/urls.csv` with columns:
   - `url` - Target URL to classify
   - `label` - Class label (`-1` phishing, `1` legitimate)

## Project Structure

```
main project/
├── main.py                           # CLI inference script
├── train_with_extractor.py           # Model training with feature extraction
├── compare_model_vs_heuristic.py     # Benchmark: ML model vs heuristic rules
├── feature_extraction.py             # URL feature extraction utilities
├── DNS_LOOKUP.py                     # DNS/network lookup module
├── dataset/
│   ├── urls.csv                      # Training dataset (URLs + labels)
│   └── news.csv                      # Reference data
├── model/
│   └── model.pkl                     # Trained model (generated after training)
└── frontend/
    └── index.html, style.css         # Web UI files (optional)
```

## Quick Start

### 1. Train the Model

```bash
python train_with_extractor.py --sample-size 5000 --random-state 42
```

**Output**: `model/model.pkl`

Options:
- `--sample-size`: Number of URLs to use for training (default: 5000)
- `--random-state`: Random seed for reproducibility (default: 42)

### 2. Predict on Single URLs (CLI)

```bash
python main.py
```

Enter a website URL when prompted. The system will:
- Extract features (URL structure, DNS, WHOIS, SSL info)
- Load the trained model
- Return classification with probability scores

### 3. Compare Model vs Heuristic

```bash
python compare_model_vs_heuristic.py --sample-size 300 --threshold 60
```

**Output**: Comparative metrics including:
- Overall accuracy
- Phishing precision, recall, and F1-score
- Performance of ML model vs heuristic rules

Options:
- `--sample-size`: URLs to evaluate (default: 300)
- `--threshold`: Confidence threshold for classification (default: 60)

## Feature Extraction

The system extracts features in two categories:

### URL-Based Features
- URL length, domain age, character patterns
- Presence of special characters
- TLD information

### Network Features
- DNS response times
- WHOIS registration details
- SSL/certificate information
- IP reputation

## Important Notes

- **Network Features Variability**: DNS/WHOIS/SSL checks can vary by environment, network, and time. If network checks fail, the extractor returns neutral values so inference continues.
- **Reproducibility**: Use fixed `--random-state` during training and keep feature extraction logic consistent between training and inference.
- **Dependencies**: Requires network access for DNS/WHOIS/SSL checks. Some corporate networks may block these checks.
- **Training First**: Always run `train_with_extractor.py` before using `main.py` for predictions.
- **Dataset Format**: Ensure `dataset/urls.csv` is properly formatted with `url` and `label` columns.
