import re
from urllib.parse import urlparse

from DNS_LOOKUP import dns_record, domain_age, domain_registration_length, ssl_final_state


SUSPICIOUS_WORDS = [
    'login', 'verify', 'update', 'secure',
    'account', 'bank', 'confirm', 'signin'
]
SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.xyz']
SHORTENERS = ['bit.ly', 'tinyurl', 'goo.gl', 'ow.ly', 't.co']
BRANDS = ['paypal', 'google', 'facebook', 'amazon', 'apple', 'bank']


def extract_features(url):
    if not isinstance(url, str):
        url = str(url)

    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    parsed = urlparse(url)
    hostname = (parsed.hostname or '').lower()
    path = parsed.path or ''

    features = []

    # 1-20: lexical/url structure features
    features.append(1 if len(url) < 75 else -1)
    features.append(-1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 1)
    features.append(-1 if any(s in url for s in SHORTENERS) else 1)
    features.append(-1 if '@' in url else 1)
    features.append(-1 if url.rfind('//') > 6 else 1)
    features.append(-1 if '-' in hostname else 1)
    features.append(hostname.count('.'))
    features.append(-1 if hostname.startswith('https') else 1)
    features.append(path.count('/'))
    features.append(sum(1 for w in SUSPICIOUS_WORDS if w in url.lower()))

    try:
        port = parsed.port
    except ValueError:
        port = None
    features.append(1 if port is None or port in [80, 443] else -1)

    features.append(-1 if url.count('.') > 5 else 1)
    features.append(len(hostname))
    features.append(-1 if len(path) > 30 else 1)
    features.append(-1 if '%' in url else 1)
    features.append(url.count('&'))
    features.append(url.count('='))
    features.append(1 if url.startswith('https://') else 0)
    features.append(-1 if any(b in hostname and len(hostname) > len(b) + 5 for b in BRANDS) else 1)
    features.append(-1 if any(hostname.endswith(tld) for tld in SUSPICIOUS_TLDS) else 1)

    # 21-24: network-derived features (can return 0 if unknown)
    try:
        features.append(0.5 * dns_record(hostname))
        features.append(0.5 * domain_age(hostname))
        features.append(0.5 * domain_registration_length(hostname))
        features.append(0.5 * ssl_final_state(hostname))
    except Exception:
        features.extend([0, 0, 0, 0])

    # 25-26: extra suspicious-tld penalties kept for compatibility.
    if any(hostname.endswith(tld) for tld in SUSPICIOUS_TLDS):
        features.append(-1)
        features.append(-1)
    else:
        features.append(1)
        features.append(1)

    # 27-30: reserved/padding for compatibility.
    while len(features) < 30:
        features.append(0)

    return features
