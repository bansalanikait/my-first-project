def extract_features(url):
    features = []

    # 1. URL length
    features.append(1 if len(url) < 54 else -1)

    # 2. Shortening service
    shortening_services = ["bit.ly", "tinyurl", "goo.gl", "ow.ly"]
    features.append(-1 if any(s in url for s in shortening_services) else 1)

    # 3. '@' symbol
    features.append(-1 if '@' in url else 1)

    # 4. Double slash redirecting
    features.append(-1 if url.rfind("//") > 6 else 1)

    # Fill remaining features with safe defaults
    while len(features) < 30:
        features.append(1)

    return features