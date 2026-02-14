import socket
import ssl
from datetime import datetime

import whois

# Error counters used during bulk extraction/training runs.
stats = {
    'dns_fail': 0,
    'ssl_fail': 0,
    'whois_fail': 0
}


def domain_age(domain):
    try:
        w = whois.whois(domain)
        creation = w.creation_date

        if creation is None:
            return -1

        if isinstance(creation, list):
            creation = creation[0]

        age_days = (datetime.now() - creation).days
        return 1 if age_days > 365 else -1
    except whois.parser.PywhoisError:
        stats['whois_fail'] += 1
        return -1
    except Exception:
        stats['whois_fail'] += 1
        return 0


def dns_record(domain):
    try:
        socket.gethostbyname(domain)
        return 1
    except socket.gaierror:
        stats['dns_fail'] += 1
        return -1
    except Exception:
        stats['dns_fail'] += 1
        return 0


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
    except whois.parser.PywhoisError:
        stats['whois_fail'] += 1
        return -1
    except Exception:
        stats['whois_fail'] += 1
        return 0


def ssl_final_state(domain):
    try:
        context = ssl.create_default_context()
        sock = socket.create_connection((domain, 443), timeout=3)
        with context.wrap_socket(sock, server_hostname=domain):
            return 1
    except ssl.SSLError:
        stats['ssl_fail'] += 1
        return -1
    except socket.timeout:
        stats['ssl_fail'] += 1
        return 0
    except Exception:
        stats['ssl_fail'] += 1
        return 0
