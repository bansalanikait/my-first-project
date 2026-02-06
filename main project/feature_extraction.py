def having_ip_address(url):
    import re
    return -1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 1