import re

def extract_features(url):
    features = []

    # 1. URL length
    features.append(1 if len(url) < 54 else -1)

    # 2. IP address in URL
    features.append(-1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 1)

    # 3. Shortening service
    shortening = ["bit.ly", "tinyurl", "goo.gl", "ow.ly"]
    features.append(-1 if any(s in url for s in shortening) else 1)

    # 4. '@' symbol
    features.append(-1 if '@' in url else 1)

    # 5. Double slash redirect
    features.append(-1 if url.rfind("//") > 6 else 1)

    # 6. Hyphen in domain
    features.append(-1 if "-" in url else 1)

    # Fill remaining features with NEUTRAL values
    while len(features) < 30:
        features.append(0)

    return features