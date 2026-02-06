def having_ip_address(url):
    import re
    return -1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 1

def extract_features(url):
    features = []

    # Example features (temporary)
    features.append(1)   # dummy feature
    features.append(-1)  # dummy feature
    features.append(1)

    return features