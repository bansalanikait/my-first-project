import re
from urllib.parse import urlparse
from DNS_LOOKUP import domain_age,dns_record,domain_registration_length,ssl_final_state


def extract_features(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    features = []
    


    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path

    # 1. URL length
    features.append(1 if len(url) < 75 else -1)


    # 2. IP address in URL
    features.append(-1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 1)

    # 3. Shortening service
    shortening = ["bit.ly", "tinyurl", "goo.gl", "ow.ly", "t.co"]
    features.append(-1 if any(s in url for s in shortening) else 1)

    # 4. '@' symbol
    features.append(-1 if '@' in url else 1)

    # 5. Double slash redirect
    features.append(-1 if url.rfind("//") > 6 else 1)

    # 6. Hyphen in domain
    features.append(-1 if "-" in domain else 1)

    # 7. Subdomain count
    features.append(domain.count('.'))

    # 8. HTTPS token misuse
    features.append(-1 if domain.lower().startswith("https") else 1)

    # 9. URL depth
    features.append(path.count('/'))

    # 10. Suspicious words
    suspicious_words = [
        "login", "verify", "update", "secure",
        "account", "bank", "confirm", "signin"
    ]
    features.append(
    sum(1 for w in suspicious_words if w in url.lower())
    )

    # 11. Port in URL
    port = parsed.port
    features.append(1 if port is None or port in [80, 443] else -1)

    # 12. Number of dots in URL
    features.append(-1 if url.count('.') > 5 else 1)

    # 13. Domain length
    features.append(len(domain))

    # 14. Path length
    features.append(-1 if len(path) > 30 else 1)

    # 15. URL encoding
    features.append(-1 if '%' in url else 1)

    # 16. Multiple query parameters
    features.append(url.count('&'))

    # 17. Excessive '=' symbols
    features.append(url.count('='))

    # 18. HTTP instead of HTTPS
    features.append(1 if url.startswith("https://") else 0)

    # 19. Brand name abuse
    brands = ["paypal", "google", "facebook", "amazon", "apple", "bank"]
    features.append(-1 if any(b in domain.lower() and len(domain) > len(b) + 5 for b in brands) else 1)

    # 20. Suspicious TLD
    suspicious_tlds = [".tk", ".ml", ".ga", ".cf", ".xyz"]
    features.append(-1 if any(domain.endswith(tld) for tld in suspicious_tlds) else 1)


    # Extract domain again (safe)
    domain = domain.split(':')[0]

    # 21–24. Network-based features (safe / optional)
    try:
        features.append(0.5 * dns_record(domain))
        features.append(0.5 * domain_age(domain))
        features.append(0.5 * domain_registration_length(domain))
        features.append(0.5 * ssl_final_state(domain))

    except Exception:
        # Unknown ≠ phishing
        features.extend([0, 0, 0, 0])




    if any(domain.endswith(tld) for tld in suspicious_tlds):
        features.append(-1)
        features.append(-1)  # extra penalty
    else:
        features.append(1)
        features.append(1)

    # Fill remaining features (for dataset compatibility)
    while len(features) < 30:
        features.append(0)

    return features