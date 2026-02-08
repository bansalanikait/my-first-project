import whois
from datetime import datetime
import socket

#Deals with error
stats = {
    "dns_fail": 0,
    "ssl_fail": 0,
    "whois_fail": 0
}

def domain_age(domain):
    try:
        w = whois.whois(domain)
        creation = w.creation_date

        if creation is None:
            stats["whois_fail"] += 1
            return -1

        if isinstance(creation, list):
            creation = creation[0]

        age_days = (datetime.now() - creation).days
        return 1 if age_days > 365 else -1
    except Exception:
        stats["whois_fail"] += 1
        return -1
    



dns_cache = {}

def dns_record(domain):
    if domain in dns_cache:
        return dns_cache[domain]
    try:
        socket.gethostbyname(domain)
        dns_cache[domain] = 1
    except:
        dns_cache[domain] = -1
    return dns_cache[domain]
    

def domain_registration_length(domain):
    try:
        w = whois.whois(domain)
        creation = w.creation_date
        expiry = w.expiration_date

        if creation is None or expiry is None:
            return -1

        if isinstance(creation, list):
            creation = creation[0]
        if isinstance(expiry, list):
            expiry = expiry[0]

        length_days = (expiry - creation).days
        return 1 if length_days > 365 else -1
    except Exception:
        return -1
    

import ssl


def ssl_final_state(domain):
    try:
        context = ssl.create_default_context()
        sock = socket.create_connection((domain, 443), timeout=3)
        with context.wrap_socket(sock, server_hostname=domain):
            return 1
    except Exception:
        stats["ssl_fail"] += 1
        return -1